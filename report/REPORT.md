# Báo cáo Lab: Self-evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Nguyễn Anh Tuấn | 2A202602700 | Toàn bộ các phần |

- Mô hình: `LAB_MODEL=deepseek:deepseek-chat`, `LAB_TEMPERATURE=0`, `recursion_limit` chủ yếu là `60` (một số lần chạy lại dùng `20` để chặn lặp vô hạn).
- Deep Agents: `deepagents==0.7.21`, hệ điều hành Windows, chạy local.
- Tổng token của 18 run chính thức sau khi hoàn thiện ma trận kết quả: xấp xỉ **7,009,668** token.
- Mốc đóng băng:
  - Commit giả thuyết: `878d816` (`hypotheses`)
  - Tag đóng băng: `freeze` tại commit `2bee870`
  - Kiểm tra bằng `python -X utf8 scripts/verify_freeze.py`: **OK**

## 2. Giả thuyết (commit trước tag `freeze`)

- **H1** (subagents so với baseline): subagents có thể tăng điểm ở tác vụ học khi cần chia nhỏ công việc, nhưng có rủi ro tăng token mạnh và không ổn định vì vòng lặp hội thoại.
- **H2** (skills-auto so với baseline): skills-auto dự kiến cải thiện nhóm check quy ước/định dạng đầu ra (`rule_*`) vì curator rút kinh nghiệm từ lỗi lặp lại.
- **H3** (học so với đánh giá): chênh lệch học–đánh giá sẽ cho thấy dấu hiệu tổng quát hóa; nếu chỉ tăng ở học mà không tăng ở đánh giá thì có khả năng overfit theo tập lỗi đã thấy.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử mặc định có các công cụ: `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`, `execute`, `task`.
2. `task` mô tả `general-purpose` là subagent cho công việc nhiều bước; subagent chỉ nhận ngữ cảnh được truyền qua prompt (không tự động thừa hưởng toàn bộ lịch sử chính).
3. System prompt mặc định rỗng. Ví dụ câu hướng dẫn:
   - Từ `task`: “Launch an ephemeral subagent to handle a complex, multi-step task.”
   - Từ `execute`: “Use absolute paths and avoid `cd` so the working directory stays stable...”

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng ngắn |
|---|---|---|---|
| code-learn | `tests_not_modified` | B | Chỉnh vào test gốc: “the original files in tests/ must not be modified...” |
| code-learn | `rule_type_hints` | E | `RULE: every public function ... has type annotations ...` |
| code-learn | `rule_regression_tests` | E | `RULE: add tests/test_regressions.py ...` |
| code-learn | `rule_changelog` | E | `RULE: record each fix in CHANGELOG.md ...` |
| data-learn | 7 check đọc `answer.json` lỗi `FileNotFoundError` | G | Không sinh ra `workspace/answer.json` do run bị lỗi vòng lặp |
| data-learn | `rule_clean_csv` | E | `RULE: write workspace/clean.csv ...` |
| logs-learn | `rule_service_names` | E | `RULE: service names ... lower-case ...` |
| logs-learn | `rule_sorted_errors` | E | `RULE: errors is sorted by service ...` |
| logs-learn | `rule_schema_header` | E | `RULE: schema_version = 2, generated_by = log-triage` |

Nhận xét:
- Lỗi **E (vi phạm quy ước)** là nhóm nổi trội ở baseline.
- Số liệu phủ định cho A-D: theo `scripts/check_breakdown.py`, baseline/learn đạt **12/18 check kỹ thuật**, cho thấy phần lớn lỗi không nằm ở năng lực code cốt lõi mà ở checklist quy ước và artifact.

## 5. Điều kiện `subagents` (Phần 2.3)

- `subagent_calls` trong 6 task:
  - `code-learn=0`, `data-learn=0`, `logs-learn=1`, `code-eval=0`, `data-eval=0`, `logs-eval=0`.
