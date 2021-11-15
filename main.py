from re import search
import sys
import webScrapping as WS
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QPainter
from PySide6.QtWidgets import (QLabel, QLineEdit, QPushButton, QApplication,
    QGridLayout, QWidget, QMainWindow, QTableWidgetItem, QTableWidget, QHeaderView)

class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.items = 0

        # Create widgets
        self.title = QLabel("WebScrapping App")
        self.title.setStyleSheet("color: black; font-size: 30pt; text-align: right")
        self.label = QLabel("Search :")
        self.research = QLineEdit()
        self.button = QPushButton("Enter")
        self.button.setShortcut("Return")

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date", "Name", "Size", "Ratio", "Link"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Create layout and add widgets
        layout = QGridLayout()
        layout.addWidget(self.title, 0 ,0)
        layout.addWidget(self.label, 1, 0)
        layout.addWidget(self.research, 1, 1)
        layout.addWidget(self.button, 1, 2)
        layout.addWidget(self.table, 2, 0, 1, 3)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.run_search)
        
    @Slot()
    # Greets the user
    def run_search(self):
        print ("Running search")
        self.add_element()
        print ("Table print")
    """
    def fill_table(self, data=None):
        self.torrents = WS.WebScrapping.get_result(f"{self.research.text()}")

        for torrent in self.torrents:
            torrent_name = QTableWidgetItem(torrent.name)
            torrent_seed = QTableWidgetItem(f"{torrent.seed:.4f}")
            torrent.seed.setTextAlignment(Qt.AlignRight)
            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, torrent_name)
            self.table.setItem(self.items, 1, torrent_seed)
            self.items += 1
    """
    @Slot()
    def add_element(self):
        #self.table.setRowCount(0)
        #self.table.setRowCount(20)
        torrents = WS.WebScrapping(self.research.text()).get_result()
        try:
            for torrent in torrents:
                date_item = QTableWidgetItem(torrent.date)
                date_item.setTextAlignment(Qt.AlignLeft)

                name_item = QTableWidgetItem(torrent.name)
                name_item.setTextAlignment(Qt.AlignRight)

                size_item = QTableWidgetItem(str(torrent.size)+ "Gb")
                size_item.setTextAlignment(Qt.AlignLeft)

                ratio_item = QTableWidgetItem(str(torrent.seed) +"/"+ str(torrent.leech))
                ratio_item.setTextAlignment(Qt.AlignLeft)

                button_item = QPushButton("Stream")
                #button_item.clicked.connect(self.get_stream(torrent.src, torrent.link))

                self.table.insertRow(self.items)

                self.table.setItem(self.items, 0, date_item)
                self.table.setItem(self.items, 1, name_item)
                self.table.setItem(self.items, 2, size_item)
                self.table.setItem(self.items, 3, ratio_item)
                self.table.setCellWidget(self.items, 4, button_item)
                #self.table.setItem(self.items, 4, button_item)
                self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

                self.items += 1
        except ValueError:
            print("Wrong price", self.research)
    @Slot()
    def get_stream(self, src, link):
        magnet = WS.WebScrapping.get_magnet(src, link)
        print (magnet)
        return magnet
class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("WebScrapping App")
        
        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(exit_action)
        self.setCentralWidget(widget)

    @Slot()
    def exit_app(self):
            QApplication.quit()
    

if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    widget = Widget()
    # QMainWindow using QWidget as central widget
    window = MainWindow(widget)
    window.resize(1200, 800)
    window.show()

    # Execute application
    sys.exit(app.exec())
