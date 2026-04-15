import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt


class QuizApp(QtWidgets.QMainWindow):
    def __init__(self, quiz_data):
        super().__init__()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(base_dir, "quizzcheckui.ui"), self)

        self.quiz_data = quiz_data
        self.current_index = 0

        # 1. Gom nhóm nút và thiết lập ban đầu
        self.buttons = []
        for name in ['pushButton', 'pushButton_2', 'pushButton_3', 'pushButton_4']:
            if hasattr(self, name):
                btn = getattr(self, name)
                btn.setCheckable(True)
                btn.setAutoExclusive(True)
                self.buttons.append(btn)

        # 2. Kết nối nút điều hướng
        if hasattr(self, 'btn_tiep'):
            self.btn_tiep.clicked.connect(self.next_question)
        if hasattr(self, 'btn_truoc'):
            self.btn_truoc.clicked.connect(self.prev_question)

        # 3. Kết nối sự kiện chọn đáp án
        for i, btn in enumerate(self.buttons):
            btn.clicked.connect(lambda checked, idx=i: self.check_answer(idx))

        self.load_question()

    def load_question(self):
        """Hàm này sẽ reset mọi thứ khi sang câu mới"""
        data = self.quiz_data[self.current_index]
        self.label_cauhoi.setText(data["question"])

        # Reset ProgressBar
        phan_tram = int(((self.current_index + 1) / len(self.quiz_data)) * 100)
        self.progressBar.setValue(phan_tram)

        # QUAN TRỌNG: Reset trạng thái của 4 nút đáp án
        for btn in self.buttons:
            btn.setEnabled(True)  # Mở khóa cho phép bấm
            btn.setStyleSheet("")  # Xóa màu xanh/đỏ của câu trước

            # Tắt AutoExclusive tạm thời để bỏ chọn (Checked = False)
            btn.setAutoExclusive(False)
            btn.setChecked(False)
            btn.setAutoExclusive(True)  # Bật lại để chỉ chọn được 1 nút

        # Cập nhật text đáp án mới
        for i, btn in enumerate(self.buttons):
            if i < len(data["options"]):
                btn.setText(data["options"][i])
                btn.show()  # Hiện nút nếu trước đó bị ẩn
            else:
                btn.hide()  # Ẩn nút nếu câu hỏi có ít hơn 4 đáp án

        self.frame_giaithich.hide()

    def check_answer(self, idx):
        """Xử lý hiển thị Đúng/Sai khi người dùng click"""
        data = self.quiz_data[self.current_index]
        correct_idx = data.get("correct_idx", -1)

        # Hiện giải thích
        self.label_noidung_gt.setText(data["explanation"])
        self.frame_giaithich.show()

        # Đổi màu trực tiếp bằng code để báo hiệu
        for i, btn in enumerate(self.buttons):
            if i == correct_idx:
                # Đáp án đúng luôn hiện màu xanh
                btn.setStyleSheet("background-color: #58cc02; color: white; border-radius: 10px; font-weight: bold;")
            elif i == idx:
                # Nếu bạn chọn sai, nút bạn chọn hiện màu đỏ
                btn.setStyleSheet("background-color: #ff4b4b; color: white; border-radius: 10px; font-weight: bold;")

            # Khóa tất cả các nút lại để người dùng không chọn lại câu này
            btn.setEnabled(False)

    def next_question(self):
        if self.current_index < len(self.quiz_data) - 1:
            self.current_index += 1
            self.load_question()  # Gọi hàm này để reset giao diện cho câu mới
        else:
            QtWidgets.QMessageBox.information(self, "Thông báo", "Bạn đã hoàn thành bài tập!")

    def prev_question(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_question()  # Quay lại cũng phải reset trạng thái