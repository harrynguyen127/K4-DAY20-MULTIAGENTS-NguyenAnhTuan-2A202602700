"""GUIDE Phần 3 - Người tuyển chọn skill (skill curator): tự viết skill từ các lần chạy thất bại.   >>> SINH VIÊN CÀI ĐẶT curate_skills <<<

Pseudo-code: guides/pseudocode/04_curator.md
Kiểm tra:    pytest tests/test_04_curator.py
Chạy thật:   python -m lab.curator
"""
import json
import re
from pathlib import Path

from .model import make_model
from .tasks import ROOT, eval_markers   # có sẵn: định danh của tác vụ đánh giá, tính lúc chạy

# ---- CÓ SẴN, KHÔNG SỬA: kiểm tra và tách khối skill (phần dễ sai và liên quan bảo mật) ----------------
SAFE_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_skill(text: str, expected_name: str | None = None) -> list[str]:
    """Kiểm tra nội dung một SKILL.md. Trả về danh sách vấn đề (rỗng = hợp lệ).

    Quy tắc: có khối YAML frontmatter; `name` chữ thường/số/gạch ngang (tối đa 64 ký tự) và bằng `expected_name`
    nếu được truyền; có `description` (tối đa 1024 ký tự); phần thân tối đa 80 dòng; không chứa chuỗi nào của
    `eval_markers()`. Quy tắc về `name` cũng là biện pháp bảo mật: tên khối do LLM sinh ra được dùng để tạo
    đường dẫn, nên `../evil` không được lọt qua.
    """
    problems = []
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text.strip() + "\n", re.S)
    if not m:
        return ["missing YAML frontmatter"]
    front, body = m.groups()
    name = re.search(r"^name:\s*(.+)$", front, re.M)
    desc = re.search(r"^description:\s*(.+)$", front, re.M)
    n = name.group(1).strip() if name else ""
    if not SAFE_NAME.fullmatch(n) or len(n) > 64:
        problems.append("invalid name")
    elif expected_name is not None and n != expected_name:
        problems.append("name differs from the block name")
    if not desc or len(desc.group(1).strip()) > 1024:
        problems.append("missing or too long description")
    if len(body.strip().splitlines()) > 80:
        problems.append("body longer than 80 lines")
    low = text.lower()
    for marker in eval_markers():
        if marker in low:
            problems.append(f"mentions evaluation material: {marker}")
    return problems


def parse_skill_blocks(reply: str) -> list[tuple[str, str]]:
    """Tách câu trả lời của LLM thành danh sách (name, nội dung SKILL.md).

    Khuôn dạng: `=== SKILL: <name> ===` ... `=== END ===`. Một khối kết thúc ở điểm nào đến trước trong ba điểm:
    `=== END ===`, tiêu đề `=== SKILL:` kế tiếp, hoặc cuối văn bản (LLM đôi khi quên dòng END).
    """
    pattern = re.compile(r"^=== SKILL: (\S+) ===[ \t]*\n(.*?)(?=^=== END ===|^=== SKILL: |\Z)", re.S | re.M)
    return [(name, text.strip()) for name, text in pattern.findall(str(reply))]
# --------------------------------------------------------------------------------------------------


