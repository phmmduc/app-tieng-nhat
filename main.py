import sys
import os
from PyQt5 import QtWidgets

from login_window import CuaSoDangNhap

if __name__ == "__main__":
    # Trỏ về thư mục gốc chứa TẤT CẢ code, ui, qss (không trỏ vào thư mục picture)

    app = QtWidgets.QApplication(sys.argv)

    main_window = CuaSoDangNhap()
    main_window.show()
1j2h3j1h23hj123

    sys.exit(app.exec())