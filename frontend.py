import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QTextEdit, QLineEdit, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import pandas as pd
from newpro import load_data, clean_data, process_query


class DataChatApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🤖 Chat with Your Data AI")
        self.setGeometry(200, 100, 800, 650)

        self.df = None

        # ---------------- MAIN LAYOUT ----------------
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # ---------------- TITLE ----------------
        self.label = QLabel("🤖 Chat with Your Data")
        self.label.setFont(QFont("Arial", 18, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label)

        # ---------------- UPLOAD BUTTON ----------------
        self.upload_btn = QPushButton("📂 Upload CSV / Excel")
        self.upload_btn.clicked.connect(self.load_file)
        main_layout.addWidget(self.upload_btn)

        # ---------------- PREVIEW ----------------
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setPlaceholderText("📊 Data preview will appear here...")
        main_layout.addWidget(self.preview)

        # ---------------- CHAT OUTPUT ----------------
        self.chat_output = QTextEdit()
        self.chat_output.setReadOnly(True)
        self.chat_output.setPlaceholderText("💬 Chat will appear here...")
        main_layout.addWidget(self.chat_output)

        # ---------------- INPUT + BUTTON (HORIZONTAL) ----------------
        bottom_layout = QHBoxLayout()

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Ask something about your data...")
        bottom_layout.addWidget(self.input_box)

        self.ask_btn = QPushButton("Ask 🚀")
        self.ask_btn.clicked.connect(self.ask_question)
        bottom_layout.addWidget(self.ask_btn)

        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        # ---------------- APPLY STYLES ----------------
        self.setStyleSheet(self.get_styles())

    # -----------------------------
    # LOAD FILE
    # -----------------------------
    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)"
        )

        if file_path:
            df = load_data(file_path)

            if isinstance(df, str):
                self.chat_output.append(f"<span style='color:red;'>{df}</span>")
                return

            self.df = clean_data(df)

            self.preview.setText(str(self.df.head()))
            self.chat_output.append("<span style='color:lightgreen;'>✅ File loaded successfully!</span><br>")

    # -----------------------------
    # HANDLE QUERY
    # -----------------------------
    def ask_question(self):
        if self.df is None:
            self.chat_output.append("<span style='color:red;'>❌ Please upload a dataset first</span><br>")
            return

        query = self.input_box.text()

        if not query:
            return

        answer = process_query(self.df, query)

        self.chat_output.append(f"<b style='color:#00BFFF;'>🧑 You:</b> {query}")
        self.chat_output.append(f"<b style='color:#90EE90;'>🤖 AI:</b> {answer}<br>")

        self.input_box.clear()

    # -----------------------------
    # STYLING
    # -----------------------------
    def get_styles(self):
        return """
        QWidget {
            background-color: #1e1e2f;
            color: white;
            font-family: Arial;
            font-size: 14px;
        }

        QPushButton {
            background-color: #4CAF50;
            border-radius: 8px;
            padding: 8px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #45a049;
        }

        QLineEdit {
            background-color: #2c2c3e;
            border: 1px solid #555;
            border-radius: 6px;
            padding: 6px;
            color: white;
        }

        QTextEdit {
            background-color: #2c2c3e;
            border: 1px solid #555;
            border-radius: 8px;
            padding: 8px;
        }
        """


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataChatApp()
    window.show()
    sys.exit(app.exec_())