# content_blocker.py
"""
Content Blocker - Ad and Tracker Blocking
Features: Block ads, trackers, pop-ups using filter lists
"""

import re
from pathlib import Path
from PyQt6.QtCore import QUrl, QStandardPaths
from PyQt6.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineUrlRequestInfo


class ContentBlocker(QWebEngineUrlRequestInterceptor):
    """Blocks ads and trackers based on filter lists."""
    
    def __init__(self):
        super().__init__()
        self.enabled = True
        self.block_ads = True
        self.block_trackers = True
        self.blocked_count = 0
        
        # Load filter lists
        self.ad_patterns = self.load_ad_patterns()
        self.tracker_patterns = self.load_tracker_patterns()
    
    def load_ad_patterns(self):
        """Load ad blocking patterns."""
        # Basic ad blocking patterns (simplified EasyList)
        patterns = [
            r'.*ads.*\.js',
            r'.*banner.*',
            r'.*advert.*',
            r'.*\/ads\/.*',
            r'.*doubleclick\.net.*',
            r'.*googlesyndication\.com.*',
            r'.*googleadservices\.com.*',
            r'.*advertising\.com.*',
            r'.*adserver.*',
            r'.*adservice.*',
            r'.*ad-.*',
            r'.*pagead.*',
            r'.*adsbygoogle.*',
        ]
        
        return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    
    def load_tracker_patterns(self):
        """Load tracker blocking patterns."""
        # Basic tracker blocking patterns
        patterns = [
            r'.*google-analytics\.com.*',
            r'.*googletagmanager\.com.*',
            r'.*facebook\.com\/tr\/.*',
            r'.*facebook\.net\/.*',
            r'.*scorecardresearch\.com.*',
            r'.*tracking.*',
            r'.*analytics.*',
            r'.*tracker.*',
            r'.*telemetry.*',
            r'.*metrics.*',
        ]
        
        return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    
    def interceptRequest(self, info: QWebEngineUrlRequestInfo):
        """Intercept and potentially block requests."""
        if not self.enabled:
            return
        
        url = info.requestUrl().toString()
        
        # Check if should block
        should_block = False
        
        if self.block_ads:
            for pattern in self.ad_patterns:
                if pattern.search(url):
                    should_block = True
                    break
        
        if not should_block and self.block_trackers:
            for pattern in self.tracker_patterns:
                if pattern.search(url):
                    should_block = True
                    break
        
        if should_block:
            info.block(True)
            self.blocked_count += 1
    
    def set_enabled(self, enabled):
        """Enable or disable content blocking."""
        self.enabled = enabled
    
    def set_block_ads(self, block):
        """Enable or disable ad blocking."""
        self.block_ads = block
    
    def set_block_trackers(self, block):
        """Enable or disable tracker blocking."""
        self.block_trackers = block
    
    def get_blocked_count(self):
        """Get count of blocked requests."""
        return self.blocked_count
    
    def reset_count(self):
        """Reset blocked count."""
        self.blocked_count = 0