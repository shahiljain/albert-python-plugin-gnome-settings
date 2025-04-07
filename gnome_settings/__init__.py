# -*- coding: utf-8 -*-
"""
Access GNOME Settings pages quickly from Albert.
Usage examples:
- `gs` to see all available settings pages
- `gs display` to access display settings
- `gs network` to access network settings
- `gs privacy` to access privacy settings
"""
import re
import subprocess
from typing import List, Dict
from pathlib import Path
from albert import *

md_iid = "3.0"
md_version = "1.0"
md_name = "Gnome Settings"
md_description = "Quick access to Gnome system settings pages"
md_license = "GPL V3.0"
md_url = "https://github.com/shahiljain/albert-python-plugin-gnome-settings"
md_authors = ["Shahil Jain"]

class Plugin(PluginInstance, GlobalQueryHandler):
    """Plugin for accessing GNOME Settings pages"""

    def __init__(self):
        PluginInstance.__init__(self)
        GlobalQueryHandler.__init__(self)
        self.settings_pages = {
            "wifi": {
                "title": "Wi-Fi",
                "description": "Configure wireless networks",
                "command": ["gnome-control-center", "wifi"]
            },
            "network": {
                "title": "Network",
                "description": "Configure network connections",
                "command": ["gnome-control-center", "network"]
            },
            "bluetooth": {
                "title": "Bluetooth",
                "description": "Configure Bluetooth devices",
                "command": ["gnome-control-center", "bluetooth"]
            },
            "display": {
                "title": "Displays",
                "description": "Configure monitors and displays",
                "command": ["gnome-control-center", "display"]
            },
            "sound": {
                "title": "Sound",
                "description": "Configure audio devices and volume",
                "command": ["gnome-control-center", "sound"]
            },
            "power": {
                "title": "Power",
                "description": "Configure power saving options",
                "command": ["gnome-control-center", "power"]
            },
            "multitasking": {
                "title": "Multitasking",
                "description": "Multitasking gestures and prefrences",
                "command": ["gnome-control-center", "multitasking"]
            },
            "appearance": {
                "title": "Appearance",
                "description": "Configure system theme and appearance",
                "command": ["gnome-control-center", "appearance"]
            },
            "applications": {
                "title": "Applications",
                "description": "Manage installed applications",
                "command": ["gnome-control-center", "applications"]
            },
            "notifications": {
                "title": "Notifications",
                "description": "Configure system notifications",
                "command": ["gnome-control-center", "notifications"]
            },
            "online-accounts": {
                "title": "Online Accounts",
                "description": "Configure online service accounts",
                "command": ["gnome-control-center", "online-accounts"]
            },
            "sharing": {
                "title": "Sharing",
                "description": "Configure file and media sharing",
                "command": ["gnome-control-center", "sharing"]
            },
            "mouse": {
                "title": "Mouse & Touchpad",
                "description": "Configure pointing devices",
                "command": ["gnome-control-center", "mouse"]
            },
            "keyboard": {
                "title": "Keyboard",
                "description": "Configure keyboard shortcuts and behavior",
                "command": ["gnome-control-center", "keyboard"]
            },
            "color": {
                "title": "Color",
                "description": "Adjust the Display Color Settings",
                "command": ["gnome-control-center", "color"]
            },
            "printers": {
                "title": "Printers",
                "description": "Configure printers",
                "command": ["gnome-control-center", "printers"]
            },
            "accessibility": {
                "title": "Accessibility",
                "description": "Configure accessibility options",
                "command": ["gnome-control-center", "universal-access"]
            },
            "privacy": {
                "title": "Privacy & Security",
                "description": "Configure privacy and security options",
                "command": ["gnome-control-center", "privacy"]
            },
            "system": {
                "title": "System Settings",
                "description": "View system settings and information",
                "command": ["gnome-control-center", "system"]
            },
            "region": {
                "title": "Region & Language",
                "description": "Configure locale and language",
                "command": ["gnome-control-center", "region"]
            },
            "datetime": {
                "title": "Date & Time",
                "description": "Configure system clock and timezone",
                "command": ["gnome-control-center", "datetime"]
            },
            "users": {
                "title": "Users",
                "description": "Manage user accounts",
                "command": ["gnome-control-center", "users"]
            },
            "about":{
                "title": "About",
                "description": "System Software and Hardware details",
                "command": ["gnome-control-center", "about"]
            }
        }
        self.icon_path = str(Path(__file__).parent / "settings.svg")
        # Create a pattern that matches complete words only
        self.match_pattern = r"^\s*(?P<query>\w+)\s*$"
        self.word_match = re.compile(self.match_pattern)

    def defaultTrigger(self):
        return "gs "

    def synopsis(self, query):
        return "<settings-page>"

    def handleTriggerQuery(self, query: Query) -> None:
        """Handle triggered queries"""
        query_string = query.string.strip().lower()
        items = self._get_matching_items(query_string)
        query.add(items)

    def handleGlobalQuery(self, query: Query) -> List[RankItem]:
        """Handle global queries with strict matching"""
        query_string = query.string.strip().lower()
        
        # Only match complete words to avoid triggering on every 2-letter combination
        if not self.word_match.match(query_string):
            return []
            
        # Check if the query exactly matches our keywords
        if query_string in self.settings_pages:
            items = [self._create_item_for_page(query_string)]
            return [RankItem(item=item, score=100) for item in items]
        
        return []

    def _get_matching_items(self, query_string: str) -> List[Item]:
        """Get settings pages matching the query string"""
        if not query_string:
            # Show all settings pages if no query
            return [self._create_item_for_page(page_id) for page_id in self.settings_pages]
        
        matching_items = []
        for page_id, page_info in self.settings_pages.items():
            if (query_string in page_id or
                query_string in page_info["title"].lower() or
                query_string in page_info["description"].lower()):
                matching_items.append(self._create_item_for_page(page_id))
        
        return matching_items

    def _create_item_for_page(self, page_id: str) -> Item:
        """Create an item for a settings page"""
        page_info = self.settings_pages[page_id]
        
        return StandardItem(
            id=f"settings:{page_id}",
            text=page_info["title"],
            subtext=page_info["description"],
            iconUrls=["file:" + self.icon_path],
            actions=[
                Action(
                    id=f"open:{page_id}",
                    text=f"Open {page_info['title']}",
                    callable=lambda cmd=page_info["command"]: subprocess.Popen(cmd)
                )
            ]
        )
