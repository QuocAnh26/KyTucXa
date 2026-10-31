"""Kết nối cơ sở dữ liệu KyTucXa."""
from __future__ import annotations

import os
import mysql.connector
from mysql.connector import MySQLConnection, Error

def connect() -> MySQLConnection:
    """Mở một kết nối tới MySQL Database."""
    try:
        connection = mysql.connector.connect(
            # Thay "localhost" nếu bạn dùng IP khác, ví dụ "127.0.0.1"
            host=os.getenv("KYTUCXA_DB_HOST", "localhost"),
            port=int(os.getenv("KYTUCXA_DB_PORT", "3306")),
            user=os.getenv("KYTUCXA_DB_USER", "root"),

            # ⬇️ ĐỔI MẬT KHẨU MYSQL CỦA BẠN VÀO ĐÂY (nếu không có mật khẩu thì để "")
            password=os.getenv("KYTUCXA_DB_PASSWORD", ""),

            # Lưu ý: Tên database phải khớp với tên trong MySQL Workbench / phpMyAdmin
            database=os.getenv("KYTUCXA_DB_NAME", "KyTucXa"),
            charset="utf8mb4",
            use_unicode=True,
            autocommit=True, # Bật autocommit=True để tự động lưu thay đổi khi Thêm/Sửa/Xóa
        )
        return connection
    except Error as e:
        print(f"❌ Lỗi kết nối MySQL: {e}")
        raise e