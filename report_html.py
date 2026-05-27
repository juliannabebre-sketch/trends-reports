"""
HTML Report Generator
Shared module used by trends_daily.py and trends_weekly.py
"""

from datetime import datetime

def badge(value, suffix="%"):
    """Color-coded badge based on growth %"""
    val = int(value) if str(value).isdigit() else 0
    if val > 10000:
        color = "#dc2626"; bg = "#fef2f2"; label = "🌋 VIRAL"
    elif val > 1000:
        color = "#ea580c"; bg = "#fff7ed"; label = "🔥 Explosive"
    elif val > 100:
        color = "#d97706"; bg = "#fffbeb"; label = "📈 Rising"
    else:
        color = "#059669"; bg = "#ecfdf5"; label = "↑ Growing"
    return f'<span style="background:{bg};color:{color};border:1px solid {color};padding:2px 8px;border-radius:12px;font-size:11px;font-weight:600;margin-right:6px;">{label}</span><span style="color:{color};font-weight:700">{value}{suffix}</span>'


def score_badge(score):
    """Reddit upvote badge"""
    return f'<span style="background:#fff7ed;color:#ea580c;border:1px solid #ea580c;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:600">⬆ {score:,}</span>'


CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #f0f4f8;
    color: #1a202c;
    line-height: 1.6;
}
.header {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
    color: white;
    padding: 48px 40px 36px;
    text-align: center;
}
.header h1 { font-size: 2rem; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 8px; }
.header .subtitle { font-size: 1rem; color: #94a3b8; margin-bottom: 16px; }
.header .meta {
    display: inline-flex; gap: 20px;
    background: rgba(255,255,255,0.08);
    border-radius: 30px; padding: 8px 24px;
    font-size: 13px; color: #cbd5e1;
}
.container { max-width: 1000px; margin: 0 auto; padding: 32px 20px; }
.platform-section {
    background: white; border-radius: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 16px rgba(0,0,0,0.04);
    margin-bottom: 28px; overflow: hidden;
}
.platform-header {
    display: flex; align-items: center; gap: 12px;
    padding: 18px 24px; font-weight: 700; font-size: 1rem;
    border-bottom: 1px solid #f1f5f9; color: white;
}
.platform-header .icon { font-size: 1.3rem; }
.platform-body { padding: 20px 24px; }
.topic-block { margin-bottom: 28px; }
.topic-block:last-child { margin-bottom: 0; }
.topic-title {
    font-size: 13px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.8px; color: #64748b; margin-bottom: 12px;
    display: flex; align-items: center; gap: 8px;
}
.topic-title::after {
    content: ''; flex: 1; height: 1px; background: #e2e8f0;
}
.col-label {
    font-size: 12px; font-weight: 600; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.6px;
    margin: 14px 0 8px;
}
.query-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 8px 12px; border-radius: 8px; margin-bottom: 4px;
    background: #f8fafc; border: 1px solid #f1f5f9;
    font-size: 14px;
}
.query-row:hover { background: #f1f5f9; }
.query-num { color: #94a3b8; font-size: 12px; width: 22px; flex-shrink: 0; }
.query-text { flex: 1; font-weight: 500; }
.reddit-post {
    padding: 12px 16px; border-radius: 10px; margin-bottom: 8px;
    border: 1px solid #f1f5f9; background: #fafafa;
}
.reddit-post:hover { background: #f1f5f9; }
.reddit-post-title { font-weight: 600; font-size: 14px; margin-bottom: 6px; }
.reddit-meta { display: flex; gap: 10px; font-size: 12px; color: #64748b; }
.yt-video {
    padding: 12px 16px; border-radius: 10px; margin-bottom: 8px;
    border: 1px solid #f1f5f9; background: #fafafa;
    display: flex; justify-content: space-between; align-items: flex-start;
}
.yt-video:hover { background: #f1f5f9; }
.yt-title { font-weight: 600; font-size: 14px; flex: 1; margin-right: 12px; }
.yt-link {
    font-size: 12px; color: #dc2626; text-decoration: none; font-weight: 600;
    white-space: nowrap;
}
.yt-views { font-size: 12px; color: #64748b; margin-top: 4px; }
.amz-item {
    padding: 8px 12px; border-radius: 8px; margin-bottom: 4px;
    background: #fafafa; border: 1px solid #f1f5f9; font-size: 14px;
    display: flex; align-items: center; gap: 10px;
}
.amz-rank {
    background: #ff9900; color: white; border-radius: 6px;
    padding: 2px 7px; font-size: 11px; font-weight: 700; flex-shrink: 0;
}
/* Commentary */
.insight-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
@media (max-width: 600px) { .insight-grid { grid-template-columns: 1fr; } }
.insight-card {
    border-radius: 12px; padding: 18px 20px;
    border-left: 4px solid;
}
.insight-card.viral   { background: #fef2f2; border-color: #dc2626; }
.insight-card.new     { background: #eff6ff; border-color: #3b82f6; }
.insight-card.steady  { background: #f0fdf4; border-color: #16a34a; }
.insight-card.cross   { background: #faf5ff; border-color: #7c3aed; }
.insight-card.tip     { background: #fffbeb; border-color: #d97706; }
.insight-title { font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
.insight-item { font-size: 13px; color: #374151; margin-bottom: 6px; }
.insight-note { font-size: 12px; color: #6b7280; font-style: italic; margin-top: 4px; }
.takeaway-section {
    background: linear-gradient(135deg, #0f172a, #1e3a5f);
    border-radius: 16px; padding: 28px 28px; margin-top: 8px;
    color: white;
}
.takeaway-section h2 { font-size: 1.1rem; margin-bottom: 18px; color: #e2e8f0; }
.takeaway-item {
    display: flex; gap: 14px; margin-bottom: 16px;
    background: rgba(255,255,255,0.06); border-radius: 10px; padding: 14px 16px;
}
.takeaway-num {
    background: #3b82f6; color: white; border-radius: 8px;
    width: 28px; height: 28px; display: flex; align-items: center;
    justify-content: center; font-weight: 700; font-size: 13px; flex-shrink: 0;
}
.takeaway-text { font-size: 14px; color: #e2e8f0; }
.takeaway-text strong { color: white; }
.footer {
    text-align: center; padding: 32px 20px; color: #94a3b8; font-size: 13px;
}
.no-data { color: #94a3b8; font-size: 13px; font-style: italic; padding: 8px 0; }
"""


def build_daily_html(snapshot):
    date_label = datetime.strptime(snapshot['date'], '%Y-%m-%d').strftime('%B %d, %Y')

    # ── Google Trends ──────────────────────────────────────
    google_html = ""
    for topic, data in snapshot.get('google', {}).items():
        rising_rows = ""
        for i, r in enumerate(data.get('rising', []), 1):
            rising_rows += f"""
            <div class="query-row">
                <span class="query-num">{i}</span>
                <span class="query-text">{r['query']}</span>
                <span>{badge(r['value'])}</span>
            </div>"""

        top_rows = ""
        for i, r in enumerate(data.get('top', []), 1):
            top_rows += f"""
            <div class="query-row">
                <span class="query-num">{i}</span>
                <span class="query-text">{r['query']}</span>
                <span style="color:#475569;font-size:13px;font-weight:600">{r['value']}</span>
            </div>"""

        google_html += f"""
        <div class="topic-block">
            <div class="topic-title">{topic}</div>
            <div class="col-label">🔥 Rising (going viral)</div>
            {rising_rows if rising_rows else '<div class="no-data">No data available</div>'}
            <div class="col-label">📊 Top Searches</div>
            {top_rows if top_rows else '<div class="no-data">No data available</div>'}
        </div>"""

    # ── Reddit ────────────────────────────────────────────
    reddit_html = ""
    for sub_name, posts in snapshot.get('reddit', {}).items():
        posts_html = ""
        for p in posts:
            posts_html += f"""
            <div class="reddit-post">
                <div class="reddit-post-title">{p['title']}</div>
                <div class="reddit-meta">
                    {score_badge(p['score'])}
                    <span>💬 {p['comments']:,} comments</span>
                </div>
            </div>"""
        reddit_html += f"""
        <div class="topic-block">
            <div class="topic-title">r/{sub_name}</div>
            {posts_html if posts_html else '<div class="no-data">No posts found</div>'}
        </div>"""

    # ── YouTube ───────────────────────────────────────────
    yt_html = ""
    for query, videos in snapshot.get('youtube', {}).items():
        vids_html = ""
        for v in videos:
            vids_html += f"""
            <div class="yt-video">
                <div>
                    <div class="yt-title">{v['title']}</div>
                    <div class="yt-views">👁 {v['views']}</div>
                </div>
                <a href="{v['link']}" target="_blank" class="yt-link">▶ Watch</a>
            </div>"""
        yt_html += f"""
        <div class="topic-block">
            <div class="topic-title">{query}</div>
            {vids_html if vids_html else '<div class="no-data">No videos found</div>'}
        </div>"""

    # ── Amazon ────────────────────────────────────────────
    amz_html = ""
    for i, name in enumerate(snapshot.get('amazon', []), 1):
        amz_html += f'<div class="amz-item"><span class="amz-rank">#{i}</span>{name}</div>'
    if not amz_html:
        amz_html = '<div class="no-data">Amazon data unavailable — <a href="https://www.amazon.com/Best-Sellers-Vitamins-Supplements/zgbs/hpc/3764441" target="_blank">view manually</a></div>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Daily Trends Report — {date_label}</title>
<style>{CSS}</style>
</head>
<body>
<div class="header">
  <h1>📊 Daily Trends Report</h1>
  <div class="subtitle">Health · Supplements · Biohacking · Ingredients</div>
  <div class="meta">
    <span>📅 {date_label}</span>
    <span>🇺🇸 US Market</span>
    <span>⏱ Last 7 Days</span>
  </div>
</div>
<div class="container">
  <div class="platform-section">
    <div class="platform-header" style="background:#4285f4">
      <span class="icon">🔵</span> Google Trends — Rising &amp; Top Searches
    </div>
    <div class="platform-body">{google_html}</div>
  </div>
  <div class="platform-section">
    <div class="platform-header" style="background:#ff4500">
      <span class="icon">🟠</span> Reddit Hot Posts
    </div>
    <div class="platform-body">{reddit_html}</div>
  </div>
  <div class="platform-section">
    <div class="platform-header" style="background:#dc2626">
      <span class="icon">🔴</span> YouTube Trending Videos
    </div>
    <div class="platform-body">{yt_html}</div>
  </div>
  <div class="platform-section">
    <div class="platform-header" style="background:#b45309">
      <span class="icon">🟡</span> Amazon Bestsellers — Vitamins &amp; Supplements
    </div>
    <div class="platform-body">{amz_html}</div>
  </div>
</div>
<div class="footer">Generated automatically · US Market · {date_label}</div>
</body>
</html>"""


def build_weekly_html(snapshot, google_30d, analysis):
    date_label = datetime.strptime(snapshot['date'], '%Y-%m-%d').strftime('%B %d, %Y')

    # ── Google 30-day ─────────────────────────────────────
    google_html = ""
    for topic, data in google_30d.items():
        rising_rows = ""
        for i, r in enumerate(data.get('rising', []), 1):
            rising_rows += f"""
            <div class="query-row">
                <span class="query-num">{i}</span>
                <span class="query-text">{r['query']}</span>
                <span>{badge(r['value'])}</span>
            </div>"""
        top_rows = ""
        for i, r in enumerate(data.get('top', []), 1):
            top_rows += f"""
            <div class="query-row">
                <span class="query-num">{i}</span>
                <span class="query-text">{r['query']}</span>
                <span style="color:#475569;font-size:13px;font-weight:600">{r['value']}</span>
            </div>"""
        google_html += f"""
        <div class="topic-block">
            <div class="topic-title">{topic}</div>
            <div class="col-label">🔥 Rising</div>
            {rising_rows if rising_rows else '<div class="no-data">No data</div>'}
            <div class="col-label">📊 Top Searches</div>
            {top_rows if top_rows else '<div class="no-data">No data</div>'}
        </div>"""

    # ── Reddit week top ───────────────────────────────────
    reddit_html = ""
    for sub_name, posts in snapshot.get('reddit', {}).items():
        posts_html = ""
        for p in posts:
            posts_html += f"""
            <div class="reddit-post">
                <div class="reddit-post-title">{p['title']}</div>
                <div class="reddit-meta">{score_badge(p['score'])}<span>💬 {p['comments']:,} comments</span></div>
            </div>"""
        reddit_html += f'<div class="topic-block"><div class="topic-title">r/{sub_name}</div>{posts_html}</div>'

    # ── YouTube ───────────────────────────────────────────
    yt_html = ""
    for query, videos in snapshot.get('youtube', {}).items():
        vids_html = "".join(f"""
            <div class="yt-video">
                <div><div class="yt-title">{v['title']}</div><div class="yt-views">👁 {v['views']}</div></div>
                <a href="{v['link']}" target="_blank" class="yt-link">▶ Watch</a>
            </div>""" for v in videos)
        yt_html += f'<div class="topic-block"><div class="topic-title">{query}</div>{vids_html}</div>'

    # ── Amazon ────────────────────────────────────────────
    amz_html = "".join(f'<div class="amz-item"><span class="amz-rank">#{i}</span>{n}</div>'
                       for i, n in enumerate(snapshot.get('amazon', []), 1))
    if not amz_html:
        amz_html = '<div class="no-data">Amazon data unavailable — <a href="https://www.amazon.com/Best-Sellers-Vitamins-Supplements/zgbs/hpc/3764441" target="_blank">view manually</a></div>'

    # ── Commentary cards ──────────────────────────────────
    def insight_items(items, note_fn):
        if not items:
            return '<div class="no-data">Not enough data yet — check back next week</div>'
        html = ""
        for item in items[:6]:
            html += f'<div class="insight-item">• {item[0]}</div>'
            html += f'<div class="insight-note">{note_fn(item)}</div>'
        return html

    viral_items = insight_items(
        analysis.get('explosives', []),
        lambda x: f'+{x[1]:,}% in {x[2]} — investigate the cause immediately'
    )
    new_items = ""
    for q in analysis.get('brand_new', [])[:6]:
        new_items += f'<div class="insight-item">• {q}</div><div class="insight-note">Just broke — low competition, move fast</div>'
    if not new_items:
        new_items = '<div class="no-data">No brand-new breakouts this week</div>'

    sustained_items = insight_items(
        analysis.get('sustained', []),
        lambda x: f'Appeared {x[1]}/7 days — consistent demand'
    )
    cross_items = ""
    for q, topic in analysis.get('cross_platform', [])[:6]:
        cross_items += f'<div class="insight-item">• {q}</div><div class="insight-note">Trending on Google ({topic}) + Reddit — validated signal</div>'
    if not cross_items:
        cross_items = '<div class="no-data">No cross-platform signals this week</div>'

    # ── Key Takeaways ─────────────────────────────────────
    takeaways = []
    if analysis.get('explosives'):
        q = analysis['explosives'][0]
        takeaways.append(f'<strong>🎯 Immediate opportunity:</strong> "{q[0]}" is your biggest breakout (+{q[1]:,}%). Create content or an ad angle around this NOW.')
    if analysis.get('sustained'):
        q = analysis['sustained'][0]
        takeaways.append(f'<strong>📌 Stable bet:</strong> "{q[0]}" appeared {q[1]}/7 days. Reliable demand — good for evergreen content or paid ads.')
    if analysis.get('brand_new'):
        q = analysis['brand_new'][0]
        takeaways.append(f'<strong>🆕 First-mover edge:</strong> "{q}" just appeared this week. Nobody has written about it yet.')
    if analysis.get('cross_platform'):
        q = analysis['cross_platform'][0]
        takeaways.append(f'<strong>💪 Strongest signal:</strong> "{q[0]}" is trending on both Google and Reddit. Multi-platform trends convert better.')

    if not takeaways:
        takeaways = ['<strong>ℹ️ Building data:</strong> Run the daily script each day this week to unlock full analysis next Monday.']

    takeaway_html = "".join(f'<div class="takeaway-item"><div class="takeaway-num">{i+1}</div><div class="takeaway-text">{t}</div></div>'
                            for i, t in enumerate(takeaways))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Weekly Trends Report — {date_label}</title>
<style>{CSS}</style>
</head>
<body>
<div class="header">
  <h1>📈 Weekly Trends Report</h1>
  <div class="subtitle">Health · Supplements · Biohacking · Ingredients</div>
  <div class="meta">
    <span>📅 {date_label}</span>
    <span>🇺🇸 US Market</span>
    <span>📆 Last 30 Days</span>
  </div>
</div>
<div class="container">

  <!-- Google Trends -->
  <div class="platform-section">
    <div class="platform-header" style="background:#4285f4">
      <span class="icon">🔵</span> Google Trends — 30-Day Overview
    </div>
    <div class="platform-body">{google_html}</div>
  </div>

  <!-- Reddit -->
  <div class="platform-section">
    <div class="platform-header" style="background:#ff4500">
      <span class="icon">🟠</span> Reddit — Top Posts This Week
    </div>
    <div class="platform-body">{reddit_html}</div>
  </div>

  <!-- YouTube -->
  <div class="platform-section">
    <div class="platform-header" style="background:#dc2626">
      <span class="icon">🔴</span> YouTube Trending Videos
    </div>
    <div class="platform-body">{yt_html}</div>
  </div>

  <!-- Amazon -->
  <div class="platform-section">
    <div class="platform-header" style="background:#b45309">
      <span class="icon">🟡</span> Amazon Bestsellers — Vitamins &amp; Supplements
    </div>
    <div class="platform-body">{amz_html}</div>
  </div>

  <!-- Commentary -->
  <div class="platform-section">
    <div class="platform-header" style="background:#7c3aed">
      <span class="icon">🧠</span> Weekly Analysis &amp; Commentary
    </div>
    <div class="platform-body">
      <div class="insight-grid">
        <div class="insight-card viral">
          <div class="insight-title">💥 Explosive Growth</div>
          {viral_items}
        </div>
        <div class="insight-card new">
          <div class="insight-title">🚀 Brand New This Week</div>
          {new_items}
        </div>
        <div class="insight-card steady">
          <div class="insight-title">📅 Sustained Trends (3+ days)</div>
          {sustained_items}
        </div>
        <div class="insight-card cross">
          <div class="insight-title">🔗 Cross-Platform Signals</div>
          {cross_items}
        </div>
      </div>
    </div>
  </div>

  <!-- Takeaways -->
  <div class="takeaway-section">
    <h2>💡 This Week's Key Takeaways</h2>
    {takeaway_html}
  </div>

</div>
<div class="footer">Generated automatically · US Market · {date_label}</div>
</body>
</html>"""
