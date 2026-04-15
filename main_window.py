import os
import json
from PyQt5 import QtWidgets, uic, sip
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from quizzcode import QuizApp  # Import class Quiz từ file quizzcode.py


class CuaSoChinh(QtWidgets.QMainWindow):
    def __init__(self, ten_nguoi_dung):
        super().__init__()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(base_dir, "mainchinh.ui"), self)

        # Biến quản lý cửa sổ Quiz để tránh mở chồng chéo hoặc lỗi bộ nhớ
        self.cua_so_quiz = None

        self.setWindowTitle(f"App Học Tiếng Nhật - こんにちは {ten_nguoi_dung}!")
        self.showMaximized()

        # 1. ĐỌC DỮ LIỆU TỪ FILE JSON
        json_path = os.path.join(base_dir, "data_quizz.json")
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                self.kho_du_lieu_quizz = json.load(f)
        except Exception as e:
            print("Lỗi khi đọc file JSON:", e)
            self.kho_du_lieu_quizz = {}

        # 2. KẾT NỐI NÚT QUIZZ DÙNG CHUNG (Dựa trên ảnh của bạn là btn_quizz)
        if hasattr(self, 'btn_quizz'):
            self.btn_quizz.clicked.connect(self.mo_quizz_theo_trang)

        # 3. KẾT NỐI 10 NÚT DANH SÁCH BÊN TRÁI (Chỉ để lật trang lý thuyết)
        for i in range(1, 11):
            nut_ten = f"btn_bai{i}"
            if hasattr(self, nut_ten):
                nut_bam = getattr(self, nut_ten)
                # Khi bấm nút bài: chỉ lật trang trong QStackedWidget (tên là 'pages')
                nut_bam.clicked.connect(lambda checked, idx=i: self.pages.setCurrentIndex(idx))

        # 4. LOAD STYLE QSS
        qss_file_path = os.path.join(base_dir, 'style_main.qss')
        if os.path.exists(qss_file_path):
            with open(qss_file_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())

        # 5. CÁC NÚT ĐIỀU HƯỚNG DƯỚI CÙNG
        self.btn_truoc.clicked.connect(self.mo_bai_truoc)
        self.btn_tiep.clicked.connect(self.mo_bai_tiep)
        self.btn_dang_xuat.clicked.connect(self.dang_xuat)

        self.load_bang_katakana_co_ban()

    def mo_quizz_theo_trang(self):
        """Tự động lấy index trang hiện tại để mở đúng bài trắc nghiệm"""
        # Đóng cửa sổ cũ an toàn (nếu đang mở) bằng thư viện sip
        if self.cua_so_quiz is not None and not sip.isdeleted(self.cua_so_quiz):
            self.cua_so_quiz.close()
            self.cua_so_quiz = None

        # Lấy chỉ số trang hiện tại (Ví dụ: Bài 1 đang ở index 1)
        index_hien_tai = self.pages.currentIndex()

        # Tạo khóa tìm kiếm trong JSON (Ví dụ: "bai_1")
        ten_key = f"bai_{index_hien_tai}"
        du_lieu_bai_tap = self.kho_du_lieu_quizz.get(ten_key, [])

        if du_lieu_bai_tap:
            self.cua_so_quiz = QuizApp(du_lieu_bai_tap)
            self.cua_so_quiz.show()
        else:
            QtWidgets.QMessageBox.information(self, "Thông báo", f"Hiện chưa có bài tập cho nội dung này ({ten_key})")

    def mo_bai_truoc(self):
        if self.pages.currentIndex() > 0:
            self.pages.setCurrentIndex(self.pages.currentIndex() - 1)

    def mo_bai_tiep(self):
        if self.pages.currentIndex() < self.pages.count() - 1:
            self.pages.setCurrentIndex(self.pages.currentIndex() + 1)

    def dang_xuat(self):
        if self.cua_so_quiz and not sip.isdeleted(self.cua_so_quiz):
            self.cua_so_quiz.close()
        self.close()
        from login_window import CuaSoDangNhap
        self.man_hinh_dang_nhap = CuaSoDangNhap()
        self.man_hinh_dang_nhap.show()

    def load_bang_katakana_co_ban(self):
        # Giữ nguyên code load bảng Katakana của bạn...
        pass