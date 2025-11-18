# main.py - Complete Browser with All Features

import sys
import os
from pathlib import Path
from PyQt6.QtCore import (
    QUrl, Qt, QSize, QTimer, QStandardPaths, QEvent, pyqtSignal
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLineEdit, 
    QPushButton, QHBoxLayout, QWidget, 
    QVBoxLayout, QTabBar, QStackedWidget,
    QProgressBar, QToolButton, QStatusBar, QMenu, QLabel,
    QInputDialog, QFileDialog, QDialog
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import (
    QWebEngineProfile, QWebEngineSettings, QWebEnginePage
)
from PyQt6.QtGui import (
    QIcon, QKeySequence, QShortcut, QAction, QCursor
)

# Import QtAwesome for Font Awesome icons
import qtawesome as qta

# Import our modules
from config_manager import ConfigManager
from settings_dialog import SettingsDialog
from bookmarks_manager import BookmarksManager, BookmarksDialog
from history_manager import HistoryManager, HistoryDialog
from downloads_manager import DownloadsManager, DownloadsDialog
from find_dialog import FindBar
from content_blocker import ContentBlocker

# --- ENHANCED FLUENT UI DESIGN TOKENS ---
COLORS = {
    'bg_primary': '#1e1e1e',
    'bg_secondary': '#252526',
    'bg_tertiary': '#2d2d30',
    'bg_hover': '#3e3e42',
    'bg_active': '#094771',
    'accent': '#0e639c',
    'accent_hover': '#1177bb',
    'accent_pressed': '#0d5a8e',
    'text_primary': '#cccccc',
    'text_secondary': '#858585',
    'border': '#3e3e42',
    'divider': '#454545',
    'success': '#43a047',
    'warning': '#ff9800',
    'error': '#e53935',
}

# --- ENHANCED FLUENT THEME ---
FLUENT_THEME = """
* {
    font-family: 'Segoe UI Variable', 'Segoe UI', system-ui, -apple-system, sans-serif;
    outline: none;
}

QWidget {
    background-color: #1e1e1e;
    color: #cccccc;
    font-size: 13px;
}

QMainWindow {
    background-color: #1e1e1e;
    border: none;
}

QStatusBar {
    background-color: #007acc;
    color: #ffffff;
    border: none;
    padding: 2px 8px;
    font-size: 11px;
}

QStatusBar QLabel {
    color: #ffffff;
    background: transparent;
}

QToolBar {
    background-color: #252526;
    border: none;
    border-bottom: 1px solid #3e3e42;
    padding: 6px 10px;
    spacing: 4px;
}

QToolBar::separator {
    background-color: #3e3e42;
    width: 1px;
    margin: 6px 8px;
}

QToolButton {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 6px;
    margin: 0 2px;
    min-width: 32px;
    max-width: 32px;
    min-height: 32px;
    max-height: 32px;
    color: #cccccc;
}

QToolButton:hover {
    background-color: #3e3e42;
    border-color: #454545;
}

QToolButton:pressed {
    background-color: #094771;
    border-color: #0e639c;
}

QToolButton:disabled {
    color: #656565;
    background-color: transparent;
}

QToolButton#bookmarked {
    color: #ffa500;
}

QLineEdit {
    background-color: #2d2d30;
    border: 1px solid #3e3e42;
    border-radius: 4px;
    padding: 7px 14px;
    color: #cccccc;
    font-size: 13px;
    min-height: 32px;
    max-height: 32px;
    margin: 0 8px;
    selection-background-color: #094771;
}

QLineEdit:hover {
    background-color: #333337;
    border-color: #454545;
}

QLineEdit:focus {
    background-color: #1e1e1e;
    border: 1px solid #0e639c;
}

QLineEdit::placeholder {
    color: #656565;
}

QPushButton#newTabButton {
    background-color: #0e639c;
    border: 1px solid #0e639c;
    border-radius: 4px;
    color: #ffffff;
    font-size: 18px;
    font-weight: 600;
    padding: 6px;
    margin: 0 2px;
    min-width: 32px;
    max-width: 32px;
    min-height: 32px;
    max-height: 32px;
}

QPushButton#newTabButton:hover {
    background-color: #1177bb;
    border-color: #1177bb;
}

QPushButton#newTabButton:pressed {
    background-color: #0d5a8e;
    border-color: #0d5a8e;
}

QTabBar {
    background-color: #252526;
    border: none;
    qproperty-drawBase: 0;
}

QTabBar::tab {
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    padding: 8px 16px;
    margin-right: 2px;
    min-width: 100px;
    max-width: 200px;
    color: #858585;
    font-size: 13px;
}

QTabBar::tab:hover:!selected {
    background: #2d2d30;
    color: #cccccc;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background: #2d2d30;
    color: #ffffff;
    border-bottom: 2px solid #0e639c;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::close-button {
    image: none;
    background: transparent;
    border-radius: 3px;
    padding: 2px;
    margin: 0 0 0 8px;
    subcontrol-position: right;
}

QTabBar::close-button:hover {
    background-color: #e53935;
}

QProgressBar {
    border: none;
    background-color: transparent;
    height: 3px;
    max-height: 3px;
}

QProgressBar::chunk {
    background-color: #0e639c;
}

QScrollBar:vertical {
    background: transparent;
    width: 12px;
    margin: 0;
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

QScrollBar:horizontal {
    background: transparent;
    height: 12px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background: #3e3e42;
    border-radius: 6px;
    min-width: 30px;
    margin: 2px;
}

QScrollBar::handle:horizontal:hover {
    background: #4e4e52;
}

QScrollBar::add-line, QScrollBar::sub-line,
QScrollBar::add-page, QScrollBar::sub-page {
    background: none;
    border: none;
}

QMenu {
    background-color: #252526;
    border: 1px solid #454545;
    padding: 4px;
    color: #cccccc;
}

QMenu::item {
    padding: 6px 24px 6px 12px;
    border-radius: 3px;
}

QMenu::item:selected {
    background-color: #094771;
    color: #ffffff;
}

QMenu::separator {
    height: 1px;
    background: #3e3e42;
    margin: 4px 8px;
}
"""


# --- ICON MANAGER ---
class IconManager:
    """Manages Font Awesome icons with caching."""
    
    _cache = {}
    _icon_options = {
        'color': '#cccccc',
        'color_disabled': '#656565',
        'color_active': '#ffffff',
    }
    
    @classmethod
    def get_icon(cls, name, color=None):
        """Get Font Awesome icon with caching."""
        if color is None:
            color = cls._icon_options['color']
            
        cache_key = f"{name}_{color}"
        
        if cache_key not in cls._cache:
            try:
                cls._cache[cache_key] = qta.icon(name, color=color)
            except Exception as e:
                print(f"Error loading icon {name}: {e}")
                cls._cache[cache_key] = QIcon()
                
        return cls._cache[cache_key]
    
    @classmethod
    def get_icon_with_states(cls, name):
        """Get icon with different states."""
        icon = qta.icon(name, 
            color=cls._icon_options['color'],
            color_disabled=cls._icon_options['color_disabled'],
            color_active=cls._icon_options['color_active']
        )
        return icon


# --- STORAGE MANAGER ---
class StorageManager:
    """Manages browser storage with memory optimization."""
    
    def __init__(self):
        """Initialize storage paths."""
        app_data = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        self.base_path = Path(app_data) / "Flux"
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        self._profile = None
        self.content_blocker = ContentBlocker()
    
    def get_profile(self):
        """Get or create the web engine profile."""
        if self._profile is None:
            self._profile = QWebEngineProfile("FluxProfile")
            
            # Set storage paths
            self._profile.setPersistentStoragePath(str(self.base_path / "storage"))
            self._profile.setCachePath(str(self.base_path / "cache"))
            
            # Cache size
            self._profile.setHttpCacheMaximumSize(100 * 1024 * 1024)
            
            # Cookies
            self._profile.setPersistentCookiesPolicy(
                QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies
            )
            
            # Set content blocker
            self._profile.setUrlRequestInterceptor(self.content_blocker)
            
            # Configure settings
            settings = self._profile.settings()
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
            
        return self._profile
    
    def clear_cookies(self):
        """Clear all cookies."""
        if self._profile:
            self._profile.cookieStore().deleteAllCookies()
    
    def clear_cache(self):
        """Clear browser cache."""
        if self._profile:
            self._profile.clearHttpCache()
    
    def clear_all_data(self):
        """Clear all browsing data."""
        if self._profile:
            self.clear_cookies()
            self.clear_cache()
            self._profile.clearAllVisitedLinks()


# --- CONFIG HELPER ---
class ConfigHelper:
    """Helper wrapper for ConfigManager."""
    
    def __init__(self, config_manager):
        self.config = config_manager
        
    def get(self, key, default=None):
        """Get setting with optional default value."""
        try:
            value = self.config.get_setting(key)
            return value if value is not None else default
        except (TypeError, KeyError, AttributeError):
            return default


# --- ENHANCED COMPONENTS ---
class LoadingIndicator(QProgressBar):
    """Enhanced loading indicator."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximum(100)
        self.setTextVisible(False)
        self.setFixedHeight(3)
        self.hide()
        
    def start_loading(self):
        self.setValue(0)
        self.show()
        
    def finish_loading(self):
        self.setValue(100)
        QTimer.singleShot(300, self.hide)


class EnhancedURLBar(QLineEdit):
    """Enhanced URL bar with better UX."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("🔍 Search or enter web address")
        
        # Context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self, pos):
        """Show custom context menu."""
        menu = self.createStandardContextMenu()
        menu.exec(self.mapToGlobal(pos))
    
    def focusInEvent(self, event):
        """Select all text on focus."""
        super().focusInEvent(event)
        QTimer.singleShot(0, self.selectAll)


class HeaderBar(QWidget):
    """Compact header combining tabs and navigation."""
    
    def __init__(self, tab_bar, nav_toolbar, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        layout.addWidget(tab_bar)
        layout.addWidget(nav_toolbar)


class TabbedBrowserWidget(QWidget):
    """Enhanced tabbed browser widget with all features."""
    
    status_message = pyqtSignal(str)
    
    def __init__(self, config_manager, storage_manager, bookmarks_manager, 
                 history_manager, downloads_manager, parent=None):
        super().__init__(parent)
        self.config = ConfigHelper(config_manager)
        self.storage = storage_manager
        self.bookmarks = bookmarks_manager
        self.history = history_manager
        self.downloads = downloads_manager
        self._vertical_mode = False
        
        # Track tabs
        self.tab_data = {}
        self.recently_closed = []  # For Ctrl+Shift+T
        self.pinned_tabs = set()  # Track pinned tabs
        
        # Components
        self.tab_bar = QTabBar(self)
        self.content_stack = QStackedWidget(self)
        self.nav_toolbar = QToolBar("Navigation")
        self.loading_indicator = LoadingIndicator(self)
        
        # Find bar
        self.find_bar = FindBar(self)
        
        # Setup UI
        self.setup_header()
        self.setup_shortcuts()
        
        # Initial Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.header = HeaderBar(self.tab_bar, self.nav_toolbar, self)
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.loading_indicator)
        self.main_layout.addWidget(self.content_stack)
        self.main_layout.addWidget(self.find_bar)
        
        # Signals
        self.tab_bar.tabBarClicked.connect(self.switch_tab)
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.content_stack.currentChanged.connect(self.on_tab_changed)
        
        # Enable middle-click to close tabs
        self.tab_bar.installEventFilter(self)
        
        # Setup tab context menu
        self.setup_tab_context_menu()

    def eventFilter(self, obj, event):
        """Handle tab bar events."""
        if obj == self.tab_bar:
            if event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.MiddleButton:
                    index = self.tab_bar.tabAt(event.pos())
                    if index != -1:
                        self.close_tab(index)
                        return True
        return super().eventFilter(obj, event)

    def setup_tab_context_menu(self):
        """Setup tab bar context menu."""
        self.tab_bar.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tab_bar.customContextMenuRequested.connect(self.show_tab_context_menu)

    def show_tab_context_menu(self, pos):
        """Show tab context menu."""
        index = self.tab_bar.tabAt(pos)
        if index == -1:
            return
        
        menu = QMenu(self)
        
        # Reload
        reload_action = menu.addAction(IconManager.get_icon('fa5s.redo'), "Reload Tab")
        reload_action.triggered.connect(lambda: self.reload_tab_at_index(index))
        
        # Duplicate
        duplicate_action = menu.addAction(IconManager.get_icon('fa5s.clone'), "Duplicate Tab")
        duplicate_action.triggered.connect(lambda: self.duplicate_tab_at_index(index))
        
        # Pin/Unpin
        if index in self.pinned_tabs:
            pin_action = menu.addAction(IconManager.get_icon('fa5s.thumbtack'), "Unpin Tab")
            pin_action.triggered.connect(lambda: self.unpin_tab(index))
        else:
            pin_action = menu.addAction(IconManager.get_icon('fa5s.thumbtack'), "Pin Tab")
            pin_action.triggered.connect(lambda: self.pin_tab(index))
        
        # Mute
        browser = self.content_stack.widget(index)
        if browser and browser.page():
            if browser.page().isAudioMuted():
                mute_action = menu.addAction(IconManager.get_icon('fa5s.volume-up'), "Unmute Tab")
            else:
                mute_action = menu.addAction(IconManager.get_icon('fa5s.volume-mute'), "Mute Tab")
            mute_action.triggered.connect(lambda: self.toggle_mute_tab(index))
        
        menu.addSeparator()
        
        # Close
        close_action = menu.addAction(IconManager.get_icon('fa5s.times'), "Close Tab")
        close_action.triggered.connect(lambda: self.close_tab(index))
        
        # Close others
        close_others = menu.addAction("Close Other Tabs")
        close_others.triggered.connect(lambda: self.close_other_tabs(index))
        
        # Close to right
        close_right = menu.addAction("Close Tabs to the Right")
        close_right.triggered.connect(lambda: self.close_tabs_to_right(index))
        
        menu.exec(QCursor.pos())

    def reload_tab_at_index(self, index):
        """Reload tab at index."""
        browser = self.content_stack.widget(index)
        if browser:
            browser.reload()

    def duplicate_tab_at_index(self, index):
        """Duplicate tab at index."""
        browser = self.content_stack.widget(index)
        if browser:
            self.add_tab(browser.url(), browser.title())

    def pin_tab(self, index):
        """Pin tab."""
        self.pinned_tabs.add(index)
        self.tab_bar.setTabText(index, "📌 " + self.tab_bar.tabText(index))

    def unpin_tab(self, index):
        """Unpin tab."""
        if index in self.pinned_tabs:
            self.pinned_tabs.remove(index)
            text = self.tab_bar.tabText(index).replace("📌 ", "")
            self.tab_bar.setTabText(index, text)

    def toggle_mute_tab(self, index):
        """Toggle tab mute."""
        browser = self.content_stack.widget(index)
        if browser and browser.page():
            is_muted = browser.page().isAudioMuted()
            browser.page().setAudioMuted(not is_muted)

    def close_other_tabs(self, keep_index):
        """Close all tabs except the specified one."""
        # Close from end to beginning to maintain indices
        for i in range(self.content_stack.count() - 1, -1, -1):
            if i != keep_index and i not in self.pinned_tabs:
                self.close_tab(i)

    def close_tabs_to_right(self, index):
        """Close all tabs to the right of index."""
        for i in range(self.content_stack.count() - 1, index, -1):
            if i not in self.pinned_tabs:
                self.close_tab(i)

    def setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        # New tab: Ctrl+T
        QShortcut(QKeySequence("Ctrl+T"), self, self.create_new_tab)
        
        # Close tab: Ctrl+W
        QShortcut(QKeySequence("Ctrl+W"), self, lambda: self.close_tab(self.tab_bar.currentIndex()))
        
        # Reopen closed tab: Ctrl+Shift+T
        QShortcut(QKeySequence("Ctrl+Shift+T"), self, self.reopen_closed_tab)
        
        # Focus URL bar: Ctrl+L or F6
        QShortcut(QKeySequence("Ctrl+L"), self, self.url_bar.setFocus)
        QShortcut(QKeySequence("F6"), self, self.url_bar.setFocus)
        
        # Reload: F5 or Ctrl+R
        QShortcut(QKeySequence("F5"), self, self.reload_page)
        QShortcut(QKeySequence("Ctrl+R"), self, self.reload_page)
        
        # Back: Alt+Left
        QShortcut(QKeySequence("Alt+Left"), self, self.navigate_back)
        
        # Forward: Alt+Right
        QShortcut(QKeySequence("Alt+Right"), self, self.navigate_forward)
        
        # Home: Alt+Home
        QShortcut(QKeySequence("Alt+Home"), self, self.navigate_home)
        
        # Switch tabs
        QShortcut(QKeySequence("Ctrl+Tab"), self, self.next_tab)
        QShortcut(QKeySequence("Ctrl+Shift+Tab"), self, self.previous_tab)
        
        # Zoom
        QShortcut(QKeySequence("Ctrl++"), self, self.zoom_in)
        QShortcut(QKeySequence("Ctrl+-"), self, self.zoom_out)
        QShortcut(QKeySequence("Ctrl+0"), self, self.zoom_reset)
        
        # Find in page: Ctrl+F
        QShortcut(QKeySequence("Ctrl+F"), self, self.show_find_bar)
        
        # View source: Ctrl+U
        QShortcut(QKeySequence("Ctrl+U"), self, self.view_page_source)
        
        # Bookmark: Ctrl+D
        QShortcut(QKeySequence("Ctrl+D"), self, self.toggle_bookmark)
        
        # Full screen: F11
        QShortcut(QKeySequence("F11"), self, self.toggle_fullscreen)

    def show_find_bar(self):
        """Show find in page bar."""
        browser = self.current_browser()
        if browser:
            self.find_bar.set_web_page(browser.page())
            self.find_bar.show_bar()

    def view_page_source(self):
        """View page source."""
        browser = self.current_browser()
        if browser:
            source_url = QUrl("view-source:" + browser.url().toString())
            self.add_tab(source_url, "Source: " + browser.title())

    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        window = self.window()
        if window.isFullScreen():
            window.showNormal()
        else:
            window.showFullScreen()

    def reopen_closed_tab(self):
        """Reopen recently closed tab."""
        if self.recently_closed:
            url, title = self.recently_closed.pop()
            self.add_tab(QUrl(url), title)

    def next_tab(self):
        """Switch to next tab."""
        current = self.tab_bar.currentIndex()
        next_index = (current + 1) % self.tab_bar.count()
        self.tab_bar.setCurrentIndex(next_index)

    def previous_tab(self):
        """Switch to previous tab."""
        current = self.tab_bar.currentIndex()
        prev_index = (current - 1) % self.tab_bar.count()
        self.tab_bar.setCurrentIndex(prev_index)

    def zoom_in(self):
        """Zoom in."""
        browser = self.current_browser()
        if browser:
            browser.setZoomFactor(browser.zoomFactor() + 0.1)

    def zoom_out(self):
        """Zoom out."""
        browser = self.current_browser()
        if browser:
            browser.setZoomFactor(max(0.25, browser.zoomFactor() - 0.1))

    def zoom_reset(self):
        """Reset zoom."""
        browser = self.current_browser()
        if browser:
            browser.setZoomFactor(1.0)

    def switch_tab(self, index):
        """Switch to tab."""
        self.content_stack.setCurrentIndex(index)

    def on_tab_changed(self, index):
        """Handle tab change."""
        browser = self.current_browser()
        if browser:
            self.url_bar.setText(browser.url().toString())
            self.update_navigation_buttons()
            self.update_bookmark_button()

    def setup_header(self):
        """Setup enhanced navigation toolbar."""
        
        self.nav_toolbar.setMovable(False)
        self.nav_toolbar.setIconSize(QSize(16, 16))
        
        # Back
        self.back_btn = QToolButton()
        self.back_btn.setIcon(IconManager.get_icon('fa5s.arrow-left'))
        self.back_btn.setToolTip("Back (Alt+Left)")
        self.back_btn.clicked.connect(self.navigate_back)
        self.nav_toolbar.addWidget(self.back_btn)

        # Forward
        self.forward_btn = QToolButton()
        self.forward_btn.setIcon(IconManager.get_icon('fa5s.arrow-right'))
        self.forward_btn.setToolTip("Forward (Alt+Right)")
        self.forward_btn.clicked.connect(self.navigate_forward)
        self.nav_toolbar.addWidget(self.forward_btn)

        # Reload
        self.reload_btn = QToolButton()
        self.reload_btn.setIcon(IconManager.get_icon('fa5s.redo'))
        self.reload_btn.setToolTip("Reload (F5)")
        self.reload_btn.clicked.connect(self.reload_page)
        self.nav_toolbar.addWidget(self.reload_btn)

        # Home
        self.home_btn = QToolButton()
        self.home_btn.setIcon(IconManager.get_icon('fa5s.home'))
        self.home_btn.setToolTip("Home (Alt+Home)")
        self.home_btn.clicked.connect(self.navigate_home)
        self.nav_toolbar.addWidget(self.home_btn)
        
        self.nav_toolbar.addSeparator()

        # URL Bar
        self.url_bar = EnhancedURLBar()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        spacer = QWidget()
        spacer_layout = QHBoxLayout(spacer)
        spacer_layout.setContentsMargins(0, 0, 0, 0)
        spacer_layout.addWidget(self.url_bar)
        self.nav_toolbar.addWidget(spacer)
        
        self.nav_toolbar.addSeparator()
        
        # Bookmark button
        self.bookmark_btn = QToolButton()
        self.bookmark_btn.setIcon(IconManager.get_icon('fa5s.star'))
        self.bookmark_btn.setToolTip("Bookmark this page (Ctrl+D)")
        self.bookmark_btn.clicked.connect(self.toggle_bookmark)
        self.nav_toolbar.addWidget(self.bookmark_btn)
        
        # Bookmarks manager
        self.bookmarks_btn = QToolButton()
        self.bookmarks_btn.setIcon(IconManager.get_icon('fa5s.bookmark'))
        self.bookmarks_btn.setToolTip("Bookmarks")
        self.bookmarks_btn.clicked.connect(self.show_bookmarks)
        self.nav_toolbar.addWidget(self.bookmarks_btn)
        
        # History
        self.history_btn = QToolButton()
        self.history_btn.setIcon(IconManager.get_icon('fa5s.history'))
        self.history_btn.setToolTip("History")
        self.history_btn.clicked.connect(self.show_history)
        self.nav_toolbar.addWidget(self.history_btn)
        
        # Downloads
        self.downloads_btn = QToolButton()
        self.downloads_btn.setIcon(IconManager.get_icon('fa5s.download'))
        self.downloads_btn.setToolTip("Downloads")
        self.downloads_btn.clicked.connect(self.show_downloads)
        self.nav_toolbar.addWidget(self.downloads_btn)
        
        # New Tab
        self.new_tab_btn = QPushButton('+')
        self.new_tab_btn.setObjectName("newTabButton")
        self.new_tab_btn.setToolTip("New Tab (Ctrl+T)")
        self.new_tab_btn.clicked.connect(self.create_new_tab)
        self.nav_toolbar.addWidget(self.new_tab_btn)
        
        # Menu
        self.menu_btn = QToolButton()
        self.menu_btn.setIcon(IconManager.get_icon('fa5s.bars'))
        self.menu_btn.setToolTip("Menu")
        self.menu_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.menu_btn.setMenu(self.create_menu())
        self.nav_toolbar.addWidget(self.menu_btn)

        # Tab bar
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.setMovable(True)
        self.tab_bar.setExpanding(False)
        self.tab_bar.setElideMode(Qt.TextElideMode.ElideRight)

        self.update_navigation_buttons()

    def create_menu(self):
        """Create application menu."""
        menu = QMenu(self)
        
        # New Tab
        new_tab_action = menu.addAction(IconManager.get_icon('fa5s.plus'), "New Tab")
        new_tab_action.setShortcut(QKeySequence("Ctrl+T"))
        new_tab_action.triggered.connect(self.create_new_tab)
        
        # New Private Window
        private_action = menu.addAction(IconManager.get_icon('fa5s.user-secret'), "New Private Window")
        private_action.setShortcut(QKeySequence("Ctrl+Shift+N"))
        private_action.triggered.connect(self.new_private_window)
        
        menu.addSeparator()
        
        # Find
        find_action = menu.addAction(IconManager.get_icon('fa5s.search'), "Find in Page")
        find_action.setShortcut(QKeySequence("Ctrl+F"))
        find_action.triggered.connect(self.show_find_bar)
        
        menu.addSeparator()
        
        # History
        history_action = menu.addAction(IconManager.get_icon('fa5s.history'), "History")
        history_action.triggered.connect(self.show_history)
        
        # Bookmarks
        bookmarks_action = menu.addAction(IconManager.get_icon('fa5s.bookmark'), "Bookmarks")
        bookmarks_action.triggered.connect(self.show_bookmarks)
        
        # Downloads
        downloads_action = menu.addAction(IconManager.get_icon('fa5s.download'), "Downloads")
        downloads_action.triggered.connect(self.show_downloads)
        
        menu.addSeparator()
        
        # Zoom
        zoom_menu = menu.addMenu(IconManager.get_icon('fa5s.search-plus'), "Zoom")
        
        zoom_in = zoom_menu.addAction("Zoom In")
        zoom_in.setShortcut(QKeySequence("Ctrl++"))
        zoom_in.triggered.connect(self.zoom_in)
        
        zoom_out = zoom_menu.addAction("Zoom Out")
        zoom_out.setShortcut(QKeySequence("Ctrl+-"))
        zoom_out.triggered.connect(self.zoom_out)
        
        zoom_reset = zoom_menu.addAction("Reset Zoom")
        zoom_reset.setShortcut(QKeySequence("Ctrl+0"))
        zoom_reset.triggered.connect(self.zoom_reset)
        
        menu.addSeparator()
        
        # Print
        print_action = menu.addAction(IconManager.get_icon('fa5s.print'), "Print...")
        print_action.setShortcut(QKeySequence("Ctrl+P"))
        print_action.triggered.connect(self.print_page)
        
        # Save Page
        save_action = menu.addAction(IconManager.get_icon('fa5s.save'), "Save Page As...")
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self.save_page)
        
        menu.addSeparator()
        
        # Settings
        settings_action = menu.addAction(IconManager.get_icon('fa5s.cog'), "Settings")
        settings_action.triggered.connect(self.show_settings)
        
        menu.addSeparator()
        
        # About
        about_action = menu.addAction(IconManager.get_icon('fa5s.info-circle'), "About")
        about_action.triggered.connect(self.show_about)
        
        return menu

    def new_private_window(self):
        """Create new private browsing window."""
        self.status_message.emit("Private browsing mode coming soon!")

    def print_page(self):
        """Print current page."""
        browser = self.current_browser()
        if browser:
            browser.page().printToPdf(str(Path.home() / "page.pdf"))
            self.status_message.emit("Page saved to page.pdf")

    def save_page(self):
        """Save page as HTML."""
        browser = self.current_browser()
        if browser:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Save Page", "", "HTML Files (*.html);;All Files (*)"
            )
            if filename:
                browser.page().toHtml(lambda html: self.save_html(html, filename))

    def save_html(self, html, filename):
        """Save HTML to file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            self.status_message.emit(f"Page saved to {filename}")
        except Exception as e:
            self.status_message.emit(f"Error saving page: {e}")

    def toggle_bookmark(self):
        """Toggle bookmark for current page."""
        browser = self.current_browser()
        if not browser:
            return
        
        url = browser.url().toString()
        title = browser.title() or "Untitled"
        
        if self.bookmarks.is_bookmarked(url):
            # Remove bookmark
            bookmark, location = self.bookmarks.get_bookmark_by_url(url)
            if bookmark:
                self.bookmarks.remove_bookmark(bookmark['id'], location)
                self.status_message.emit("Bookmark removed")
                self.bookmark_btn.setIcon(IconManager.get_icon('fa5s.star'))
                self.bookmark_btn.setObjectName("")
        else:
            # Add bookmark
            self.bookmarks.add_bookmark(url, title)
            self.status_message.emit("Bookmark added")
            self.bookmark_btn.setIcon(IconManager.get_icon('fa5s.star', '#ffa500'))
            self.bookmark_btn.setObjectName("bookmarked")
        
        self.bookmark_btn.style().unpolish(self.bookmark_btn)
        self.bookmark_btn.style().polish(self.bookmark_btn)

    def update_bookmark_button(self):
        """Update bookmark button state."""
        browser = self.current_browser()
        if not browser:
            return
        
        url = browser.url().toString()
        
        if self.bookmarks.is_bookmarked(url):
            self.bookmark_btn.setIcon(IconManager.get_icon('fa5s.star', '#ffa500'))
            self.bookmark_btn.setObjectName("bookmarked")
        else:
            self.bookmark_btn.setIcon(IconManager.get_icon('fa5s.star'))
            self.bookmark_btn.setObjectName("")
        
        self.bookmark_btn.style().unpolish(self.bookmark_btn)
        self.bookmark_btn.style().polish(self.bookmark_btn)

    def show_bookmarks(self):
        """Show bookmarks manager."""
        dialog = BookmarksDialog(self.bookmarks, self)
        dialog.bookmark_activated.connect(lambda url: self.add_tab(QUrl(url)))
        dialog.exec()

    def show_history(self):
        """Show history manager."""
        dialog = HistoryDialog(self.history, self)
        dialog.history_activated.connect(lambda url: self.add_tab(QUrl(url)))
        dialog.exec()

    def show_downloads(self):
        """Show downloads manager."""
        dialog = DownloadsDialog(self.downloads, self)
        dialog.exec()

    def show_about(self):
        """Show about dialog."""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            "About Flux",
            "<h3>Flux</h3>"
            "<p>Version 2.0</p>"
            "<p>A feature-rich web browser built with PyQt6</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Bookmarks Management</li>"
            "<li>Browsing History</li>"
            "<li>Downloads Manager</li>"
            "<li>Find in Page</li>"
            "<li>Ad & Tracker Blocking</li>"
            "<li>And much more!</li>"
            "</ul>"
        )

    def update_navigation_buttons(self):
        """Update navigation button states."""
        browser = self.current_browser()
        if browser:
            self.back_btn.setEnabled(browser.history().canGoBack())
            self.forward_btn.setEnabled(browser.history().canGoForward())
        else:
            self.back_btn.setEnabled(False)
            self.forward_btn.setEnabled(False)

    def navigate_back(self):
        """Navigate back."""
        if self.current_browser():
            self.current_browser().back()
            self.update_navigation_buttons()

    def navigate_forward(self):
        """Navigate forward."""
        if self.current_browser():
            self.current_browser().forward()
            self.update_navigation_buttons()

    def reload_page(self):
        """Reload page."""
        if self.current_browser():
            self.current_browser().reload()

    def navigate_home(self):
        """Navigate to homepage."""
        if self.current_browser():
            homepage = self.config.get("homepage", "https://www.google.com")
            self.current_browser().setUrl(QUrl(homepage))

    def create_new_tab(self):
        """Create new tab."""
        new_tab_page = self.config.get("new_tab_page", "homepage")
        
        if new_tab_page == "blank":
            url = QUrl("about:blank")
        else:
            url = QUrl(self.config.get("homepage", "https://www.google.com"))
        
        self.add_tab(url)

    def add_tab(self, qurl=None, label="New Tab"):
        """Add new tab."""
        if qurl is None:
            qurl = QUrl("about:blank")
        
        # Create page
        page = QWebEnginePage(self.storage.get_profile(), self)
        browser = QWebEngineView()
        browser.setPage(page)
        
        # Handle download requests
        page.profile().downloadRequested.connect(self.handle_download)
        
        # Store URL
        tab_id = id(browser)
        self.tab_data[tab_id] = {
            'url': qurl,
            'title': label
        }
        
        browser.setUrl(qurl)

        # Connect signals
        browser.urlChanged.connect(lambda url, b=browser: self.update_urlbar(url, b))
        browser.titleChanged.connect(lambda title, b=browser: self.update_tab_title(title, b))
        browser.loadStarted.connect(self.on_load_start)
        browser.loadProgress.connect(self.on_load_progress)
        browser.loadFinished.connect(lambda ok, b=browser: self.on_load_finish(ok, b))
        browser.iconChanged.connect(lambda icon, b=browser: self.update_tab_icon(icon, b))
        
        # Add to stack
        index = self.content_stack.addWidget(browser)
        
        # Add tab
        tab_index = self.tab_bar.addTab(label)
        self.tab_bar.setTabToolTip(tab_index, qurl.toString())
        
        # Switch to new tab
        self.tab_bar.setCurrentIndex(tab_index)
        self.content_stack.setCurrentIndex(index)

    def handle_download(self, download):
        """Handle download request."""
        # Ask where to save (if enabled in settings)
        ask_location = self.config.get("ask_download_location", True)
        
        if ask_location:
            suggested_name = download.suggestedFileName()
            filepath, _ = QFileDialog.getSaveFileName(
                self, "Save File", suggested_name, "All Files (*)"
            )
            
            if not filepath:
                download.cancel()
                return
            
            download.setDownloadFileName(filepath)
        else:
            # Use default download location
            download_path = self.downloads.download_path
            filepath = str(Path(download_path) / download.suggestedFileName())
            download.setDownloadFileName(filepath)
        
        # Add to downloads manager
        download_item = self.downloads.add_download(download)
        download_item.path = filepath
        
        # Accept download
        download.accept()
        
        self.status_message.emit(f"Downloading {download.suggestedFileName()}...")
        
    def close_tab(self, index):
        """Close tab."""
        if self.content_stack.count() < 2:
            return
        
        # Don't close pinned tabs easily
        if index in self.pinned_tabs:
            from PyQt6.QtWidgets import QMessageBox
            reply = QMessageBox.question(
                self, "Close Pinned Tab",
                "This tab is pinned. Close anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
            self.pinned_tabs.remove(index)

        widget = self.content_stack.widget(index)
        
        # Save to recently closed
        if widget:
            url = widget.url().toString()
            title = widget.title()
            self.recently_closed.append((url, title))
            self.recently_closed = self.recently_closed[-10:]  # Keep last 10
        
        # Remove from tracking
        tab_id = id(widget)
        if tab_id in self.tab_data:
            del self.tab_data[tab_id]
        
        # Cleanup
        if widget:
            widget.setPage(None)
            self.content_stack.removeWidget(widget)
            widget.deleteLater()
        
        self.tab_bar.removeTab(index)
        
    def current_browser(self):
        """Get current browser."""
        return self.content_stack.currentWidget()

    def navigate_to_url(self):
        """Navigate to URL."""
        url_text = self.url_bar.text().strip()
        
        if not url_text:
            return
        
        browser = self.current_browser()
        if not browser:
            return
        
        search_engine = self.config.get("search_engine", "https://www.google.com/search?q={}")
        
        # URL detection
        if url_text.startswith(('http://', 'https://', 'file://', 'about:')):
            url = QUrl(url_text)
        elif url_text.startswith('localhost') or url_text.startswith('127.0.0.1'):
            url = QUrl('http://' + url_text)
        elif ' ' in url_text or ('.' not in url_text and ':' not in url_text):
            url = QUrl(search_engine.format(url_text.replace(' ', '+')))
        elif '.' in url_text:
            url = QUrl('https://' + url_text)
        else:
            url = QUrl(search_engine.format(url_text))
            
        browser.setUrl(url)
        
        tab_id = id(browser)
        if tab_id in self.tab_data:
            self.tab_data[tab_id]['url'] = url

    def update_tab_title(self, title, browser):
        """Update tab title."""
        index = self.content_stack.indexOf(browser)
        if index != -1:
            # Check if pinned
            if index in self.pinned_tabs:
                display_title = "📌 " + ((title[:20] + "...") if len(title) > 20 else title)
            else:
                display_title = (title[:25] + "...") if len(title) > 25 else title
            
            self.tab_bar.setTabText(index, display_title or "Loading...")
            self.tab_bar.setTabToolTip(index, title or "")
            
            tab_id = id(browser)
            if tab_id in self.tab_data:
                self.tab_data[tab_id]['title'] = title

    def update_tab_icon(self, icon, browser):
        """Update tab icon."""
        index = self.content_stack.indexOf(browser)
        if index != -1 and not icon.isNull():
            self.tab_bar.setTabIcon(index, icon)
            
    def update_urlbar(self, url, browser=None):
        """Update URL bar."""
        if browser != self.current_browser():
            return
            
        url_str = url.toString()
        self.url_bar.setText(url_str)
        self.url_bar.setCursorPosition(0)
        
        # Add to history
        title = browser.title() if browser else ""
        self.history.add_visit(url_str, title)
        
        if browser:
            tab_id = id(browser)
            if tab_id in self.tab_data:
                self.tab_data[tab_id]['url'] = url
        
        self.update_navigation_buttons()
        self.update_bookmark_button()

    def on_load_start(self):
        """Handle load start."""
        self.loading_indicator.start_loading()
        self.reload_btn.setIcon(IconManager.get_icon('fa5s.times'))
        self.reload_btn.setToolTip("Stop loading")
        self.status_message.emit("Loading...")

    def on_load_progress(self, progress):
        """Update progress."""
        self.loading_indicator.setValue(progress)
        self.status_message.emit(f"Loading... {progress}%")

    def on_load_finish(self, success, browser):
        """Handle load finish."""
        self.loading_indicator.finish_loading()
        self.reload_btn.setIcon(IconManager.get_icon('fa5s.redo'))
        self.reload_btn.setToolTip("Reload (F5)")
        
        if success:
            self.status_message.emit("Done")
        else:
            self.status_message.emit("Failed to load page")
        
        self.update_navigation_buttons()

    def show_settings(self):
        """Show settings dialog."""
        dialog = SettingsDialog(self.config.config, self)
        dialog.settings_saved.connect(self.apply_settings)
        dialog.exec()

    def switch_to_horizontal_layout(self):
        """Switch to horizontal layout."""
        if not self._vertical_mode:
            return
        
        self.tab_bar.setParent(None)
        self.nav_toolbar.setParent(None)
        self.loading_indicator.setParent(None)
        self.content_stack.setParent(None)
        self.find_bar.setParent(None)
        
        old_layout = self.layout()
        if old_layout:
            while old_layout.count():
                old_layout.takeAt(0)
            QWidget().setLayout(old_layout)
        
        new_layout = QVBoxLayout(self)
        new_layout.setContentsMargins(0, 0, 0, 0)
        new_layout.setSpacing(0)
        
        self.header = HeaderBar(self.tab_bar, self.nav_toolbar, self)
        new_layout.addWidget(self.header)
        new_layout.addWidget(self.loading_indicator)
        new_layout.addWidget(self.content_stack)
        new_layout.addWidget(self.find_bar)
        
        self.main_layout = new_layout
        self._vertical_mode = False
        
        self.tab_bar.setShape(QTabBar.Shape.RoundedNorth)
        self.tab_bar.setExpanding(False)
        self.tab_bar.setStyleSheet("")
        
    def switch_to_vertical_layout(self):
        """Switch to vertical layout."""
        if self._vertical_mode:
            return
        
        self.tab_bar.setParent(None)
        self.nav_toolbar.setParent(None)
        self.loading_indicator.setParent(None)
        self.content_stack.setParent(None)
        self.find_bar.setParent(None)
        
        old_layout = self.layout()
        if old_layout:
            while old_layout.count():
                old_layout.takeAt(0)
            QWidget().setLayout(old_layout)
        
        new_layout = QHBoxLayout(self)
        new_layout.setContentsMargins(0, 0, 0, 0)
        new_layout.setSpacing(0)
        
        tab_container = QWidget()
        tab_container.setFixedWidth(200)
        tab_container_layout = QVBoxLayout(tab_container)
        tab_container_layout.setContentsMargins(0, 0, 0, 0)
        tab_container_layout.setSpacing(0)
        tab_container_layout.addWidget(self.tab_bar)
        tab_container_layout.addStretch()
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.addWidget(self.nav_toolbar)
        content_layout.addWidget(self.loading_indicator)
        content_layout.addWidget(self.content_stack)
        content_layout.addWidget(self.find_bar)
        
        new_layout.addWidget(tab_container)
        new_layout.addWidget(content_widget, 1)
        
        self.main_layout = new_layout
        self._vertical_mode = True
        
        self.tab_bar.setShape(QTabBar.Shape.RoundedWest)
        self.tab_bar.setExpanding(True)
        
        self.tab_bar.setStyleSheet("""
            QTabBar {
                background-color: #252526;
                border-right: 1px solid #3e3e42;
            }
            QTabBar::tab {
                background: transparent;
                border: none;
                border-left: 2px solid transparent;
                padding: 12px 16px;
                margin-bottom: 2px;
                min-height: 36px;
                max-height: 48px;
                min-width: 160px;
                color: #858585;
                text-align: left;
            }
            QTabBar::tab:hover:!selected {
                background: #2d2d30;
                color: #cccccc;
                border-top-left-radius: 4px;
                border-bottom-left-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #2d2d30;
                color: #ffffff;
                border-left: 2px solid #0e639c;
                border-top-left-radius: 4px;
                border-bottom-left-radius: 4px;
            }
            QTabBar::close-button {
                image: none;
                background: transparent;
                border-radius: 3px;
                padding: 3px;
                margin: 0;
                subcontrol-position: right;
            }
            QTabBar::close-button:hover {
                background-color: #e53935;
            }
        """)

    def apply_settings(self):
        """Apply settings."""
        tab_pos = self.config.get("tab_position", "top")
        
        if tab_pos == "left":
            self.switch_to_vertical_layout()
        else:
            self.switch_to_horizontal_layout()
        
        # Apply content blocker settings
        block_ads = self.config.get("block_ads", True)
        block_trackers = self.config.get("block_trackers", True)
        
        self.storage.content_blocker.set_block_ads(block_ads)
        self.storage.content_blocker.set_block_trackers(block_trackers)
        
        self.tab_bar.style().unpolish(self.tab_bar)
        self.tab_bar.style().polish(self.tab_bar)
        self.update()


class WelcomeDialog(QDialog):
    """A modern welcome and onboarding dialog for Flux."""

    def __init__(self, config_manager, settings_dialog_cls, bookmarks_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.settings_dialog_cls = settings_dialog_cls
        self.bookmarks_manager = bookmarks_manager

        self.setWindowTitle("Welcome to Flux")
        self.setModal(True)
        self.setMinimumSize(700, 420)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Title
        title = QLabel("Welcome to Flux")
        title.setStyleSheet("font-size:28px; font-weight:700; color: #ffffff;")
        subtitle = QLabel("A fast, minimal, and modern browser built for clarity and speed.")
        subtitle.setStyleSheet("color: #cccccc; font-size:14px;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Stacked pages
        from PyQt6.QtWidgets import QStackedWidget, QTextBrowser
        self.stack = QStackedWidget()

        # Intro page
        intro = QWidget()
        intro_layout = QVBoxLayout(intro)
        intro_text = QTextBrowser()
        intro_text.setOpenExternalLinks(True)
        intro_text.setStyleSheet("background: transparent; color: #cccccc; border: none;")
        intro_text.setHtml(
            "<h3 style='color:#ffffff'>Get comfortable</h3>"
            "<p>Flux is minimal, fast, and configurable. During setup you can import bookmarks, set privacy preferences, and choose your homepage.</p>"
        )
        intro_layout.addWidget(intro_text)

        # Customize page
        custom = QWidget()
        custom_layout = QVBoxLayout(custom)
        custom_layout.setSpacing(8)
        custom_layout.addWidget(QLabel("Quick customization"))

        custom_buttons = QHBoxLayout()
        btn_settings = QPushButton("Open Settings")
        btn_settings.clicked.connect(self.open_settings)
        btn_import = QPushButton("Import Bookmarks")
        btn_import.clicked.connect(self.import_bookmarks)
        custom_buttons.addWidget(btn_settings)
        custom_buttons.addWidget(btn_import)
        custom_layout.addLayout(custom_buttons)

        # Finish page
        finish = QWidget()
        finish_layout = QVBoxLayout(finish)
        self.dont_show_cb = QPushButton("Don't show this again")
        # toggle-like behavior
        self.dont_show_cb.setCheckable(True)
        finish_layout.addWidget(QLabel("You're ready to go"))
        finish_layout.addWidget(QLabel("Click Get Started to open Flux.") )
        finish_layout.addWidget(self.dont_show_cb)

        self.stack.addWidget(intro)
        self.stack.addWidget(custom)
        self.stack.addWidget(finish)

        layout.addWidget(self.stack, 1)

        # Navigation buttons
        nav = QHBoxLayout()
        nav.addStretch()
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.go_back)
        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.go_next)
        self.finish_btn = QPushButton("Get Started")
        self.finish_btn.clicked.connect(self.finish)

        nav.addWidget(self.back_btn)
        nav.addWidget(self.next_btn)
        nav.addWidget(self.finish_btn)

        layout.addLayout(nav)

        self.update_buttons()

    def update_buttons(self):
        index = self.stack.currentIndex()
        self.back_btn.setEnabled(index > 0)
        self.next_btn.setEnabled(index < (self.stack.count() - 1))

    def go_back(self):
        idx = self.stack.currentIndex()
        if idx > 0:
            self.stack.setCurrentIndex(idx - 1)
        self.update_buttons()

    def go_next(self):
        idx = self.stack.currentIndex()
        if idx < (self.stack.count() - 1):
            self.stack.setCurrentIndex(idx + 1)
        self.update_buttons()

    def open_settings(self):
        dlg = self.settings_dialog_cls(self.config_manager, None)
        dlg.exec()

    def import_bookmarks(self):
        # Simple import implementation: open file and merge if possible
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.FileMode.ExistingFile)
        dlg.setNameFilter("Bookmarks Files (*.html *.htm);;All Files (*)")
        if dlg.exec():
            files = dlg.selectedFiles()
            # Basic import: attempt to read as exported HTML and ignore complexity
            try:
                with open(files[0], 'r', encoding='utf-8') as f:
                    data = f.read()
                # store imported file as a single bookmark for now
                self.bookmarks_manager.add_bookmark(f'file://{files[0]}', 'Imported Bookmarks')
            except Exception as e:
                pass

    def finish(self):
        if self.dont_show_cb.isChecked():
            try:
                self.config_manager.set_setting('first_run', False)
                self.config_manager.save_config()
            except Exception:
                pass
        self.accept()



class BrowserWindow(QMainWindow):
    """Enhanced main browser window."""
    
    def __init__(self, config_manager, storage_manager, bookmarks_manager,
                 history_manager, downloads_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Flux")
        self.setWindowIcon(IconManager.get_icon('fa5s.compass'))
        
        self.config = ConfigHelper(config_manager)
        self.storage = storage_manager
        self.bookmarks = bookmarks_manager
        self.history = history_manager
        self.downloads = downloads_manager
        
        # Browser widget
        self.browser_widget = TabbedBrowserWidget(
            config_manager, storage_manager, bookmarks_manager,
            history_manager, downloads_manager, self
        )
        self.setCentralWidget(self.browser_widget)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #252526;
                color: #cccccc;
                border-top: 1px solid #3e3e42;
            }
        """)
        
        # Blocker stats in status bar
        self.blocker_label = QLabel()
        self.status_bar.addPermanentWidget(self.blocker_label)
        
        # Update blocker stats periodically
        self.stats_timer = QTimer(self)
        self.stats_timer.timeout.connect(self.update_blocker_stats)
        self.stats_timer.start(5000)  # Update every 5 seconds
        
        # Connect signals
        self.browser_widget.status_message.connect(self.show_status_message)
        
        # Window settings
        self.resize(1200, 750)
        self.setMinimumSize(900, 600)
        
        # Signals
        self.browser_widget.content_stack.currentChanged.connect(
            self.update_window_title
        )

        # Initial tab
        homepage = self.config.get("homepage", "https://www.google.com")
        self.browser_widget.add_tab(QUrl(homepage), 'Home')
        
        self.show()
        
        self.show_status_message("Welcome to Flux")
        # Show welcome/onboarding on first run
        QTimer.singleShot(200, self.show_welcome_if_first_run)

    def update_blocker_stats(self):
        """Update content blocker statistics."""
        blocked = self.storage.content_blocker.get_blocked_count()
        self.blocker_label.setText(f"🛡️ {blocked} blocked")

    def show_status_message(self, message, timeout=3000):
        """Show status message."""
        self.status_bar.showMessage(message, timeout)

    def update_window_title(self, index):
        """Update window title."""
        browser = self.browser_widget.content_stack.widget(index)
        if browser:
            title = browser.title() or "New Tab"
            self.setWindowTitle(f"{title} - Flux")
    
    def closeEvent(self, event):
        """Handle window close."""
        while self.browser_widget.content_stack.count() > 0:
            widget = self.browser_widget.content_stack.widget(0)
            if widget:
                widget.setPage(None)
                self.browser_widget.content_stack.removeWidget(widget)
                widget.deleteLater()
        
        if self.storage._profile:
            self.storage._profile.deleteLater()
        
        event.accept()

    def show_welcome_if_first_run(self):
        try:
            # Access underlying config manager
            cfg_mgr = self.config.config
            first = cfg_mgr.get_setting('first_run')
            if first:
                dlg = WelcomeDialog(cfg_mgr, SettingsDialog, self.bookmarks, self)
                dlg.exec()
                # mark as shown
                cfg_mgr.set_setting('first_run', False)
                cfg_mgr.save_config()
        except Exception:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Flux")
    app.setOrganizationName("Flux")
    app.setStyleSheet(FLUENT_THEME)
    
    # Initialize managers
    config_manager = ConfigManager()
    storage_manager = StorageManager()
    bookmarks_manager = BookmarksManager()
    history_manager = HistoryManager()
    downloads_manager = DownloadsManager()
    
    # Create window
    window = BrowserWindow(
        config_manager, storage_manager, bookmarks_manager,
        history_manager, downloads_manager
    )
    
    sys.exit(app.exec())