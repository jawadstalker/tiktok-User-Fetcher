# TikTok Video URL Grabber

**Author:** Jawad  

A lightweight and efficient tool to **extract all video URLs from a TikTok profile** without downloading the videos. This project is ideal for anyone who wants to:  

- Quickly gather video URLs for analysis  
- Collect data for **AI and neural network experiments**  
- Extend functionality later to include additional video metadata like likes, hashtags, captions, and more  

---

## Features

- Extract all video URLs from any TikTok profile  
- Save the URLs to a text file for later use  
- Optionally limit the number of videos to extract  
- Fast and lightweight, no video downloads required  
- Ready for extension to AI/ML projects and data analysis  

> ⚡ Future versions can include additional metadata extraction such as like counts, hashtags, captions, and upload dates.

---

## Requirements

- Python 3.8+  
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) library  

Install dependencies quickly via pip:

```bash
pip install yt-dlp
```

> Colab-ready: You can run this script directly in Google Colab.

---

## Usage

1. Run the Python script in any Python environment or Google Colab.  
2. Enter the TikTok profile username or URL when prompted. Examples:  

```
@therock
therock
https://www.tiktok.com/@therock
```

3. The script will fetch all available video URLs and save them to a file (`tiktok_video_links.txt` by default).

**Example usage in Python code:**

```python
from tiktok_grabber import get_tiktok_video_links

profile = "@therock"
links = get_tiktok_video_links(profile, output_file="links.txt", max_items=50)

print("Video URLs:", links)
```

- `output_file`: path to save the URLs  
- `max_items`: optional maximum number of videos to fetch (`None` means fetch all)

---

## AI & ML Applications

- Use the extracted URLs to gather additional metadata (captions, hashtags, like counts) via web scraping or APIs.  
- Ideal for practicing **NLP**, **neural networks**, and other AI models using real TikTok data.  

---

## Notes

- This project **does not download videos**; it only extracts URLs.  
- Collecting additional metadata will require further development or API access.  
- Always comply with TikTok's Terms of Service and copyright rules when using this data.

---

## License

MIT License – free to use and modify.

