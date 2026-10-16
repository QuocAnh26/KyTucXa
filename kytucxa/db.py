"""Kết nối cơ sở dữ liệu KyTucXa."""
from __future__ import annotations

import os

import mysql.connector
from mysql.connector import MySQLConnection


def connect() -> MySQLConnection:
    """Mở một kết nối qua localhost:3306.
    """
    return mysql.connector.connect(
        host=os.getenv("KYTUCXA_DB_HOST", "localhost"),  #dùng kytucxa_db_host nếu đã đặt, không thì dùng localhost
        port=int(os.getenv("KYTUCXA_DB_PORT", "3306")),
        user=os.getenv("KYTUCXA_DB_USER", "root"),
        password=os.getenv("KYTUCXA_DB_PASSWORD", ""),
        database=os.getenv("KYTUCXA_DB_NAME", "KyTucXa"),
        charset="utf8mb4",
        use_unicode=True,
        autocommit=False,
    )

