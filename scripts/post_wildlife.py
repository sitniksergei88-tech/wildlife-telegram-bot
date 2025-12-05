#!/usr/bin/env python3
import requests
import os
import json
import time
from telegram import Bot
import asyncio

# Configuration
SUBREDDITS = ['wildlife', 'AnimalsBeingBros', 'NatureIsFuckingLit']
VIDEO_LIMIT = 5  # Get top 5 videos

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

if not bot_token or not chat_id:
    print("ERROR: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set!")
    exit(1)

bot = Bot(token=bot_token)

def fetch_reddit_videos():
    """
    Fetch wildlife videos from Reddit
    """
    videos = []
    
    for subreddit in SUBREDDITS:
        try:
            url = f'https://www.reddit.com/r/{subreddit}/top.json?t=day&limit={VIDEO_LIMIT}'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            for post in data.get('data', {}).get('children', []):
                post_data = post.get('data', {})
                
                # Skip if no media
                if not post_data.get('media'):
                    continue
                
                try:
                    video_url = post_data['media']['reddit_video']['fallback_url']
                    title = post_data.get('title', 'Wildlife Video')
                    upvotes = post_data.get('ups', 0)
                    
                    # Only include videos with good engagement
                    if upvotes > 50:
                        videos.append({
                            'url': video_url,
                            'title': title[:200],  # Truncate title
                            'subreddit': subreddit,
                            'upvotes': upvotes
                        })
                except (KeyError, TypeError):
                    continue
        
        except Exception as e:
            print(f"Error fetching from r/{subreddit}: {e}")
            continue
    
    return videos

async def post_to_telegram(videos):
    """
    Post videos to Telegram channel
    """
    if not videos:
        print("No videos found!")
        return
    
    posted_count = 0
    for video in videos[:3]:  # Post top 3 videos
        try:
            caption = f"🐿 {video['title']}\n\n🐱 From: r/{video['subreddit']}\n👍 Upvotes: {video['upvotes']}"
            
            await bot.send_video(
                chat_id=chat_id,
                video=video['url'],
                caption=caption,
                read_timeout=30,
                write_timeout=30,
                connect_timeout=30
            )
            
            posted_count += 1
            print(f"Posted: {video['title']}")
            time.sleep(2)  # Rate limiting
            
        except Exception as e:
            print(f"Error posting video: {e}")
            continue
    
    print(f"Successfully posted {posted_count} videos!")

async def main():
    print("Fetching wildlife videos from Reddit...")
    videos = fetch_reddit_videos()
    print(f"Found {len(videos)} videos!")
    
    if videos:
        print("Posting to Telegram...")
        await post_to_telegram(videos)
    else:
        print("No suitable videos found.")

if __name__ == "__main__":
    asyncio.run(main())
