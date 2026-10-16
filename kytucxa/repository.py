"""Queries and write operations for the KyTucXa application."""
from __future__ import annotations

from datetime import date
from calendar import monthrange
from typing import Any

from .db import connect


def _read_all(sql: str, params: tuple[Any, ...]) -> list[dict[str, Any]]:
    connection = connect()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(sql, params)
        return list(cursor.fetchall())
    finally:
        cursor.close()
        connection.close()


def _validated_range(start: str, end: str) -> tuple[str, str]:
    first, last = date.fromisoformat(start), date.fromisoformat(end)
    if last < first:
        raise ValueError("Ngày kết thúc phải bằng hoặc sau ngày bắt đầu.")
    return first.isoformat(), last.isoformat()

def monthly_costs(month: str) -> list[dict[str, Any]]:
    """Return each student's room, services, monthly passes, parking and total."""
    first_day = date.fromisoformat(f"{month}-01")
    last_day = date(first_day.year, first_day.month, monthrange(first_day.year, first_day.month)[1])
    start, end = first_day.isoformat(), last_day.isoformat()

    sql = """
        SELECT
            sv.MaSV,
            sv.SoPhong,
            COALESCE(p.DonGiaThang, 0) AS TienPhong,
            COALESCE(dv.TienDichVu, 0) AS TienDichVu,
            COALESCE(dk.TienVeThang, 0) AS TienVeThang,
            COALESCE(lx.TienGuiXe, 0) AS TienGuiXe,
            COALESCE(p.DonGiaThang, 0)
              + COALESCE(dv.TienDichVu, 0)
              + COALESCE(dk.TienVeThang, 0)
              + COALESCE(lx.TienGuiXe, 0) AS TongPhaiTra
        FROM SINHVIEN sv
        LEFT JOIN PHONG p ON p.SoPhong = sv.SoPhong
        LEFT JOIN (
            SELECT MaSV, SUM(TongTienDichVu) AS TienDichVu
            FROM SUDUNG
            WHERE NgaySuDung BETWEEN %s AND %s
            GROUP BY MaSV
        ) dv ON dv.MaSV = sv.MaSV
        LEFT JOIN (
            SELECT MaSV, SUM(DonGiaThang) AS TienVeThang
            FROM DANG_KY_XE_THANG
            WHERE NgayBatDau <= %s AND NgayKetThuc >= %s
            GROUP BY MaSV
        ) dk ON dk.MaSV = sv.MaSV
        LEFT JOIN (
            SELECT xe.MaSV, SUM(l.SoTienPhatSinh) AS TienGuiXe
            FROM LUOT_XE l
            JOIN XE xe ON xe.MaXe = l.MaXe
            WHERE l.ThoiGianGui >= %s AND l.ThoiGianGui < DATE_ADD(%s, INTERVAL 1 DAY)
            GROUP BY xe.MaSV
        ) lx ON lx.MaSV = sv.MaSV
        ORDER BY sv.MaSV
    """
    return _read_all(sql, (start, end, end, start, start, end))


def service_totals(start: str, end: str) -> list[dict[str, Any]]:
    start, end = _validated_range(start, end)
    sql = """
        SELECT sv.MaSV,
               dv.MaDV, dv.TenDV,
               SUM(sd.SoLuong) AS TongSoLuong,
               SUM(sd.TongTienDichVu) AS TongTien
        FROM SUDUNG sd
        JOIN SINHVIEN sv ON sv.MaSV = sd.MaSV
        JOIN DICHVU dv ON dv.MaDV = sd.MaDV
        WHERE sd.NgaySuDung BETWEEN %s AND %s
        GROUP BY sv.MaSV, dv.MaDV, dv.TenDV
        ORDER BY sv.MaSV, dv.TenDV
    """
    return _read_all(sql, (start, end))


def visitor_summary(start: str, end: str) -> list[dict[str, Any]]:
    start, end = _validated_range(start, end)
    sql = """
        SELECT sv.MaSV,
               k.K_CCCD, k.HoTen AS HoTenKhach, COUNT(*) AS SoLanTham
        FROM THAM t
        JOIN SINHVIEN sv ON sv.MaSV = t.MaSV
        JOIN KHACH k ON k.K_CCCD = t.K_CCCD
        WHERE t.NgayTham BETWEEN %s AND %s
        GROUP BY sv.MaSV, k.K_CCCD, k.HoTen
        ORDER BY sv.MaSV, SoLanTham DESC, k.HoTen
    """
    return _read_all(sql, (start, end))


