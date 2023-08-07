import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QMessageBox, QPushButton
from PySide6.QtGui import Qt, QPixmap
from PySide6.QtCore import QSize
import qrcode

class ImageButton(QPushButton):
    def __init__(self, pixmap_path):
        super().__init__()
        self.pixmap = QPixmap(pixmap_path)
        self.setIcon(self.pixmap)
        self.setIconSize(QSize(80, 80))
        self.setStyleSheet("background-color: transparent; border: none;")
        self.setCursor(Qt.PointingHandCursor)


class QrCodeGenerator(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Shisaku QR Generator")
        self.setStyleSheet("background-color: black")
        self.setGeometry(300, 300, 300, 400)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)  # Adding internal margins to the layout

        h_layout = QHBoxLayout()

        self.text_bar = QLineEdit(self)
        self.text_bar.setPlaceholderText("Veuillez entrer l'url...")
        self.text_bar.setStyleSheet("background-color: white; color: black; border: 3px solid blue; border-radius: 30px;")
        self.text_bar.setFixedHeight(60)
        self.text_bar.setFixedWidth(200)
        h_layout.addWidget(self.text_bar)

        start_button = ImageButton(os.path.join(os.path.dirname(__file__), "img/button.png"))
        start_button.clicked.connect(self.start_button_clicked)
        h_layout.addWidget(start_button)

        # Set alignment for the horizontal layout to align to the top of the parent layout
        h_layout.setAlignment(Qt.AlignTop)

        layout.addLayout(h_layout)

        # Add a label to display the QR code image
        self.qr_code_label = QLabel(self)
        self.qr_code_label.setStyleSheet("margin-bottom: 50px;")
        self.qr_code_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.qr_code_label)

    def start_button_clicked(self):
        data = self.text_bar.text()
        if not data:
            self.show_error_message("Le champ est vide. Veuillez entrer une donnée pour générer le QR code.")
        else:
            qr = qrcode.QRCode(
                version=3,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,
                border=2
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Save the QR code image to a file
            img.save("qrcode.png")

            # Display the QR code image on the label
            qrcode_pixmap = QPixmap("qrcode.png")
            self.qr_code_label.setPixmap(qrcode_pixmap)

            self.text_bar.clear()

    def show_error_message(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.setWindowTitle("Champ Vide")
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.Ok)
        error_dialog.exec_()

if __name__ == "__main__":
    app = QApplication()
    window = QrCodeGenerator()
    window.show()
    sys.exit(app.exec())
