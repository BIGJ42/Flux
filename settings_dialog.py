# settings_dialog.py
"""
Settings Dialog for Flux
This file can be used standalone or compiled into an executable.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, 
    QPushButton, QComboBox, QGroupBox, QSpacerItem, QSizePolicy,
    QLineEdit, QTabWidget, QWidget, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

try:
    import qtawesome as qta
    HAS_ICONS = True
except ImportError:
    HAS_ICONS = False
    print("Warning: qtawesome not found. Icons will not be displayed in settings.")

# --- ENHANCED FLUENT UI SETTINGS THEME ---
SETTINGS_THEME = """
QDialog {
    background-color: #1e1e1e;
    color: #cccccc;
    font-family: 'Segoe UI Variable', 'Segoe UI', system-ui, -apple-system, sans-serif;
    font-size: 13px;
}

QTabWidget::pane {
    border: 1px solid #3e3e42;
    background-color: #252526;
    border-radius: 4px;
    padding: 4px;
}

QTabWidget::tab-bar {
    alignment: left;
}

QTabBar::tab {
    background: transparent;
    color: #858585;
    padding: 12px 24px;
    margin-right: 2px;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 13px;
}

QTabBar::tab:hover {
    background: #2d2d30;
    color: #cccccc;
}

QTabBar::tab:selected {
    color: #ffffff;
    border-bottom: 2px solid #0e639c;
    background: #2d2d30;
}

QGroupBox {
    background-color: #252526;
    border: 1px solid #3e3e42;
    border-radius: 6px;
    margin-top: 16px;
    padding-top: 16px;
    font-weight: 600;
    font-size: 14px;
    color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 6px 12px;
    color: #ffffff;
}

QLabel {
    color: #cccccc;
    font-size: 13px;
    padding: 2px;
}

QLineEdit {
    background-color: #2d2d30;
    border: 1px solid #3e3e42;
    border-radius: 4px;
    padding: 8px 12px;
    color: #cccccc;
    font-size: 13px;
    min-height: 32px;
    selection-background-color: #094771;
}

QLineEdit:hover {
    border-color: #454545;
    background-color: #333337;
}

QLineEdit:focus {
    border-color: #0e639c;
    background-color: #1e1e1e;
}

QComboBox {
    background-color: #2d2d30;
    border: 1px solid #3e3e42;
    border-radius: 4px;
    padding: 8px 12px;
    color: #cccccc;
    font-size: 13px;
    min-height: 32px;
}

QComboBox:hover {
    border-color: #454545;
    background-color: #333337;
}

QComboBox:focus {
    border-color: #0e639c;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #cccccc;
    margin-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #252526;
    border: 1px solid #3e3e42;
    selection-background-color: #094771;
    selection-color: #ffffff;
    color: #cccccc;
    padding: 4px;
    outline: none;
}

QCheckBox {
    color: #cccccc;
    spacing: 10px;
    font-size: 13px;
    padding: 4px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 1px solid #3e3e42;
    background-color: #2d2d30;
}

QCheckBox::indicator:hover {
    border-color: #0e639c;
    background-color: #333337;
}

QCheckBox::indicator:checked {
    background-color: #0e639c;
    border-color: #0e639c;
}

QPushButton {
    background-color: #2d2d30;
    border: 1px solid #3e3e42;
    border-radius: 4px;
    color: #cccccc;
    padding: 10px 24px;
    font-size: 13px;
    min-width: 90px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #3e3e42;
    border-color: #454545;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #252526;
}

QPushButton#primaryButton {
    background-color: #0e639c;
    border-color: #0e639c;
    color: #ffffff;
    font-weight: 600;
}

QPushButton#primaryButton:hover {
    background-color: #1177bb;
    border-color: #1177bb;
}

QPushButton#primaryButton:pressed {
    background-color: #0d5a8e;
}

QPushButton#dangerButton {
    background-color: transparent;
    border-color: #e53935;
    color: #ff6b6b;
}