- Quan sát: phần lớn run không giao việc; tác tử chính chủ yếu tự xử lý.
- Với run có giao việc (`logs-learn`), hiệu quả điểm không vượt baseline (đều 6/9), nhưng token tăng đáng kể.
- So với baseline:
  - Mean tokens/run: **514,675** (subagents) vs **302,538** (baseline).
  - Mean score eval: **0.38** (subagents) vs **0.57** (baseline).
  => Trong thí nghiệm này, cấu hình đa tác tử không hiệu quả về chi phí/điểm.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Curator tạo 3 skill trong [skills/auto/](C:/Users/tuann/MyStorage/VinUniAI/Phase2/K4-DAY20-MULTIAGENTS-NguyenAnhTuan-2A202602700/skills/auto):
  - [repo-rule-compliance/SKILL.md](C:/Users/tuann/MyStorage/VinUniAI/Phase2/K4-DAY20-MULTIAGENTS-NguyenAnhTuan-2A202602700/skills/auto/repo-rule-compliance/SKILL.md)
  - [required-output-artifacts/SKILL.md](C:/Users/tuann/MyStorage/VinUniAI/Phase2/K4-DAY20-MULTIAGENTS-NguyenAnhTuan-2A202602700/skills/auto/required-output-artifacts/SKILL.md)
  - [output-normalization-and-schema/SKILL.md](C:/Users/tuann/MyStorage/VinUniAI/Phase2/K4-DAY20-MULTIAGENTS-NguyenAnhTuan-2A202602700/skills/auto/output-normalization-and-schema/SKILL.md)
- Cả 3 skill đều khá tổng quát, không cứng theo tên task.
- Không phát hiện hướng dẫn có hại rõ ràng; các skill tập trung vào checklist output/schema/test.
- Độ dài ngắn gọn (khoảng 10–11 bullet/skill), `description` bám đúng trigger.
- Điều kiện `skills-auto`: có đọc skill ở **4/6 run** (2 run không đọc đều là run gặp recursion error).

## 7. Kết quả so sánh (dán từ `report/table.md`)

| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| code-learn | 6/10 | 7/10 | 8/10 |
| data-learn | 0/8 | 5/8 | 5/8 |
| logs-learn | 6/9 | 6/9 | 6/9 |
| code-eval | 6/11 | 6/11 | 8/11 |
| data-eval | 5/9 | 0/9 | 5/9 |
| logs-eval | 6/10 | 6/10 | 6/10 |
| **Mean score - learning tasks** | 0.42 | 0.66 | 0.70 |
| **Mean score - evaluation tasks** | 0.57 | 0.38 | 0.63 |
| **Mean tokens per run** | 302,538 | 514,675 | 351,065 |
| **Runs that read a skill** | 0/6 | 0/6 | 4/6 |

## 8. Phân tích

1. **Điều kiện cải thiện điểm**
   - Tác vụ học: `subagents` (0.66) và `skills-auto` (0.70) đều cao hơn `baseline` (0.42).
   - Tác vụ đánh giá: chỉ `skills-auto` cải thiện rõ (0.63 > 0.57), còn `subagents` giảm mạnh (0.38).
   - Có trường hợp “cải thiện học nhưng không cải thiện đánh giá”: `subagents` → dấu hiệu thiếu ổn định/tổng quát hóa kém.

2. **Tách kỹ thuật và quy ước**
   - Theo `check_breakdown.py`:
     - baseline/eval: kỹ thuật 17/18, quy ước 0/12.
     - skills-auto/eval: kỹ thuật 17/18, quy ước 2/12.
   - Skill sinh ra chủ yếu giúp nhóm **quy ước (`rule_`)**, ít tác động nhóm kỹ thuật vốn đã cao.

3. **Một check được skill giúp và một check chưa được giúp**
   - Được giúp: `code-learn: rule_type_hints` (baseline fail -> skills-auto pass), đồng thời run đó có `skills_read=3`.
   - Chưa được giúp: `data-learn` ở skills-auto run có `skills_read=0` và `GraphRecursionError`, dẫn đến fail do thiếu artifact đầu ra.

