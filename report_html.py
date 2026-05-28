"""
HTML Report Generator — Redesigned
Shared module used by trends_daily.py and trends_weekly.py
"""

from datetime import datetime, timedelta

def get_timeframe_label(period):
    """Returns human-readable date range for a given period code"""
    today = datetime.now()
    if period == 'now 7-d':
        start = today - timedelta(days=7)
        return f"{start.strftime('%b %d')} – {today.strftime('%b %d, %Y')}", "Last 7 Days"
    elif period == 'today 1-m':
        start = today - timedelta(days=30)
        return f"{start.strftime('%b %d')} – {today.strftime('%b %d, %Y')}", "Last 30 Days"
    elif period == 'today 3-m':
        start = today - timedelta(days=90)
        return f"{start.strftime('%b %d')} – {today.strftime('%b %d, %Y')}", "Last 90 Days"
    elif period == 'today 12-m':
        start = today - timedelta(days=365)
        return f"{start.strftime('%b %Y')} – {today.strftime('%b %Y')}", "Last 12 Months"
    return today.strftime('%B %d, %Y'), "Custom Period"


def growth_bar(value):
    """Visual percentage bar for growth"""
    try:
        val = int(str(value).replace('%','').replace(',',''))
    except:
        val = 0
    if val > 10000:
        color = "#dc2626"; label = "🌋 Viral"; width = 100
    elif val > 1000:
        color = "#ea580c"; label = "🔥 Explosive"; width = 85
    elif val > 500:
        color = "#d97706"; label = "⚡ Surging"; width = 70
    elif val > 100:
        color = "#65a30d"; label = "📈 Rising"; width = 50
    else:
        color = "#2563eb"; label = "↑ Growing"; width = 30
    return f"""
    <div style="display:flex;align-items:center;gap:10px;min-width:180px">
      <div style="flex:1;height:5px;background:#f1f5f9;border-radius:10px;overflow:hidden">
        <div style="width:{width}%;height:100%;background:{color};border-radius:10px;"></div>
      </div>
      <span style="font-size:11px;font-weight:700;color:{color};white-space:nowrap">+{value}%</span>
      <span style="font-size:10px;background:{color}18;color:{color};padding:2px 7px;border-radius:8px;font-weight:600;white-space:nowrap">{label}</span>
    </div>"""


def is_viral(value):
    try:
        return int(str(value).replace('%','').replace(',','')) >= 500
    except:
        return False


def viral_links(query):
    """Returns Google News + Google Trends links for a query"""
    q_enc = query.replace(' ', '+')
    news_url   = f"https://news.google.com/search?q={q_enc}&hl=en-US&gl=US&ceid=US:en"
    trends_url = f"https://trends.google.com/trends/explore?q={q_enc}&geo=US"
    return news_url, trends_url


def score_pill(score, comments):
    return f"""<span style="display:inline-flex;align-items:center;gap:4px;background:#fff7ed;color:#c2410c;border:1px solid #fed7aa;padding:3px 10px;border-radius:10px;font-size:11px;font-weight:700">⬆ {score:,}</span>
    <span style="display:inline-flex;align-items:center;gap:4px;background:#f0f9ff;color:#0369a1;border:1px solid #bae6fd;padding:3px 10px;border-radius:10px;font-size:11px;font-weight:700">💬 {comments:,}</span>"""


FONTS = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">'

BASE_CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: #f1f5f9; color: #0f172a; line-height: 1.6;
}

