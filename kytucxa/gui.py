"""Giao diện sử dụng CustomTkinter để xuất báo cáo cho chương trình quản lí Ký túc xá và nhập dữ liệu"""
from __future__ import annotations

import csv
from datetime import date
from tkinter import filedialog, messagebox, ttk
from typing import Any, Callable

import customtkinter as ctk

from . import repository
from .db import connect


# --- WIDGET SƠ ĐỒ PHÒNG DẠNG LƯỚI (ROOM GRID) ---
class RoomGridFrame(ctk.CTkFrame):
    def __init__(self, master: Any) -> None:
        super().__init__(master, fg_color="transparent")

        # Thanh công cụ trên cùng
        top_bar = ctk.CTkFrame(self, corner_radius=12)
        top_bar.pack(fill="x", padx=16, pady=10)

        ctk.CTkLabel(
            top_bar, text="Sơ đồ phòng KTX", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left", padx=16, pady=10)

        ctk.CTkButton(
            top_bar, text="Tải lại sơ đồ", command=self.load_grid, height=36,
            corner_radius=8, font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="right", padx=16, pady=10)

        # Chú thích màu sắc
        legend = ctk.CTkFrame(top_bar, fg_color="transparent")
        legend.pack(side="right", padx=20)

        ctk.CTkLabel(legend, text="■ Đã đầy", text_color="#D9534F", font=("Segoe UI", 12, "bold")).pack(side="right", padx=8)
        ctk.CTkLabel(legend, text="■ Còn trống", text_color="#28A745", font=("Segoe UI", 12, "bold")).pack(side="right", padx=8)

        # Khung chứa danh sách các ô phòng có hỗ trợ cuộn (Scrollable)
        self.grid_scroll = ctk.CTkScrollableFrame(self, corner_radius=12)
        self.grid_scroll.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        self.load_grid()

        # Hiển thị frame lên giao diện mẹ
        self.pack(fill="both", expand=True)

    def load_grid(self) -> None:
        # Xóa các ô phòng cũ
        for widget in self.grid_scroll.winfo_children():
            widget.destroy()

        try:
            rooms = repository.room_occupancy()
            row, col = 0, 0
            max_cols = 5  # Hiển thị 5 phòng trên 1 hàng

            for room in rooms:
                so_phong = str(room.get("SoPhong", ""))
                loai_phong = str(room.get("LoaiPhong", ""))
                dang_o = int(room.get("SoNguoiDangO", 0))
                toi_da = int(room.get("SoNguoiToiDa", 0))

                # Đổi màu ô dựa trên sức chứa
                if dang_o >= toi_da:
                    bg_color = "#D9534F"  # Đỏ: Đã đầy
                    hover_color = "#C9302C"
                else:
                    bg_color = "#28A745"  # Xanh: Còn trống
                    hover_color = "#218838"

                # Tạo nút bấm đại diện cho phòng
                btn_text = f"Phòng {so_phong}\n{loai_phong}\n({dang_o}/{toi_da} SV)"
                room_btn = ctk.CTkButton(
                    self.grid_scroll,
                    text=btn_text,
                    fg_color=bg_color,
                    hover_color=hover_color,
                    width=170,
                    height=95,
                    corner_radius=10,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    command=lambda p=so_phong: self.show_room_details(p)
                )
                room_btn.grid(row=row, column=col, padx=12, pady=12)

                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

        except Exception as exc:
            messagebox.showerror("Lỗi tải sơ đồ phòng", str(exc))

    def show_room_details(self, so_phong: str) -> None:
        """Hiển thị cửa sổ pop-up danh sách sinh viên trong phòng khi nhấp chọn."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Chi tiết Phòng {so_phong}")
        dialog.geometry("550x380")
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog, text=f"Danh sách sinh viên phòng {so_phong}",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(padx=16, pady=12)

        table_frame = ctk.CTkFrame(dialog, corner_radius=8)
        table_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        tree = ttk.Treeview(
            table_frame,
            columns=["MaSV", "CCCD", "Lop", "QueQuan"],
            show="headings",
            height=8
        )
        tree.heading("MaSV", text="Mã SV")
        tree.heading("CCCD", text="CCCD")
        tree.heading("Lop", text="Lớp")
        tree.heading("QueQuan", text="Quê quán")

        tree.column("MaSV", width=80, anchor="center")
        tree.column("CCCD", width=120, anchor="center")
        tree.column("Lop", width=90, anchor="center")
        tree.column("QueQuan", width=140, anchor="center")

        tree.pack(fill="both", expand=True, padx=8, pady=8)

        # Lấy dữ liệu hồ sơ sinh viên để lọc theo số phòng
        try:
            all_students = repository.student_summary("")
            room_students = [s for s in all_students if str(s.get("SoPhong", "")) == str(so_phong)]

            for index, sv in enumerate(room_students):
                tree.insert("", "end", values=[
                    sv.get("MaSV", ""),
                    sv.get("SV_CCCD", ""),
                    sv.get("Lop", ""),
                    sv.get("QueQuan", "")
                ])
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy thông tin sinh viên: {e}")


# Frame báo cáo (nhận điều kiện rồi truy vấn tạo bảng)
class ReportFrame(ctk.CTkFrame):
    def __init__(
            self,
            master: Any,
            columns: list[tuple[str, str, int]],
            runner: Callable[[dict[str, str]], list[dict[str, Any]]],
            fields: list[tuple[str, str]],
            note: str = "",
            require_fields: bool = True,
            action: tuple[str, Callable[[dict[str, str]], str]] | None = None,
    ) -> None:
        super().__init__(master, fg_color="transparent")
        self.columns = columns
        self.runner = runner
        self.require_fields = require_fields
        self.action = action
        self.fields: dict[str, ctk.CTkEntry] = {}
        self.rows: list[dict[str, Any]] = []

        if note:
            ctk.CTkLabel(
                self, text=note, anchor="w", wraplength=1100,
                font=ctk.CTkFont(size=13), text_color=("#526174", "#b6c2d2"),
            ).pack(
                fill="x", padx=18, pady=(14, 6)
            )

        controls = ctk.CTkFrame(self, corner_radius=12)
        controls.pack(fill="x", padx=16, pady=8)
        for index, (key, label) in enumerate(fields):
            ctk.CTkLabel(
                controls, text=label, font=ctk.CTkFont(size=13, weight="bold")
            ).grid(
                row=0, column=index * 2, padx=(14, 6), pady=12, sticky="e"
            )
            entry = ctk.CTkEntry(
                controls, width=155, height=38, font=ctk.CTkFont(size=14),
                corner_radius=8, placeholder_text=label,
            )
            entry.grid(row=0, column=index * 2 + 1, padx=(0, 10), pady=10)
            self.fields[key] = entry

        self.run_button = ctk.CTkButton(
            controls, text="Xem báo cáo", command=self.run, height=38,
            corner_radius=8, font=ctk.CTkFont(size=13, weight="bold"),
        )
        self.run_button.grid(row=0, column=len(fields) * 2, padx=(10, 6), pady=10)
        ctk.CTkButton(
            controls, text="Xuất CSV", command=self.export_csv, height=38,
            corner_radius=8, fg_color=("#e8eef7", "#263449"),
            hover_color=("#d8e2f0", "#354761"),
            text_color=("#26364a", "#e4ebf5"),
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(
            row=0, column=len(fields) * 2 + 1, padx=5, pady=10
        )
        if action:
            ctk.CTkButton(
                controls, text=action[0], command=self.run_action, height=38,
                corner_radius=8, font=ctk.CTkFont(size=13, weight="bold"),
            ).grid(row=0, column=len(fields) * 2 + 2, padx=5, pady=10)

        table_frame = ctk.CTkFrame(self, corner_radius=12)
        table_frame.pack(fill="both", expand=True, padx=16, pady=(2, 10))
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "KyTucXa.Treeview", font=("Segoe UI", 12), rowheight=34,
            background="#ffffff", fieldbackground="#ffffff", foreground="#243247",
            borderwidth=0,
        )
        style.configure(
            "KyTucXa.Treeview.Heading", font=("Segoe UI", 12, "bold"),
            background="#eaf0f8", foreground="#26364a", relief="flat", padding=(9, 9),
        )
        style.map(
            "KyTucXa.Treeview",
            background=[("selected", "#cfe0ff")],
            foreground=[("selected", "#172b4d")],
        )
        self.tree = ttk.Treeview(
            table_frame,
            columns=[key for key, _, _ in columns],
            show="headings",
            height=18,
            style="KyTucXa.Treeview",
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
            self.tree.heading(key, text=title, anchor="center")
            self.tree.column(
                key, width=max(width, 100), minwidth=90, anchor="center", stretch=True
            )
        self.tree.tag_configure("odd", background="#f4f7fb")
        self.tree.tag_configure("even", background="#ffffff")
        self.status = ctk.CTkLabel(
            self, text="", anchor="w", font=ctk.CTkFont(size=12),
            text_color=("#526174", "#b6c2d2"),
        )
        self.status.pack(fill="x", padx=18, pady=(0, 10))
        self.pack(fill="both", expand=True)

    def set_field(self, key: str, value: str) -> None:
        field = self.fields[key]
        field.delete(0, "end")
        field.insert(0, value)

    def run(self) -> None:
        try:
            values = {key: field.get().strip() for key, field in self.fields.items()}
            if self.require_fields and any(not value for value in values.values()):
                raise ValueError("Vui lòng nhập đủ thông tin lọc.")
            rows = self.runner(values)
            self.rows = rows
            self.tree.delete(*self.tree.get_children())
            for index, row in enumerate(rows):
                cells = []
                for key, _, _ in self.columns:
                    value = row.get(key, "")
                    if isinstance(value, (int, float)):
                        value = f"{value:,}"
                    cells.append("" if value is None else str(value))
                self.tree.insert("", "end", values=cells, tags=("even" if index % 2 else "odd",))
            self.status.configure(text=f"Có {len(rows)} dòng.")
        except Exception as exc:
            messagebox.showerror("Không thể chạy báo cáo", str(exc))

    def export_csv(self) -> None:
        if not self.rows:
            messagebox.showinfo("Xuất CSV", "Hãy chạy báo cáo trước khi xuất.")
            return
        path = filedialog.asksaveasfilename(
            title="Lưu báo cáo CSV",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
        )
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as output:
                writer = csv.writer(output)
                writer.writerow([title for _, title, _ in self.columns])
                for row in self.rows:
                    writer.writerow([row.get(key, "") for key, _, _ in self.columns])
            self.status.configure(text=f"Đã xuất {len(self.rows)} dòng: {path}")
        except Exception as exc:
            messagebox.showerror("Không thể xuất CSV", str(exc))

    def run_action(self) -> None:
        if not self.action:
            return
        try:
            values = {key: field.get().strip() for key, field in self.fields.items()}
            if self.require_fields and any(not value for value in values.values()):
                raise ValueError("Vui lòng nhập đủ thông tin.")
            messagebox.showinfo(self.action[0], self.action[1](values))
        except Exception as exc:
            messagebox.showerror(self.action[0], str(exc))


# Frame nhập dữ liệu vào database
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
        ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=21, weight="bold")).pack(
            anchor="w", padx=20, pady=(20, 8)
        )
        if note:
            ctk.CTkLabel(
                self, text=note, anchor="w", wraplength=1000,
                font=ctk.CTkFont(size=13), text_color=("#526174", "#b6c2d2"),
            ).pack(
                anchor="w", padx=20, pady=(0, 10)
            )
        self.entries: dict[str, ctk.CTkEntry] = {}
        form = ctk.CTkFrame(self, corner_radius=12)
        form.pack(fill="x", padx=18, pady=10)
        for index, (key, label) in enumerate(fields):
            row, col = divmod(index, 2)
            ctk.CTkLabel(
                form, text=label, font=ctk.CTkFont(size=13, weight="bold")
            ).grid(
                row=row, column=col * 2, padx=(16, 7), pady=11, sticky="e"
            )
            entry = ctk.CTkEntry(
                form, width=240, height=40, font=ctk.CTkFont(size=14), corner_radius=8
            )
            entry.grid(row=row, column=col * 2 + 1, padx=(0, 18), pady=10, sticky="ew")
            self.entries[key] = entry
        form.grid_columnconfigure(1, weight=1)
        form.grid_columnconfigure(3, weight=1)
        ctk.CTkButton(
            self, text="Lưu thông tin", command=lambda: self._submit(submit),
            height=40, width=170, corner_radius=9,
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(
            anchor="center", padx=18, pady=12
        )
        self.status = ctk.CTkLabel(
            self, text="", anchor="w", wraplength=1000, font=ctk.CTkFont(size=13)
        )
        self.status.pack(anchor="w", padx=20, pady=10)
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
        self.geometry("1360x850")
        self.minsize(1040, 700)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        header = ctk.CTkFrame(self, corner_radius=16, fg_color=("#ffffff", "#202b3b"))
        header.pack(fill="x", padx=18, pady=(18, 8))
        title_block = ctk.CTkFrame(header, fg_color="transparent")
        title_block.pack(side="left", padx=18, pady=14)
        ctk.CTkLabel(
            title_block,
            text="Ký túc xá", font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#17365d",
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_block, text="Quản lý sinh viên · dịch vụ · phòng ở",
            font=ctk.CTkFont(size=13), text_color="#64748b",
        ).pack(anchor="w", pady=(2, 0))
        ctk.CTkLabel(
            header, text="MySQL  ·  localhost:3306  ·  KyTucXa",
            font=ctk.CTkFont(size=12), text_color="#64748b",
        ).pack(side="left", padx=22)
        ctk.CTkButton(
            header, text="Kiểm tra kết nối", command=self.check_connection,
            height=40, corner_radius=9, font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(
            side="right", padx=18, pady=14
        )

        self.tabs = ctk.CTkTabview(self, corner_radius=14, border_width=0)
        self.tabs.pack(fill="both", expand=True, padx=18, pady=(4, 18))
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

        # TAB 1: Sơ đồ phòng trực quan (Lưới)
        grid_tab = subtabs.add("Sơ đồ phòng (Lưới)")
        RoomGridFrame(grid_tab)

        # TAB 2: Chi phí tháng
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
            action=("Tạo hóa đơn tháng", self._create_invoices),
        )
        pane.set_field("month", month)

        # TAB 3: Sức chứa phòng dạng bảng
        ReportFrame(
            subtabs.add("Sức chứa phòng"),
            [
                ("SoPhong", "Phòng", 90),
                ("LoaiPhong", "Loại phòng", 180),
                ("DonGiaThang", "Giá tháng", 130),
                ("SoNguoiToiDa", "Sức chứa", 110),
                ("SoNguoiDangO", "Đang ở", 100),
                ("ChoTrong", "Còn trống", 100),
            ],
            lambda _v: repository.room_occupancy(),
            [],
            "Tổng hợp số sinh viên đang ở và số chỗ còn trống theo từng phòng.",
            require_fields=False,
        )

        # TAB 4: Hồ sơ sinh viên
        pane = ReportFrame(
            subtabs.add("Hồ sơ sinh viên"),
            [
                ("MaSV", "Mã SV", 100), ("SV_CCCD", "CCCD", 150),
                ("Lop", "Lớp", 110), ("NgaySinh", "Ngày sinh", 110),
                ("QueQuan", "Quê quán", 130), ("SoPhong", "Phòng", 80),
                ("LoaiPhong", "Loại phòng", 150), ("DonGiaThang", "Giá phòng", 120),
                ("SoLuotDichVu", "Lượt dịch vụ", 110),
                ("SoLuotKhachTham", "Lượt khách", 100),
                ("SoXe", "Số xe", 80), ("SoVeThangConHan", "Vé còn hạn", 100),
            ],
            lambda v: repository.student_summary(v["student_id"]),
            [("student_id", "Mã sinh viên")],
            "Tra cứu thông tin cơ bản và số liệu hoạt động liên quan của một sinh viên.",
        )

        # TAB 5: Dịch vụ theo kỳ
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

        # TAB 6: Khách thăm
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

        # TAB 7: Doanh thu dịch vụ
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
            subtabs.add("Chuyển phòng"),
            "Chuyển sinh viên sang phòng khác",
            [("student_id", "Mã sinh viên"), ("room_id", "Số phòng mới")],
            self._transfer_student,
            "Kiểm tra chỗ trống trước khi chuyển; trigger sức chứa trong CSDL cũng được áp dụng.",
        )

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
    def _create_invoices(values: dict[str, str]) -> str:
        month = values["month"]
        date.fromisoformat(f"{month}-01")
        created, skipped = repository.create_monthly_invoices(month)
        return f"Đã tạo {created} hóa đơn; bỏ qua {skipped} sinh viên đã có hóa đơn trong tháng {month}."

    @staticmethod
    def _transfer_student(values: dict[str, str]) -> str:
        repository.transfer_student(values["student_id"], values["room_id"])
        return f"Đã chuyển {values['student_id']} sang phòng {values['room_id']}."

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
        vehicle_id, created = repository.register_monthly_vehicle(
            values["student_id"],
            values["plate"],
            values["vehicle_type"],
            values["start_date"],
            values["end_date"],
        )
        if created:
            return f"Đã tạo xe {vehicle_id} mới và đăng ký vé tháng."
        return f"Biển số đã có, đã thêm vé tháng cho xe {vehicle_id}."


def run() -> None:
    app = DormitoryApp()
    app.mainloop()