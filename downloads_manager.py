# downloads_manager.py
"""
Complete Downloads Management System
Features: Track downloads, progress, pause/resume, history
"""

import os
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QWidget,
    QPushButton, QProgressBar, QLabel, QHeaderView, QMenu, QFileDialog,
    QMessageBox, QToolBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QUrl, QStandardPaths, QTimer
from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest
from PyQt6.QtGui import QCursor, QDesktopServices

try:
    import qtawesome as qta
    HAS_ICONS = True
except ImportError:
    HAS_ICONS = False


class DownloadItem:
    """Represents a single download."""
    
    def __init__(self, download_request):
        self.download_request = download_request
        self.url = download_request.url().toString()
        self.filename = download_request.suggestedFileName()
        self.path = ""
        self.total_bytes = download_request.totalBytes()
        self.received_bytes = 0
        self.state = "starting"
        self.start_time = datetime.now()
        self.speed = 0
        
        # Connect signals
        download_request.receivedBytesChanged.connect(self.update_progress)
        download_request.stateChanged.connect(self.state_changed)
    
    def update_progress(self):
        """Update download progress."""
        self.received_bytes = self.download_request.receivedBytes()
        self.total_bytes = self.download_request.totalBytes()
        
        # Calculate speed
        elapsed = (datetime.now() - self.start_time).total_seconds()
        if elapsed > 0:
            self.speed = self.received_bytes / elapsed
    
    def state_changed(self, state):
        """Handle state changes."""
        if state == QWebEngineDownloadRequest.DownloadState.DownloadCompleted:
            self.state = "completed"
        elif state == QWebEngineDownloadRequest.DownloadState.DownloadCancelled:
            self.state = "cancelled"
        elif state == QWebEngineDownloadRequest.DownloadState.DownloadInProgress:
            self.state = "downloading"
        elif state == QWebEngineDownloadRequest.DownloadState.DownloadInterrupted:
            self.state = "interrupted"
    
    def pause(self):
        """Pause download."""
        self.download_request.pause()
        self.state = "paused"
    
    def resume(self):
        """Resume download."""
        self.download_request.resume()
        self.state = "downloading"
    
    def cancel(self):
        """Cancel download."""
        self.download_request.cancel()
        self.state = "cancelled"
    
    def get_progress_percent(self):
        """Get progress percentage."""
        if self.total_bytes > 0:
            return int((self.received_bytes / self.total_bytes) * 100)
        return 0
    
    def get_speed_text(self):
        """Get human-readable speed."""
        return self.format_bytes(self.speed) + "/s"
    
    @staticmethod
    def format_bytes(bytes_value):
        """Format bytes to human-readable size."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"


class DownloadsManager:
    """Manages browser downloads."""
    
    def __init__(self):
        self.downloads = []
        self.download_path = self.get_default_download_path()
    
    @staticmethod
    def get_default_download_path():
        """Get default download directory."""
        return QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DownloadLocation
        )
    
    def add_download(self, download_request):
        """Add a new download."""
        download_item = DownloadItem(download_request)
        self.downloads.append(download_item)
        return download_item
    
    def get_active_downloads(self):
        """Get list of active downloads."""
        return [d for d in self.downloads if d.state in ["downloading", "starting", "paused"]]
    
    def get_completed_downloads(self):
        """Get list of completed downloads."""
        return [d for d in self.downloads if d.state == "completed"]
    
    def clear_completed(self):
        """Clear completed downloads from list."""
        self.downloads = [d for d in self.downloads if d.state != "completed"]


class DownloadsDialog(QDialog):
    """Downloads manager dialog."""
    
    def __init__(self, downloads_manager, parent=None):
        super().__init__(parent)
        self.downloads_manager = downloads_manager
        self.setWindowTitle("Downloads")
        self.setMinimumSize(800, 500)
        self.init_ui()
        
        # Update timer
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_downloads)
        self.update_timer.start(500)  # Update every 500ms
    
    def init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(False)
        
        if HAS_ICONS:
            refresh_action = toolbar.addAction(qta.icon('fa5s.sync'), "Refresh")
            open_folder_action = toolbar.addAction(qta.icon('fa5s.folder-open'), "Open Downloads Folder")
            clear_action = toolbar.addAction(qta.icon('fa5s.broom'), "Clear Completed")
        else:
            refresh_action = toolbar.addAction("Refresh")
            open_folder_action = toolbar.addAction("Open Folder")
            clear_action = toolbar.addAction("Clear Completed")
        
        refresh_action.triggered.connect(self.update_downloads)
        open_folder_action.triggered.connect(self.open_downloads_folder)
        clear_action.triggered.connect(self.clear_completed)
        
        layout.addWidget(toolbar)
        
        # Downloads table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["File", "Status", "Size", "Progress", "Speed", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 150)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        
        layout.addWidget(self.table)
        
        # Stats label
        self.stats_label = QLabel()
        layout.addWidget(self.stats_label)
        
        # Button bar
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        
        # Initial update
        self.update_downloads()
    
    def update_downloads(self):
        """Update downloads table."""
        downloads = self.downloads_manager.downloads
        self.table.setRowCount(len(downloads))
        
        for i, download in enumerate(downloads):
            # Filename
            filename_item = QTableWidgetItem(download.filename)
            self.table.setItem(i, 0, filename_item)
            
            # Status
            status_item = QTableWidgetItem(download.state.capitalize())
            self.table.setItem(i, 1, status_item)
            
            # Size
            if download.total_bytes > 0:
                size_text = f"{DownloadItem.format_bytes(download.received_bytes)} / {DownloadItem.format_bytes(download.total_bytes)}"
            else:
                size_text = DownloadItem.format_bytes(download.received_bytes)
            size_item = QTableWidgetItem(size_text)
            self.table.setItem(i, 2, size_item)
            
            # Progress bar
            progress_widget = QWidget()
            progress_layout = QVBoxLayout(progress_widget)
            progress_layout.setContentsMargins(4, 4, 4, 4)
            
            progress_bar = QProgressBar()
            progress_bar.setValue(download.get_progress_percent())
            progress_layout.addWidget(progress_bar)
            
            self.table.setCellWidget(i, 3, progress_widget)
            
            # Speed
            if download.state == "downloading":
                speed_text = download.get_speed_text()
            else:
                speed_text = "-"
            speed_item = QTableWidgetItem(speed_text)
            self.table.setItem(i, 4, speed_item)
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 4, 4, 4)
            actions_layout.setSpacing(4)
            
            if download.state == "downloading":
                pause_btn = QPushButton("Pause")
                pause_btn.clicked.connect(lambda checked, d=download: d.pause())
                actions_layout.addWidget(pause_btn)
                
                cancel_btn = QPushButton("Cancel")
                cancel_btn.clicked.connect(lambda checked, d=download: d.cancel())
                actions_layout.addWidget(cancel_btn)
            
            elif download.state == "paused":
                resume_btn = QPushButton("Resume")
                resume_btn.clicked.connect(lambda checked, d=download: d.resume())
                actions_layout.addWidget(resume_btn)
                
                cancel_btn = QPushButton("Cancel")
                cancel_btn.clicked.connect(lambda checked, d=download: d.cancel())
                actions_layout.addWidget(cancel_btn)
            
            elif download.state == "completed":
                open_btn = QPushButton("Open")
                open_btn.clicked.connect(lambda checked, d=download: self.open_file(d))
                actions_layout.addWidget(open_btn)
                
                show_btn = QPushButton("Show in Folder")
                show_btn.clicked.connect(lambda checked, d=download: self.show_in_folder(d))
                actions_layout.addWidget(show_btn)
            
            self.table.setCellWidget(i, 5, actions_widget)
        
        # Update stats
        active = len(self.downloads_manager.get_active_downloads())
        completed = len(self.downloads_manager.get_completed_downloads())
        self.stats_label.setText(f"Active: {active} | Completed: {completed} | Total: {len(downloads)}")
    
    def show_context_menu(self, pos):
        """Show context menu."""
        row = self.table.rowAt(pos.y())
        if row < 0:
            return
        
        download = self.downloads_manager.downloads[row]
        menu = QMenu(self)
        
        if download.state == "completed":
            if HAS_ICONS:
                open_action = menu.addAction(qta.icon('fa5s.folder-open'), "Open File")
                show_action = menu.addAction(qta.icon('fa5s.search'), "Show in Folder")
            else:
                open_action = menu.addAction("Open File")
                show_action = menu.addAction("Show in Folder")
            
            open_action.triggered.connect(lambda: self.open_file(download))
            show_action.triggered.connect(lambda: self.show_in_folder(download))
        
        menu.exec(QCursor.pos())
    
    def open_file(self, download):
        """Open downloaded file."""
        if download.path and os.path.exists(download.path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(download.path))
        else:
            QMessageBox.warning(self, "Error", "File not found!")
    
    def show_in_folder(self, download):
        """Show file in folder."""
        if download.path and os.path.exists(download.path):
            folder_path = os.path.dirname(download.path)
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))
        else:
            QMessageBox.warning(self, "Error", "File not found!")
    
    def open_downloads_folder(self):
        """Open downloads folder."""
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.downloads_manager.download_path))
    
    def clear_completed(self):
        """Clear completed downloads."""
        self.downloads_manager.clear_completed()
        self.update_downloads()
    
    def closeEvent(self, event):
        """Handle dialog close."""
        self.update_timer.stop()
        super().closeEvent(event)