def service_revenue(month: str) -> list[dict[str, Any]]:
    first_day = date.fromisoformat(f"{month}-01")
    last_day = date(first_day.year, first_day.month, monthrange(first_day.year, first_day.month)[1])
    start, end = first_day.isoformat(), last_day.isoformat()
    sql = """
        SELECT dv.MaDV, dv.TenDV, dv.DonGia,
               COALESCE(r.TongSoLuong, 0) AS TongSoLuong,
               COALESCE(r.DoanhThu, 0) AS DoanhThu
        FROM DICHVU dv
        LEFT JOIN (
            SELECT MaDV, SUM(SoLuong) AS TongSoLuong, SUM(DoanhThu) AS DoanhThu
            FROM (
                SELECT MaDV, SUM(SoLuong) AS SoLuong,
                       SUM(TongTienDichVu) AS DoanhThu
                FROM SUDUNG
                WHERE NgaySuDung BETWEEN %s AND %s
                GROUP BY MaDV

                UNION ALL

                SELECT 'DV00002', COUNT(*), COALESCE(SUM(DonGiaThang), 0)
                FROM DANG_KY_XE_THANG
                WHERE NgayBatDau <= %s AND NgayKetThuc >= %s

                UNION ALL

                SELECT 'DV00002', COUNT(*), COALESCE(SUM(SoTienPhatSinh), 0)
                FROM LUOT_XE
                WHERE ThoiGianGui >= %s
                  AND ThoiGianGui < DATE_ADD(%s, INTERVAL 1 DAY)
            ) revenue_parts
            GROUP BY MaDV
        ) r ON r.MaDV = dv.MaDV
        ORDER BY dv.TenDV
    """
    return _read_all(sql, (start, end, end, start, start, end))

def add_student(
    student_id: str,
    cccd: str,
    hometown: str,
    birth_date: str,
    class_name: str,
    room_id: str,
) -> None:
    connection = connect()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT p.SoNguoiToiDa, COUNT(s.MaSV) AS SoDangO
            FROM PHONG p
            LEFT JOIN SINHVIEN s ON s.SoPhong = p.SoPhong
            WHERE p.SoPhong = %s
            GROUP BY p.SoPhong, p.SoNguoiToiDa
            """,
            (room_id,),
        )
        room = cursor.fetchone()
        if room is None:
            raise ValueError(f"Không tìm thấy phòng {room_id}.")
        if room["SoDangO"] >= room["SoNguoiToiDa"]:
            raise ValueError(f"Phòng {room_id} đã đủ người.")

        cursor.execute(
            """
            INSERT INTO SINHVIEN (MaSV, SV_CCCD, QueQuan, NgaySinh, Lop, SoPhong)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (student_id, cccd, hometown, birth_date, class_name, room_id),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def add_service_use(student_id: str, service_id: str, used_on: str, quantity: int) -> None:
    if quantity <= 0:
        raise ValueError("Số lượng phải lớn hơn 0.")
    connection = connect()
    cursor = connection.cursor()
    try:
        # SUDUNG_BEFORE_INSERT calculates the amount from the current service price.
        cursor.execute(
            """
            INSERT INTO SUDUNG (NgaySuDung, SoLuong, TongTienDichVu, MaSV, MaDV)
            VALUES (%s, %s, 0, %s, %s)
            """,
            (used_on, quantity, student_id, service_id),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def add_visitor_visit(
    cccd: str, guest_name: str, birth_date: str, student_id: str, visit_date: str
) -> None:
    connection = connect()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT 1 FROM KHACH WHERE K_CCCD = %s", (cccd,))
        if cursor.fetchone():
            cursor.execute(
                "UPDATE KHACH SET HoTen = %s, NgaySinh = %s WHERE K_CCCD = %s",
                (guest_name, birth_date, cccd),
            )
        else:
            cursor.execute(
                "INSERT INTO KHACH (K_CCCD, HoTen, NgaySinh) VALUES (%s, %s, %s)",
                (cccd, guest_name, birth_date),
            )
        cursor.execute(
            "INSERT INTO THAM (NgayTham, MaSV, K_CCCD) VALUES (%s, %s, %s)",
            (visit_date, student_id, cccd),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def register_monthly_vehicle(
    student_id: str, plate: str, vehicle_type: str, start_date: str, end_date: str
) -> str:
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    if end < start:
        raise ValueError("Ngày kết thúc không được trước ngày bắt đầu.")

    connection = connect()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT CURDATE() AS HomNay")
        today = cursor.fetchone()["HomNay"]
        cursor.execute(
            """
            SELECT COUNT(*) AS SoVe
            FROM DANG_KY_XE_THANG
            WHERE MaSV = %s AND NgayKetThuc >= CURDATE()
            """,
            (student_id,),
        )
        active_count = cursor.fetchone()["SoVe"]
        if end >= today and active_count >= 2:
            raise ValueError("Sinh viên đã có tối đa 2 vé tháng còn hạn.")

        cursor.execute(
            """
            SELECT COALESCE(MAX(CAST(SUBSTRING(MaXe, 3) AS UNSIGNED)), 0) + 1 AS SoTiepTheo
            FROM XE
            WHERE MaXe REGEXP '^XE[0-9]{5}$'
            """
        )
        vehicle_id = f"XE{cursor.fetchone()['SoTiepTheo']:05d}"
        cursor.execute(
            "INSERT INTO XE (MaXe, BienSo, LoaiXe, MaSV) VALUES (%s, %s, %s, %s)",
            (vehicle_id, plate, vehicle_type, student_id),
        )
        cursor.execute(
            """
            INSERT INTO DANG_KY_XE_THANG
                (DonGiaThang, NgayBatDau, NgayKetThuc, MaXe, MaSV)
            VALUES (100000, %s, %s, %s, %s)
            """,
            (start_date, end_date, vehicle_id, student_id),
        )
        connection.commit()
        return vehicle_id
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
