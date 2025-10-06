from PyQt6.QtWidgets import QApplication, QGridLayout, QTabWidget, QWidget, QSpinBox
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QStatusBar
from PyQt6.QtWidgets import QToolBar
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction, QPixmap, QKeySequence

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
        self.actionExit.triggered.connect(self.close)
        self.fileMenu.addAction(self.actionExit)

        self.task1Menu = self.menu.addMenu("Task 1")
        self.actionOpen = QAction("Open file", self)
        self.actionOpen.setShortcut(QKeySequence("Ctrl+G"))
        self.actionOpen.triggered.connect(self.openImageDialog)
        self.task1Menu.addAction(self.actionOpen)

        self.task2Menu = self.menu.addMenu("Task 2")
        self.actionOpen = QAction("Clear", self)
        self.actionOpen.setShortcut(QKeySequence("Ctrl+W"))
        self.actionOpen.triggered.connect(self.ClearTxtBox)
        self.task2Menu.addAction(self.actionOpen)
        self.actionOpen = QAction("Open", self)
        self.actionOpen.setShortcut(QKeySequence("Ctrl+O"))
        self.actionOpen.triggered.connect(self.OpenTxtFile)
        self.task2Menu.addAction(self.actionOpen)
        self.actionOpen = QAction("Save", self)
        self.actionOpen.setShortcut(QKeySequence("Ctrl+S"))
        self.actionOpen.triggered.connect(self.SaveTxtFile)
        self.task2Menu.addAction(self.actionOpen)
        self.actionOpen = QAction("Save As", self)
        self.actionOpen.setShortcut(QKeySequence("Ctrl+K"))
        self.actionOpen.triggered.connect(self.SaveAsTxtFile)
        self.task2Menu.addAction(self.actionOpen)

        self.task3Menu = self.menu.addMenu("Task 3")
        self.actionClearTab3 = QAction("Clear", self)
        self.actionClearTab3.setShortcut(QKeySequence("Ctrl+Q"))
        self.actionClearTab3.triggered.connect(self.clearTab3Fields)
        self.task3Menu.addAction(self.actionClearTab3)

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

        self.tab_2.layout.addWidget(QLabel("Tytuł:"), 0, 0)
        self.title_field = QLineEdit()
        self.tab_2.layout.addWidget(self.title_field, 0, 1, 1, 2)

        self.tab_2.layout.addWidget(QLabel("Treść:"), 1, 0)
        self.content_field = QTextEdit()
        self.tab_2.layout.addWidget(self.content_field, 1, 1, 1, 2)

        self.open_button = QPushButton("Open")
        self.save_button = QPushButton("Zapisz")
        self.save_as_button = QPushButton("Save As")
        self.clear_button = QPushButton("Wyczyść")

        self.open_button.clicked.connect(self.OpenTxtFile)
        self.save_button.clicked.connect(self.SaveTxtFile)
        self.save_as_button.clicked.connect(self.SaveAsTxtFile)
        self.clear_button.clicked.connect(self.ClearTxtBox)

        self.tab_2.layout.addWidget(self.open_button, 2, 0)
        self.tab_2.layout.addWidget(self.save_button, 2, 1)
        self.tab_2.layout.addWidget(self.save_as_button, 2, 2)
        self.tab_2.layout.addWidget(self.clear_button, 2, 3)

        self.tab_2.setLayout(self.tab_2.layout)

        self.tab_3.layout = None
        self.tab_3.layout = QGridLayout()

        self.tab_3.layout.addWidget(QLabel("Pole A:"), 0, 0)
        self.field_a = QLineEdit()
        self.field_a.textChanged.connect(self.updateConcatenatedField)
        self.tab_3.layout.addWidget(self.field_a, 0, 1)

        self.tab_3.layout.addWidget(QLabel("Pole B:"), 1, 0)
        self.field_b = QLineEdit()
        self.field_b.textChanged.connect(self.updateConcatenatedField)
        self.tab_3.layout.addWidget(self.field_b, 1, 1)

        self.tab_3.layout.addWidget(QLabel("Pole C:"), 2, 0)

        self.field_c = QSpinBox()
        self.field_c.setValue(0)
        self.field_c.valueChanged.connect(self.updateConcatenatedField)
        self.tab_3.layout.addWidget(self.field_c, 2, 1)

        self.tab_3.layout.addWidget(QLabel("Pole A + B + C:"), 3, 0)
        self.field_concatenated = QLineEdit()
        self.field_concatenated.setReadOnly(True)
        self.tab_3.layout.addWidget(self.field_concatenated, 3, 1)

        self.clear_tab3_button = QPushButton("Clear (Ctrl+Q)")
        self.clear_tab3_button.clicked.connect(self.clearTab3Fields)
        self.tab_3.layout.addWidget(self.clear_tab3_button, 4, 0, 1, 2)

        self.tab_3.setLayout(self.tab_3.layout)

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
                self.statusBar().showMessage(f"Wybrano plik: {self.image_path}")
                self.displayImageOnTab1(self.image_path)

    def displayImageOnTab1(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.tab_1.image_label.setPixmap(
                pixmap.scaled(
                    600,
                    600,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            self.tab_1.image_label.setText("")
        else:
            self.tab_1.image_label.setText("Nie można załadować obrazu")

    def ClearTxtBox(self):
        self.title_field.clear()
        self.content_field.clear()
        self.statusBar().showMessage("Wyczyszczono pola tekstowe")

    def OpenTxtFile(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Text files (*.txt);;All files (*.*)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                txt_path = selected_files[0]
                try:
                    with open(txt_path, "r", encoding="utf-8") as file:
                        content = file.read()
                        import os

                        filename = os.path.basename(txt_path)
                        self.title_field.setText(filename)
                        self.content_field.setPlainText(content)
                        self.statusBar().showMessage(f"Otwarto plik: {txt_path}")
                except Exception as e:
                    self.statusBar().showMessage(
                        f"Błąd podczas otwierania pliku: {str(e)}"
                    )

    def SaveTxtFile(self):
        title = self.title_field.text()
        content = self.content_field.toPlainText()

        if not title and not content:
            self.statusBar().showMessage("Brak treści do zapisania")
            return

        if not title:
            title = "untitled.txt"

        if not title.endswith(".txt"):
            title += ".txt"

        try:
            with open(title, "w", encoding="utf-8") as file:
                file.write(content)
            self.statusBar().showMessage(f"Zapisano plik: {title}")
        except Exception as e:
            self.statusBar().showMessage(f"Błąd podczas zapisywania: {str(e)}")

    def SaveAsTxtFile(self):
        title = self.title_field.text()
        content = self.content_field.toPlainText()

        if not title and not content:
            self.statusBar().showMessage("Brak treści do zapisania")
            return

        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("Text files (*.txt);;All files (*.*)")
        file_dialog.setDefaultSuffix("txt")

        if title:
            if title.endswith(".txt"):
                title = title[:-4]
            file_dialog.selectFile(title)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(content)

                    import os

                    filename = os.path.basename(file_path)
                    self.title_field.setText(filename)

                    self.statusBar().showMessage(f"Zapisano plik jako: {file_path}")
                except Exception as e:
                    self.statusBar().showMessage(f"Błąd podczas zapisywania: {str(e)}")

    def ClearTxtBox(self):
        self.title_field.clear()
        self.content_field.clear()
        self.statusBar().showMessage("Wyczyszczono pola tekstowe")

    def OpenTxtFile(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Text files (*.txt);;All files (*.*)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                txt_path = selected_files[0]
                try:
                    with open(txt_path, "r", encoding="utf-8") as file:
                        content = file.read()
                        import os

                        filename = os.path.basename(txt_path)
                        self.title_field.setText(filename)
                        self.content_field.setPlainText(content)
                        self.statusBar().showMessage(f"Otwarto plik: {txt_path}")
                except Exception as e:
                    self.statusBar().showMessage(
                        f"Błąd podczas otwierania pliku: {str(e)}"
                    )

    def SaveTxtFile(self):
        title = self.title_field.text()
        content = self.content_field.toPlainText()

        if not title and not content:
            self.statusBar().showMessage("Brak treści do zapisania")
            return

        if not title:
            title = "untitled.txt"

        if not title.endswith(".txt"):
            title += ".txt"

        try:
            with open(title, "w", encoding="utf-8") as file:
                file.write(content)
            self.statusBar().showMessage(f"Zapisano plik: {title}")
        except Exception as e:
            self.statusBar().showMessage(f"Błąd podczas zapisywania: {str(e)}")

    def SaveAsTxtFile(self):
        title = self.title_field.text()
        content = self.content_field.toPlainText()

        if not title and not content:
            self.statusBar().showMessage("Brak treści do zapisania")
            return

        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("Text files (*.txt);;All files (*.*)")
        file_dialog.setDefaultSuffix("txt")

        if title:
            if title.endswith(".txt"):
                title = title[:-4]
            file_dialog.selectFile(title)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(content)
                    import os

                    filename = os.path.basename(file_path)
                    self.title_field.setText(filename)

                    self.statusBar().showMessage(f"Zapisano plik jako: {file_path}")
                except Exception as e:
                    self.statusBar().showMessage(f"Błąd podczas zapisywania: {str(e)}")

    def validateNumericInput(self):
        text = self.field_c.text()
        if text and not text.replace(".", "").replace("-", "").isdigit():
            self.field_c.setText(text[:-1])

    def updateConcatenatedField(self):
        field_a_text = self.field_a.text()
        field_b_text = self.field_b.text()
        field_c_text = self.field_c.text()

        concatenated = field_a_text + field_b_text + field_c_text
        self.field_concatenated.setText(concatenated)

    def clearTab3Fields(self):
        self.field_a.clear()
        self.field_b.clear()
        self.field_c.clear()
        self.field_concatenated.clear()
        self.statusBar().showMessage("Wyczyszczono pola zakładki 3")


# Uruchomienie okna
app = QApplication([])
win = Window()
win.show()
app.exec()
