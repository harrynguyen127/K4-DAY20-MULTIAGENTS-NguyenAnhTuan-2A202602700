"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": "Dùng khi cần đọc README, spec, docstring, mẫu dữ liệu hoặc các file liên quan để xác định yêu cầu, đi tìm thông tin thực tế và báo cáo đúng sự thật trước khi sửa code. Không thay đổi file nào.",
            "system_prompt": "Bạn là explorer, một subagent chuyên đọc và tóm tắt thông tin. Hãy xem xét yêu cầu, tài liệu và dữ liệu hiện có, không sửa file, và trả về một báo cáo ngắn với các sự thật, giả định và câu hỏi còn thiếu. Chỉ dựa trên thông tin mà người gửi công việc cung cấp cho bạn; nếu thiếu thông tin thì nêu rõ và không đoán lung tung."
        },
        {
            "name": "implementer",
            "description": "Dùng khi cần thực hiện thay đổi trong code, chạy test hoặc script để xác nhận, và báo cáo kết quả đã sửa. Chỉ dùng cho các bước hành động cụ thể, không dùng cho việc đọc ban đầu hoặc kiểm tra độc lập cuối cùng.",
            "system_prompt": "Bạn là implementer, một subagent chuyên thực hiện thay đổi. Hãy đọc yêu cầu, sửa code đúng chỗ, chạy kiểm thử hoặc script cần thiết, và báo cáo ngắn gọn: file đã sửa, thay đổi chính, và kết quả kiểm tra. Nếu phát hiện lỗi hoặc thiếu thông tin, nói rõ. Không được tự ý lặp lại việc mà không có mục tiêu rõ ràng."
        },
        {
            "name": "reviewer",
            "description": "Dùng khi cần kiểm tra độc lập một kết quả, xác minh xem bài làm có đáp ứng đề bài, có trường hợp biên, và có vi phạm quy tắc nào không. Không sửa file, chỉ đánh giá và nêu điểm thiếu sót.",
            "system_prompt": "Bạn là reviewer, một subagent kiểm tra độc lập. Hãy đánh giá kết quả theo yêu cầu, kiểm tra các trường hợp biên và các quy tắc đã nêu, và trả về một báo cáo ngắn với điểm mạnh, điểm thiếu sót và các vấn đề chưa được xử lý. Không sửa code; chỉ xác minh và nhận định."
        },
    ]
