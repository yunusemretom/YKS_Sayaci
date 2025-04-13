from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMenu
from PySide6.QtCore import Qt, QTimer, QPoint, QDateTime
from PySide6.QtGui import QFont, QPainter, QColor, QAction
import json
import sys

# Sayaç tarihi: YKS 2025 için örnek tarih
target_date = QDateTime.fromString("2025-06-21 10:15:00", "yyyy-MM-dd hh:mm:ss")

class TransparentCountdown(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(300, 100)
        try:
            with open("settings.json", "r") as f:
                self.data = json.load(f)
                self.setGeometry(self.data["x_coordinate"], self.data["y_coordinate"], 60, 30)
        except FileNotFoundError:

            self.setGeometry(1230, 660, 60, 30)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 16, QFont.Bold))
        self.label.setStyleSheet("color: white;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)  # her saniye yenile
        self.update_countdown()

        self.drag_position = QPoint()
        self.onceki_konum = self.pos()

    def moveEvent(self, event):
        """Pencerenin konumu değiştiğinde tetiklenen olay."""
        yeni_konum = self.pos()
        if yeni_konum != self.onceki_konum:
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump({"x_coordinate": yeni_konum.x(), "y_coordinate": yeni_konum.y()}, f,ensure_ascii=False)
            
            # Burada pencere konumu değiştiğinde yapmak istediğiniz diğer işlemleri tanımlayabilirsiniz.
            self.onceki_konum = yeni_konum
        super().moveEvent(event)  # Temel sınıfın moveEvent'ini de çağırın

    
        

    def update_countdown(self):
        now = QDateTime.currentDateTime()
        remaining = now.secsTo(target_date)

        if remaining > 0:
            days = remaining // 86400
            hours = (remaining % 86400) // 3600
            minutes = (remaining % 3600) // 60
            seconds = remaining % 60
            self.label.setText(f"YKS'ye Kalan Süre\n{days}g {hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            self.label.setText("Sınav Günü Geldi! 🎉")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Hafif şeffaf siyah arka plan
        painter.setBrush(QColor(0, 0, 0, 0))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
    
    def closeEvent(self, event):
        """Pencere kapatılırken tetiklenen olay."""
        self.timer.stop()  # Timer'ı durdur
        event.accept() # Kapatma olayını kabul et
        exit()
        
    def contextMenuEvent(self, event):
        """Sağ tıklama yapıldığında bağlam menüsünü gösterir."""
        context_menu = QMenu(self)
        kapat_action = QAction("Kapat", self)
        kapat_action.triggered.connect(self.close)
        context_menu.addAction(kapat_action)
        context_menu.exec(event.globalPos())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = TransparentCountdown()
    widget.show()
    exit_code = app.exec() # Uygulama çıktığında exit kodunu al
    sys.exit(exit_code) # Sistemden çık