QPushButton#dangerButton:hover {
    background-color: #e53935;
    color: #ffffff;
    border-color: #e53935;
}

QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    background: #252526;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: #3e3e42;
    border-radius: 6px;
    min-height: 30px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background: #4e4e52;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0px;
}
"""


class SettingsDialog(QDialog):
    """Enhanced settings dialog with Fluent UI design."""
    
    settings_saved = pyqtSignal()

    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.config = config_manager
        self.setModal(True)
        self.setStyleSheet(SETTINGS_THEME)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI with tabbed interface."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        
        # Create tabs
        self.tabs.addTab(self.create_general_tab(), "⚙️  General")
        self.tabs.addTab(self.create_appearance_tab(), "🎨  Appearance")
        self.tabs.addTab(self.create_privacy_tab(), "🔒  Privacy")
        self.tabs.addTab(self.create_advanced_tab(), "🔧  Advanced")
        
        main_layout.addWidget(self.tabs)
        
        # Button bar
        button_bar = self.create_button_bar()
        main_layout.addWidget(button_bar)
        
        self.resize(700, 600)

    def create_general_tab(self):
        """Create general settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Startup Group
        startup_group = QGroupBox("🏠 Startup")
        startup_layout = QVBoxLayout(startup_group)
        startup_layout.setSpacing(12)
        
        # Homepage
        homepage_layout = QHBoxLayout()
        homepage_label = QLabel("Homepage:")
        homepage_label.setMinimumWidth(140)
        self.homepage_input = QLineEdit()
        self.homepage_input.setPlaceholderText("https://www.google.com")
        self.homepage_input.setText(
            self.config.get_setting("homepage") or "https://www.google.com"
        )
        homepage_layout.addWidget(homepage_label)
        homepage_layout.addWidget(self.homepage_input, 1)
        startup_layout.addLayout(homepage_layout)
        
        # New tab
        newtab_layout = QHBoxLayout()
        newtab_label = QLabel("New tabs open:")
        newtab_label.setMinimumWidth(140)
        self.newtab_combo = QComboBox()
        self.newtab_combo.addItem("Homepage", "homepage")
        self.newtab_combo.addItem("Blank page", "blank")
        self.newtab_combo.addItem("Continue where left off", "restore")
        
        current_newtab = self.config.get_setting("new_tab_page") or "homepage"
        index = self.newtab_combo.findData(current_newtab)
        if index != -1:
            self.newtab_combo.setCurrentIndex(index)
            
        newtab_layout.addWidget(newtab_label)
        newtab_layout.addWidget(self.newtab_combo, 1)
        startup_layout.addLayout(newtab_layout)
        
        layout.addWidget(startup_group)
        
        # Search Group
        search_group = QGroupBox("🔍 Search")
        search_layout = QVBoxLayout(search_group)
        search_layout.setSpacing(12)
        
        search_engine_layout = QHBoxLayout()
        search_label = QLabel("Search engine:")
        search_label.setMinimumWidth(140)
        self.search_combo = QComboBox()
        self.search_combo.addItem("Google", "https://www.google.com/search?q={}")
        self.search_combo.addItem("DuckDuckGo", "https://duckduckgo.com/?q={}")
        self.search_combo.addItem("Bing", "https://www.bing.com/search?q={}")
        self.search_combo.addItem("Brave", "https://search.brave.com/search?q={}")
        
        current_search = self.config.get_setting("search_engine") or "https://www.google.com/search?q={}"
        index = self.search_combo.findData(current_search)
        if index != -1:
            self.search_combo.setCurrentIndex(index)
            
        search_engine_layout.addWidget(search_label)
        search_engine_layout.addWidget(self.search_combo, 1)
        search_layout.addLayout(search_engine_layout)
        
        layout.addWidget(search_group)
        
        # Downloads Group
        downloads_group = QGroupBox("📥 Downloads")
        downloads_layout = QVBoxLayout(downloads_group)
        
        self.ask_download_check = QCheckBox("Ask where to save each file before downloading")
        self.ask_download_check.setChecked(
            self.config.get_setting("ask_download_location") or True
        )
        downloads_layout.addWidget(self.ask_download_check)
        
        layout.addWidget(downloads_group)
        
        # Spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        return widget

    def create_appearance_tab(self):
        """Create appearance settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Layout Group
        layout_group = QGroupBox("📐 Layout")
        layout_layout = QVBoxLayout(layout_group)
        layout_layout.setSpacing(12)
        
        # Tab Position
        tab_pos_layout = QHBoxLayout()
        tab_pos_label = QLabel("Tab position:")
        tab_pos_label.setMinimumWidth(140)
        self.tab_pos_combo = QComboBox()
        self.tab_pos_combo.addItem("Top (Horizontal)", "top")
        self.tab_pos_combo.addItem("Left (Vertical)", "left")
        
        current_tab_pos = self.config.get_setting("tab_position") or "top"
        index = self.tab_pos_combo.findData(current_tab_pos)
        if index != -1:
            self.tab_pos_combo.setCurrentIndex(index)
            
        tab_pos_layout.addWidget(tab_pos_label)
        tab_pos_layout.addWidget(self.tab_pos_combo, 1)
        layout_layout.addLayout(tab_pos_layout)
        
        # Compact mode
        self.compact_mode_check = QCheckBox("Compact mode (reduced spacing)")
        self.compact_mode_check.setChecked(
            self.config.get_setting("compact_mode") or False
        )
        layout_layout.addWidget(self.compact_mode_check)
        
        layout.addWidget(layout_group)
        
        # Theme Group
        theme_group = QGroupBox("🌓 Theme")
        theme_layout = QVBoxLayout(theme_group)
        theme_layout.setSpacing(12)
        
        theme_select_layout = QHBoxLayout()
        theme_label = QLabel("Color theme:")
        theme_label.setMinimumWidth(140)
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Dark (Default)", "dark")
        self.theme_combo.addItem("Light (Coming soon)", "light")
        self.theme_combo.addItem("Auto (Coming soon)", "auto")
        
        # Disable non-implemented
        model = self.theme_combo.model()
        for i in range(1, 3):
            item = model.item(i)
            item.setEnabled(False)
        
        theme_select_layout.addWidget(theme_label)
        theme_select_layout.addWidget(self.theme_combo, 1)
        theme_layout.addLayout(theme_select_layout)
        
        layout.addWidget(theme_group)
        
        # Spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        return widget

    def create_privacy_tab(self):
        """Create privacy settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Cookies Group
        cookies_group = QGroupBox("🍪 Cookies and Site Data")
        cookies_layout = QVBoxLayout(cookies_group)
        cookies_layout.setSpacing(12)
        
        cookie_policy_layout = QHBoxLayout()
        cookie_label = QLabel("Cookies:")
        cookie_label.setMinimumWidth(140)
        self.cookie_combo = QComboBox()
        self.cookie_combo.addItem("Allow all cookies", "allow_all")
        self.cookie_combo.addItem("Block third-party cookies", "block_third_party")
        self.cookie_combo.addItem("Block all cookies", "block_all")
        
        current_cookie = self.config.get_setting("cookie_policy") or "allow_all"
        index = self.cookie_combo.findData(current_cookie)
        if index != -1:
            self.cookie_combo.setCurrentIndex(index)
            
        cookie_policy_layout.addWidget(cookie_label)
        cookie_policy_layout.addWidget(self.cookie_combo, 1)
        cookies_layout.addLayout(cookie_policy_layout)
        
        # Clear data button
        clear_data_btn = QPushButton("🗑️  Clear Browsing Data...")
        clear_data_btn.setObjectName("dangerButton")
        clear_data_btn.clicked.connect(self.clear_browsing_data)
        cookies_layout.addWidget(clear_data_btn)
        
        layout.addWidget(cookies_group)
        
        # Tracking Group
        tracking_group = QGroupBox("👁️ Tracking Prevention")
        tracking_layout = QVBoxLayout(tracking_group)
        
        self.do_not_track_check = QCheckBox("Send 'Do Not Track' request with browsing traffic")
        self.do_not_track_check.setChecked(
            self.config.get_setting("do_not_track") or False
        )
        tracking_layout.addWidget(self.do_not_track_check)
        
        layout.addWidget(tracking_group)
        
        # Permissions Group
        permissions_group = QGroupBox("🔐 Permissions")
        permissions_layout = QVBoxLayout(permissions_group)
        permissions_layout.setSpacing(8)
        
        self.location_check = QCheckBox("Allow sites to request location access")
        self.location_check.setChecked(
            self.config.get_setting("allow_location") or False
        )
        permissions_layout.addWidget(self.location_check)
        
        self.notifications_check = QCheckBox("Allow sites to show notifications")
        self.notifications_check.setChecked(
            self.config.get_setting("allow_notifications") or False
        )
        permissions_layout.addWidget(self.notifications_check)
        
        layout.addWidget(permissions_group)
        
        # Spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        return widget

    def create_advanced_tab(self):
        """Create advanced settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Performance Group
        performance_group = QGroupBox("⚡ Performance")
        performance_layout = QVBoxLayout(performance_group)
        
        self.hardware_accel_check = QCheckBox("Use hardware acceleration when available")
        self.hardware_accel_check.setChecked(
            self.config.get_setting("hardware_acceleration") or True
        )
        performance_layout.addWidget(self.hardware_accel_check)
        
        layout.addWidget(performance_group)
        
        # Content Settings Group
        content_group = QGroupBox("📄 Content Settings")
        content_layout = QVBoxLayout(content_group)
        content_layout.setSpacing(8)
        
        self.javascript_check = QCheckBox("Enable JavaScript (required for most sites)")
        self.javascript_check.setChecked(
            self.config.get_setting("javascript_enabled") or True
        )
        content_layout.addWidget(self.javascript_check)
        
        self.images_check = QCheckBox("Load images automatically")
        self.images_check.setChecked(
            self.config.get_setting("auto_load_images") or True
        )
        content_layout.addWidget(self.images_check)
        
        self.plugins_check = QCheckBox("Enable plugins")
        self.plugins_check.setChecked(
            self.config.get_setting("plugins_enabled") or False
        )
        content_layout.addWidget(self.plugins_check)
        
        layout.addWidget(content_group)
        
        # Developer Group
        developer_group = QGroupBox("👨‍💻 Developer")
        developer_layout = QVBoxLayout(developer_group)
        developer_layout.setSpacing(8)
        
        self.edit_mode_check = QCheckBox("Enable UI edit mode (experimental)")
        self.edit_mode_check.setToolTip("Allows customizing the browser interface")
        self.edit_mode_check.setChecked(
            self.config.get_setting("edit_mode_enabled") or False
        )
        developer_layout.addWidget(self.edit_mode_check)
        
        self.dev_tools_check = QCheckBox("Enable developer tools (F12)")
        self.dev_tools_check.setChecked(
            self.config.get_setting("dev_tools_enabled") or True
        )
        developer_layout.addWidget(self.dev_tools_check)
        
        layout.addWidget(developer_group)
        
        # Reset Group
        reset_group = QGroupBox("🔄 Reset")
        reset_layout = QVBoxLayout(reset_group)
        
        reset_label = QLabel("Restore all settings to their default values")
        reset_label.setStyleSheet("color: #858585; font-size: 12px;")
        reset_layout.addWidget(reset_label)
        
        reset_btn = QPushButton("⚠️  Reset All Settings")
        reset_btn.setObjectName("dangerButton")
        reset_btn.clicked.connect(self.reset_settings)
        reset_layout.addWidget(reset_btn)
        
        layout.addWidget(reset_group)
        
        # Spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        return widget

    def create_button_bar(self):
        """Create the bottom button bar."""
        bar = QFrame()
        bar.setStyleSheet("""
            QFrame {
                background-color: #252526;
                border-top: 1px solid #3e3e42;
            }
        """)
        
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 16, 20, 16)
        
        # Info label
        info_label = QLabel("💡 Changes take effect immediately")
        info_label.setStyleSheet("color: #858585; font-size: 12px;")
        layout.addWidget(info_label)
        
        # Spacer
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Cancel button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setMinimumWidth(100)
        self.cancel_btn.clicked.connect(self.reject)
        layout.addWidget(self.cancel_btn)
        
        # Save button
        self.save_btn = QPushButton("💾 Save")
        self.save_btn.setObjectName("primaryButton")
        self.save_btn.setMinimumWidth(100)
        self.save_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_btn)
        
        return bar

    def save_settings(self):
        """Save all settings to config."""
        # General
        self.config.set_setting("homepage", self.homepage_input.text())
        self.config.set_setting("new_tab_page", self.newtab_combo.currentData())
        self.config.set_setting("search_engine", self.search_combo.currentData())
        self.config.set_setting("ask_download_location", self.ask_download_check.isChecked())
        
        # Appearance
        self.config.set_setting("tab_position", self.tab_pos_combo.currentData())
        self.config.set_setting("compact_mode", self.compact_mode_check.isChecked())
        
        # Privacy
        self.config.set_setting("cookie_policy", self.cookie_combo.currentData())
        self.config.set_setting("do_not_track", self.do_not_track_check.isChecked())
        self.config.set_setting("allow_location", self.location_check.isChecked())
        self.config.set_setting("allow_notifications", self.notifications_check.isChecked())
        
        # Advanced
        self.config.set_setting("hardware_acceleration", self.hardware_accel_check.isChecked())
        self.config.set_setting("javascript_enabled", self.javascript_check.isChecked())
        self.config.set_setting("auto_load_images", self.images_check.isChecked())
        self.config.set_setting("plugins_enabled", self.plugins_check.isChecked())
        self.config.set_setting("edit_mode_enabled", self.edit_mode_check.isChecked())
        self.config.set_setting("dev_tools_enabled", self.dev_tools_check.isChecked())
        
        # Save to disk
        self.config.save_config()
        
        # Emit signal
        self.settings_saved.emit()
        
        self.accept()

    def clear_browsing_data(self):
        """Clear browsing data."""
        reply = QMessageBox.question(
            self,
            "Clear Browsing Data",
            "This will clear cookies, cache, and browsing history.\n\nAre you sure you want to continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if hasattr(self.parent(), 'storage'):
                self.parent().storage.clear_all_data()
                QMessageBox.information(
                    self,
                    "Data Cleared",
                    "✅ Browsing data has been cleared successfully."
                )

    def reset_settings(self):
        """Reset all settings to defaults."""
        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "⚠️ This will reset ALL settings to default values.\n\nThis action cannot be undone. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.config.reset_to_defaults()
            
            QMessageBox.information(
                self,
                "Settings Reset",
                "✅ Settings have been reset to defaults.\n\nPlease restart the browser for changes to take full effect."
            )
            
            self.accept()


# Standalone test
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    # Mock config for testing
    class MockConfig:
        def __init__(self):
            self.config = {
                "homepage": "https://www.google.com",
                "tab_position": "top",
            }
        
        def get_setting(self, key):
            return self.config.get(key)
        
        def set_setting(self, key, value):
            self.config[key] = value
        
        def save_config(self):
            print("Config saved:", self.config)
        
        def reset_to_defaults(self):
            self.config = {}
    
    app = QApplication(sys.argv)
    app.setStyleSheet(SETTINGS_THEME)
    
    mock_config = MockConfig()
    dialog = SettingsDialog(mock_config)
    dialog.exec()
    
    sys.exit()