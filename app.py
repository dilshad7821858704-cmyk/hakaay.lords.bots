import sys
import random
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTabWidget, QCheckBox, 
                             QComboBox, QSpinBox, QLabel, QTextEdit, QGroupBox, 
                             QFormLayout)
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot

class EngineWorker(QThread):
    """
    Handles processing simulation in a separate thread to prevent 
    the graphical user interface from freezing during intensive loops.
    """
    log_signal = pyqtSignal(str, str) # Emits: (message, text_color_hex)
    status_signal = pyqtSignal(str)

    def __init__(self, config_data):
        super().__init__()
        self.config = config_data
        self._is_running = True

    def run(self):
        self.status_signal.emit("RUNNING")
        self.log_signal.emit("Engine lifecycle started successfully.", "#28a745")
        
        # Simulated action pool based on category parameter state
        while self._is_running:
            actions = ["Refreshing local cache records...", "Verifying internal data states..."]
            
            if self.config.get('auto_resource'):
                actions.append(f"Analyzing production optimization for: {self.config['focus'].upper()}")
            if self.config.get('auto_train'):
                actions.append(f"Evaluating queue requirements against threshold: {self.config['shelter_min']}")
            if self.config.get('guild_quests'):
                actions.append("Scanning available validation logs for guild events.")

            chosen_action = random.choice(actions)
            self.log_signal.emit(chosen_action, "#ffffff")
            
            # Context-switch delay simulating operational cycles
            time.sleep(2.5)

    def stop(self):
        self._is_running = False
        self.status_signal.emit("STOPPING")
        self.log_signal.emit("Termination request received. Cleaning up worker processes...", "#ffc107")
        self.wait() # Ensure thread closes cleanly
        self.status_signal.emit("IDLE")


class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Simulation Dashboard Architecture")
        self.resize(750, 550)
        self.worker = None
        
        # Root layout structure
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        self.init_control_panel()
        self.init_parameter_tabs()
        self.init_log_panel()

    def init_control_panel(self):
        """Creates the primary action layout and status displays."""
        group = QGroupBox("System Lifecycles")
        layout = QHBoxLayout()

        self.start_btn = QPushButton("START LIFE CYCLE")
        self.start_btn.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; padding: 8px;")
        self.start_btn.clicked.connect(self.handle_start)

        self.stop_btn = QPushButton("STOP LIFE CYCLE")
        self.stop_btn.setStyleSheet("background-color: #dc3545; color: white; font-weight: bold; padding: 8px;")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.handle_stop)

        self.status_label = QLabel("STATUS: IDLE")
        self.status_label.setStyleSheet("font-weight: bold; color: #dc3545; font-size: 14px; margin-left: 15px;")

        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.status_label)
        layout.addStretch()
        group.setLayout(layout)
        self.main_layout.addWidget(group)

    def init_parameter_tabs(self):
        """Constructs multi-category tabs to separate feature parameters."""
        self.tabs = QTabWidget()
        
        # Category 1: Economy Elements
        self.tab_econ = QWidget()
        econ_layout = QFormLayout(self.tab_econ)
        self.chk_resource = QCheckBox("Enable Resource Optimization Loop")
        self.chk_resource.setChecked(True)
        self.cmb_focus = QComboBox()
        self.cmb_focus.addItems(["Food Focus", "Stone Focus", "Wood Focus", "Ore Focus"])
        econ_layout.addRow(self.chk_resource)
        econ_layout.addRow("Primary Production Target:", self.cmb_focus)
        
        # Category 2: Military Elements
        self.tab_mili = QWidget()
        mili_layout = QFormLayout(self.tab_mili)
        self.chk_train = QCheckBox("Enable Background Force Metrics")
        self.spin_shelter = QSpinBox()
        self.spin_shelter.setRange(0, 500000)
        self.spin_shelter.setValue(5000)
        mili_layout.addRow(self.chk_train)
        mili_layout.addRow("Minimum Core Reserve Limit:", self.spin_shelter)

        # Category 3: Administrative Elements
        self.tab_admin = QWidget()
        admin_layout = QVBoxLayout(self.tab_admin)
        self.chk_guild = QCheckBox("Process Local Guild Record Synchronization")
        self.chk_guild.setChecked(True)
        self.chk_quest = QCheckBox("Process Periodic Daily Admin Evaluation Requests")
        admin_layout.addWidget(self.chk_guild)
        admin_layout.addWidget(self.chk_quest)
        admin_layout.addStretch()

        self.tabs.addTab(self.tab_econ, "Economy & Processing")
        self.tabs.addTab(self.tab_mili, "Military Systems")
        self.tabs.addTab(self.tab_admin, "Administrative / Quests")
        self.main_layout.addWidget(self.tabs)

    def init_log_panel(self):
        """Creates the runtime telemetry viewing field."""
        group = QGroupBox("Live Activity Log (Telemetry)")
        layout = QVBoxLayout()
        
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet("background-color: #111116; color: #00ff00; font-family: 'Courier New';")
        
        layout.addWidget(self.log_view)
        group.setLayout(layout)
        self.main_layout.addWidget(group)

    @pyqtSlot(str, str)
    def update_log_view(self, text, color_hex):
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f'<span style="color:#888888;">[{timestamp}]</span> <span style="color:{color_hex};">{text}</span>'
        self.log_view.append(formatted_message)

    @pyqtSlot(str)
    def update_status(self, status_text):
        self.status_label.setText(f"STATUS: {status_text}")
        if status_text == "RUNNING":
            self.status_label.setStyleSheet("font-weight: bold; color: #28a745; font-size: 14px; margin-left: 15px;")
        elif status_text == "IDLE":
            self.status_label.setStyleSheet("font-weight: bold; color: #dc3545; font-size: 14px; margin-left: 15px;")

    def handle_start(self):
        # Package UI configurations into state object
        runtime_config = {
            'auto_resource': self.chk_resource.isChecked(),
            'focus': self.cmb_focus.currentText(),
            'auto_train': self.chk_train.isChecked(),
            'shelter_min': self.spin_shelter.value(),
            'guild_quests': self.chk_guild.isChecked()
        }
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        # Instantiate worker thread safe-lifecycle execution
        self.worker = EngineWorker(runtime_config)
        self.worker.log_signal.connect(self.update_log_view)
        self.worker.status_signal.connect(self.update_status)
        self.worker.start()

    def handle_stop(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())
