"""CustomTkinter interface for dormitory reports and data entry."""
from __future__ import annotations

import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk
from typing import Any, Callable

import customtkinter as ctk

from . import repository
from .db import connect


class ReportFrame(ctk.CTkFrame):
    def __init__(
        self,
        master: Any,
        columns: list[tuple[str, str, int]],
        runner: Callable[[dict[str, str]], list[dict[str, Any]]],
        fields: list[tuple[str, str]],
        note: str = "",
    ) -> None:
        super().__init__(master, fg_color="transparent")
        self.columns = columns
        self.runner = runner
        self.fields: dict[str, ctk.CTkEntry] = {}

        if note:
            ctk.CTkLabel(self, text=note, anchor="w", wraplength=1000).pack(
                fill="x", padx=12, pady=(10, 4)
            )

        controls = ctk.CTkFrame(self)
        controls.pack(fill="x", padx=12, pady=8)
        for index, (key, label) in enumerate(fields):
            ctk.CTkLabel(controls, text=label).grid(
                row=0, column=index * 2, padx=(12, 5), pady=10, sticky="e"
            )
            entry = ctk.CTkEntry(controls, width=130)
            entry.grid(row=0, column=index * 2 + 1, padx=(0, 12), pady=10)
            self.fields[key] = entry
        self.run_button = ctk.CTkButton(controls, text="Xem báo cáo", command=self.run)
        self.run_button.grid(row=0, column=len(fields) * 2, padx=12, pady=10)

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.tree = ttk.Treeview(
            table_frame,
            columns=[key for key, _, _ in columns],
            show="headings",
            height=18,
        )
        vertical = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        horizontal = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        for key, title, width in columns:
            self.tree.heading(key, text=title)
            self.tree.column(key, width=width, minwidth=80, anchor="w")
        self.status = ctk.CTkLabel(self, text="", anchor="w")
        self.status.pack(fill="x", padx=14, pady=(0, 8))
        self.pack(fill="both", expand=True)

    def set_field(self, key: str, value: str) -> None:
        field = self.fields[key]
        field.delete(0, "end")
        field.insert(0, value)

    def run(self) -> None:
        try:
            values = {key: field.get().strip() for key, field in self.fields.items()}
            for value in values.values():
                if not value:
                    raise ValueError("Vui lòng nhập đủ thông tin lọc.")
            rows = self.runner(values)
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                cells = []
                for key, _, _ in self.columns:
                    value = row.get(key, "")
                    if isinstance(value, (int, float)):
                        value = f"{value:,}"
                    cells.append("" if value is None else str(value))
                self.tree.insert("", "end", values=cells)
            self.status.configure(text=f"Có {len(rows)} dòng.")
        except Exception as exc:
            messagebox.showerror("Không thể chạy báo cáo", str(exc))


class DataEntryFrame(ctk.CTkFrame):
    def __init__(
        self,
        master: Any,
        title: str,
        fields: list[tuple[str, str]],
        submit: Callable[[dict[str, str]], str],
        note: str = "",
    ) -> None:
        super().__init__(master, fg_color="transparent")
        ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=18, weight="bold")).pack(
            anchor="w", padx=14, pady=(14, 6)
        )
        if note:
            ctk.CTkLabel(self, text=note, anchor="w", wraplength=850).pack(
                anchor="w", padx=14, pady=(0, 8)
            )
        self.entries: dict[str, ctk.CTkEntry] = {}
        form = ctk.CTkFrame(self)
        form.pack(fill="x", padx=14, pady=8)
        for index, (key, label) in enumerate(fields):
            row, col = divmod(index, 2)
            ctk.CTkLabel(form, text=label).grid(
                row=row, column=col * 2, padx=(12, 5), pady=9, sticky="e"
            )
            entry = ctk.CTkEntry(form, width=220)
            entry.grid(row=row, column=col * 2 + 1, padx=(0, 16), pady=9, sticky="ew")
            self.entries[key] = entry
        form.grid_columnconfigure(1, weight=1)
        form.grid_columnconfigure(3, weight=1)
        ctk.CTkButton(self, text="Lưu", command=lambda: self._submit(submit)).pack(
            anchor="w", padx=14, pady=8
        )
        self.status = ctk.CTkLabel(self, text="", anchor="w", wraplength=850)
        self.status.pack(anchor="w", padx=14, pady=8)
        self.pack(fill="both", expand=True)

    def _submit(self, action: Callable[[dict[str, str]], str]) -> None:
        try:
            values = {key: entry.get().strip() for key, entry in self.entries.items()}
            if any(not value for value in values.values()):
                raise ValueError("Vui lòng nhập đầy đủ các trường.")
            message = action(values)
            self.status.configure(text=message, text_color=("green", "#75d68a"))
            for entry in self.entries.values():
                entry.delete(0, "end")
        except Exception as exc:
            self.status.configure(text=str(exc), text_color=("red", "#ff7777"))


class DormitoryApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Quản lý ký túc xá")
        self.geometry("1180x760")
        self.minsize(900, 620)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=14, pady=(14, 6))
        ctk.CTkLabel(
            header,
            text="Hệ thống quản lý ký túc xá",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(side="left", padx=14, pady=12)
        ctk.CTkLabel(
            header, text="MySQL localhost:3306 · root · không mật khẩu"
        ).pack(side="left", padx=12)
        ctk.CTkButton(header, text="Kiểm tra kết nối", command=self.check_connection).pack(
            side="right", padx=12, pady=8
        )

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=14, pady=(4, 14))
        self._build_reports()
        self._build_entry_forms()

    def check_connection(self) -> None:
        try:
            connection = connect()
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE(), VERSION()")
            database_name, version = cursor.fetchone()
            cursor.close()
            connection.close()
            messagebox.showinfo(
                "Kết nối thành công",
                f"Đã kết nối tới schema {database_name} trên MySQL {version}.",
            )
        except Exception as exc:
            messagebox.showerror(
                "Không kết nối được",
                f"Kiểm tra MySQL đang chạy và schema KyTucXa đã tồn tại.\n\n{exc}",
            )

    def _build_reports(self) -> None:
        report_tab = self.tabs.add("Báo cáo")
        subtabs = ctk.CTkTabview(report_tab)
        subtabs.pack(fill="both", expand=True, padx=4, pady=4)
        today = date.today()
        month = today.strftime("%Y-%m")
        first_day = today.replace(day=1).isoformat()
        last_day = today.isoformat()

        pane = ReportFrame(
            subtabs.add("Chi phí tháng"),
            [
                ("MaSV", "Mã SV", 100),
                ("SoPhong", "Phòng", 80),
                ("TienPhong", "Tiền phòng", 130),
                ("TienDichVu", "Tiền dịch vụ", 140),
                ("TienVeThang", "Vé tháng", 120),
                ("TienGuiXe", "Phát sinh gửi xe", 150),
                ("TongPhaiTra", "Tổng phải trả", 150),
            ],
            lambda v: repository.monthly_costs(v["month"]),
            [("month", "Tháng (YYYY-MM)")],
            "Tổng gồm tiền phòng theo giá phòng hiện tại, sử dụng dịch vụ, vé tháng giao với tháng được chọn và phí lượt gửi xe.",
        )
        pane.set_field("month", month)

        pane = ReportFrame(
            subtabs.add("Dịch vụ theo kỳ"),
            [
                ("MaSV", "Mã SV", 100),
                ("MaDV", "Mã DV", 100),
                ("TenDV", "Dịch vụ", 200),
                ("TongSoLuong", "Số lượng", 110),
                ("TongTien", "Tổng tiền", 140),
            ],
            lambda v: repository.service_totals(v["start"], v["end"]),
            [("start", "Từ ngày (YYYY-MM-DD)"), ("end", "Đến ngày (YYYY-MM-DD)")],
        )
        pane.set_field("start", first_day)
        pane.set_field("end", last_day)

        pane = ReportFrame(
            subtabs.add("Khách thăm"),
            [
                ("MaSV", "Mã SV", 100),
                ("K_CCCD", "CCCD khách", 160),
                ("HoTenKhach", "Tên khách", 220),
                ("SoLanTham", "Số lần", 100),
            ],
            lambda v: repository.visitor_summary(v["start"], v["end"]),
            [("start", "Từ ngày (YYYY-MM-DD)"), ("end", "Đến ngày (YYYY-MM-DD)")],
        )
        pane.set_field("start", first_day)
        pane.set_field("end", last_day)

        pane = ReportFrame(
            subtabs.add("Doanh thu dịch vụ"),
            [
                ("MaDV", "Mã DV", 100),
                ("TenDV", "Dịch vụ", 220),
                ("DonGia", "Đơn giá", 130),
                ("TongSoLuong", "Số lượng", 110),
                ("DoanhThu", "Doanh thu", 150),
            ],
            lambda v: repository.service_revenue(v["month"]),
            [("month", "Tháng (YYYY-MM)")],
            "Doanh thu DV00002 gồm lượt dịch vụ, vé tháng và phí phát sinh gửi xe; kiểm tra mã DV00002 có trong DICHVU.",
        )
        pane.set_field("month", month)

    def _build_entry_forms(self) -> None:
        entry_tab = self.tabs.add("Ghi nhận / đăng ký")
        subtabs = ctk.CTkTabview(entry_tab)
        subtabs.pack(fill="both", expand=True, padx=4, pady=4)

        DataEntryFrame(
            subtabs.add("Sinh viên"),
            "Thêm sinh viên vào phòng",
            [
                ("student_id", "Mã sinh viên"),
                ("cccd", "CCCD"),
                ("hometown", "Quê quán"),
                ("birth_date", "Ngày sinh (YYYY-MM-DD)"),
                ("class_name", "Lớp"),
                ("room_id", "Số phòng"),
            ],
            self._save_student,
            "Ứng dụng kiểm tra sức chứa phòng trước khi thêm; khóa ngoại và trigger trong CSDL cũng được áp dụng.",
        )

        DataEntryFrame(
            subtabs.add("Dùng dịch vụ"),
            "Ghi nhận sử dụng dịch vụ",
            [
                ("student_id", "Mã sinh viên"),
                ("service_id", "Mã dịch vụ"),
                ("used_on", "Ngày dùng (YYYY-MM-DD)"),
                ("quantity", "Số lượng"),
            ],
            self._save_service_use,
            "Trigger SUDUNG_BEFORE_INSERT trong CSDL tự tính tổng tiền từ đơn giá hiện hành.",
        )

        DataEntryFrame(
            subtabs.add("Khách thăm"),
            "Ghi nhận khách đến thăm",
            [
                ("cccd", "CCCD khách"),
                ("guest_name", "Họ tên khách"),
                ("birth_date", "Ngày sinh (YYYY-MM-DD)"),
                ("student_id", "Mã sinh viên được thăm"),
                ("visit_date", "Ngày thăm (YYYY-MM-DD)"),
            ],
            self._save_visit,
            "Nếu CCCD đã có trong danh sách khách, thông tin tên và ngày sinh sẽ được cập nhật rồi ghi lượt thăm.",
        )

        DataEntryFrame(
            subtabs.add("Xe vé tháng"),
            "Thêm xe và đăng ký vé tháng",
            [
                ("student_id", "Mã sinh viên"),
                ("plate", "Biển số"),
                ("vehicle_type", "Loại xe"),
                ("start_date", "Ngày bắt đầu (YYYY-MM-DD)"),
                ("end_date", "Ngày kết thúc (YYYY-MM-DD)"),
            ],
            self._save_monthly_vehicle,
            "Giá vé mặc định 100.000 đồng/tháng. Ứng dụng kiểm tra tối đa 2 vé tháng còn hạn; trigger CSDL kiểm tra lại.",
        )

    @staticmethod
    def _save_student(values: dict[str, str]) -> str:
        date.fromisoformat(values["birth_date"])
        repository.add_student(
            values["student_id"],
            values["cccd"],
            values["hometown"],
            values["birth_date"],
            values["class_name"],
            values["room_id"],
        )
        return f"Đã thêm sinh viên {values['student_id']} vào phòng {values['room_id']}."

    @staticmethod
    def _save_service_use(values: dict[str, str]) -> str:
        date.fromisoformat(values["used_on"])
        quantity = int(values["quantity"])
        repository.add_service_use(
            values["student_id"], values["service_id"], values["used_on"], quantity
        )
        return "Đã ghi nhận lượt sử dụng; trigger CSDL tính tổng tiền."

    @staticmethod
    def _save_visit(values: dict[str, str]) -> str:
        date.fromisoformat(values["birth_date"])
        date.fromisoformat(values["visit_date"])
        repository.add_visitor_visit(
            values["cccd"],
            values["guest_name"],
            values["birth_date"],
            values["student_id"],
            values["visit_date"],
        )
        return "Đã lưu thông tin khách và ghi nhận lượt thăm."

    @staticmethod
    def _save_monthly_vehicle(values: dict[str, str]) -> str:
        date.fromisoformat(values["start_date"])
        date.fromisoformat(values["end_date"])
        vehicle_id = repository.register_monthly_vehicle(
            values["student_id"],
            values["plate"],
            values["vehicle_type"],
            values["start_date"],
            values["end_date"],
        )
        return f"Đã tạo xe {vehicle_id} và đăng ký vé tháng."


def run() -> None:
    app = DormitoryApp()
    app.mainloop()
