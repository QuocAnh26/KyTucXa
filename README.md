# KyTucXa

Ứng dụng desktop Python cho Project 2: hệ thống quản lý ký túc xá. Giao diện dùng CustomTkinter; dữ liệu đọc/ghi qua MySQL Connector/Python.

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
- MySQL Server chạy trên máy local, schema KyTucXa đã được tạo và có các bảng của Project 2.
- CSDL nên có các trigger trong file dump để tính tiền dịch vụ/xe và kiểm tra sức chứa, số vé tháng. Ứng dụng kiểm tra các điều kiện chính trước khi lưu; khóa ngoại và trigger của MySQL là lớp bảo vệ cuối.

Nếu chưa tạo schema, chạy trong MySQL Workbench:

```sql
CREATE DATABASE IF NOT EXISTS KyTucXa
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;
```

Sau đó import cấu trúc và dữ liệu Project 2 vào schema đó. Nếu dump bắt đầu bằng CREATE DATABASE có tên đặt trong dấu ngoặc kép hoặc dấu nháy đơn, sửa dòng đó sang tên schema không quote như ví dụ trên hoặc bỏ dòng tạo database và chọn KyTucXa làm schema đích khi import.

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

Nút **Kiểm tra kết nối** trên đầu cửa sổ báo schema/version hoặc lỗi kết nối.

## Lưu ý về cách tính báo cáo

- Bảng SINHVIEN hiện không có cột họ tên, vì vậy danh sách hiển thị MaSV.
- CSDL không lưu lịch sử chuyển phòng; báo cáo tháng dùng phòng và giá phòng hiện tại cho mọi tháng đã chọn.
- Vé tháng được tính một lần theo DonGiaThang nếu thời hạn đăng ký giao với tháng báo cáo. Dữ liệu hiện có phù hợp với một bản ghi đăng ký cho mỗi tháng.
- Phí gửi xe lấy từ LUOT_XE.SoTienPhatSinh theo ngày gửi; dữ liệu xe không vé tháng chỉ được tính nếu hiện diện trong schema.

## Cấu trúc

- main.py: điểm chạy ứng dụng.
- kytucxa/db.py: cấu hình kết nối MySQL.
- kytucxa/repository.py: truy vấn báo cáo và thao tác ghi dữ liệu.
- kytucxa/gui.py: các tab báo cáo và nhập liệu.
