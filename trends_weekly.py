"""
WEEKLY TRENDS REPORT
Runs every Monday at 11am.
- Pulls 30-day Google Trends overview
- Reads last 7 daily snapshots
- Compares & detects patterns
- Generates commentary: breakouts, sustained trends, cross-platform signals
"""

import time, os, json, requests, glob, sys
sys.path.insert(0, '/Users/dzulijanna/Documents/TrendsData')
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
from youtubesearchpython import VideosSearch
from report_html import build_weekly_html

TODAY       = datetime.now().strftime('%Y-%m-%d')
DATE_LABEL  = datetime.now().strftime('%B %d, %Y')
BASE_DIR    = '/Users/dzulijanna/Documents/TrendsData'
DAILY_DIR   = f'{BASE_DIR}/daily'
REPORTS_DIR = f'{BASE_DIR}/reports'

TOPICS      = ['health', 'supplements', 'biohacking', 'supplement ingredients']
SUBREDDITS  = ['supplements', 'biohacking', 'health']

lines = []

def log(text=""):
    print(text)
    lines.append(str(text))

def header(title):
    log(); log("=" * 60); log(f"  {title}"); log("=" * 60)

def sub(title):
    log(f"\n📌 {title}"); log("-" * 40)


# ──────────────────────────────────────────────────────────
# LOAD LAST 7 DAILY SNAPSHOTS
# ──────────────────────────────────────────────────────────
def load_daily_snapshots():
    snapshots = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        path = f'{DAILY_DIR}/snapshot_{date}.json'
        if os.path.exists(path):
            with open(path) as f:
                snapshots.append(json.load(f))
    return snapshots

snapshots = load_daily_snapshots()
log(f"📂 Loaded {len(snapshots)} daily snapshots for analysis")


# ──────────────────────────────────────────────────────────
# 1. GOOGLE TRENDS — 30-DAY OVERVIEW
# ──────────────────────────────────────────────────────────
header(f"1. GOOGLE TRENDS — Last 30 Days | US Market | {DATE_LABEL}")
pytrends   = TrendReq(hl='en-US', tz=360, timeout=(10, 25))
google_30d = {}

for topic in TOPICS:
    log(f"⏳ Fetching 30-day data: {topic}...")
    time.sleep(30)
    try:
        pytrends.build_payload([topic], timeframe='today 1-m', geo='US')
        related = pytrends.related_queries()
        rising  = related[topic]['rising']
        top     = related[topic]['top']
        google_30d[topic] = {
            'rising': rising.head(10).to_dict('records') if rising is not None else [],
            'top':    top.head(10).to_dict('records')    if top    is not None else []
        }
        log(f"✅ Done: {topic}")
    except Exception as e:
        log(f"❌ Error ({topic}): {e}")
        google_30d[topic] = {'rising': [], 'top': []}

for topic, data in google_30d.items():
    sub(f"TOPIC: {topic.upper()} — 30-Day View")
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
header(f"2. REDDIT HOT POSTS | {DATE_LABEL}")
reddit_headers = {'User-Agent': 'TrendBot/1.0'}

for sub_name in SUBREDDITS:
    sub(f"r/{sub_name} — Top Posts This Week")
    try:
        res   = requests.get(f'https://www.reddit.com/r/{sub_name}/top.json?t=week&limit=7',
                             headers=reddit_headers, timeout=10)
        posts = res.json()['data']['children']
        for i, post in enumerate(posts, 1):
            d = post['data']
            log(f"   {i}. {d['title']}")
            log(f"      ⬆️  {d['score']} upvotes | 💬 {d['num_comments']} comments")
    except Exception as e:
        log(f"   ❌ Error: {e}")
    time.sleep(3)


# ──────────────────────────────────────────────────────────
# 3. YOUTUBE
# ──────────────────────────────────────────────────────────
header(f"3. YOUTUBE TRENDING VIDEOS | {DATE_LABEL}")
yt_queries = ['supplements 2026', 'biohacking 2026', 'health trends 2026', 'supplement ingredients 2026']

