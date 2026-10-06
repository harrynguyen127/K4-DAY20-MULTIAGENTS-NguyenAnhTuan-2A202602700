# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Nguyễn Anh Tuấn | 2A202602700 | Toàn bộ các phần|

- Mô hình: `LAB_MODEL=deepseek:deepseek-chat`, `LAB_TEMPERATURE=0`, `recursion_limit=60`.
- Deep Agents: `deepagents==0.7.21`, hệ điều hành `Windows 10`, chạy trực tiếp trên máy local (không dùng Docker).
- Số lần chạy tác vụ đã dùng / ngân sách: đã chạy các lần baseline/subagents/skills-auto trên các tác vụ học, tổng khoảng hàng trăm nghìn token; hiện tại còn gặp lỗi `GraphRecursionError` ở các lần chạy có mô hình DeepSeek trong điều kiện phức tạp.
- Commit của tag `freeze`: chưa thực hiện do chưa chạy đủ bước đóng băng của lab; report này là bản nháp dựa trên dữ liệu có sẵn.

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

- H1 (subagents so với baseline): Subagents sẽ cải thiện score trên tác vụ học ở các bước cần đọc/spec và chạy kiểm tra, nhưng không chắc cải thiện ổn định vì chi phí token tăng mạnh và mô hình có xu hướng lặp vô hạn khi giao việc phức tạp.
- H2 (skills-auto so với baseline): Skills-auto sẽ giúp cải thiện các check quy tắc thực thi và tài liệu/metadata, vì curator rút ra được các skill về `repo-rule-compliance`, `required-output-artifacts`, `output-normalization-and-schema` từ các lỗi lặp lại.
- H3 (tác vụ học so với tác vụ đánh giá): Tác vụ học dễ hơn đánh giá vì dữ liệu học có thể đọc được và lỗi chủ yếu là quy tắc, trong khi tác vụ đánh giá thêm quy tắc mới hoặc định dạng ẩn nên dễ hơn nhiều so với baseline nếu mô hình không đọc kỹ.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử mặc định có các công cụ tệp `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`; shell `execute`; subagent `task`.
2. Mô tả `task` nêu rõ: `general-purpose` là subagent dùng cho tìm kiếm, nghiên cứu và thực hiện multi-step tasks; nó chỉ nhìn thấy prompt được gởi đi và không thừa hưởng toàn bộ hội thoại trừ khi tài liệu mô tả khác.
3. System prompt mặc định rỗng. Một câu hướng dẫn hành vi từ `task`: “Launch an ephemeral subagent to handle a complex, multi-step task.” Một câu từ `execute`: “Use absolute paths and avoid `cd` so the working directory stays stable...”

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| code-learn | `rule_type_hints` | E | `RULE: every public function ... has type annotations...` |
| code-learn | `rule_regression_tests` | E | `RULE: add tests/test_regressions.py ...` |
| code-learn | `rule_changelog` | E | `RULE: record each fix in CHANGELOG.md ...` |
| data-learn | `rule_clean_csv` | D | `RULE: write workspace/clean.csv ... one row per distinct order ...` |
| data-learn | `rule_money_in_cents` | D | `RULE: money values in answer.json are integer cents ...` |
| logs-learn | `rule_service_names` | E | `RULE: service names in the output are lower-case ...` |
| logs-learn | `rule_sorted_errors` | E | `RULE: errors is sorted by service, then by timestamp_utc, ascending.` |
| logs-learn | `rule_schema_header` | E | `RULE: the top-level object has "schema_version": 2 and "generated_by": "log-triage".` |

Nhận xét: lỗi quy ước (`E`) chiếm đa số trong dữ liệu học hiện có. Đây là vùng mà skill có thể phòng ngừa tốt vì các lỗi này lặp lại ở dạng “thiếu metadata / schema / checklist” chứ không phải là bug logic cốt lõi. Các lỗi kiểu `A-D` về đọc spec hoặc dữ liệu bẩn xuất hiện ít hơn và thường được mô hình xử lý khá tốt hơn khi có câu hỏi rõ ràng.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa: `explorer`, `implementer`, `reviewer`.
- `subagent_calls` ở từng tác vụ: `data-learn` trong điều kiện subagents có `subagent_calls = 0` trên lần chạy thu được; `code-learn` ở lần chạy khác cũng cho thấy `subagent_calls = 0` và bị `GraphRecursionError` nên không có bằng chứng rõ ràng rằng subagent được dùng.
- Thông tin thiếu hoặc thừa khi giao việc: do tài liệu phụ, task chính đã nêu đủ, nhưng tác tử chủ đạo không cần phải delegate nên các subagent phần lớn không được gọi. Điều này cho thấy hành vi “tự làm” chiếm ưu thế khi mô hình chưa có động lực hay kỹ thuật phân tách công việc.
- Ảnh hưởng đến token và thời gian: khi subagents không được gọi, chi phí token thấp hơn nhưng không đổi được chất lượng; khi subagent có gọi, token tăng rất mạnh ở `code-learn` (vượt 1.3M input token ở lần chạy subagents), cho thấy phương án này rất tốn kém dù không đảm bảo cải thiện đáng kể.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator: 1 lần.
- Số skill bị xóa: 0; các skill sinh ra hợp lệ về tên/frontmatter và không chứa marker đánh giá.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `repo-rule-compliance` | Tổng quát | Đúng, tập trung vào checklist của repo, type hints, regression tests, changelog | 11 mục, `description` phù hợp cho task có quy tắc repo; chưa chắc đã được đọc trong lần run skills-auto vì `skills_read` = 0 trên dữ liệu thu được |
| `required-output-artifacts` | Tổng quát | Đúng, nhấn mạnh output file, schema và metadata | 10 mục, rõ ràng; phù hợp cho tác vụ dữ liệu/logs |
| `output-normalization-and-schema` | Tổng quát | Đúng, có trọng tâm rõ về chuẩn hóa và schema | 11 mục; phù hợp cho tasks xử lý dữ liệu/logs |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

