import requests
import time
import os

ACCESS_TOKEN = "ACCESS_TOKEN"
IG_USER_ID = "IG_USER_ID"
IMAGE_URL = "video and image url"
CAPTION = "Otomatik paylaşım testi! #bot"
work_url ="http://yourdomain/videos/video.mp4"
save_dir = "/var/www/html/videos"
save_path = os.path.join(save_dir, "video.mp4")
# Klasörü oluştur (zaten varsa hata vermez)
os.makedirs(save_dir, exist_ok=True)
response = requests.get(IMAGE_URL)
with open(save_path, "wb") as f:
    f.write(response.content)
print("✅ Video indirildi:", save_path)
# 1. Medya nesnesi oluştur
'''
media = requests.post(
    f"https://graph.instagram.com/v23.0/{IG_USER_ID}/media",
    data={
        "image_url": IMAGE_URL,
        "caption": CAPTION,
        "access_token": ACCESS_TOKEN,
    }
)
'''

media = requests.post(
    f"https://graph.instagram.com/v23.0/{IG_USER_ID}/media",
    data={
        "media_type": "REELS",
        "video_url": work_url,
        "caption": CAPTION,
        "access_token": ACCESS_TOKEN
    }
)

media_json = media.json()
print("🎬 Media Oluşturma Yanıtı:", media_json)

creation_id = media_json.get("id")
if not creation_id:
    print("❌ creation_id alınamadı.")
    exit()
print(creation_id)
# 2. Medya işlenene kadar bekle
def wait_until_ready(creation_id, access_token, timeout=400):
    status_url = f"https://graph.instagram.com/v23.0/{creation_id}?fields=status_code,status&access_token={access_token}"
    waited = 0
    while waited < timeout:
        res = requests.get(status_url).json()
        status = res.get("status_code")
        print(f"⏳ Medya durumu: {res}")
        if status == "FINISHED":
            return True
        elif status == "ERROR":
            print("❌ Medya işlenemedi:", res)
            return False
        time.sleep(5)
        waited += 5
    print("❌ Zaman aşımı. Medya hazır olmadı.")
    return False

# 3. Eğer video hazırsa paylaş
if wait_until_ready(creation_id, ACCESS_TOKEN):
    publish = requests.post(
        f"https://graph.instagram.com/v23.0/{IG_USER_ID}/media_publish",
        data={
            "creation_id": creation_id,
            "access_token": ACCESS_TOKEN,
        }
    )
    print("✅ Yayınlama yanıtı:", publish.json())
else:
    print("⏸ Yayınlama iptal edildi.")
