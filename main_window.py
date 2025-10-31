import os
from pathlib import Path
import datetime as dt

from PySide6.QtCore import (
    Qt,
    QDate,
    QObject,
    QRunnable,
    QThreadPool,
    Signal,
    Slot,
)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QDateEdit,
    QFileDialog,
    QGridLayout,
    QFrame,
    QMessageBox,
    QStatusBar,
)

from database_window import DatabaseWindow
from processing import Parameters, Search


class WorkerSignals(QObject):
    progress = Signal(int)
    finished = Signal(str)


class Task(QRunnable):
    def __init__(self, parameters: Parameters, signals: WorkerSignals):
        super().__init__()
        self.parameters = parameters
        self.signals = signals

    @Slot()
    def run(self) -> None:
        search = Search(self.parameters)
        search.run()
        self.signals.progress.emit(100)
        self.signals.finished.emit("Done.")


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Akebono_Pass 0.2")
        self._setup_icon()

        lbl_L = QLabel("L:")
        lbl_dL = QLabel("ΔL:")
        lbl_Lon = QLabel("Lon:")
        lbl_dLon = QLabel("ΔLon:")
        lbl_out = QLabel("Output file:")
        lbl_start = QLabel("Start date:")
        lbl_end = QLabel("End date:")

        self.shell_entry = QLineEdit()
        self.shell_delta_entry = QLineEdit()
        self.longitude_entry = QLineEdit()
        self.longitude_delta_entry = QLineEdit()
        self.output_filename_entry = QLineEdit()

        btn_submit = QPushButton("Submit")
        btn_choose = QPushButton("Choose")
        btn_submit.clicked.connect(self.on_button_press)
        btn_choose.clicked.connect(self.choose_output_filename_button_press)

        self.start_date = QDateEdit(calendarPopup=True)
        self.end_date = QDateEdit(calendarPopup=True)
        for d in (self.start_date, self.end_date):
            d.setDisplayFormat("yyyy-MM-dd")
            d.setDate(QDate.currentDate())

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)

        self.status_bar = QStatusBar()

        self.widgets = [
            btn_submit,
            btn_choose,
            self.start_date,
            self.end_date,
            self.shell_entry,
            self.shell_delta_entry,
            self.longitude_entry,
            self.longitude_delta_entry,
            self.output_filename_entry,
        ]

        grid = QGridLayout()
        # Row 0 – L and ΔL
        grid.addWidget(lbl_L, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.shell_entry, 0, 1)
        grid.addWidget(lbl_dL, 0, 2, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.shell_delta_entry, 0, 3)

        # Row 1 – Lon and ΔLon
        grid.addWidget(lbl_Lon, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.longitude_entry, 1, 1)
        grid.addWidget(lbl_dLon, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.longitude_delta_entry, 1, 3)

        # Row 2 – Output file + chooser
        grid.addWidget(lbl_out, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.output_filename_entry, 2, 1, 1, 3)
        grid.addWidget(btn_choose, 2, 4)

        # Row 3 – Start / End dates
        grid.addWidget(lbl_start, 3, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.start_date, 3, 1)
        grid.addWidget(lbl_end, 3, 2, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.end_date, 3, 3)

        # Row 4 – Separator
        grid.addWidget(separator, 4, 0, 1, 5)

        # Row 5 – Submit button (aligned right)
        grid.addWidget(btn_submit, 5, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)

        # Row 6 – Status bar
        grid.addWidget(self.status_bar, 6, 0, 1, 5)

        # Apply layout and fix size (non‑resizable)
        self.setLayout(grid)
        self.setFixedSize(self.sizeHint())

        # ----- database check ------------------------------------------------
        if not Path("akebono.db").is_file():
            try:
                db_win = DatabaseWindow(self)
                db_win.exec()
            except Exception as ex:
                QMessageBox.critical(
                    self,
                    "Database error",
                    f"Could not open the database configuration window:\n{ex}",
                )

        self.thread_pool = QThreadPool.globalInstance()
        self.signals = WorkerSignals()
        self.signals.progress.connect(self.on_progress)
        self.signals.finished.connect(self.on_finished)

    def _setup_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), "images", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            # Silently ignore
            pass

    def on_button_press(self):

        try:
            start_date = dt.date.fromisoformat(
                self.start_date.date().toString("yyyy-MM-dd")
            )
            end_date = dt.date.fromisoformat(
                self.end_date.date().toString("yyyy-MM-dd")
            ) + dt.timedelta(days=1)
            shell = float(self.shell_entry.text().strip())
            shell_delta = float(self.shell_delta_entry.text().strip())
            longitude = float(self.longitude_entry.text().strip())
            longitude_delta = float(self.longitude_delta_entry.text().strip())
        except ValueError:
            return

        output_filename = self.output_filename_entry.text()

        parameters = Parameters(
            start_date=start_date,
            end_date=end_date,
            shell=shell,
            shell_delta=shell_delta,
            longitude=longitude,
            longitude_delta=longitude_delta,
            output_filename=output_filename,
        )

        for w in self.widgets:
            w.setEnabled(False)

        self.status_bar.showMessage("Working...")

        task = Task(parameters, self.signals)
        self.thread_pool.start(task)

    def choose_output_filename_button_press(self):

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Choose output file",
            "",
            "All Files (*)",
        )
        if file_name:
            self.output_filename_entry.setText(file_name)

    @Slot(int)
    def on_progress(self, value: int):
        pass

    @Slot(str)
    def on_finished(self, message: str):
        self.status_bar.showMessage(message, 5000)
        QMessageBox.information(
                    self,
                    "Task",
                    message,
                )
        for w in self.widgets:
            w.setEnabled(True)
