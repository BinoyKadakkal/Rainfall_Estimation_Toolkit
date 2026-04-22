from PyQt5.QtWidgets import *
from core.download import run_download
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime



class LeftPanel(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        self.toolbox = QToolBox()

        # ---------------- DOWNLOAD ----------------
        download_widget = QWidget()
        d_layout = QVBoxLayout()

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        self.start_date = QLineEdit()
        self.end_date = QLineEdit()

        self.source = QComboBox()
        self.source.addItems(["TERLS", "SHAR", "CHERRAPUNJI"])

        self.download_out = QLineEdit()
        btn_out = QPushButton("Browse")
        btn_out.clicked.connect(self.select_download_folder)

        h = QHBoxLayout()
        h.addWidget(self.download_out)
        h.addWidget(btn_out)

        run_btn = QPushButton("Run Download")
        run_btn.clicked.connect(self.run_download)

        d_layout.addWidget(QLabel("Username"))
        d_layout.addWidget(self.username)

        d_layout.addWidget(QLabel("Password"))
        d_layout.addWidget(self.password)

        d_layout.addWidget(QLabel("Start Date"))
        d_layout.addWidget(self.start_date)

        d_layout.addWidget(QLabel("End Date"))
        d_layout.addWidget(self.end_date)

        d_layout.addWidget(QLabel("Source"))
        d_layout.addWidget(self.source)

        d_layout.addWidget(QLabel("Output Folder"))
        d_layout.addLayout(h)

        d_layout.addWidget(run_btn)

        download_widget.setLayout(d_layout)

        # ---------------- RASTER ----------------
        raster_widget = self.simple_io_widget(self.run_raster)

        # ---------------- CORRECTION ----------------
        correction_widget = self.simple_io_widget(self.run_correction)

        # ---------------- RAIN ----------------
        rain_widget = self.simple_io_widget(self.run_rain)

        # ---------------- PPI ----------------
        ppi_widget = QWidget()
        ppi_layout = QVBoxLayout()

        self.ppi_in = QLineEdit()
        self.ppi_out = QLineEdit()
        self.sweep = QSpinBox()

        ppi_layout.addWidget(QLabel("Input"))
        ppi_layout.addWidget(self.ppi_in)

        ppi_layout.addWidget(QLabel("Output"))
        ppi_layout.addWidget(self.ppi_out)

        ppi_layout.addWidget(QLabel("Sweep Number"))
        ppi_layout.addWidget(self.sweep)

        btn_ppi = QPushButton("Run PPI")
        btn_ppi.clicked.connect(self.run_ppi)

        ppi_layout.addWidget(btn_ppi)

        ppi_widget.setLayout(ppi_layout)

        # ---------------- CAPPI ----------------
        cappi_widget = QWidget()
        cappi_layout = QVBoxLayout()

        self.cappi_in = QLineEdit()
        self.cappi_out = QLineEdit()
        self.altitude = QDoubleSpinBox()
        self.altitude.setValue(2.0)

        cappi_layout.addWidget(QLabel("Input"))
        cappi_layout.addWidget(self.cappi_in)

        cappi_layout.addWidget(QLabel("Output"))
        cappi_layout.addWidget(self.cappi_out)

        cappi_layout.addWidget(QLabel("Altitude (km)"))
        cappi_layout.addWidget(self.altitude)

        btn_cappi = QPushButton("Run CAPPI")
        btn_cappi.clicked.connect(self.run_cappi)

        cappi_layout.addWidget(btn_cappi)

        cappi_widget.setLayout(cappi_layout)

        # ADD TO TOOLBOX
        self.toolbox.addItem(download_widget, "Download")
        self.toolbox.addItem(raster_widget, "Raster Conversion")
        self.toolbox.addItem(correction_widget, "Correction")
        self.toolbox.addItem(rain_widget, "Convert to Rain")
        self.toolbox.addItem(ppi_widget, "PPI")
        self.toolbox.addItem(cappi_widget, "CAPPI")

        layout.addWidget(self.toolbox)
        self.setLayout(layout)

    # ---------------- COMMON IO WIDGET ----------------
    def simple_io_widget(self, run_func):

        widget = QWidget()
        layout = QVBoxLayout()

        inp = QLineEdit()
        out = QLineEdit()

        btn = QPushButton("Run")
        btn.clicked.connect(run_func)

        layout.addWidget(QLabel("Input"))
        layout.addWidget(inp)

        layout.addWidget(QLabel("Output"))
        layout.addWidget(out)

        layout.addWidget(btn)

        widget.setLayout(layout)

        return widget

    # ---------------- FUNCTIONS ----------------
    def select_download_folder(self):
        folder = QFileDialog.getExistingDirectory(self)
        self.download_out.setText(folder)

    
    def run_download(self):

        username = self.username.text().strip()
        password = self.password.text().strip()
        start = self.start_date.text().strip()
        end = self.end_date.text().strip()
        source = self.source.currentText()
        output = self.download_out.text().strip()

        # ✅ validation
        if not username:
            self.parent.log_panel.log("❌ Enter username")
            return

        if not password:
            self.parent.log_panel.log("❌ Enter password")
            return

        if not output:
            self.parent.log_panel.log("❌ Select output folder")
            return

        self.parent.log_panel.log("⬇ Starting download...")

        params = (username, password, start, end, source, output)

        self.thread = DownloadThread(params)
        self.thread.setParent(self)   # 🔥 important
        self.thread.log_signal.connect(self.parent.log_panel.log)

        self.thread.start()
        start_raw = self.start_date.text().strip()
        end_raw = self.end_date.text().strip()

        start = format_date(start_raw)
        end = format_date(end_raw)

        if not start or not end:
            self.parent.log_panel.log("❌ Invalid date format (use DD-MM-YYYY)")
            return
        if not start or not end:
            self.parent.log_panel.log("❌ Invalid date format (use DD-MM-YYYY)")
            return
    def run_raster(self):
        self.parent.log_panel.log("Raster conversion started")

    def run_correction(self):
        self.parent.log_panel.log("Correction started")

    def run_rain(self):
        self.parent.left_panel_run_rain()

    def run_ppi(self):
        self.parent.left_panel_run_ppi()

    def run_cappi(self):
        self.parent.left_panel_run_cappi()

class DownloadThread(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, params):
        super().__init__()
        self.params = params

    def run(self):
        from core.download import run_download
        run_download(*self.params, self.log_signal.emit)

def format_date(date_str):
    try:
        dt = datetime.strptime(date_str, "%d-%m-%Y")
        return dt.strftime("%Y-%m-%dT00:00:00")
    except:
        return None