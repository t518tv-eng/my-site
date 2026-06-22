import glob
import json
import re
from bs4 import BeautifulSoup

SOURCE_DIR = r"C:\Users\Близнец\Desktop\telegram"

files = glob.glob(f"{SOURCE_DIR}\\messages*.html")

def get_index(path):
    m = re.search(r"messages(\d+)", path)
    return int(m.group(1)) if m else 0

files = sorted(files, key=get_index)

print("FILES:", len(files))

messages = []
current_date = ""
last_author = ""

for file in files:
    print("READ:", file)

    with open(file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    blocks = soup.find_all("div", class_=lambda x: x and "message" in x)

    for b in blocks:

        # ---------------- DATE
        if "service" in b.get("class", []):
            date_text = b.get_text(strip=True)
            if date_text:
                current_date = date_text
            continue

        # ---------------- AUTHOR
        author_block = b.find("div", class_="from_name")
        if author_block:
            last_author = author_block.get_text(strip=True)

        author = last_author

        # ---------------- TIME
        time_block = b.find("div", class_="pull_right date details")
        time = time_block.get_text(strip=True) if time_block else ""

        # ---------------- TEXT
        text_block = b.find("div", class_="text")
        text = text_block.get_text("\n", strip=True) if text_block else ""

        msg_type = "text"
        media = None

        # =========================================================
        # 🎥 ROUND VIDEO (ВСЕ ВАРИАНТЫ TELEGRAM)
        # =========================================================
        if (
            "round_video_messages" in str(b)
            or b.find("video")
            or b.find("a", href=re.compile(r"round_video_messages"))
            or (b.find("div") and "round" in str(b).lower())
        ):
            msg_type = "round_video"

            # 1) video tag
            video = b.find("video")
            if video:
                media = video.get("src")

            # 2) link
            if not media:
                link = b.find("a", href=re.compile(r"round_video_messages"))
                if link:
                    media = link.get("href")

            # 3) img fallback
            if not media:
                img = b.find("img")
                if img:
                    media = img.get("src")

            # cleanup thumb
            if media:
                media = media.replace("_thumb.jpg", "")

            # only mp4 allowed
            if media and ".mp4" not in media:
                media = None

            # skip empty round videos
            if not media:
                continue

        # =========================================================
        # 📷 PHOTO
        # =========================================================
        elif b.find("a", class_="photo_wrap") or b.find("img"):
            msg_type = "photo"

            photo = b.find("a", class_="photo_wrap")
            if photo:
                media = photo.get("href") or photo.get("src")

        # =========================================================
        # 🎤 VOICE
        # =========================================================
        elif (
            b.find("audio")
            or b.find("a", href=re.compile(r"\.(ogg|mp3|oga|wav)"))
            or "voice" in str(b).lower()
        ):
            msg_type = "voice"

            audio = b.find("audio")
            if audio:
                media = audio.get("src")

            file_link = b.find("a", href=re.compile(r"\.(ogg|mp3|oga|wav)"))
            if file_link:
                media = file_link.get("href")

        # =========================================================
        # 🎬 VIDEO
        # =========================================================
        elif b.find("div", class_="video_file"):
            msg_type = "video"

        # =========================================================
        # 🧩 STICKER
        # =========================================================
        elif b.find("div", class_="sticker_message"):
            msg_type = "sticker"

        # ---------------- SKIP EMPTY
        if not text and not media:
            continue

        messages.append({
            "dt": f"{current_date} {time}".strip(),
            "author": author,
            "type": msg_type,
            "text": text,
            "media": media
        })

print("TOTAL MESSAGES:", len(messages))

with open("data.js", "w", encoding="utf-8") as f:
    f.write("const messages = ")
    f.write(json.dumps(messages, ensure_ascii=False, indent=2))
    f.write(";")

print("DONE → data.js created")