> Dữ liệu chính thức đầy đủ cho `report/table.md` và `check_breakdown.py` chưa được chạy xong vì các tác vụ thực thi bằng model DeepSeek tiếp tục gặp `GraphRecursionError` ở các điều kiện phức tạp. Dưới đây là các số liệu thu được từ các lần chạy có sẵn và các cảnh báo kỹ thuật.

```text
baseline      code-learn  score=6/10 tokens=134887 calls=22 25.7s
baseline      data-learn  score=0/8 tokens=384245 calls=0 35.9s ERROR=GraphRecursionError
baseline      logs-learn  score=6/9 tokens=204996 calls=15 19.1s
subagents     code-learn  score=6/10 tokens=1283267 calls=50 264.8s
subagents     data-learn  score=5/8 tokens=109114 calls=16 26.9s
skills-auto   code-learn  score=8/10 tokens=440637 calls=0 64.3s ERROR=GraphRecursionError
```

Lần chạy `skills-auto` trên `code-learn` cho thấy skill tăng score từ 6/10 lên 8/10, nhưng vẫn bị lỗi `GraphRecursionError` sau đó; nên không thể kết luận “đã hoàn toàn ổn định” mà chỉ có thể nói skill cải thiện được một phần các check quy tắc.

## 8. Phân tích

> Trả lời từng câu bằng số liệu từ mục 7 và bằng chứng từ vết. Kết quả âm hoặc không có khác biệt vẫn hợp lệ nếu được phân tích tốt.

1. So với `baseline`, điều kiện nào cải thiện điểm tác vụ **học**? Điều kiện nào cải thiện điểm tác vụ **đánh giá**? Có điều kiện nào cải thiện tác vụ học nhưng không cải thiện tác vụ đánh giá? Nếu có, đó là dấu hiệu gì?
2. Tách điểm thành check kỹ thuật và check quy ước (`rule_`). Skill do curator sinh giúp nhóm check nào? Check quy ước **mới** của tác vụ đánh giá có được skill giúp không, và vì sao?
3. Dựa vào vết và `skills_read`, giải thích một check mà skill giúp đạt và một check mà skill không giúp (skill chưa được đọc, đọc nhưng không làm theo, skill thiếu hoặc sai).
4. Chi phí: so sánh số token trung bình giữa các điều kiện. Điều kiện nào có hiệu quả tốt nhất theo điểm trên mỗi token? Đa tác tử có đáng chi phí trong thí nghiệm này không?
5. Có dấu hiệu rò rỉ dữ liệu hoặc quá khớp nào trong skill sinh ra không? Nhóm đã phòng tránh như thế nào?
6. Nhiễu: so sánh điểm tác vụ học của cùng bộ skill ở Phần 3.4 (đã sao lưu) và sau đóng băng. Chênh lệch bao nhiêu? Nó cho biết điều gì về độ tin cậy của các chênh lệch trong bảng ở mục 7?

## 9. Hạn chế và tính hợp lệ

> Nêu ít nhất 3 hạn chế và ảnh hưởng của từng hạn chế đến kết luận (ví dụ: chỉ 3 tác vụ mỗi vai trò, mỗi cấu hình chạy một lần, nhiễu của mô hình, tác vụ do giảng viên thiết kế sẵn quy ước, chỉ một mô hình).

1.
2.
3.

## 10. Kết luận

> Tối đa 5 câu. Chỉ khẳng định điều số liệu hỗ trợ. Nêu một đề xuất cải tiến tiếp theo.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
- Thử thách mở rộng (nếu có): hướng chọn, kết quả, nhận xét.
- Ghi chú khác:
