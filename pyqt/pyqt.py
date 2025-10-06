from PyQt6.QtWidgets import QApplication, QGridLayout, QTabWidget, QWidget
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QStatusBar
from PyQt6.QtWidgets import QToolBar
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction, QPixmap

# Tworzenie klasy głównego okna aplikacji dziedziczącej po QMainWindow


class Window(QMainWindow):
    # Dodanie konstruktora przyjmującego okno nadrzędne
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_path = None
        self.setWindowTitle("PyQt6 Lab")
        self.setGeometry(100, 100, 1240, 720)
        self.createMenu()
        self.createTabs()

    # Funkcja dodająca pasek menu do okna
    def createMenu(self):
        # Stworzenie paska menu
        self.menu = self.menuBar()
        # Dodanie do paska listy rozwijalnej o nazwie File
        self.fileMenu = self.menu.addMenu("File")
        self.actionExit = QAction("Exit", self)
        self.actionExit.setShortcut("Ctrl+Q")
        self.actionExit.triggered.connect(self.close)
        self.fileMenu.addAction(self.actionExit)

        self.task1Menu = self.menu.addMenu("Task 1")
        self.actionOpen = QAction("Open file", self)
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.triggered.connect(self.openImageDialog)
        self.task1Menu.addAction(self.actionOpen)

        self.task2Menu = self.menu.addMenu("Task 2")

        self.task3Menu = self.menu.addMenu("Task 3")
        # Dodanie do menu File pozycji zamykającej aplikacje

    # Funkcja dodająca wenętrzeny widżet do okna
    def createTabs(self):
        # Tworzenie widżetu posiadającego zakładki
        self.tabs = QTabWidget()

        # Stworzenie osobnych widżetów dla zakładek
        self.tab_1 = QWidget()
        self.tab_2 = QWidget()
        self.tab_3 = QWidget()

        # Dodanie zakładek do widżetu obsługującego zakładki
        self.tabs.addTab(self.tab_1, "Pierwsza zakładka")
        self.tabs.addTab(self.tab_2, "Druga zakładka")
        self.tabs.addTab(self.tab_3, "Trzecia zakładka")

        # Dodanie widżetu do głównego okna jako centralny widżet
        self.setCentralWidget(self.tabs)

        self.tab_1.layout = None
        self.tab_1.layout = QGridLayout()
        self.tab_1.image_label = QLabel("Brak obrazu")
        self.tab_1.layout.addWidget(self.tab_1.image_label, 0, 0)
        self.tab_1.setLayout(self.tab_1.layout)

        self.tab_2.layout = None
        self.tab_2.layout = QGridLayout()
        self.tab_2.layout.addWidget(QLabel("Zawartość drugiej zakładki"), 0, 0)
        self.tab_2.setLayout(self.tab_2.layout)

        # Dodanie paska stanu do okna
        self.setStatusBar(QStatusBar(self))

    # Funkcja obsługująca kliknięcie przycisku na pasku narzędzi
    def onMyToolBarButtonClick(self):
        self.statusBar().showMessage("Kliknięto przycisk na pasku narzędzi")

    def openImageDialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.image_path = selected_files[0]
                # Tu możesz dodać kod do wyświetlania obrazu w zakładce 1
                self.statusBar().showMessage(f"Wybrano plik: {self.image_path}")
                self.displayImageOnTab1(self.image_path)

    def displayImageOnTab1(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.tab_1.image_label.setPixmap(
                pixmap.scaled(
                    400,
                    400,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            self.tab_1.image_label.setText(
                ""
            )  # Usunięcie tekstu jeśli obraz jest wyświetlany
        else:
            self.tab_1.image_label.setText("Nie można załadować obrazu")


# Uruchomienie okna
app = QApplication([])
win = Window()
win.show()
app.exec()
