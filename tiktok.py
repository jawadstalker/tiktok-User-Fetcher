import requests
from bs4 import BeautifulSoup
import os
import sys

def get_profile_image(username: str):
    username = username.lstrip("@")
    url = f"https://www.tiktok.com/@{username}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.tiktok.com/"
    }

    print(f"[*] Fetching profile page for @{username}...")
    response = requests.get(url, headers=headers, timeout=15)

    if response.status_code != 200:
        print(f"[!] Failed to fetch page (status {response.status_code}).")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Try common meta tags for profile image
    img_url = None
    og_tag = soup.find("meta", property="og:image")
    twitter_tag = soup.find("meta", attrs={"name": "twitter:image"})
    if og_tag and og_tag.get("content"):
        img_url = og_tag["content"]
    elif twitter_tag and twitter_tag.get("content"):
        img_url = twitter_tag["content"]
    else:
        # fallback: try to find inside scripts
        import re
        m = re.search(r'"avatarLarger"\s*:\s*"([^"]+)"', response.text)
        if m:
            img_url = m.group(1).replace("\\u002F", "/")

    if not img_url:
        print("[!] Could not find profile image URL. Page layout may have changed.")
        return None

    if img_url.startswith("//"):
        img_url = "https:" + img_url

    print(f"[+] Found image URL: {img_url}")
    return img_url


def download_image(img_url: str, username: str):
    print("[*] Downloading image...")
    response = requests.get(img_url, stream=True)
    if response.status_code != 200:
        print(f"[!] Failed to download image (status {response.status_code})")
        return

    ext = ".png" if "png" in response.headers.get("content-type", "") else ".jpg"
    filename = f"{username}_pfp{ext}"
    with open(filename, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

    print(f"[✓] Saved profile picture as: {filename}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_tiktok_pfp.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    img_url = get_profile_image(username)
    if img_url:
        download_image(img_url, username)
