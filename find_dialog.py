# find_dialog.py
"""
Find in Page Dialog
Features: Search text, highlight matches, navigate results
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWebEngineCore import QWebEnginePage

try:
    import qtawesome as qta
    HAS_ICONS = True
except ImportError:
    HAS_ICONS = False


class FindBar(QWidget):
    """Find in page bar widget."""
    
    closed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.web_page = None
        self.init_ui()
        self.setVisible(False)
    
    def init_ui(self):
        """Initialize UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)
        
        # Find label
        find_label = QLabel("Find:")
        layout.addWidget(find_label)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Find in page...")
        self.search_input.textChanged.connect(self.search_text)
        self.search_input.returnPressed.connect(self.find_next)
        layout.addWidget(self.search_input)
        
        # Match case checkbox
        self.match_case_check = QCheckBox("Match case")
        self.match_case_check.stateChanged.connect(self.search_text)
        layout.addWidget(self.match_case_check)
        
        # Results label
        self.results_label = QLabel("")
        layout.addWidget(self.results_label)
        
        # Previous button
        if HAS_ICONS:
            self.prev_btn = QPushButton()
            self.prev_btn.setIcon(qta.icon('fa5s.chevron-up'))
        else:
            self.prev_btn = QPushButton("Previous")
        self.prev_btn.clicked.connect(self.find_previous)
        self.prev_btn.setToolTip("Previous match")
        layout.addWidget(self.prev_btn)
        
        # Next button
        if HAS_ICONS:
            self.next_btn = QPushButton()
            self.next_btn.setIcon(qta.icon('fa5s.chevron-down'))
        else:
            self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.find_next)
        self.next_btn.setToolTip("Next match")
        layout.addWidget(self.next_btn)
        
        # Close button
        if HAS_ICONS:
            self.close_btn = QPushButton()
            self.close_btn.setIcon(qta.icon('fa5s.times'))
        else:
            self.close_btn = QPushButton("✕")
        self.close_btn.clicked.connect(self.hide_bar)
        self.close_btn.setToolTip("Close")
        layout.addWidget(self.close_btn)
        
        # Style
        self.setStyleSheet("""
            FindBar {
                background-color: #252526;
                border-top: 1px solid #3e3e42;
            }
            QLineEdit {
                background-color: #2d2d30;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                padding: 6px 10px;
                color: #cccccc;
                min-width: 200px;
            }
            QLineEdit:focus {
                border-color: #0e639c;
            }
            QPushButton {
                background-color: #2d2d30;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                padding: 6px 12px;
                color: #cccccc;
            }
            QPushButton:hover {
                background-color: #3e3e42;
            }
            QCheckBox {
                color: #cccccc;
            }
            QLabel {
                color: #cccccc;
            }
        """)
    
    def set_web_page(self, web_page):
        """Set the web page to search in."""
        self.web_page = web_page
    
    def show_bar(self):
        """Show find bar and focus search input."""
        self.setVisible(True)
        self.search_input.setFocus()
        self.search_input.selectAll()
    
    def hide_bar(self):
        """Hide find bar and clear search."""
        self.setVisible(False)
        if self.web_page:
            self.web_page.findText("")  # Clear highlights
        self.closed.emit()
    
    def search_text(self):
        """Search for text."""
        if not self.web_page:
            return
        
        search_term = self.search_input.text()
        
        if not search_term:
            self.results_label.setText("")
            self.web_page.findText("")
            return
        
        # Build find flags
        flags = QWebEnginePage.FindFlag(0)
        if self.match_case_check.isChecked():
            flags |= QWebEnginePage.FindFlag.FindCaseSensitively
        
        # Search
        self.web_page.findText(search_term, flags, self.search_callback)
    
    def search_callback(self, found):
        """Handle search result."""
        if found:
            self.results_label.setText("✓")
            self.results_label.setStyleSheet("color: #43a047;")
        else:
            search_term = self.search_input.text()
            if search_term:
                self.results_label.setText("No matches")
                self.results_label.setStyleSheet("color: #e53935;")
            else:
                self.results_label.setText("")
    
    def find_next(self):
        """Find next match."""
        if not self.web_page:
            return
        
        search_term = self.search_input.text()
        if not search_term:
            return
        
        flags = QWebEnginePage.FindFlag(0)
        if self.match_case_check.isChecked():
            flags |= QWebEnginePage.FindFlag.FindCaseSensitively
        
        self.web_page.findText(search_term, flags)
    
    def find_previous(self):
        """Find previous match."""
        if not self.web_page:
            return
        
        search_term = self.search_input.text()
        if not search_term:
            return
        
        flags = QWebEnginePage.FindFlag.FindBackward
        if self.match_case_check.isChecked():
            flags |= QWebEnginePage.FindFlag.FindCaseSensitively
        
        self.web_page.findText(search_term, flags)
    
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Escape:
            self.hide_bar()
        else:
            super().keyPressEvent(event)