/* HERO */
.hero {
  background: #0f172a;
  position: relative; overflow: hidden;
  padding: 56px 24px 48px; text-align: center;
}
.hero::before {
  content:''; position:absolute; inset:0;
  background:
    radial-gradient(ellipse 70% 80% at 15% 50%, rgba(124,58,237,0.22) 0%, transparent 55%),
    radial-gradient(ellipse 60% 70% at 85% 50%, rgba(37,99,235,0.18) 0%, transparent 55%),
    radial-gradient(ellipse 40% 40% at 50% 100%, rgba(16,185,129,0.1) 0%, transparent 50%);
}
.hero::after {
  content:''; position:absolute; bottom:0; left:0; right:0; height:1px;
  background: linear-gradient(90deg, transparent, rgba(124,58,237,0.6), rgba(37,99,235,0.6), transparent);
}
.hero-inner { position:relative; z-index:1; max-width:680px; margin:0 auto; }
.report-type-badge {
  display:inline-flex; align-items:center; gap:6px;
  font-size:11px; font-weight:700; letter-spacing:0.8px; text-transform:uppercase;
  padding:5px 16px; border-radius:20px; margin-bottom:20px;
}
.badge-weekly { background:rgba(124,58,237,0.15); border:1px solid rgba(124,58,237,0.35); color:#c4b5fd; }
.badge-daily  { background:rgba(37,99,235,0.15);  border:1px solid rgba(37,99,235,0.35);  color:#93c5fd; }
.badge-annual { background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.35); color:#6ee7b7; }
.hero h1 {
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  font-weight: 900; letter-spacing: -1px; color: white;
  line-height: 1.1; margin-bottom: 12px;
}
.hero h1 em {
  font-style: normal;
  background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub { color: #94a3b8; font-size: 15px; margin-bottom: 28px; }

/* TIMEFRAME BLOCK */
.timeframe-block {
  display: inline-flex; align-items: stretch;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 14px; overflow: hidden; margin-bottom: 24px;
}
.tf-segment {
  padding: 12px 20px; text-align: center;
  border-right: 1px solid rgba(255,255,255,0.08);
}
.tf-segment:last-child { border-right: none; }
.tf-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: #475569; margin-bottom: 3px; }
.tf-value { font-size: 14px; font-weight: 700; color: white; }
.tf-value.accent { color: #a78bfa; }

/* TOPIC TAGS */
.hero-topics {
  display: flex; flex-wrap: wrap; justify-content: center; gap: 7px;
}
.topic-tag {
  background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.1);
  color: #cbd5e1; font-size: 12px; font-weight: 500;
  padding: 5px 13px; border-radius: 20px;
}

/* PLATFORM TABS */
.platform-nav {
  background: white; border-bottom: 1px solid #e2e8f0;
  display: flex; overflow-x: auto; gap: 0;
  padding: 0 24px;
}
.platform-nav::-webkit-scrollbar { display: none; }
.nav-tab {
  display: flex; align-items: center; gap: 7px;
  padding: 14px 20px; font-size: 13px; font-weight: 600;
  color: #64748b; border-bottom: 2px solid transparent;
  white-space: nowrap; cursor: pointer; transition: all 0.15s;
  text-decoration: none;
}
.nav-tab:hover { color: #1e293b; }
.nav-tab.active { color: #7c3aed; border-bottom-color: #7c3aed; }

/* LAYOUT */
.container { max-width: 960px; margin: 0 auto; padding: 36px 20px 60px; }

/* SECTION */
.section {
  background: white; border-radius: 22px; overflow: hidden;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05), 0 8px 24px rgba(0,0,0,0.05);
  margin-bottom: 24px; border: 1px solid #e2e8f0;
}
.section-head {
  display: flex; align-items: center; gap: 14px;
  padding: 20px 26px; border-bottom: 1px solid rgba(0,0,0,0.05);
}
.section-icon {
  width: 42px; height: 42px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.section-info { flex: 1; }
.section-title { font-size: 16px; font-weight: 800; color: #0f172a; letter-spacing: -0.3px; }
.section-desc  { font-size: 12px; color: #94a3b8; margin-top: 2px; font-weight: 500; }
.section-badge {
  font-size: 11px; font-weight: 700; padding: 5px 14px;
  border-radius: 20px; white-space: nowrap; letter-spacing: 0.3px;
}
.section-body { padding: 22px 26px; }

/* COLOR THEMES */
.theme-google .section-head { background: linear-gradient(135deg, #eff6ff, #dbeafe); }
.theme-google .section-icon { background: #dbeafe; }
.theme-google .section-badge { background: #dbeafe; color: #1d4ed8; }

.theme-reddit .section-head { background: linear-gradient(135deg, #fff7ed, #ffedd5); }
.theme-reddit .section-icon { background: #ffedd5; }
.theme-reddit .section-badge { background: #ffedd5; color: #c2410c; }

.theme-youtube .section-head { background: linear-gradient(135deg, #fef2f2, #fee2e2); }
.theme-youtube .section-icon { background: #fee2e2; }
.theme-youtube .section-badge { background: #fee2e2; color: #dc2626; }

.theme-amazon .section-head { background: linear-gradient(135deg, #fffbeb, #fef3c7); }
.theme-amazon .section-icon { background: #fef3c7; }
.theme-amazon .section-badge { background: #fef3c7; color: #b45309; }

.theme-insights .section-head { background: linear-gradient(135deg, #faf5ff, #ede9fe); }
.theme-insights .section-icon { background: #ede9fe; }
.theme-insights .section-badge { background: #ede9fe; color: #7c3aed; }

/* TOPIC BLOCK */
.topic-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
@media(max-width:640px){ .topic-grid { grid-template-columns: 1fr; } }
.topic-block {
  background: white; border-radius: 16px; padding: 18px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.topic-name {
  font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px;
  color: #7c3aed; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;
}
.topic-name::after { content:''; flex:1; height:1px; background:#ede9fe; }
.col-head {
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.6px; color: #94a3b8; margin: 12px 0 7px;
  display: flex; align-items: center; gap: 6px;
}
.col-head::after { content:''; flex:1; height:1px; background:#f1f5f9; }

/* QUERY ROWS */
.query-row {
  display: flex; align-items: center; gap: 10px;
  padding: 9px 12px; border-radius: 10px; margin-bottom: 5px;
  background: #f8fafc; border: 1px solid #f1f5f9; transition: all 0.15s;
  text-decoration: none; color: inherit;
}
.query-row:hover { background: #eff6ff; border-color: #bfdbfe; transform: translateX(2px); }

/* VIRAL ROW — clickable with glow */
a.query-row.viral-row {
  background: linear-gradient(135deg, #fff5f5, #fff7ed);
  border: 1.5px solid #fca5a5;
  cursor: pointer; position: relative;
}
a.query-row.viral-row:hover {
  background: linear-gradient(135deg, #fef2f2, #fff7ed);
  border-color: #f87171;
  transform: translateX(3px);
  box-shadow: 0 4px 14px rgba(220,38,38,0.12);
}
a.query-row.explosive-row {
  background: linear-gradient(135deg, #fff7ed, #fffbeb);
  border: 1.5px solid #fb923c;
}
a.query-row.explosive-row:hover {
  border-color: #f97316;
  box-shadow: 0 4px 14px rgba(249,115,22,0.12);
  transform: translateX(3px);
}
.why-btn {
  display: inline-flex; align-items: center; gap: 4px;
  font-size: 11px; font-weight: 700; padding: 4px 10px;
  border-radius: 8px; white-space: nowrap; flex-shrink: 0;
  text-decoration: none; transition: all 0.15s;
}
.why-news { background: #fef2f2; color: #dc2626; border: 1px solid #fca5a5; }
.why-news:hover { background: #dc2626; color: white; }
.why-trends { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; margin-left: 4px; }
.why-trends:hover { background: #2563eb; color: white; }
.viral-pulse {
  width: 8px; height: 8px; border-radius: 50%; background: #dc2626;
  flex-shrink: 0; animation: vpulse 1.5s ease-in-out infinite;
}
@keyframes vpulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(1.4)} }

.q-num {
  color: #c7d2fe; font-size: 11px; font-weight: 800; width: 20px;
  flex-shrink: 0; text-align: center;
}
.q-text { flex: 1; font-size: 13px; font-weight: 600; color: #1e293b; }
.q-score {
  font-size: 12px; font-weight: 700; color: #4f46e5;
  background: #eef2ff; padding: 2px 8px; border-radius: 6px;
}

/* BACK TO HOME LINK */
.back-bar {
  background: #0f172a; padding: 12px 28px;
  display: flex; align-items: center; justify-content: space-between;
}
.back-link {
  display: inline-flex; align-items: center; gap: 8px;
  color: #94a3b8; font-size: 13px; font-weight: 600;
  text-decoration: none; transition: color 0.15s;
}
.back-link:hover { color: #a78bfa; }
.back-site { color: #475569; font-size: 12px; }

/* REDDIT CARDS */
.reddit-card {
  padding: 14px 16px; border-radius: 12px; margin-bottom: 8px;
  border: 1px solid #e2e8f0; background: white; transition: all 0.2s;
  text-decoration: none; color: inherit; display: block;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.reddit-card:hover {
  background: #fff7ed; border-color: #fb923c;
  box-shadow: 0 4px 14px rgba(251,146,60,0.15);
  transform: translateY(-1px);
}
.reddit-card-inner { display: flex; gap: 12px; align-items: flex-start; }
.reddit-icon {
  width: 36px; height: 36px; background: #ff4500; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; flex-shrink: 0; color: white; font-weight: 800;
}
.reddit-body { flex: 1; }
.reddit-title { font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 8px; line-height: 1.45; }
.reddit-card:hover .reddit-title { color: #c2410c; }
.reddit-meta { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.reddit-arrow { color: #94a3b8; font-size: 16px; align-self: center; flex-shrink: 0; transition: transform 0.2s; }
.reddit-card:hover .reddit-arrow { transform: translateX(3px); color: #c2410c; }

/* YOUTUBE CARDS */
.yt-card {
  display: flex; justify-content: space-between; align-items: center;
  padding: 14px 16px; border-radius: 12px; margin-bottom: 8px;
  border: 1px solid #f1f5f9; background: #fafafa; transition: all 0.15s;
  gap: 12px;
}
.yt-card:hover { background: #fef2f2; border-color: #fecaca; }
.yt-info { flex: 1; }
.yt-title { font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 4px; line-height: 1.4; }
.yt-views { font-size: 12px; color: #64748b; }
.yt-btn {
  display: inline-flex; align-items: center; gap: 5px;
  background: #dc2626; color: white; padding: 7px 14px;
  border-radius: 8px; font-size: 12px; font-weight: 700;
  text-decoration: none; white-space: nowrap; flex-shrink: 0;
  transition: background 0.15s;
}
.yt-btn:hover { background: #b91c1c; }

/* AMAZON */
.amz-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 10px; }
.amz-card {
  background: white; border: 1px solid #e2e8f0; border-radius: 14px;
  padding: 14px 16px; display: flex; align-items: flex-start; gap: 12px;
  transition: all 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.amz-card:hover {
  background: #fffbeb; border-color: #fbbf24;
  box-shadow: 0 4px 12px rgba(251,191,36,0.15);
  transform: translateY(-1px);
}
.amz-rank {
  background: linear-gradient(135deg, #ff9900, #f59e0b);
  color: white; border-radius: 8px;
  width: 30px; height: 30px; display: flex; align-items: center;
  justify-content: center; font-size: 12px; font-weight: 800; flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(255,153,0,0.3);
}
.amz-name { font-size: 13px; font-weight: 600; color: #1e293b; line-height: 1.4; }

/* INSIGHT CARDS */
.insight-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
@media(max-width:600px){ .insight-grid { grid-template-columns: 1fr; } }
.insight-card {
  border-radius: 14px; padding: 18px 20px;
  border: 1.5px solid;
}
.ic-viral  { background:#fef2f2; border-color:#fca5a5; }
.ic-new    { background:#eff6ff; border-color:#93c5fd; }
.ic-steady { background:#f0fdf4; border-color:#86efac; }
.ic-cross  { background:#faf5ff; border-color:#c4b5fd; }
.ic-title {
  font-size: 12px; font-weight: 800; text-transform: uppercase;
  letter-spacing: 0.6px; margin-bottom: 10px;
  display: flex; align-items: center; gap: 6px;
}
.ic-viral  .ic-title { color: #dc2626; }
.ic-new    .ic-title { color: #2563eb; }
.ic-steady .ic-title { color: #16a34a; }
.ic-cross  .ic-title { color: #7c3aed; }
.ic-item { font-size: 13px; color: #374151; margin-bottom: 4px; font-weight: 600; }
.ic-note { font-size: 11px; color: #6b7280; font-style: italic; margin-bottom: 8px; line-height: 1.4; }

/* TAKEAWAYS */
.takeaway-box {
  background: linear-gradient(135deg, #0f172a, #1e1b4b);
  border-radius: 20px; padding: 28px; margin-top: 8px;
  border: 1px solid rgba(124,58,237,0.2);
}
.takeaway-box h3 { color: #e2e8f0; font-size: 14px; font-weight: 800; margin-bottom: 16px; }
.takeaway-item {
  display: flex; gap: 14px; margin-bottom: 12px;
  background: rgba(255,255,255,0.05); border-radius: 12px; padding: 14px;
  border: 1px solid rgba(255,255,255,0.06);
}
.t-num {
  width: 28px; height: 28px; background: linear-gradient(135deg, #7c3aed, #2563eb);
  border-radius: 8px; display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 800; color: white; flex-shrink: 0;
}
.t-text { font-size: 13px; color: #cbd5e1; line-height: 1.5; }
.t-text strong { color: white; }

/* QUERY BLOCK (full width) */
.query-full {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 14px; border-radius: 10px; margin-bottom: 6px;
  background: white; border: 1px solid #f1f5f9;
}
.query-full:hover { background: #f8fafc; }

.no-data { font-size: 13px; color: #94a3b8; font-style: italic; padding: 12px 0; }

/* FOOTER */
.footer {
  background: #0f172a; color: #334155;
  text-align: center; padding: 36px 24px; font-size: 12px;
}
.footer-brand {
  font-size: 15px; font-weight: 800; margin-bottom: 6px;
  background: linear-gradient(135deg, #a78bfa, #60a5fa);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.footer-links { display: flex; justify-content: center; gap: 20px; margin-top: 14px; flex-wrap: wrap; }
.footer-links a { color: #334155; text-decoration: none; transition: color 0.15s; }
.footer-links a:hover { color: #94a3b8; }
"""


def _google_topics_html(google_data):
    html = '<div class="topic-grid">'
    for topic, data in google_data.items():
        rising_rows = ""
        for i, r in enumerate(data.get('rising', []), 1):
            q     = r['query']
            val   = r['value']
            viral = is_viral(val)
            news_url, trends_url = viral_links(q)

            try:
                v = int(str(val).replace('%','').replace(',',''))
            except:
                v = 0

            if v >= 10000:
                row_class = "query-row viral-row"
            elif v >= 500:
                row_class = "query-row explosive-row"
            else:
                row_class = "query-row"

            if viral:
                rising_rows += f"""
                <a class="{row_class}" href="{news_url}" target="_blank" rel="noopener">
                  <span class="viral-pulse"></span>
                  <span class="q-num">{i}</span>
                  <span class="q-text">{q}</span>
                  {growth_bar(val)}
                  <a class="why-btn why-news" href="{news_url}" target="_blank" onclick="event.stopPropagation()">📰 Why?</a>
                  <a class="why-btn why-trends" href="{trends_url}" target="_blank" onclick="event.stopPropagation()">📊 Trends</a>
                </a>"""
            else:
                rising_rows += f"""
                <div class="query-row">
                  <span class="q-num">{i}</span>
                  <span class="q-text">{q}</span>
                  {growth_bar(val)}
                </div>"""

        top_rows = ""
        for i, r in enumerate(data.get('top', []), 1):
            top_rows += f"""
            <div class="query-row">
              <span class="q-num">{i}</span>
              <span class="q-text">{r['query']}</span>
              <span class="q-score">{r['value']}</span>
            </div>"""

        html += f"""
        <div class="topic-block">
          <div class="topic-name">{topic}</div>
          <div class="col-head">🔥 Rising</div>
          {rising_rows or '<div class="no-data">No data</div>'}
          <div class="col-head">📊 Top Searches</div>
          {top_rows or '<div class="no-data">No data</div>'}
        </div>"""
    html += '</div>'
    return html


def _reddit_html(reddit_data):
    html = ""
    for sub_name, posts in reddit_data.items():
        cards = ""
        for i, p in enumerate(posts, 1):
            url = p.get('url', f'https://reddit.com/r/{sub_name}')
            cards += f"""
            <a class="reddit-card" href="{url}" target="_blank" rel="noopener">
              <div class="reddit-card-inner">
                <div class="reddit-icon">r/</div>
                <div class="reddit-body">
                  <div class="reddit-title">{p['title']}</div>
                  <div class="reddit-meta">{score_pill(p['score'], p['comments'])}</div>
                </div>
                <span class="reddit-arrow">→</span>
              </div>
            </a>"""
        html += f"""
        <div style="margin-bottom:28px">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px">
            <span style="background:#ff4500;color:white;font-size:11px;font-weight:800;padding:3px 10px;border-radius:8px">r/{sub_name}</span>
            <span style="font-size:11px;color:#94a3b8">Click any post to open on Reddit →</span>
          </div>
          {cards or '<div class="no-data">No posts found</div>'}
        </div>"""
    return html


def _youtube_html(youtube_data):
    html = ""
    for query, videos in youtube_data.items():
        cards = ""
        for v in videos:
            cards += f"""
            <div class="yt-card">
              <div class="yt-info">
                <div class="yt-title">{v['title']}</div>
                <div class="yt-views">👁 {v['views']}</div>
              </div>
              <a href="{v['link']}" target="_blank" class="yt-btn">▶ Watch</a>
            </div>"""
        html += f"""
        <div style="margin-bottom:24px">
          <div style="font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:0.8px;color:#dc2626;margin-bottom:10px">{query}</div>
          {cards or '<div class="no-data">No videos found</div>'}
        </div>"""
    return html


def _amazon_html(amazon_data):
    if not amazon_data:
        return '<div class="no-data">Amazon data unavailable — <a href="https://www.amazon.com/Best-Sellers-Vitamins-Supplements/zgbs/hpc/3764441" target="_blank">view manually →</a></div>'
    cards = ""
    for i, name in enumerate(amazon_data, 1):
        cards += f'<div class="amz-card"><div class="amz-rank">#{i}</div><div class="amz-name">{name}</div></div>'
    return f'<div class="amz-grid">{cards}</div>'


def _hero(badge_class, badge_text, title_main, title_accent, subtitle, period_code, date_str, topics):
    date_range, period_label = get_timeframe_label(period_code)
    topics_html = "".join(f'<span class="topic-tag">{t}</span>' for t in topics)
    return f"""
<div class="hero">
  <div class="hero-inner">
    <div class="report-type-badge {badge_class}">{badge_text}</div>
    <h1>{title_main} <em>{title_accent}</em></h1>
    <p class="hero-sub">{subtitle}</p>
    <div class="timeframe-block">
      <div class="tf-segment">
        <div class="tf-label">Period</div>
        <div class="tf-value accent">{period_label}</div>
      </div>
      <div class="tf-segment">
        <div class="tf-label">Date Range</div>
        <div class="tf-value">{date_range}</div>
      </div>
      <div class="tf-segment">
        <div class="tf-label">Published</div>
        <div class="tf-value">{date_str}</div>
      </div>
      <div class="tf-segment">
        <div class="tf-label">Market</div>
        <div class="tf-value">🇺🇸 US</div>
      </div>
    </div>
    <div class="hero-topics">{topics_html}</div>
  </div>
</div>"""


def _section(theme, icon, title, desc, badge_text, body_html):
    return f"""
<div class="section theme-{theme}">
  <div class="section-head">
    <div class="section-icon">{icon}</div>
    <div class="section-info">
      <div class="section-title">{title}</div>
      <div class="section-desc">{desc}</div>
    </div>
    <span class="section-badge">{badge_text}</span>
  </div>
  <div class="section-body">{body_html}</div>
</div>"""


def _page(title, hero_html, sections_html, footer_note):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
{FONTS}
<style>{BASE_CSS}</style>
</head>
<body>
<div class="back-bar">
  <a class="back-link" href="https://juliannabebre-sketch.github.io/trends-reports/">
    ← All Reports
  </a>
  <span class="back-site">🇺🇸 US Market Intelligence</span>
</div>
{hero_html}
<div class="container">
{sections_html}
</div>
<div class="footer">
  <div class="footer-brand">Trends Intelligence</div>
  <div>{footer_note}</div>
  <div class="footer-links">
    <a href="https://juliannabebre-sketch.github.io/trends-reports/">← All Reports</a>
    <a href="https://trends.google.com" target="_blank">Google Trends</a>
    <a href="https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pWVXlnQVAB" target="_blank">Google News: Health</a>
    <a href="https://reddit.com/r/supplements" target="_blank">r/supplements</a>
    <a href="https://reddit.com/r/biohacking" target="_blank">r/biohacking</a>
  </div>
</div>
</body>
</html>"""


# ─────────────────────────────────────────────────────────
# PUBLIC: BUILD DAILY HTML
# ─────────────────────────────────────────────────────────
def build_daily_html(snapshot, period='now 7-d'):
    date_str   = datetime.strptime(snapshot['date'], '%Y-%m-%d').strftime('%B %d, %Y')
    _, p_label = get_timeframe_label(period)

    hero = _hero(
        'badge-daily', f'📊 Daily Snapshot',
        'Daily Trends', 'Snapshot',
        'What\'s trending today across Google, Reddit, YouTube & Amazon.',
        period, date_str,
        ['🌿 Health', '💊 Supplements', '⚡ Biohacking', '🔬 Ingredients']
    )

    google_sec = _section('google','🔵','Google Trends',
        f'Rising & top search queries · {p_label} · US Market',
        p_label, _google_topics_html(snapshot.get('google',{})))

    reddit_sec = _section('reddit','🟠','Reddit Hot Posts',
        'Top posts from r/supplements · r/biohacking · r/health',
        'This Week', _reddit_html(snapshot.get('reddit',{})))

    youtube_sec = _section('youtube','🔴','YouTube Trending',
        'Most relevant videos for your topics right now',
        'Latest', _youtube_html(snapshot.get('youtube',{})))

    amazon_sec = _section('amazon','🟡','Amazon Bestsellers',
        'Top-selling vitamins & supplements · US store',
        'Bestsellers', _amazon_html(snapshot.get('amazon',[])))

    return _page(
        f'Daily Trends — {date_str}',
        hero,
        google_sec + reddit_sec + youtube_sec + amazon_sec,
        f'Daily snapshot · US Market · {date_str}'
    )


# ─────────────────────────────────────────────────────────
# PUBLIC: BUILD WEEKLY HTML
# ─────────────────────────────────────────────────────────
def build_weekly_html(snapshot, google_30d, analysis, period='today 1-m'):
    date_str   = datetime.strptime(snapshot['date'], '%Y-%m-%d').strftime('%B %d, %Y')
    _, p_label = get_timeframe_label(period)

    hero = _hero(
        'badge-weekly', '📈 Weekly Report',
        'Weekly Trends', 'Report',
        '30-day overview with AI analysis — what\'s rising, sustained, and going viral.',
        period, date_str,
        ['🌿 Health', '💊 Supplements', '⚡ Biohacking', '🔬 Ingredients']
    )

    google_sec = _section('google','🔵','Google Trends',
        f'Rising & top search queries · {p_label} · US Market',
        p_label, _google_topics_html(google_30d))

    reddit_sec = _section('reddit','🟠','Reddit — Top Posts This Week',
        'Highest-rated posts from r/supplements · r/biohacking · r/health',
        'Top of Week', _reddit_html(snapshot.get('reddit',{})))

    youtube_sec = _section('youtube','🔴','YouTube Trending',
        'Most relevant videos for your topics',
        'Latest', _youtube_html(snapshot.get('youtube',{})))

    amazon_sec = _section('amazon','🟡','Amazon Bestsellers',
        'Top-selling vitamins & supplements · US store',
        'Bestsellers', _amazon_html(snapshot.get('amazon',[])))

    # ── Insight cards ──
    def ic_items(items, note_fn):
        if not items:
            return '<div class="no-data">Not enough data yet — check back next week</div>'
        out = ""
        for item in items[:5]:
            out += f'<div class="ic-item">• {item[0]}</div>'
            out += f'<div class="ic-note">{note_fn(item)}</div>'
        return out

    viral_html = ic_items(analysis.get('explosives',[]),
        lambda x: f'+{x[1]:,}% in {x[2]} · investigate immediately')
    new_html = "".join(
        f'<div class="ic-item">• {q}</div><div class="ic-note">Just appeared · low competition · move fast</div>'
        for q in analysis.get('brand_new',[])[:5]
    ) or '<div class="no-data">No new breakouts this week</div>'
    steady_html = ic_items(analysis.get('sustained',[]),
        lambda x: f'Appeared {x[1]}/7 days · consistent demand')
    cross_html = "".join(
        f'<div class="ic-item">• {q}</div><div class="ic-note">Trending on Google ({t}) + Reddit · validated signal</div>'
        for q, t in analysis.get('cross_platform',[])[:5]
    ) or '<div class="no-data">No cross-platform signals this week</div>'

    insights_body = f"""
    <div class="insight-grid">
      <div class="insight-card ic-viral"><div class="ic-title">💥 Explosive Growth</div>{viral_html}</div>
      <div class="insight-card ic-new"><div class="ic-title">🚀 Brand New This Week</div>{new_html}</div>
      <div class="insight-card ic-steady"><div class="ic-title">📅 Sustained (3+ days)</div>{steady_html}</div>
      <div class="insight-card ic-cross"><div class="ic-title">🔗 Cross-Platform</div>{cross_html}</div>
    </div>"""

    insights_sec = _section('insights','🧠','Weekly Analysis',
        'Pattern detection across all platforms and 7 daily snapshots',
        'AI Commentary', insights_body)

    # ── Takeaways ──
    takeaways = []
    if analysis.get('explosives'):
        q = analysis['explosives'][0]
        takeaways.append(f'<strong>🎯 Immediate:</strong> "{q[0]}" is your biggest breakout (+{q[1]:,}%). Create content around this NOW.')
    if analysis.get('sustained'):
        q = analysis['sustained'][0]
        takeaways.append(f'<strong>📌 Stable bet:</strong> "{q[0]}" appeared {q[1]}/7 days. Reliable for evergreen content or paid ads.')
    if analysis.get('brand_new'):
        q = analysis['brand_new'][0]
        takeaways.append(f'<strong>🆕 First-mover:</strong> "{q}" just appeared. Nobody has written about it yet — own the conversation.')
    if analysis.get('cross_platform'):
        q = analysis['cross_platform'][0]
        takeaways.append(f'<strong>💪 Strongest signal:</strong> "{q[0]}" is validated across platforms. Best for ads or product angle.')
    if not takeaways:
        takeaways = ['<strong>ℹ️ Building data:</strong> Run the daily script each day to unlock full analysis next Monday.']

    t_items = "".join(f'<div class="takeaway-item"><div class="t-num">{i+1}</div><div class="t-text">{t}</div></div>'
                      for i, t in enumerate(takeaways))
    takeaway_html = f'<div class="takeaway-box"><h3>💡 This Week\'s Key Takeaways</h3>{t_items}</div>'

    return _page(
        f'Weekly Trends Report — {date_str}',
        hero,
        google_sec + reddit_sec + youtube_sec + amazon_sec + insights_sec + takeaway_html,
        f'Weekly report · US Market · {date_str}'
    )