4. **Chi phí**
   - Mean token/run: baseline 302,538; subagents 514,675; skills-auto 351,065.
   - Hiệu quả điểm/token (xấp xỉ) cao nhất thuộc `skills-auto`, thấp nhất là `subagents`.
   - Kết luận: đa tác tử **không đáng chi phí** trong cấu hình hiện tại.

5. **Rò rỉ dữ liệu / quá khớp**
   - Không thấy skill chứa tên task đánh giá hay đáp án cứng.
   - Skill chỉ là quy tắc tổng quát (artifact/schema/checklist), nên rủi ro leakage thấp.
   - Đã phòng tránh bằng: giữ nguyên output curator, không sửa tay nội dung trong [skills/auto/](C:/Users/tuann/MyStorage/VinUniAI/Phase2/K4-DAY20-MULTIAGENTS-NguyenAnhTuan-2A202602700/skills/auto), và kiểm tra `verify_freeze`.

6. **Nhiễu**
   - Điểm học của `skills-auto` trước/sau đóng băng giữ nguyên trung bình **0.70** (8/10, 5/8, 6/9), nhưng token dao động mạnh giữa các run.
   - Điều này cho thấy với bộ task nhỏ, chênh lệch điểm nhỏ cần diễn giải thận trọng; chỉ score chưa phản ánh hết độ ổn định.

## 9. Hạn chế và tính hợp lệ

1. **Mỗi cấu hình-task chủ yếu một run chính thức**: khó ước lượng phương sai, nên kết luận về chênh lệch nhỏ có độ tin cậy hạn chế.
2. **Nhiều run gặp `GraphRecursionError`**: ảnh hưởng trực tiếp đến điểm và token, làm nhiễu so sánh năng lực thực giữa điều kiện.
3. **Chỉ dùng một mô hình (`deepseek-chat`)**: kết luận chưa chắc chuyển giao cho model khác hoặc backend khác.
4. **Bộ task nhỏ (3 learn + 3 eval)**: chưa bao phủ đủ kiểu lỗi tác tử trong thực tế.

## 10. Kết luận

Trong thí nghiệm này, `skills-auto` là điều kiện cân bằng tốt nhất giữa chất lượng và chi phí: tăng điểm cả ở tập học và tập đánh giá, đồng thời token thấp hơn nhiều so với `subagents`. `subagents` tăng điểm trên tập học nhưng giảm mạnh ở tập đánh giá và tốn token nhất. Lợi ích quan sát được của self-evolving skill chủ yếu nằm ở nhóm check quy ước/đầu ra. Tuy nhiên, lỗi recursion và số lần chạy ít khiến kết luận cần thận trọng. Bước tiếp theo nên lặp thêm nhiều seed/run (hướng 6e) để định lượng nhiễu trước khi chốt nhận định cuối.

## Phụ lục

- Lệnh đã chạy (theo thứ tự hoàn thiện):
  - `pytest -q`
  - `python -m lab.runner --condition subagents --tasks eval` (dừng do treo)
  - `python -m lab.runner --condition skills-auto --tasks eval`
  - `python -m lab.runner --condition subagents --tasks data-eval --recursion-limit 20`
  - `python -m lab.runner --condition subagents --tasks logs-eval --recursion-limit 20`
  - `python -X utf8 scripts/verify_freeze.py`
  - `python -m lab.runner --condition skills-auto --tasks learn`
  - `python -X utf8 scripts/verify_freeze.py` (OK)
  - `python -m lab.compare | Out-File -FilePath report/table.md -Encoding utf8`
  - `python scripts/check_breakdown.py`
- Thử thách mở rộng: chưa thực hiện.
- Ghi chú:
  - Không chạy lặp lại các lệnh API đã có kết quả, trừ khi bắt buộc để đáp ứng quy tắc đóng băng (`skills-auto` learn trước freeze phải chạy lại).
