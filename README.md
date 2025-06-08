# macOS Installed Applications Analyzer

This Python script analyzes and categorizes all installed applications on your macOS system. It provides a detailed overview of your installed applications, organizing them by categories and including information about their installation sources.

## Features

- Lists all installed applications on your macOS system
- Categorizes applications into meaningful groups (Development, Browsers, Security, etc.)
- Identifies system applications vs. user-installed applications
- Provides details about application sources (App Store, third-party, etc.)
- Exports results in JSON format with timestamp

## Categories

The script categorizes applications into the following groups:

- Development
- Browsers & Internet
- Security & Privacy
- Productivity
- Utilities
- Media & Creative
- Cloud Storage
- Virtualization
- Other

## Requirements

- macOS operating system
- Python 3.x
- System permissions to access application directories

## Usage

1. Clone this repository:

```bash
git clone https://github.com/[your-username]/macos-installed-apps.git
cd macos-installed-apps
```

1. Make the script executable:

```bash
chmod +x list_installed_apps.py
```

1. Run the script:

```bash
./list_installed_apps.py
```

The script will generate a JSON file in the current directory with the format `installed_apps_YYYY-MM-DD.json`, containing the analysis results.

## Output Format

The output JSON file contains:

- Timestamp of the analysis
- List of all applications grouped by category
- Application details including:
  - Name
  - Source (App Store, Third-party, etc.)
  - Installation path
  - Category

## Note

Some applications might be categorized as "Other" if they don't match any predefined category patterns. You can modify the categorization logic in the script by updating the `get_app_category()` function.
