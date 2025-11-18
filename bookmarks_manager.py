# bookmarks_manager.py
"""
Complete Bookmarks Management System
Features: Add, edit, delete, folders, import/export, search
"""

import json
import os
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QLineEdit, QMenu, QMessageBox, QInputDialog,
    QLabel, QToolBar, QWidget, QSplitter, QTextEdit, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, QUrl, QStandardPaths
from PyQt6.QtGui import QIcon, QAction, QCursor
from PyQt6.QtWebEngineCore import QWebEngineSettings

try:
    import qtawesome as qta
    HAS_ICONS = True
except ImportError:
    HAS_ICONS = False


class BookmarksManager:
    """Manages browser bookmarks with JSON storage."""
    
    def __init__(self):
        """Initialize bookmarks manager."""
        self.bookmarks_file = self.get_bookmarks_path()
        self.bookmarks = self.load_bookmarks()
    
    @staticmethod
    def get_bookmarks_path():
        """Get bookmarks file path."""
        app_data = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        bookmarks_dir = Path(app_data) / "Flux"
        bookmarks_dir.mkdir(parents=True, exist_ok=True)
        return bookmarks_dir / "bookmarks.json"
    
    def load_bookmarks(self):
        """Load bookmarks from file."""
        if self.bookmarks_file.exists():
            try:
                with open(self.bookmarks_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading bookmarks: {e}")
                return self.get_default_structure()
        else:
            return self.get_default_structure()
    
    def get_default_structure(self):
        """Get default bookmarks structure."""
        return {
            "bookmarks_bar": [],
            "other_bookmarks": [],
            "folders": {}
        }
    
    def save_bookmarks(self):
        """Save bookmarks to file."""
        try:
            with open(self.bookmarks_file, 'w', encoding='utf-8') as f:
                json.dump(self.bookmarks, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving bookmarks: {e}")
    
    def add_bookmark(self, url, title, folder="other_bookmarks"):
        """Add a bookmark."""
        bookmark = {
            "url": url,
            "title": title,
            "date_added": datetime.now().isoformat(),
            "id": self.generate_id()
        }
        
        if folder in self.bookmarks:
            self.bookmarks[folder].append(bookmark)
        elif folder in self.bookmarks.get("folders", {}):
            self.bookmarks["folders"][folder].append(bookmark)
        else:
            self.bookmarks["other_bookmarks"].append(bookmark)
        
        self.save_bookmarks()
        return bookmark
    
    def remove_bookmark(self, bookmark_id, folder=None):
        """Remove a bookmark by ID."""
        # Search in all locations
        locations = ["bookmarks_bar", "other_bookmarks"]
        locations.extend(self.bookmarks.get("folders", {}).keys())
        
        for loc in locations:
            if folder and loc != folder:
                continue
                
            if loc in ["bookmarks_bar", "other_bookmarks"]:
                items = self.bookmarks[loc]
            else:
                items = self.bookmarks["folders"].get(loc, [])
            
            for i, bookmark in enumerate(items):
                if bookmark.get("id") == bookmark_id:
                    items.pop(i)
                    self.save_bookmarks()
                    return True
        
        return False
    
    def create_folder(self, folder_name):
        """Create a new bookmark folder."""
        if "folders" not in self.bookmarks:
            self.bookmarks["folders"] = {}
        
        if folder_name not in self.bookmarks["folders"]:
            self.bookmarks["folders"][folder_name] = []
            self.save_bookmarks()
            return True
        return False
    
    def is_bookmarked(self, url):
        """Check if URL is bookmarked."""
        url_str = url if isinstance(url, str) else url.toString()
        
        # Check all locations
        for bookmarks in [
            self.bookmarks.get("bookmarks_bar", []),
            self.bookmarks.get("other_bookmarks", [])
        ]:
            for bookmark in bookmarks:
                if bookmark.get("url") == url_str:
                    return True
        
        # Check folders
        for folder_bookmarks in self.bookmarks.get("folders", {}).values():
            for bookmark in folder_bookmarks:
                if bookmark.get("url") == url_str:
                    return True
        
        return False
    
    def get_bookmark_by_url(self, url):
        """Get bookmark by URL."""
        url_str = url if isinstance(url, str) else url.toString()
        
        # Search all locations
        for location in ["bookmarks_bar", "other_bookmarks"]:
            for bookmark in self.bookmarks.get(location, []):
                if bookmark.get("url") == url_str:
                    return bookmark, location
        
        for folder_name, folder_bookmarks in self.bookmarks.get("folders", {}).items():
            for bookmark in folder_bookmarks:
                if bookmark.get("url") == url_str:
                    return bookmark, folder_name
        
        return None, None
    
    def search_bookmarks(self, query):
        """Search bookmarks by title or URL."""
        results = []
        query_lower = query.lower()
        
        # Search all locations
        for location in ["bookmarks_bar", "other_bookmarks"]:
            for bookmark in self.bookmarks.get(location, []):
                if (query_lower in bookmark.get("title", "").lower() or
                    query_lower in bookmark.get("url", "").lower()):
                    results.append((bookmark, location))
        
        for folder_name, folder_bookmarks in self.bookmarks.get("folders", {}).items():
            for bookmark in folder_bookmarks:
                if (query_lower in bookmark.get("title", "").lower() or
                    query_lower in bookmark.get("url", "").lower()):
                    results.append((bookmark, folder_name))
        
        return results
    
    def generate_id(self):
        """Generate unique bookmark ID."""
        import time
        return str(int(time.time() * 1000000))
    
    def export_bookmarks(self, filepath):
        """Export bookmarks to HTML file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('<!DOCTYPE NETSCAPE-Bookmark-file-1>\n')
                f.write('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n')
                f.write('<TITLE>Bookmarks</TITLE>\n')
                f.write('<H1>Bookmarks</H1>\n')
                f.write('<DL><p>\n')
                
                # Bookmarks bar
                if self.bookmarks.get("bookmarks_bar"):
                    f.write('    <DT><H3>Bookmarks Bar</H3>\n')
                    f.write('    <DL><p>\n')
                    for bookmark in self.bookmarks["bookmarks_bar"]:
                        f.write(f'        <DT><A HREF="{bookmark["url"]}">{bookmark["title"]}</A>\n')
                    f.write('    </DL><p>\n')
                
                # Other bookmarks
                if self.bookmarks.get("other_bookmarks"):
                    f.write('    <DT><H3>Other Bookmarks</H3>\n')
                    f.write('    <DL><p>\n')
                    for bookmark in self.bookmarks["other_bookmarks"]:
                        f.write(f'        <DT><A HREF="{bookmark["url"]}">{bookmark["title"]}</A>\n')
                    f.write('    </DL><p>\n')
                
                # Folders
                for folder_name, folder_bookmarks in self.bookmarks.get("folders", {}).items():
                    f.write(f'    <DT><H3>{folder_name}</H3>\n')
                    f.write('    <DL><p>\n')
                    for bookmark in folder_bookmarks:
                        f.write(f'        <DT><A HREF="{bookmark["url"]}">{bookmark["title"]}</A>\n')
                    f.write('    </DL><p>\n')
                
                f.write('</DL><p>\n')
            
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False


class BookmarksDialog(QDialog):
    """Bookmarks manager dialog."""
    
    bookmark_activated = pyqtSignal(str)  # URL
    
    def __init__(self, bookmarks_manager, parent=None):
        super().__init__(parent)
        self.bookmarks_manager = bookmarks_manager
        self.setWindowTitle("Bookmarks Manager")
        self.setMinimumSize(800, 600)
        self.init_ui()
        self.load_bookmarks_tree()
    
    def init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(False)
        
        if HAS_ICONS:
            add_action = toolbar.addAction(qta.icon('fa5s.plus'), "Add Bookmark")
            folder_action = toolbar.addAction(qta.icon('fa5s.folder-plus'), "New Folder")
            delete_action = toolbar.addAction(qta.icon('fa5s.trash'), "Delete")
            toolbar.addSeparator()
            import_action = toolbar.addAction(qta.icon('fa5s.file-import'), "Import")
            export_action = toolbar.addAction(qta.icon('fa5s.file-export'), "Export")
        else:
            add_action = toolbar.addAction("Add")
            folder_action = toolbar.addAction("New Folder")
            delete_action = toolbar.addAction("Delete")
            toolbar.addSeparator()
            import_action = toolbar.addAction("Import")
            export_action = toolbar.addAction("Export")
        
        add_action.triggered.connect(self.add_bookmark)
        folder_action.triggered.connect(self.add_folder)
        delete_action.triggered.connect(self.delete_selected)
        import_action.triggered.connect(self.import_bookmarks)
        export_action.triggered.connect(self.export_bookmarks)
        
        layout.addWidget(toolbar)
        
        # Search bar
        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(8, 8, 8, 8)
        
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search bookmarks...")
        self.search_input.textChanged.connect(self.filter_bookmarks)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        
        layout.addWidget(search_widget)
        
        # Bookmarks tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Title", "URL", "Date Added"])
        self.tree.setColumnWidth(0, 300)
        self.tree.setColumnWidth(1, 350)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        self.tree.itemDoubleClicked.connect(self.open_bookmark)
        
        layout.addWidget(self.tree)
        
        # Button bar
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
    
    def load_bookmarks_tree(self):
        """Load bookmarks into tree."""
        self.tree.clear()
        bookmarks = self.bookmarks_manager.bookmarks
        
        # Bookmarks bar
        if bookmarks.get("bookmarks_bar"):
            bar_item = QTreeWidgetItem(self.tree, ["Bookmarks Bar", "", ""])
            bar_item.setData(0, Qt.ItemDataRole.UserRole, "bookmarks_bar")
            if HAS_ICONS:
                bar_item.setIcon(0, qta.icon('fa5s.star'))
            
            for bookmark in bookmarks["bookmarks_bar"]:
                self.add_bookmark_item(bar_item, bookmark, "bookmarks_bar")
            
            bar_item.setExpanded(True)
        
        # Other bookmarks
        if bookmarks.get("other_bookmarks"):
            other_item = QTreeWidgetItem(self.tree, ["Other Bookmarks", "", ""])
            other_item.setData(0, Qt.ItemDataRole.UserRole, "other_bookmarks")
            if HAS_ICONS:
                other_item.setIcon(0, qta.icon('fa5s.bookmark'))
            
            for bookmark in bookmarks["other_bookmarks"]:
                self.add_bookmark_item(other_item, bookmark, "other_bookmarks")
            
            other_item.setExpanded(True)
        
        # Folders
        for folder_name, folder_bookmarks in bookmarks.get("folders", {}).items():
            folder_item = QTreeWidgetItem(self.tree, [folder_name, "", ""])
            folder_item.setData(0, Qt.ItemDataRole.UserRole, f"folder:{folder_name}")
            if HAS_ICONS:
                folder_item.setIcon(0, qta.icon('fa5s.folder'))
            
            for bookmark in folder_bookmarks:
                self.add_bookmark_item(folder_item, bookmark, folder_name)
            
            folder_item.setExpanded(True)
    
    def add_bookmark_item(self, parent, bookmark, location):
        """Add bookmark to tree."""
        date_str = bookmark.get("date_added", "")
        if date_str:
            try:
                date_obj = datetime.fromisoformat(date_str)
                date_str = date_obj.strftime("%Y-%m-%d %H:%M")
            except:
                pass
        
        item = QTreeWidgetItem(parent, [
            bookmark.get("title", "Untitled"),
            bookmark.get("url", ""),
            date_str
        ])
        item.setData(0, Qt.ItemDataRole.UserRole, bookmark.get("id"))
        item.setData(1, Qt.ItemDataRole.UserRole, location)
        
        if HAS_ICONS:
            item.setIcon(0, qta.icon('fa5s.link'))
        
        return item
    
    def filter_bookmarks(self, query):
        """Filter bookmarks by search query."""
        if not query:
            # Show all
            for i in range(self.tree.topLevelItemCount()):
                item = self.tree.topLevelItem(i)
                self.show_item_recursive(item, True)
        else:
            # Hide non-matching
            query_lower = query.lower()
            for i in range(self.tree.topLevelItemCount()):
                item = self.tree.topLevelItem(i)
                self.filter_item_recursive(item, query_lower)
    
    def filter_item_recursive(self, item, query):
        """Recursively filter items."""
        has_visible_child = False
        
        for i in range(item.childCount()):
            child = item.child(i)
            child_visible = self.filter_item_recursive(child, query)
            has_visible_child = has_visible_child or child_visible
        
        # Check if this item matches
        title = item.text(0).lower()
        url = item.text(1).lower()
        matches = query in title or query in url
        
        visible = matches or has_visible_child
        item.setHidden(not visible)
        
        return visible
    
    def show_item_recursive(self, item, visible):
        """Recursively show/hide items."""
        item.setHidden(not visible)
        for i in range(item.childCount()):
            self.show_item_recursive(item.child(i), visible)
    
    def show_context_menu(self, pos):
        """Show context menu."""
        item = self.tree.itemAt(pos)
        if not item:
            return
        
        menu = QMenu(self)
        
        # Check if it's a bookmark or folder
        bookmark_id = item.data(0, Qt.ItemDataRole.UserRole)
        
        if item.childCount() == 0 and item.text(1):  # It's a bookmark
            if HAS_ICONS:
                open_action = menu.addAction(qta.icon('fa5s.external-link-alt'), "Open")
                open_new_action = menu.addAction(qta.icon('fa5s.window-maximize'), "Open in New Tab")
                menu.addSeparator()
                edit_action = menu.addAction(qta.icon('fa5s.edit'), "Edit")
                delete_action = menu.addAction(qta.icon('fa5s.trash'), "Delete")
            else:
                open_action = menu.addAction("Open")
                open_new_action = menu.addAction("Open in New Tab")
                menu.addSeparator()
                edit_action = menu.addAction("Edit")
                delete_action = menu.addAction("Delete")
            
            open_action.triggered.connect(lambda: self.open_bookmark(item))
            open_new_action.triggered.connect(lambda: self.open_bookmark(item, new_tab=True))
            edit_action.triggered.connect(lambda: self.edit_bookmark(item))
            delete_action.triggered.connect(lambda: self.delete_bookmark(item))
        else:  # It's a folder
            if HAS_ICONS:
                delete_action = menu.addAction(qta.icon('fa5s.trash'), "Delete Folder")
            else:
                delete_action = menu.addAction("Delete Folder")
            
            delete_action.triggered.connect(lambda: self.delete_folder(item))
        
        menu.exec(QCursor.pos())
    
    def open_bookmark(self, item, column=0, new_tab=False):
        """Open selected bookmark."""
        if item.childCount() > 0:  # It's a folder
            return
        
        url = item.text(1)
        if url:
            self.bookmark_activated.emit(url)
            if not new_tab:
                self.accept()
    
    def add_bookmark(self):
        """Add new bookmark manually."""
        title, ok1 = QInputDialog.getText(self, "Add Bookmark", "Title:")
        if not ok1 or not title:
            return
        
        url, ok2 = QInputDialog.getText(self, "Add Bookmark", "URL:")
        if not ok2 or not url:
            return
        
        self.bookmarks_manager.add_bookmark(url, title)
        self.load_bookmarks_tree()
    
    def add_folder(self):
        """Add new folder."""
        folder_name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
        if ok and folder_name:
            if self.bookmarks_manager.create_folder(folder_name):
                self.load_bookmarks_tree()
            else:
                QMessageBox.warning(self, "Error", "Folder already exists!")
    
    def edit_bookmark(self, item):
        """Edit bookmark."""
        old_title = item.text(0)
        old_url = item.text(1)
        
        title, ok1 = QInputDialog.getText(self, "Edit Bookmark", "Title:", text=old_title)
        if not ok1:
            return
        
        url, ok2 = QInputDialog.getText(self, "Edit Bookmark", "URL:", text=old_url)
        if not ok2:
            return
        
        # Update bookmark
        bookmark_id = item.data(0, Qt.ItemDataRole.UserRole)
        location = item.data(1, Qt.ItemDataRole.UserRole)
        
        # Find and update
        if location in ["bookmarks_bar", "other_bookmarks"]:
            bookmarks_list = self.bookmarks_manager.bookmarks[location]
        else:
            bookmarks_list = self.bookmarks_manager.bookmarks["folders"].get(location, [])
        
        for bookmark in bookmarks_list:
            if bookmark.get("id") == bookmark_id:
                bookmark["title"] = title
                bookmark["url"] = url
                break
        
        self.bookmarks_manager.save_bookmarks()
        self.load_bookmarks_tree()
    
    def delete_bookmark(self, item):
        """Delete bookmark."""
        reply = QMessageBox.question(
            self, "Delete Bookmark",
            f"Delete bookmark '{item.text(0)}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            bookmark_id = item.data(0, Qt.ItemDataRole.UserRole)
            location = item.data(1, Qt.ItemDataRole.UserRole)
            self.bookmarks_manager.remove_bookmark(bookmark_id, location)
            self.load_bookmarks_tree()
    
    def delete_folder(self, item):
        """Delete folder."""
        folder_data = item.data(0, Qt.ItemDataRole.UserRole)
        
        if folder_data.startswith("folder:"):
            folder_name = folder_data.replace("folder:", "")
            
            reply = QMessageBox.question(
                self, "Delete Folder",
                f"Delete folder '{folder_name}' and all its bookmarks?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                if folder_name in self.bookmarks_manager.bookmarks.get("folders", {}):
                    del self.bookmarks_manager.bookmarks["folders"][folder_name]
                    self.bookmarks_manager.save_bookmarks()
                    self.load_bookmarks_tree()
    
    def delete_selected(self):
        """Delete selected item."""
        item = self.tree.currentItem()
        if not item:
            return
        
        if item.childCount() > 0:
            self.delete_folder(item)
        else:
            self.delete_bookmark(item)
    
    def import_bookmarks(self):
        """Import bookmarks from HTML file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Import Bookmarks", "", "HTML Files (*.html);;All Files (*)"
        )
        
        if filepath:
            # TODO: Implement HTML parsing
            QMessageBox.information(
                self, "Import",
                "Import feature will be available in the next update!"
            )
    
    def export_bookmarks(self):
        """Export bookmarks to HTML file."""
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Export Bookmarks", "bookmarks.html", "HTML Files (*.html)"
        )
        
        if filepath:
            if self.bookmarks_manager.export_bookmarks(filepath):
                QMessageBox.information(self, "Export", "Bookmarks exported successfully!")
            else:
                QMessageBox.warning(self, "Export", "Failed to export bookmarks!")  