def curate_skills(results_dir="results", source_condition="baseline", out_dir=None, model=None, max_skills: int = 3) -> list[Path]:
    """Đọc các lần chạy của TÁC VỤ HỌC (role == "learn") trong `source_condition`, nhờ LLM viết skill, ghi file.

    Các bước: nạp run.json + trace.md -> (nếu không có check nào thất bại: in cảnh báo và trả về [] mà KHÔNG gọi LLM)
    -> dựng prompt -> model.invoke(prompt) -> parse_skill_blocks -> validate_skill(text, expected_name=name)
    -> ghi `<out_dir>/<name>/SKILL.md`. Mặc định `out_dir` = <gốc lab>/skills/auto (dùng `ROOT` từ lab.tasks).
    Giữ tối đa `max_skills` skill hợp lệ; skill không hợp lệ bị bỏ qua.
    Prompt chứa, với mỗi check thất bại, TÊN và trường `detail` (lời nhận xét của bot đánh giá: phát biểu quy tắc bị vi phạm)
    cùng phần cuối của vết (trace). Với tác vụ học, `detail` chỉ phát biểu quy tắc, không chứa đáp án.
    Tuyệt đối KHÔNG đưa dữ liệu của tác vụ đánh giá (role == "eval") vào prompt.
    model mặc định: make_model() (lab.model).
    Trả về: danh sách đường dẫn SKILL.md đã ghi.
    """
    if out_dir is None:
        out_dir = ROOT / "skills" / "auto"
    out_dir = Path(out_dir)
    results_dir = Path(results_dir)
    base_dir = results_dir / source_condition

    runs: list[dict] = []
    if base_dir.exists():
        for run_path in sorted(base_dir.glob("*/run.json")):
            try:
                record = json.loads(run_path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if record.get("role") != "learn":
                continue
            failed_checks = []
            for check in record.get("checks", []) or []:
                if check.get("passed") is False:
                    failed_checks.append({
                        "name": str(check.get("name", "unnamed-check")),
                        "detail": str(check.get("detail", "")),
                    })
            if not failed_checks:
                continue
            trace_path = run_path.with_name("trace.md")
            trace = ""
            if trace_path.exists():
                trace = trace_path.read_text(encoding="utf-8", errors="replace")[-6000:]
            runs.append({
                "task": str(record.get("task", run_path.parent.name)),
                "failed": failed_checks,
                "trace": trace,
            })

    if not runs:
        print("không có check thất bại ở tác vụ học")
        return []

    prompt_lines = [
        "Bạn viết SKILL cho một tác tử lập trình và phân tích dữ liệu.",
        "Dưới đây là các check thất bại (tên và nhận xét của bot đánh giá) và vết của các lần chạy.",
        "Hãy tìm các lỗi QUY TRÌNH chung (không phải đáp án cụ thể) và viết tối đa {max_skills} skill ngắn "
        "giúp tránh các lỗi đó trên tác vụ MỚI cùng loại.",
        "",
        "Quy tắc:",
        "- Skill phải tổng quát: không nêu id tác vụ, không nêu tên tệp riêng của một tác vụ, không nêu đáp án hay con số.",
        "- Mỗi skill có frontmatter YAML gồm `name` (chữ thường, gạch ngang) và `description` (một câu: DÙNG KHI NÀO),",
        "  sau đó tối đa 40 dòng chỉ dẫn mệnh lệnh (danh sách kiểm tra - checklist - hoạt động tốt).",
        "- Định dạng đầu ra, đúng từng ký tự:",
        "=== SKILL: <name> ===",
        "---",
        "name: <name>",
        "description: <khi nào dùng>",
        "---",
        "<nội dung>",
        "=== END ===",
        "",
    ]
    # Keep the prompt in English as expected by the model and tasks.
    prompt_lines = [
        "You write SKILL for a coding and data-analysis agent.",
        "Below are failed checks (name and bot feedback) and the traces of the learning runs.",
        f"Write at most {max_skills} short skills that capture the common process errors and prevent them on future similar tasks.",
        "",
        "Rules:",
        "- The skill must be general: no task ids, no specific filenames from one task, no answers or numbers.",
        "- Each skill must have YAML frontmatter with `name` and `description` and then at most 40 lines of actionable checklist instructions.",
        "- Output format must be exact:",
        "=== SKILL: <name> ===",
        "---",
        "name: <name>",
        "description: <when to use>",
        "---",
        "<body>",
        "=== END ===",
        "",
    ]
    for idx, run in enumerate(runs, start=1):
        prompt_lines.append(f"RUN {idx}: {run['task']}")
        for check in run["failed"]:
            prompt_lines.append(f"- check: {check['name']}")
            prompt_lines.append(f"  detail: {check['detail']}")
        prompt_lines.append("Trace tail:")
        prompt_lines.append(run["trace"] or "<no trace>")
        prompt_lines.append("")
    prompt = "\n".join(prompt_lines)

    model = model or make_model()
    reply = model.invoke(prompt).content
    written: list[Path] = []
    for name, text in parse_skill_blocks(str(reply)):
        if len(written) >= max_skills:
            break
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
            continue
        if validate_skill(text, expected_name=name):
            continue
        safe_dir = out_dir / name
        if not safe_dir.parent == out_dir:
            continue
        safe_dir.mkdir(parents=True, exist_ok=True)
        skill_path = safe_dir / "SKILL.md"
        skill_path.write_text(text, encoding="utf-8")
        written.append(skill_path)
    return written


if __name__ == "__main__":
    for p in curate_skills():
        print("wrote", p)
