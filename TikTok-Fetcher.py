# ==============================================
# Colab-ready TikTok Video URL Extractor
# Written by: Jawad
# Purpose: Extract all video URLs from a TikTok profile
# Using: yt-dlp
# ==============================================

# 1) Install the dependency
#pip install -q yt-dlp

# 2) Import necessary libraries
from yt_dlp import YoutubeDL
from urllib.parse import urlparse
import os

# ----------------------------
# Helper function to normalize a TikTok profile URL
# ----------------------------
def normalize_profile_url(u: str) -> str:
    """
    Accepts either:
        - username only: "someuser" or "@someuser"
        - full URL: "https://www.tiktok.com/@someuser"
    Returns a normalized TikTok profile URL suitable for yt-dlp.
    """
    u = u.strip()
    if u.startswith("http://") or u.startswith("https://"):
        return u  # already a full URL
    if u.startswith("@"):
        u = u[1:]  # remove @ if present
    # assume it's a plain username
    return f"https://www.tiktok.com/@{u}"

# ----------------------------
# Main function to get TikTok video links
# ----------------------------
def get_tiktok_video_links(profile_url: str, output_file: str = None, max_items: int = None):
    """
    profile_url: TikTok profile link or username (e.g. "user" or "@user" or full URL)
    output_file: optional file path to save video URLs
    max_items: optional limit on number of videos to fetch (default: all)
    Returns: list of video URLs
    """
    profile_url = normalize_profile_url(profile_url)

    # yt-dlp options: we just want the video URLs, not to download videos
    ydl_opts = {
        "extract_flat": True,  # don't download media
        "skip_download": True,
        "quiet": True,         # no clutter in output
    }

    videos = []
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(profile_url, download=False)
        except Exception as e:
            raise RuntimeError(f"yt-dlp failed to extract info: {e}")

        # Usually 'entries' contains the video list
        entries = info.get("entries") if isinstance(info, dict) else None
        if not entries:
            # Sometimes profile has only one video or unexpected format
            if isinstance(info, dict):
                candidate = info.get("webpage_url") or info.get("url") or info.get("id")
                if candidate:
                    videos.append(candidate if candidate.startswith("http") else str(candidate))
        else:
            for i, e in enumerate(entries):
                if max_items is not None and i >= max_items:
                    break
                if not e:
                    continue
                # Pick the best available URL
                url = e.get("webpage_url") or e.get("original_url") or e.get("url") or None
                if url is None:
                    # fallback: construct URL manually if needed
                    vid_id = e.get("id")
                    username = None
                    if isinstance(info, dict):
                        username = info.get("uploader") or info.get("uploader_id") or info.get("display_id")
                        if not username and info.get("webpage_url"):
                            parsed = urlparse(info.get("webpage_url"))
                            if parsed.path:
                                username = parsed.path.strip("/").split("/")[0].lstrip("@")
                    if vid_id and username:
                        url = f"https://www.tiktok.com/@{username}/video/{vid_id}"
                if url:
                    videos.append(url)

    # Remove duplicates while preserving order
    seen = set()
    unique_videos = []
    for v in videos:
        if v not in seen:
            unique_videos.append(v)
            seen.add(v)

    # Save to file if requested
    if output_file:
        os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            for v in unique_videos:
                f.write(v + "\n")

    return unique_videos

# ----------------------------
# Example usage (interactive)
# ----------------------------
if __name__ == "__main__":
    profile = input("Enter TikTok profile URL or username (e.g. @username or username or full URL): ").strip()
    if not profile:
        print("No profile provided. Exiting.")
    else:
        try:
            output_path = "tiktok_video_links.txt"  # file to save URLs
            print(f"Fetching video links for: {profile} ...")
            links = get_tiktok_video_links(profile, output_file=output_path, max_items=None)
            if not links:
                print("No videos found or extraction failed.")
            else:
                print(f"Found {len(links)} videos. Sample (first 20):")
                for i, link in enumerate(links[:20], 1):
                    print(f"{i}. {link}")
                print(f"\nAll links saved to: {os.path.abspath(output_path)}")
        except Exception as e:
            print("Error:", e)
