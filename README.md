# KyTucXa

Ứng dụng desktop : hệ thống quản lý ký túc xá. Giao diện dùng CustomTkinter; dữ liệu đọc/ghi qua MySQL Connector/Python.

## Tính năng

Bốn báo cáo theo yêu cầu Project 2:

1. Chi phí của từng sinh viên trong tháng: tiền phòng, dịch vụ, vé tháng và phí gửi xe phát sinh.
2. Tổng số lượng và chi phí từng dịch vụ theo sinh viên trong khoảng ngày.
3. Khách đến thăm từng sinh viên và số lượt thăm trong khoảng ngày.
4. Số lượng sử dụng và doanh thu từng dịch vụ trong tháng.

Các tiện ích nhập liệu:

- Thêm sinh viên vào phòng, kiểm tra sức chứa trước khi lưu.
- Ghi lượt sử dụng dịch vụ; trigger trong CSDL tính tiền.
- Ghi khách và lượt thăm.
- Thêm xe và đăng ký vé tháng; kiểm tra giới hạn hai vé còn hạn trước khi lưu.

## Yêu cầu

- Windows, Python 3.10 trở lên.
- MySQL Server chạy trên máy local, schema KyTucXa đã được tạo và có các bảng.

Nếu chưa tạo schema, chạy trong MySQL Workbench:

```sql
CREATE DATABASE IF NOT EXISTS KyTucXa
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;
```
Rồi Server -> Data Import -> Import from Self-contained File -> chọn KyTucXa_import.sql -> Để trống Default Target Schema -> Start import

## Cài đặt và chạy

Mở PowerShell tại thư mục repo:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Mặc định ứng dụng kết nối localhost:3306, user root, mật khẩu trống, database KyTucXa. Nếu cấu hình MySQL khác, đặt biến môi trường trước khi chạy:

```powershell
$env:KYTUCXA_DB_HOST = "localhost"
$env:KYTUCXA_DB_PORT = "3306"
$env:KYTUCXA_DB_USER = "root"
$env:KYTUCXA_DB_PASSWORD = ""
$env:KYTUCXA_DB_NAME = "KyTucXa"
python main.py
```

## Cấu trúc

- main.py: điểm chạy ứng dụng.
- kytucxa/db.py: cấu hình kết nối MySQL.
- kytucxa/repository.py: truy vấn báo cáo và thao tác ghi dữ liệu.
- kytucxa/gui.py: các tab báo cáo và nhập liệu.
