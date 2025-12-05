#!/usr/bin/env python3
"""
Local testing script for wildlife bot
Use this to test the bot locally before deploying to GitHub Actions
"""

import requests
import json

SUBREDDITS = ['wildlife', 'AnimalsBeingBros', 'NatureIsFuckingLit']
VIDEO_LIMIT = 5

def test_reddit_fetch():
    """
    Test fetching videos from Reddit
    """
    print("\n=== Testing Reddit Video Fetch ===")
    print(f"Fetching from: {SUBREDDITS}\n")
    
    videos = []
    
    for subreddit in SUBREDDITS:
        try:
            url = f'https://www.reddit.com/r/{subreddit}/top.json?t=day&limit={VIDEO_LIMIT}'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            print(f"✓ Successfully fetched r/{subreddit}")
            
            for post in data.get('data', {}).get('children', []):
                post_data = post.get('data', {})
                
                if not post_data.get('media'):
                    continue
                
                try:
                    video_url = post_data['media']['reddit_video']['fallback_url']
                    title = post_data.get('title', 'Wildlife Video')
                    upvotes = post_data.get('ups', 0)
                    
                    if upvotes > 50:
                        videos.append({
                            'url': video_url,
                            'title': title[:100],
                            'subreddit': subreddit,
                            'upvotes': upvotes
                        })
                except (KeyError, TypeError):
                    continue
        
        except Exception as e:
            print(f"✗ Error fetching from r/{subreddit}: {e}")
            continue
    
    print(f"\nTotal videos found: {len(videos)}")
    
    if videos:
        print("\n=== Top Videos ===")
        for i, video in enumerate(videos[:3], 1):
            print(f"\n{i}. {video['title'][:60]}...")
            print(f"   From: r/{video['subreddit']}")
            print(f"   Upvotes: {video['upvotes']}")
            print(f"   URL: {video['url'][:80]}...")
    
    return videos

if __name__ == "__main__":
    print("🦁 Wildlife Telegram Bot - Local Test\n")
    
    try:
        videos = test_reddit_fetch()
        print("\n✅ Test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
