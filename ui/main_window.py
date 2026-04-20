from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import os

# UI modules
from ui.left_panel import LeftPanel
from ui.log_panel import LogPanel
from map.map_view import MapView

# Core modules
from core.grid import create_grid
from core.cappi import generate_cappi
from core.rainfall import marshall_palmer
from core.viewer3d import show_3d


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.apply_theme()
        self.setWindowTitle("GeoRain Radar Studio")
        self.setGeometry(100, 50, 1400, 850)
        self.left_panel = LeftPanel(self)
        self.log_panel = LogPanel()
        self.xg = None  # store grid data

        self.initUI()

    # ================= UI =================
    def initUI(self):

        central = QWidget()
        main_layout = QVBoxLayout()

        title = QLabel("GeoRain Radar Studio")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #00d4ff;
            padding: 10px;
        """)

        main_layout.addWidget(title)
        
        
        # -------- SPLITTERS (Resizable Layout) --------
        main_splitter = QSplitter(Qt.Vertical)

        top_splitter = QSplitter(Qt.Horizontal)

        # LEFT PANEL (TOOLS)
        self.left_panel.setStyleSheet("""
        background-color: rgba(18, 24, 41, 0.85);
        border-radius: 12px;
        """)

        # MAP VIEW
        self.map_view = MapView()

        top_splitter.addWidget(self.left_panel)
        top_splitter.addWidget(self.map_view)

        top_splitter.setStretchFactor(0, 1)
        top_splitter.setStretchFactor(1, 3)

        # LOG PANEL
        self.log_panel.setStyleSheet("""
        background-color: rgba(5, 7, 15, 0.9);
        border-radius: 12px;
        padding: 5px;
        """)

        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(self.log_panel)

        main_splitter.setStretchFactor(0, 4)
        main_splitter.setStretchFactor(1, 1)

        main_layout.addWidget(main_splitter)

        central.setLayout(main_layout)
        self.setCentralWidget(central)

    # =========================================================
    # ---------------- TOOL FUNCTIONS ----------------
    # =========================================================

    def left_panel_run_grid(self):

        file = QFileDialog.getOpenFileName(self, "Select NC File", "", "*.nc")[0]

        if not file:
            return

        try:
            self.log_panel.log("🔄 Running 3D grid conversion...")
            self.xg = create_grid(file)
            self.log_panel.log("✅ Grid created successfully")

        except Exception as e:
            self.log_panel.log(f"❌ Grid error: {e}")

    # ---------------- CAPPI ----------------
    def left_panel_run_cappi(self):

        if self.xg is None:
            self.log_panel.log("❌ Run grid first")
            return

        try:
            self.log_panel.log("📡 Generating CAPPI...")

            dbz = generate_cappi(self.xg)

            self.display(dbz)

            self.log_panel.log("✅ CAPPI displayed")

        except Exception as e:
            self.log_panel.log(f"❌ CAPPI error: {e}")

    # ---------------- PPI ----------------
    def left_panel_run_ppi(self):

        file = QFileDialog.getOpenFileName(self, "Select NC File", "", "*.nc")[0]

        if not file:
            return

        try:
            import pyiwr

            self.log_panel.log("📡 Generating PPI...")

            radar = pyiwr.correctednc(file)
            dbz = radar['DBZ'][0]

            self.display(dbz)

            self.log_panel.log("✅ PPI displayed")

        except Exception as e:
            self.log_panel.log(f"❌ PPI error: {e}")

    # ---------------- RAINFALL ----------------
    def left_panel_run_rain(self):

        if self.xg is None:
            self.log_panel.log("❌ Run grid first")
            return

        try:
            self.log_panel.log("🌧 Computing rainfall (Marshall-Palmer)...")

            dbz = generate_cappi(self.xg)
            rain = marshall_palmer(dbz)

            self.display(rain)

            self.log_panel.log("✅ Rainfall displayed")

        except Exception as e:
            self.log_panel.log(f"❌ Rainfall error: {e}")

    # ---------------- 3D ----------------
    def left_panel_run_3d(self):

        if self.xg is None:
            self.log_panel.log("❌ Run grid first")
            return

        try:
            self.log_panel.log("🧊 Opening 3D visualization...")

            show_3d(self.xg['DBZ'].values[0])

            self.log_panel.log("✅ 3D view opened")

        except Exception as e:
            self.log_panel.log(f"❌ 3D error: {e}")

    # =========================================================
    # ---------------- DISPLAY FUNCTION ----------------
    # =========================================================

    def apply_theme(self):

        self.setStyleSheet("""

        QWidget {
            background-color: #0f172a;
            color: #f1f5f9;
            font-family: 'Segoe UI';
            font-size: 13px;
        }

        QToolBox::tab {
            background: #1e293b;
            padding: 12px;
            margin: 1px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 16px;
            color: #f1f5f9;   /* 🔥 ADD THIS */
        }

        QToolBox::tab:selected {
            background: #334155;
            border-left: 3px solid #38bdf8;
            color: #ffffff;   /* 🔥 ADD THIS */
        }
        QLabel {
            color: #cbd5f5;
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 2px;
        }

        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
            background-color: #334155;
            border: 1px solid #475569;
            border-radius: 6px;
            padding: 6px;
            color: #f1f5f9;
        }

        QLineEdit:focus, QComboBox:focus {
            border: 1px solid #38bdf8;
        }

        QPushButton {
            background-color: #38bdf8;
            border-radius: 12px;
            padding: 10px;
            color: #0f172a;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #0ea5e9;
        }

        QPushButton:pressed {
            background-color: #0284c7;
        }

        QToolBox::tab {
            background: #1e293b;
            padding: 10px;
            margin: 3px;
            border-radius: 6px;
            font-weight: bold;
        }

        QToolBox::tab:selected {
            background: #334155;
            border-left: 3px solid #38bdf8;
        }

        QTextEdit {
            background-color: #020617;
            border: 1px solid #334155;
            border-radius: 6px;
            padding: 6px;
        }

        QSplitter::handle {
            background-color: #334155;
            width: 4px;
        }

        """)


    def display(self, data):

        try:
            img_path = "temp_layer.png"

            plt.imshow(data, cmap='jet')
            plt.axis('off')
            plt.savefig(img_path, bbox_inches='tight', pad_inches=0)
            plt.close()

            self.map_view.add_layer(os.path.abspath(img_path))

        except Exception as e:
            self.log_panel.log(f"❌ Display error: {e}")