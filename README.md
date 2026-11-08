# KyTucXa

Ứng dụng desktop : hệ thống quản lý ký túc xá. Giao diện dùng CustomTkinter; dữ liệu đọc/ghi qua MySQL Connector/Python.

## Tính năng

Bốn báo cáo theo yêu cầu Project 2:

1. Chi phí của từng sinh viên trong tháng: tiền phòng, dịch vụ, vé tháng và phí gửi xe phát sinh.
2. Tổng số lượng và chi phí từng dịch vụ theo sinh viên trong khoảng ngày.
3. Khách đến thăm từng sinh viên và số lượt thăm trong khoảng ngày.
4. Số lượng sử dụng và doanh thu từng dịch vụ trong tháng.

Các tiện ích nhập liệu và tính năng bổ sung:

- Thêm sinh viên vào phòng, kiểm tra sức chứa trước khi lưu.
- Ghi lượt sử dụng dịch vụ; trigger trong CSDL tính tiền.
- Ghi khách và lượt thăm.
- Thêm xe và đăng ký vé tháng; kiểm tra giới hạn hai vé còn hạn trước khi lưu

- Tra cứu hồ sơ sinh viên cùng số lượt sử dụng dịch vụ, khách thăm, xe và vé tháng còn hạn.
- Xem sức chứa và số chỗ còn trống của tất cả phòng.
- Xuất các bảng báo cáo ra CSV (mã hóa UTF-8 có BOM để mở thuận tiện trong Excel).
- Tạo hóa đơn tháng trong `HOADON` từ báo cáo chi phí. Chương trình bỏ qua sinh viên đã có hóa đơn trong tháng để hạn chế ghi trùng khi bấm lại.
- Chuyển phòng sinh viên

## Yêu cầu

- Windows, Python 3.10 trở lên.
- MySQL Server chạy trên máy local, schema KyTucXa đã được tạo và có các bảng.

- Nếu chưa import KyTucXa_import.sql: Chọn tab Server -> Data Import -> Import from Self-contained File -> chọn KyTucXa_import.sql -> Để trống Default Target Schema -> Start import

## Cài đặt và chạy

### Với Windows: 
Chạy run.bat (Tự động cài đặt môi trường và mở app)

Nếu chạy run.bat thất bại:
Cài đặt thư viện:
```bash
    pip install -r requirements.txt
```

Chạy app:
```bash
    python main.py
```

### Với Linux / MacOS:
Cài đặt thư viện:
```bash
    pip install -r requirements.txt
```

Chạy app:
```bash
    python3 main.py
```

Mặc định ứng dụng kết nối localhost:3306, user root, mật khẩu trống, database KyTucXa. Nếu cấu hình MySQL khác, vui lòng chỉnh sửa trong src/db.py

## Cấu trúc

- main.py: điểm chạy ứng dụng.
- kytucxa/db.py: cấu hình kết nối MySQL.
- kytucxa/repository.py: truy vấn báo cáo và thao tác ghi dữ liệu.
- kytucxa/gui.py: các tab báo cáo và nhập liệu.
