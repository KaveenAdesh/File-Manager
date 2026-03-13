A lightweight, terminal-based file management system designed for high-efficiency navigation and file operations on Windows environments. This tool provides a clear, visual representation of drive usage and file structures with built-in support for multi-target operations.

## 🚀 Key Features
* **Drive Intelligence**: Automatically scans and displays all active drives with real-time usage percentages and visual health bars.
* **Multi-Target Support**: Copy, delete, or create multiple files and folders simultaneously using comma-separated inputs.
* **Visual Icons**: Context-aware rendering of icons based on file extensions (Documents, Media, Executables, etc.).
* **Robust Metadata Handling**: Uses `shutil.copy2` to preserve file metadata during copy/paste operations.
* **Path Resilience**: Built-in protection against non-existent paths and input type errors.

## 🛠️ Commands
Navigate and manipulate your file system using the following command structure:

| Command | Action |
| :--- | :--- |
| `name` | Open a specific file or folder |
| `copy <name/s>` | Copy items to the clipboard (use `,` for multiple) |
| `paste` | Deploy copied items to the current location |
| `clear copy` | Wipe the current clipboard |
| `delete <name>` | Neutralize files or folders |
| `new <name>` | Create new empty files |
| `new folder <name>` | Establish new directories |
| `/back` | Retreat to the previous parent folder |
| `/home` | Return to the drive selection screen |

## 📦 Installation & Usage
### Running from Source
1. Ensure you have **Python 3.10+** installed.
2. Clone the repository:
   bash
   git clone [https://github.com/KaveenAdesh/File-Manager/.git](https://github.com/KaveenAdesh/File-Manager/.git)
3. Run this code:
   bash
   python file-manager.py    
