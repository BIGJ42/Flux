# Python Browser

A small, local Python-based GUI browser application.
# Python Browser

A small, local Python-based GUI browser application.

Overview
- Lightweight browser app implemented in Python. The project includes window/dialog modules, a content blocker, download manager, bookmarks and history managers, and a PyInstaller spec for packaging (`PythonBrowser.spec`).

Releases (GitHub)
- This repository publishes built binaries and installers in the GitHub Releases page. If you prefer a quick install, download the appropriate release asset for your platform from the Releases tab on GitHub.
- Recommended steps when using releases:
  - Download the installer or archive that matches your OS/architecture.
  - Verify the SHA256 checksum if a checksum file is provided.
  - On Windows, run the provided installer or `.exe` and follow the installer prompts.

Quickstart
- Option A — Install from Releases (recommended for most users):

  1. Open the repository on GitHub and go to the `Releases` tab.
  2. Download the installer or executable for your platform.
  3. Run the installer or unpack the archive and launch the included executable.

- Option B — Run from source (developer / advanced users)

  1. Ensure you have Python 3.8+ installed.
  2. From PowerShell:

```powershell
cd "c:\Users\joshu\Documents\browser"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pyqt5 pyqtwebengine
python browser.py
```

- The output will be in the `dist` folder (or wherever the spec declares). The workspace may also contain a `build\PythonBrowser` folder from a previous build.

Project layout (key files)
- `browser.py`: Main application entry and UI initialization.
- `bookmarks_manager.py`: Manages saving/loading bookmarks and bookmark UI.
- `history_manager.py`: Tracks visited pages and persistence of history.
- `config_manager.py`: Reads/writes application configuration and preferences.
- `content_blocker.py`: Implements content/blocking rules and filters.
- `downloads_manager.py`: Handles downloads (queueing, saving files).
- `find_dialog.py`: Find-in-page dialog implementation.
- `settings_dialog.py`: Settings/preferences UI.

Configuration and data files
- Check `config_manager.py` for where config and data (bookmarks/history) are stored. Typical locations are the application folder or the user's AppData directory on Windows.

Contributing
- If you want to contribute:
  - Fork the repo and create a feature branch.
  - Run the app locally and add tests where appropriate.
  - Open a pull request with a concise description of changes.

Notes & Next steps
- Add a `requirements.txt` or `pyproject.toml` with pinned dependency versions for reproducibility.
- Add a `LICENSE` file (e.g., MIT) if you plan to open-source the project.
- If packaging for distribution, consider bundling the appropriate Qt runtime for the chosen GUI toolkit.

Contact
- For questions about running or packaging the app, inspect the top-level `browser.py` for required imports and reach out to the repository owner.
