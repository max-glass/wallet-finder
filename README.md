# wallet\_finder

**Recursively search and collect cryptocurrency wallet files and folders.**

---

## Overview

`wallet_finder.py` is a Python 3 script designed to scan specified directories for known cryptocurrency wallet files and folders, and copy any matches into a centralized `Findings` directory. It supports a configurable list of file extensions and folder names, skips files above a configurable maximum size, and handles naming collisions.

## Features

* **Recursive scanning** of one or more root directories
* **Configurable file extensions** and folder names for wallet data
* **Size-based filtering**: skip files larger than a specified threshold (default 100 MB)
* **Collision-safe copying**: append a counter to file/folder names to avoid overwriting
* **Verbose output**: prints each file or folder as it is found and copied
* **Configurable via CLI**: override default roots, target directory, and max file size

## Requirements

* Python 3.6 or higher
* Run on Windows (tested on Windows 10/11)
* Elevated privileges (Administrator) to access hidden/system folders

## Installation

1. Clone or download this repository.
2. Ensure Python 3 is installed and added to your system PATH.

## Usage

1. Open **Command Prompt** as Administrator.
2. Navigate to the script directory:

   ```powershell
   cd C:\path\to\script
   ```
3. Run the script:

   ```powershell
   python wallet_finder.py
   ```

### Command-Line Arguments

| Argument           | Description                                                          | Default                               |
| ------------------ | -------------------------------------------------------------------- | ------------------------------------- |
| `roots`            | One or more root paths to scan (space-separated)                     | `['E:\\']`                            |
| `-t`, `--target`   | Base directory where `Findings` folder will be created and populated | `C:\Users\Max\Projects\wallet-finder` |
| `-m`, `--max-size` | Maximum file size in bytes to copy (files above this are skipped)    | `104857600` (100 MB)                  |

Example:

```powershell
python wallet_finder.py D:\ F:\ --target "C:\Backup\Wallets" --max-size 52428800
```

## Configuration

You can also modify the default settings at the top of `wallet_finder.py`:

* `ROOT_PATHS` – list of drives/folders to scan
* `BASE_TARGET_DIR` – base path for findings
* `MAX_FILE_SIZE` – size threshold in bytes
* `EXTENSIONS` – set of file extensions to detect
* `FOLDER_NAMES` – set of folder names to copy entirely

## Adding New Wallet Formats

1. **File Extensions**: Add additional extensions (e.g. `.seco`, `.keystore`) to the `EXTENSIONS` set.
2. **Directories**: Include new wallet folder names (e.g. `MyCrypto`, `.mycrypto`) in the `FOLDER_NAMES` set.

## Permissions

* For full scanning of hidden and system folders, run the script as **Administrator**.
* If you encounter `PermissionError`, ensure you have the proper rights or exclude protected system paths if desired.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

* Inspired by the need to recover lost or forgotten cryptocurrency wallets from backup drives.
* Supports a wide range of wallet formats and storage conventions.

---

*Happy hunting!*
