#!/usr/bin/env python3
import requests
import os
import time
from telegram import Bot
import asyncio

# ========== PEXELS API - ОСНОВНОЙ ИСТОЧНИК ==========
# Бесплатный доступ: 200 запросов в час
# Тысячи видео о животных в высоком качестве
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', 'DUMMY_KEY')

# Fallback видео если API не работает
FALLBACK_VIDEOS = [
    {
        'url': 'https://videos.pexels.com/video-files/7451512/7451512-sd_640_360_30fps.mp4',
        'title': '🦁 Лев в дикой природе',
        'source': 'pexels'
    },
    {
        'url': 'https://videos.pexels.com/video-files/6590210/6590210-sd_640_360_24fps.mp4',
        'title': '🦓 Зебры в Африке',
        'source': 'pexels'
    },
    {
        'url': 'https://videos.pexels.com/video-files/6945871/6945871-sd_640_360_30fps.mp4',
        'title': '🦘 Кенгуру в движении',
        'source': 'pexels'
    },
    {
        'url': 'https://videos.pexels.com/video-files/9021637/9021637-sd_640_360_24fps.mp4',
        'title': '🐘 Слоны в саванне',
        'source': 'pexels'
    },
    {
        'url': 'https://videos.pexels.com/video-files/7988576/7988576-sd_640_360_24fps.mp4',
        'title': '🦅 Орел в полете',
        'source': 'pexels'
    },
]

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

if not bot_token or not chat_id:
    print("ERROR: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set!")
    exit(1)

bot = Bot(token=bot_token)

def fetch_pexels_videos():
    """
    Получить видео с Pexels API
    """
    videos = []
    
    # Если нет API key, используем fallback
    if PEXELS_API_KEY == 'DUMMY_KEY':
        print("⚠ PEXELS_API_KEY не установлен, используем кэшированные видео")
        return FALLBACK_VIDEOS[:3]
    
    try:
        headers = {'Authorization': PEXELS_API_KEY}
        queries = ['wildlife', 'animals', 'nature', 'lion', 'elephant', 'safari']
        
        for query in queries:
            try:
                url = 'https://api.pexels.com/videos/search'
                params = {
                    'query': query,
                    'per_page': 5,
                    'min_duration': 10,
                    'max_duration': 60
                }
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                print(f"✓ Получено видео по запросу '{query}': {len(data.get('videos', []))} штук")
                
                for video in data.get('videos', []):
                    video_files = video.get('video_files', [])
                    if video_files:
                        # Берем первый доступный файл
                        video_url = video_files[0]['link']
                        videos.append({
                            'url': video_url,
                            'title': f"{query.title()} - видео #{len(videos)+1}",
                            'source': 'pexels',
                            'upvotes': 100
                        })
                
                if len(videos) >= 5:
                    break
                    
            except requests.exceptions.RequestException as e:
                print(f"⚠ Ошибка запроса для '{query}': {e}")
                continue
    
    except Exception as e:
        print(f"✗ Ошибка Pexels API: {e}")
    
    return videos

async def post_to_telegram(videos):
    """
    Отправить видео в Telegram
    """
    if not videos:
        print("✗ Нет видео для отправки!")
        return
    
    posted_count = 0
    
    for video in videos[:3]:  # Отправляем максимум 3 видео
        try:
            caption = f"{video['title']}\n\n📺 Источник: {video['source'].upper()}\n👍 Рейтинг: {video['upvotes']}"
            
            print(f"📤 Отправляю: {video['title'][:50]}...")
            
            await bot.send_video(
                chat_id=chat_id,
                video=video['url'],
                caption=caption,
                read_timeout=30,
                write_timeout=30,
                connect_timeout=30
            )
            
            posted_count += 1
            print(f"✓ Успешно отправлено!")
            time.sleep(2)  # Rate limiting между видео
            
        except Exception as e:
            print(f"⚠ Ошибка отправки видео: {e}")
            continue
    
    print(f"\n✓ Отправлено видео: {posted_count} шт!")

async def main():
    print("\n🦁 Запуск Wildlife Telegram Bot\n")
    print("="*50)
    
    # Пытаемся получить видео с Pexels
    print("\n📡 Подключение к Pexels API...")
    videos = fetch_pexels_videos()
    
    # Если нет видео, используем fallback
    if not videos:
        print("\n⚠ Pexels API не подошел, используем кэшированные видео...")
        videos = FALLBACK_VIDEOS
    
    print(f"\n📊 Найдено видео: {len(videos)} шт")
    
    if videos:
        print("\n📤 Отправка в Telegram...\n")
        await post_to_telegram(videos)
    else:
        print("✗ Не удалось получить видео из любых источников.")
    
    print("\n" + "="*50)
    print("✓ Бот завершил работу\n")

if __name__ == "__main__":
    asyncio.run(main())
