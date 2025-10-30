import os
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QGridLayout,
    QFrame,
    QMessageBox,
)


from database import Database


class DatabaseWindow(QDialog):

    def __init__(self, parent: QDialog):
        super().__init__(parent)

        self.setWindowTitle("Create Akebono database")
        self.setModal(True)
        self.setFixedSize(self.sizeHint())  # non‑resizable

        # widgets
        lbl_orbit = QLabel("Directory with orbit files:")
        lbl_data = QLabel("Directory with data files:")

        self.orbit_directory_entry = QLineEdit()
        self.datafile_directory_entry = QLineEdit()

        btn_choose_orbit = QPushButton("Choose")
        btn_choose_data = QPushButton("Choose")
        btn_create_db = QPushButton("Create database")

        btn_choose_orbit.clicked.connect(self._choose_orbit_directory)
        btn_choose_data.clicked.connect(self._choose_datafile_directory)
        btn_create_db.clicked.connect(self._create_database)

        # Separator – thin horizontal line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)

        # layout
        grid = QGridLayout()
        # row 0 – orbit directory
        grid.addWidget(lbl_orbit, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.orbit_directory_entry, 0, 1, 1, 3)
        grid.addWidget(btn_choose_orbit, 0, 4)

        # row 1 – datafile directory
        grid.addWidget(lbl_data, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.datafile_directory_entry, 1, 1, 1, 3)
        grid.addWidget(btn_choose_data, 1, 4)

        # row 2 – separator
        grid.addWidget(separator, 2, 0, 1, 5)

        # row 3 – create‑db button (right‑aligned)
        grid.addWidget(btn_create_db, 3, 3, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(grid)
        self.setFixedSize(self.sizeHint())

    def _choose_orbit_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select directory that contains orbit files",
            str(Path.home()),
        )
        if directory:
            self.orbit_directory_entry.setText(directory)

    def _choose_datafile_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select directory that contains data files",
            str(Path.home()),
        )
        if directory:
            self.datafile_directory_entry.setText(directory)

    def _create_database(self):
        db_path = Path("akebono.db")
        if db_path.is_file():
            QMessageBox.information(
                self,
                "Database already exists",
                f"The file '{db_path}' is already present - nothing to do.",
            )
            return

        orbit_dir = self.orbit_directory_entry.text().strip()
        datafile_dir = self.datafile_directory_entry.text().strip()

        if not orbit_dir or not datafile_dir:
            QMessageBox.warning(
                self,
                "Missing information",
                "Both directory fields must be filled before creating the database.",
            )
            return

        try:
            db = Database()
            db.connect(str(db_path))
            db.create_data_table()
            db.create_orbits_table()
            db.create_database(orbit_dir, datafile_dir)
            db.close()
        except Exception as ex:
            QMessageBox.critical(
                self,
                "Database creation failed",
                f"An error occurred while building the DB:\n{ex}",
            )
            return

        QMessageBox.information(
            self,
            "Success",
            f"The database '{db_path}' has been created successfully.",
        )
        self.accept()