for query in yt_queries:
    sub(f"Search: {query}")
    try:
        results = VideosSearch(query, limit=5).result()['result']
        for i, v in enumerate(results, 1):
            views = v.get('viewCount', {}).get('text', 'N/A') if v.get('viewCount') else 'N/A'
            log(f"   {i}. {v['title']}")
            log(f"      👁  {views} | 🔗 {v['link']}")
    except Exception as e:
        log(f"   ❌ Error: {e}")
    time.sleep(2)


# ──────────────────────────────────────────────────────────
# 4. AMAZON BESTSELLERS
# ──────────────────────────────────────────────────────────
header(f"4. AMAZON BESTSELLERS — Vitamins & Supplements | {DATE_LABEL}")
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
            log(f"   #{i}. {name}")
    else:
        log("   ⚠️  Amazon blocked. Manual link:")
        log("   🔗 https://www.amazon.com/Best-Sellers-Vitamins-Supplements/zgbs/hpc/3764441")
except Exception as e:
    log(f"   ❌ Error: {e}")


# ──────────────────────────────────────────────────────────
# 5. WEEKLY ANALYSIS & COMMENTARY
# ──────────────────────────────────────────────────────────
header(f"5. WEEKLY ANALYSIS & COMMENTARY — {DATE_LABEL}")

if snapshots:
    # Count how many days each rising query appeared
    query_days   = {}
    query_values = {}
    for snap in snapshots:
        for topic, data in snap.get('google', {}).items():
            for item in data.get('rising', []):
                q = item['query'].lower()
                query_days[q]   = query_days.get(q, 0) + 1
                query_values[q] = max(query_values.get(q, 0), item['value'])

    # Sustained trends (appeared 3+ days)
    sustained = sorted(
        [(q, d, query_values[q]) for q, d in query_days.items() if d >= 3],
        key=lambda x: -x[1]
    )

    # New breakouts (only in latest snapshot, high %)
    latest_queries = set()
    if snapshots:
        for topic, data in snapshots[0].get('google', {}).items():
            for item in data.get('rising', []):
                latest_queries.add(item['query'].lower())

    older_queries = set()
    for snap in snapshots[1:]:
        for topic, data in snap.get('google', {}).items():
            for item in data.get('rising', []):
                older_queries.add(item['query'].lower())

    brand_new = [q for q in latest_queries if q not in older_queries]

    # Explosive growth (>1000% in 30d data)
    explosives = []
    for topic, data in google_30d.items():
        for item in data.get('rising', []):
            if item['value'] > 1000:
                explosives.append((item['query'], item['value'], topic))
    explosives.sort(key=lambda x: -x[1])

    # Cross-platform: appears in Google AND Reddit
    reddit_titles = []
    for snap in snapshots:
        for sub_name, posts in snap.get('reddit', {}).items():
            for post in posts:
                reddit_titles.append(post['title'].lower())

    cross_platform = []
    for topic, data in google_30d.items():
        for item in data.get('rising', []):
            q = item['query'].lower()
            if any(q in title for title in reddit_titles):
                cross_platform.append((item['query'], topic))

    # ── Print commentary ──
    log()
    log("🧠 SUSTAINED TRENDS (appeared 3+ days this week):")
    if sustained:
        for q, days, val in sustained[:8]:
            log(f"   • '{q}' — {days}/7 days | peak {val}%")
            if days >= 6:
                log(f"     → 🔥 Extremely consistent — strong underlying demand")
            elif days >= 4:
                log(f"     → 📈 Building momentum — worth creating content around this")
    else:
        log("   Not enough daily data yet — will populate after first full week")

    log()
    log("🚀 BRAND NEW THIS WEEK (just appeared, wasn't trending before):")
    if brand_new:
        for q in brand_new[:8]:
            log(f"   • '{q}'")
            log(f"     → 👀 Just broke — move fast, competition is low")
    else:
        log("   No brand-new breakouts detected this week")

    log()
    log("💥 EXPLOSIVE GROWTH (30-day, >1000% rise):")
    if explosives:
        for q, val, topic in explosives[:8]:
            log(f"   • '{q}' ({topic}) — +{val}%")
            if val > 50000:
                log(f"     → 🌋 Viral spike — investigate cause immediately")
            elif val > 5000:
                log(f"     → 🔥 Major breakout — strong content/product opportunity")
            else:
                log(f"     → 📊 Significant rise — monitor closely next week")
    else:
        log("   No explosive growth detected this week")

    log()
    log("🔗 CROSS-PLATFORM SIGNALS (trending on both Google & Reddit):")
    if cross_platform:
        for q, topic in cross_platform[:6]:
            log(f"   • '{q}' (Google: {topic} | also on Reddit)")
            log(f"     → ✅ Validated trend — real consumer interest, not just search curiosity")
    else:
        log("   No cross-platform signals detected this week")

    log()
    log("💡 THIS WEEK'S KEY TAKEAWAYS:")
    log("   Based on the data above, here's what to focus on:")
    log()
    if explosives:
        top_exp = explosives[0]
        log(f"   1. 🎯 IMMEDIATE OPPORTUNITY: '{top_exp[0]}' is your biggest breakout")
        log(f"      Create content/posts around this NOW while it's early")
    if sustained:
        top_sus = sustained[0]
        log(f"   2. 📌 STABLE BET: '{top_sus[0]}' has shown up {top_sus[1]} days straight")
        log(f"      This is a reliable topic with consistent audience interest")
    if brand_new:
        log(f"   3. 🆕 FIRST-MOVER EDGE: '{brand_new[0]}' just appeared this week")
        log(f"      Nobody has written about this yet — you could own the conversation")
    if cross_platform:
        log(f"   4. 💪 STRONGEST SIGNAL: '{cross_platform[0][0]}' is validated across platforms")
        log(f"      Multi-platform trends convert better — ads, content, or product angle")

