#!/usr/bin/env python3
import requests
import os
import time
from telegram import Bot
import asyncio

PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', 'DUMMY_KEY')

FALLBACK_VIDEOS = [
    {'url': 'https://videos.pexels.com/video-files/7451512/7451512-sd_640_360_30fps.mp4', 'title': '🦁 Лев в дикой природе', 'source': 'pexels', 'rating': 100},
    {'url': 'https://videos.pexels.com/video-files/6590210/6590210-sd_640_360_24fps.mp4', 'title': '🦓 Зебры в Африке', 'source': 'pexels', 'rating': 100},
    {'url': 'https://videos.pexels.com/video-files/6945871/6945871-sd_640_360_30fps.mp4', 'title': '🦘 Кенгуру в движении', 'source': 'pexels', 'rating': 100},
    {'url': 'https://videos.pexels.com/video-files/9021637/9021637-sd_640_360_24fps.mp4', 'title': '🐘 Слоны в саванне', 'source': 'pexels', 'rating': 100},
    {'url': 'https://videos.pexels.com/video-files/7988576/7988576-sd_640_360_24fps.mp4', 'title': '🦅 Орел в полете', 'source': 'pexels', 'rating': 100},
]

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

if not bot_token or not chat_id:
    print("ERROR: Missing credentials!")
    exit(1)

bot = Bot(token=bot_token)

def get_videos():
    if PEXELS_API_KEY == 'DUMMY_KEY':
        print("⚠ Используем кэшированные видео")
        return FALLBACK_VIDEOS[:3]
    
    videos = []
    try:
        headers = {'Authorization': PEXELS_API_KEY}
        for query in ['wildlife', 'animals']:
            url = 'https://api.pexels.com/videos/search'
            params = {'query': query, 'per_page': 5, 'min_duration': 10, 'max_duration': 60}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()
            
            for video in data.get('videos', []):
                if video.get('video_files'):
                    videos.append({
                        'url': video['video_files'][0]['link'],
                        'title': f"{query.title()} видео",
                        'source': 'pexels',
                        'rating': 100
                    })
            if len(videos) >= 3:
                break
    except Exception as e:
        print(f"⚠ API ошибка: {e}")
    
    return videos if videos else FALLBACK_VIDEOS[:3]

async def send_videos(videos):
    posted = 0
    for video in videos[:3]:
        try:
            rating = video.get('rating', 100)
            caption = f"{video['title']}\n\n📺 {video.get('source', 'unknown').upper()}\n👍 {rating}"
            
            print(f"📤 Отправляю: {video['title'][:40]}")
            
            await bot.send_video(
                chat_id=chat_id,
                video=video['url'],
                caption=caption,
                read_timeout=30,
                write_timeout=30,
                connect_timeout=30
            )
            
            posted += 1
            print(f"✓ Успешно!")
            time.sleep(2)
        except Exception as e:
            print(f"⚠ Ошибка: {e}")
    
    return posted

async def main():
    print("\n🦁 Wildlife Bot запущен\n")
    videos = get_videos()
    print(f"📊 Найдено: {len(videos)} видео")
    
    if videos:
        posted = await send_videos(videos)
        print(f"\n✓ Отправлено: {posted} видео!")
    else:
        print("✗ Нет видео")

if __name__ == "__main__":
    asyncio.run(main())
