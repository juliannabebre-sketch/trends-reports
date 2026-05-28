"""
DAILY TRENDS SNAPSHOT
Runs every day — captures last 7 days of trends across platforms.
Saves JSON (for weekly analysis) + TXT (for daily reading).
"""

import time, os, json, requests, sys
sys.path.insert(0, '/Users/dzulijanna/Documents/TrendsData')
from datetime import datetime
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
from youtubesearchpython import VideosSearch
from report_html import build_daily_html

TODAY       = datetime.now().strftime('%Y-%m-%d')
DATE_LABEL  = datetime.now().strftime('%B %d, %Y')
BASE_DIR    = '/Users/dzulijanna/Documents/TrendsData'
DAILY_DIR   = f'{BASE_DIR}/daily'
REPORTS_DIR = f'{BASE_DIR}/reports'

TOPICS      = ['health', 'supplements', 'biohacking', 'supplement ingredients']
SUBREDDITS  = ['supplements', 'biohacking', 'health']

snapshot    = {'date': TODAY, 'google': {}, 'reddit': {}, 'youtube': {}, 'amazon': []}
lines       = []

def log(text=""):
    print(text)
    lines.append(str(text))

def header(title):
    log(); log("=" * 60); log(f"  {title}"); log("=" * 60)

def sub(title):
    log(f"\n📌 {title}"); log("-" * 40)


# ──────────────────────────────────────────────────────────
# 1. GOOGLE TRENDS  (last 7 days)
# ──────────────────────────────────────────────────────────
header(f"GOOGLE TRENDS — Last 7 Days | US Market | {DATE_LABEL}")
pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25))

for topic in TOPICS:
    log(f"⏳ Fetching: {topic}...")
    time.sleep(30)
    try:
        pytrends.build_payload([topic], timeframe='now 7-d', geo='US')
        related = pytrends.related_queries()
        rising  = related[topic]['rising']
        top     = related[topic]['top']
        snapshot['google'][topic] = {
            'rising': rising.head(10).to_dict('records') if rising is not None else [],
            'top':    top.head(10).to_dict('records')    if top    is not None else []
        }
        log(f"✅ Done: {topic}")
    except Exception as e:
        log(f"❌ Error ({topic}): {e}")
        snapshot['google'][topic] = {'rising': [], 'top': []}

for topic, data in snapshot['google'].items():
    sub(f"TOPIC: {topic.upper()}")
    log("🔥 RISING (going viral):")
    for i, r in enumerate(data['rising'], 1):
        log(f"   {i}. {r['query']} — {r['value']}%")
    if not data['rising']: log("   No data")
    log("\n📊 TOP SEARCHES:")
    for i, r in enumerate(data['top'], 1):
        log(f"   {i}. {r['query']} — {r['value']}")
    if not data['top']: log("   No data")


# ──────────────────────────────────────────────────────────
# 2. REDDIT
# ──────────────────────────────────────────────────────────
header(f"REDDIT HOT POSTS | {DATE_LABEL}")
reddit_headers = {'User-Agent': 'TrendBot/1.0'}

for sub_name in SUBREDDITS:
    sub(f"r/{sub_name}")
    try:
        res   = requests.get(f'https://www.reddit.com/r/{sub_name}/hot.json?limit=7',
                             headers=reddit_headers, timeout=10)
        posts = res.json()['data']['children']
        snapshot['reddit'][sub_name] = []
        for i, post in enumerate(posts, 1):
            d = post['data']
            snapshot['reddit'][sub_name].append({'title': d['title'], 'score': d['score'], 'comments': d['num_comments'], 'url': f"https://reddit.com{d['permalink']}"})
            log(f"   {i}. {d['title']}")
            log(f"      ⬆️  {d['score']} upvotes | 💬 {d['num_comments']} comments")
    except Exception as e:
        log(f"   ❌ Error: {e}")
    time.sleep(3)


# ──────────────────────────────────────────────────────────
# 3. YOUTUBE
# ──────────────────────────────────────────────────────────
header(f"YOUTUBE TRENDING VIDEOS | {DATE_LABEL}")
yt_queries = ['supplements 2026', 'biohacking 2026', 'health trends 2026', 'supplement ingredients 2026']

for query in yt_queries:
    sub(f"Search: {query}")
    try:
        results = VideosSearch(query, limit=5).result()['result']
        snapshot['youtube'][query] = []
        for i, v in enumerate(results, 1):
            views = v.get('viewCount', {}).get('text', 'N/A') if v.get('viewCount') else 'N/A'
            snapshot['youtube'][query].append({'title': v['title'], 'views': views, 'link': v['link']})
            log(f"   {i}. {v['title']}")
            log(f"      👁  {views} | 🔗 {v['link']}")
    except Exception as e:
        log(f"   ❌ Error: {e}")
    time.sleep(2)


# ──────────────────────────────────────────────────────────
# 4. AMAZON BESTSELLERS
# ──────────────────────────────────────────────────────────
header(f"AMAZON BESTSELLERS — Vitamins & Supplements | {DATE_LABEL}")
try:
    url = 'https://www.amazon.com/Best-Sellers-Health-Personal-Care-Vitamins-Supplements/zgbs/hpc/3764441'
    amz_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    res   = requests.get(url, headers=amz_headers, timeout=15)
    soup  = BeautifulSoup(res.content, 'html.parser')
    items = soup.select('div.zg-grid-general-faceout')[:10]
    log()
    if items:
        for i, item in enumerate(items, 1):
            name_tag = item.select_one('span.a-size-small, div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1, span.a-color-base')
            name = name_tag.get_text(strip=True) if name_tag else 'Unknown'
            snapshot['amazon'].append(name)
            log(f"   #{i}. {name}")
    else:
        log("   ⚠️  Amazon blocked. Manual link:")
        log("   🔗 https://www.amazon.com/Best-Sellers-Vitamins-Supplements/zgbs/hpc/3764441")
except Exception as e:
    log(f"   ❌ Error: {e}")


# ──────────────────────────────────────────────────────────
# SAVE FILES
# ──────────────────────────────────────────────────────────
json_file = f'{DAILY_DIR}/snapshot_{TODAY}.json'
html_file = f'{REPORTS_DIR}/Daily_Report_{TODAY}.html'

with open(json_file, 'w') as f:
    json.dump(snapshot, f, indent=2)

html = build_daily_html(snapshot)
with open(html_file, 'w') as f:
    f.write(html)

print()
print("=" * 60)
print(f"✅ Daily report saved!")
print(f"   📊 Data:   {json_file}")
print(f"   🌐 Report: {html_file}")
print("=" * 60)

os.system(f"open '{html_file}'")

# ── Publish to GitHub Pages ──
print("\n🚀 Publishing to GitHub Pages...")
os.system(f"""
cd /Users/dzulijanna/Documents/TrendsData && \
git add reports/ && \
git commit -m "Daily report {TODAY}" && \
git push origin main
""")
print(f"✅ Published! View at: https://juliannabebre-sketch.github.io/trends-reports/")