else:
    log()
    log("   ℹ️  No daily snapshots found yet.")
    log("   Run trends_daily.py each day this week to unlock full analysis.")
    log("   This section will automatically populate with insights next Monday.")


# ──────────────────────────────────────────────────────────
# SAVE REPORT
# ──────────────────────────────────────────────────────────
analysis = {
    'explosives':    explosives    if snapshots else [],
    'brand_new':     brand_new     if snapshots else [],
    'sustained':     sustained     if snapshots else [],
    'cross_platform': cross_platform if snapshots else [],
}

weekly_snapshot = {
    'date':    TODAY,
    'reddit':  {sub_name: [] for sub_name in SUBREDDITS},
    'youtube': {},
    'amazon':  [],
}

# re-fetch Reddit week top for the HTML snapshot
reddit_headers = {'User-Agent': 'TrendBot/1.0'}
for sub_name in SUBREDDITS:
    try:
        res   = requests.get(f'https://www.reddit.com/r/{sub_name}/top.json?t=week&limit=7',
                             headers=reddit_headers, timeout=10)
        posts = res.json()['data']['children']
        weekly_snapshot['reddit'][sub_name] = [
            {'title': p['data']['title'], 'score': p['data']['score'], 'comments': p['data']['num_comments'], 'url': f"https://reddit.com{p['data']['permalink']}"}
            for p in posts
        ]
    except:
        pass
    time.sleep(2)

html_file = f'{REPORTS_DIR}/Weekly_Report_{TODAY}.html'
html = build_weekly_html(weekly_snapshot, google_30d, analysis)
with open(html_file, 'w') as f:
    f.write(html)

print()
print("=" * 60)
print(f"✅ Weekly report complete!")
print(f"   🌐 Saved to: {html_file}")
print("=" * 60)

os.system(f"open '{html_file}'")

# ── Publish to GitHub Pages ──
print("\n🚀 Publishing to GitHub Pages...")
os.system(f"""
cd /Users/dzulijanna/Documents/TrendsData && \
git add reports/ && \
git commit -m "Weekly report {TODAY}" && \
git push origin main
""")
print(f"✅ Published! View at: https://juliannabebre-sketch.github.io/trends-reports/")
