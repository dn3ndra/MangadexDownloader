# 📚 MangaDex CLI Downloader

A simple Python CLI tool to download manga chapters from [MangaDex](https://mangadex.org), package them as `.cbz` files, and optionally transfer them to a manga reader like **Panels** on iOS.

---

## ✨ Features

- 🔍 Search for manga by title from MangaDex
- 📖 Automatically download all English-translated chapters
- 🗂️ Saves pages as `.cbz` (Comic Book ZIP) files per chapter
- 📂 Clean folder structure: `downloads/<Manga_Title>/Chapter_<N>.cbz`
- 🖥️ CLI interface with colored output and progress bars
- ✅ Compatible with iOS manga reader **Panels** (via Web Server upload)

---

## 🚀 Installation

1. Clone this repository or download the script:
    ```bash
    git clone https://github.com/yourusername/mangadex-cli-downloader.git
    cd mangadex-cli-downloader
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

    Or manually:
    ```bash
    pip install requests tqdm colorama
    ```

---

## 🛠 Usage

Run the main script:

```bash
python mangadexDownloader.py
