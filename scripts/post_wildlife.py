#!/usr/bin/env python3
import requests
import os
import json
import time
from telegram import Bot
import asyncio
import random

# Configuration
REDDIT_SUBREDDITS = ['wildlife', 'AnimalsBeingBros', 'NatureIsFuckingLit']
PIKASU_URLS = [
    'https://api.pikabu.ru/api/v2/feed/trending?page=1&sort=hot',
    'https://api.pikabu.ru/api/v2/communities/feed?communities=animals&sort=hot&page=1'
]
VIDEO_LIMIT = 10  # Get more videos as fallback

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

if not bot_token or not chat_id:
    print("ERROR: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set!")
    exit(1)

bot = Bot(token=bot_token)

def fetch_reddit_videos():
    """
    Fetch wildlife videos from Reddit with better headers
    """
    videos = []
    
    # Better headers to avoid Reddit blocking
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Referer': 'https://www.reddit.com/',
    }
    
    for subreddit in REDDIT_SUBREDDITS:
        try:
            url = f'https://www.reddit.com/r/{subreddit}/top.json?t=day&limit={VIDEO_LIMIT}'
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            print(f"✓ Successfully fetched r/{subreddit}")
            
            for post in data.get('data', {}).get('children', []):
                post_data = post.get('data', {})
                
                # Skip if no media or video
                if not post_data.get('media'):
                    continue
                
                try:
                    video_url = post_data['media']['reddit_video']['fallback_url']
                    title = post_data.get('title', 'Wildlife Video')
                    upvotes = post_data.get('ups', 0)
                    
                    # Only include videos with engagement
                    if upvotes > 20:
                        videos.append({
                            'url': video_url,
                            'title': title[:200],
                            'subreddit': subreddit,
                            'upvotes': upvotes,
                            'source': 'reddit'
                        })
                except (KeyError, TypeError):
                    continue
        
        except requests.exceptions.RequestException as e:
            print(f"⚠ Error fetching from r/{subreddit}: {e}")
            continue
        except Exception as e:
            print(f"✗ Unexpected error from r/{subreddit}: {e}")
            continue
    
    return videos

def fetch_imgur_videos():
    """
    Fetch videos from Imgur as fallback
    """
    videos = []
    try:
        # Imgur doesn't require auth for public content
        url = 'https://imgur.com/ajaxalbums/list/t/1/week/0?client_id=546c25a59c58ad7'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        print(f"✓ Successfully fetched from Imgur")
        
        for item in data.get('data', [])[:10]:
            if item.get('type') == 'video/mp4':
                videos.append({
                    'url': item.get('link'),
                    'title': item.get('title', 'Imgur Video'),
                    'subreddit': 'imgur',
                    'upvotes': item.get('views', 0),
                    'source': 'imgur'
                })
    except Exception as e:
        print(f"⚠ Error fetching from Imgur: {e}")
    
    return videos

async def post_to_telegram(videos):
    """
    Post videos to Telegram channel
    """
    if not videos:
        print("No videos found!")
        return
    
    # Shuffle and take top 3
    random.shuffle(videos)
    posted_count = 0
    
    for video in videos[:3]:
        try:
            caption = f"🦁 {video['title']}\n\n📺 From: {video['source'].upper()}\n👍 Engagement: {video['upvotes']}"
            
            # Validate URL
            if not video['url'].startswith('http'):
                print(f"⚠ Skipping invalid URL")
                continue
            
            await bot.send_video(
                chat_id=chat_id,
                video=video['url'],
                caption=caption,
                read_timeout=30,
                write_timeout=30,
                connect_timeout=30
            )
            
            posted_count += 1
            print(f"✓ Posted: {video['title'][:50]}...")
            time.sleep(2)  # Rate limiting
            
        except Exception as e:
            print(f"⚠ Error posting video: {e}")
            continue
    
    print(f"✓ Successfully posted {posted_count} videos!")

async def main():
    print("🦁 Fetching wildlife videos...\n")
    
    # Try Reddit first
    videos = fetch_reddit_videos()
    
    # If Reddit fails, try Imgur as fallback
    if not videos:
        print("\n⚠ Reddit fetch failed, trying Imgur fallback...\n")
        videos = fetch_imgur_videos()
    
    print(f"\nTotal videos found: {len(videos)}")
    
    if videos:
        print("\nPosting to Telegram...")
        await post_to_telegram(videos)
    else:
        print("✗ No suitable videos found from any source.")

if __name__ == "__main__":
    asyncio.run(main())
