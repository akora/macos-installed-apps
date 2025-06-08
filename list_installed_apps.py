#!/usr/bin/env python3
import os
import subprocess
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

def get_system_apps():
    """Get list of default macOS applications."""
    system_paths = [
        "/System/Applications",
        "/System/Applications/Utilities"
    ]
    system_apps = set()
    for path in system_paths:
        if os.path.exists(path):
            apps = [f.replace(".app", "") for f in os.listdir(path) if f.endswith(".app")]
            system_apps.update(apps)
    return system_apps

def get_app_category(app_name, path):
    """Categorize applications based on name and path."""
    # Special cases for specific apps
    special_cases = {
        "Google Slides": "Productivity",
        "Google Docs": "Productivity",
        "Google Sheets": "Productivity",
        "Keynote": "Productivity",
        "Pages": "Productivity",
        "Numbers": "Productivity",
        "Obsidian": "Productivity",
        "OnyX": "Utilities",
        "SteerMouse": "Utilities",
        "Tabby": "Development",
        "Ubuntu": "Virtualization",
        # Add your custom app categorizations here
        "Yubico Authenticator": "Security & Privacy",
        "iStat Menus": "Utilities",
        "iStat Menus Helper": "Utilities",
        "iStat Menus Menubar": "Utilities",
        "Scam Copilot": "Security & Privacy",
        "Rectangle Pro": "Utilities",
        "AppCleaner": "Utilities",
        "Bartender 5": "Utilities",
        "ForkLift": "Utilities",
        "Swift Quit": "Utilities"
    }
    
    if app_name in special_cases:
        return special_cases[app_name]
    
    # Check for Ubuntu with version in name (like "vUbuntu")
    if "ubuntu" in app_name.lower():
        return "Virtualization"
    
    categories = {
        "Development": [
            "Visual Studio Code", "Xcode", "Docker", "iTerm", "Python",
            "Developer", "IDE", "Terminal", "Code", "Git"
        ],
        "Browsers & Internet": [
            "Chrome", "Firefox", "Safari", "Opera", "Edge", "Arc", "Browser"
        ],
        "Security & Privacy": [
            "1Password", "Bitwarden", "VPN", "Antivirus", "Bitdefender",
            "Password", "Security", "Radio Silence", "Yubico", "Scam"
        ],
        "Productivity": [
            "Office", "Docs", "Sheets", "Slides", "Notes", "Task",
            "Calendar", "Mail", "Presentation", "Document"
        ],
        "Utilities": [
            "Rectangle", "Bartender", "AppCleaner", "ForkLift",
            "Utility", "Cleaner", "Manager", "Stats", "Monitor",
            "Helper", "Menu"
        ],
        "Media & Creative": [
            "DaVinci", "Luminar", "Screen", "Spotify",
            "Music", "Photo", "Video", "Audio", "Creative", "Media"
        ],
        "Cloud Storage": [
            "Google Drive", "Dropbox", "iCloud", "OneDrive", "Box", "Sync"
        ],
        "Virtualization": [
            "Parallels", "VMware", "VirtualBox", "Virtual", "VM", "Linux",
            "Windows", "Ubuntu"
        ]
    }
    
    app_name_lower = app_name.lower()
    for category, keywords in categories.items():
        if any(keyword.lower() in app_name_lower for keyword in keywords):
            return category
    return "Other"

def get_installed_apps():
    """Get all installed applications using system_profiler."""
    try:
        cmd = ["system_profiler", "SPApplicationsDataType", "-json"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)
        
        apps_info = []
        for app in data.get("SPApplicationsDataType", []):
            app_info = {
                "name": app.get("_name", "Unknown"),
                "path": app.get("path", "Unknown"),
                "version": app.get("version", "Unknown"),
                "obtained_from": app.get("obtained_from", "Unknown"),
                "last_modified": app.get("lastModified", "Unknown")
            }
            apps_info.append(app_info)
        return apps_info
    except Exception as e:
        print(f"Error getting installed apps: {e}")
        return []

def format_source(source):
    """Format the source information more concisely."""
    source_map = {
        "mac_app_store": "App Store",
        "identified_developer": "Verified Dev",
        "unknown": "Unknown",
        "apple": "Apple"
    }
    return source_map.get(source.lower(), source)

def should_include_app(app):
    """Determine if an app should be included in the output."""
    # List of apps to explicitly exclude
    excluded_apps = {
        "GarageBand",  # Pre-installed by Apple
        "iMovie",      # Pre-installed by Apple
        "Keynote",     # Pre-installed by Apple
        "Numbers",     # Pre-installed by Apple
        "Pages"        # Pre-installed by Apple
    }
    
    if app["name"] in excluded_apps:
        return False
    
    # Exclude Apple applications
    if app.get("obtained_from", "").lower() == "apple":
        return False
    
    # Exclude system applications and utilities
    system_prefixes = [
        "/System/Library/",
        "/System/Applications/",
        "/Library/Apple/"
    ]
    app_path = app.get("path", "")
    if any(app_path.startswith(prefix) for prefix in system_prefixes):
        return False
    
    return True

def main():
    print("Analyzing installed applications...")
    
    # Get system (pre-installed) apps
    system_apps = get_system_apps()
    
    # Get all installed apps
    installed_apps = get_installed_apps()
    
    # Categorize non-default applications
    categorized_apps = defaultdict(list)
    for app in installed_apps:
        app_name = app["name"]
        if app_name not in system_apps and should_include_app(app):
            category = get_app_category(app_name, app["path"])
            app_info = {
                "name": app_name,
                "version": app["version"],
                "source": format_source(app["obtained_from"])
            }
            categorized_apps[category].append(app_info)
    
    # Print categorized applications
    print("\nThird-Party Applications by Category:")
    print("=" * 50)
    
    # Only print categories that have apps
    for category, apps in sorted(categorized_apps.items()):
        if apps:
            filtered_apps = [app for app in apps if app["source"] != "Apple"]
            if filtered_apps:
                print(f"\n{category}:")
                print("-" * len(category))
                for app in sorted(filtered_apps, key=lambda x: x["name"]):
                    if app["version"] != "Unknown":
                        print(f"• {app['name']} (v{app['version']}) [{app['source']}]")
                    else:
                        print(f"• {app['name']} [{app['source']}]")

if __name__ == "__main__":
    main()
