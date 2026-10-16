"""Database connection settings for the local dormitory database."""
from __future__ import annotations

import os

import mysql.connector
from mysql.connector import MySQLConnection


def connect() -> MySQLConnection:
    """Open a connection using localhost/root/blank-password defaults.

    Settings can be overridden with KYTUCXA_DB_* environment variables.
    """
    return mysql.connector.connect(
        host=os.getenv("KYTUCXA_DB_HOST", "localhost"),
        port=int(os.getenv("KYTUCXA_DB_PORT", "3306")),
        user=os.getenv("KYTUCXA_DB_USER", "root"),
        password=os.getenv("KYTUCXA_DB_PASSWORD", ""),
        database=os.getenv("KYTUCXA_DB_NAME", "KyTucXa"),
        charset="utf8mb4",
        use_unicode=True,
        autocommit=False,
    )
