import os
import requests
from tqdm import tqdm
import zipfile
from colorama import init, Fore, Style

init(autoreset=True)

API_BASE = "https://api.mangadex.org"

def sanitize(name):
    return ''.join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in name)

def search_manga(title):
    params = {"title": title, "limit": 10}
    res = requests.get(f"{API_BASE}/manga", params=params).json()
    return res.get("data", [])

def get_all_chapters(manga_id, lang="en"):
    chapters = []
    offset = 0
    limit = 100
    while True:
        params = {
            "manga": manga_id,
            "translatedLanguage[]": lang,
            "order[chapter]": "asc",
            "limit": limit,
            "offset": offset
        }
        res = requests.get(f"{API_BASE}/chapter", params=params).json()
        data = res.get("data", [])
        chapters.extend(data)
        if len(data) < limit:
            break
        offset += limit
    return chapters

def get_page_urls(chapter_id):
    res = requests.get(f"{API_BASE}/at-home/server/{chapter_id}").json()
    base_url = res['baseUrl']
    chapter = res['chapter']
    hash = chapter['hash']
    return [f"{base_url}/data/{hash}/{f}" for f in chapter['data']]

def download_chapter(chapter, title, root_dir):
    chapter_num = chapter['attributes'].get('chapter', 'NA')
    chapter_title = sanitize(title)
    chapter_folder = os.path.join(root_dir, chapter_title)
    os.makedirs(chapter_folder, exist_ok=True)

    # Folder to store images temporarily
    temp_folder = os.path.join(chapter_folder, f"Chapter_{chapter_num}")
    os.makedirs(temp_folder, exist_ok=True)

    image_urls = get_page_urls(chapter['id'])
    image_paths = []

    for i, url in enumerate(tqdm(image_urls, desc=f"📥 Chapter {chapter_num}", ncols=70)):
        res = requests.get(url)
        filename = f"Page_{i+1:03}.jpg"
        filepath = os.path.join(temp_folder, filename)
        with open(filepath, "wb") as f:
            f.write(res.content)
        image_paths.append(filepath)

    # Create CBZ file (zip)
    cbz_path = os.path.join(chapter_folder, f"Chapter_{chapter_num}.cbz")
    with zipfile.ZipFile(cbz_path, 'w') as cbz:
        for img in image_paths:
            cbz.write(img, os.path.basename(img))

    # Optionally delete the temp folder
    for img in image_paths:
        os.remove(img)
    os.rmdir(temp_folder)


def main():
    print(Fore.CYAN + "📚 MangaDex Downloader - CLI Edition")
    title = input(Fore.YELLOW + "🔍 Enter manga title to search: ").strip()

    print(Fore.BLUE + "\n🔎 Searching MangaDex...\n")
    results = search_manga(title)
    if not results:
        print(Fore.RED + "❌ No results found.")
        return

    for i, manga in enumerate(results, 1):
        name = manga['attributes']['title'].get('en', 'No Title')
        print(f"{Fore.GREEN}{i}. {name}")

    idx = int(input(Fore.YELLOW + "\n📌 Select a manga by number: ")) - 1
    if idx < 0 or idx >= len(results):
        print(Fore.RED + "❌ Invalid selection.")
        return

    selected = results[idx]
    manga_title = selected['attributes']['title'].get('en', 'Unknown Title')
    manga_id = selected['id']

    print(Fore.BLUE + f"\n📖 Fetching chapters for: {manga_title}\n")
    chapters = get_all_chapters(manga_id)

    if not chapters:
        print(Fore.RED + "❌ No chapters found in English.")
        return

    print(Fore.MAGENTA + f"📦 Found {len(chapters)} chapters. Starting download...\n")

    for chap in chapters:
        download_chapter(chap, manga_title, "downloads")

    print(Fore.GREEN + f"\n✅ Download complete! Saved to: downloads/{sanitize(manga_title)}")

if __name__ == "__main__":
    main()
