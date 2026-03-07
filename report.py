import base64
import json
import os
from datetime import datetime
from stats.weekdays import WEEKDAY_NAMES


def _embed_image(path):
    """Read an image file and return a base64 data URI, or empty string if missing."""
    if not os.path.exists(path):
        return ""
    ext = os.path.splitext(path)[1].lstrip(".")
    mime = {"webp": "image/webp", "png": "image/png", "svg": "image/svg+xml",
            "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(ext, "image/png")
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"


def generate_report(data, repo_name, since, until, repo_path=None):
    """Generate a self-contained HTML report with Chart.js graphs."""
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_range = f"{since} to {until or 'now'}"

    # Embed images
    logo_src = ""
    nat_src = ""
    if repo_path:
        pub = os.path.join(repo_path, "frontend", "public")
        logo_src = _embed_image(os.path.join(pub, "itk_logo_1024x317.webp"))
        nat_src = _embed_image(os.path.join(pub, "footernats", "256x185", "NAT_DEFAULT_256x185.webp"))

    # Summary card values
    commits_per_month = data.get("commits_per_month", {})
    total_commits = sum(commits_per_month.values())
    author_totals = data.get("author_totals", {})
    total_contributors = len(author_totals)
    streak_data = data.get("streaks", None)
    streak_days = streak_data["best_streak"] if streak_data else 0
    coauthored = data.get("coauthored", 0)

    # Commits per month chart data
    cpm_labels = json.dumps(sorted(commits_per_month.keys()))
    cpm_values = json.dumps([commits_per_month[k] for k in sorted(commits_per_month.keys())])

    # Author monthly stacked bar data
    author_monthly = data.get("author_monthly", {})
    months_sorted = sorted(author_monthly.keys())
    all_authors = sorted(author_totals.keys(), key=lambda a: author_totals[a], reverse=True)
    author_datasets_js = _build_author_datasets(months_sorted, all_authors, author_monthly)

    # Author totals table — with rank and bar visualization (colors match stacked chart)
    author_palette = [
        '#39ff14', '#22d3ee', '#fbbf24', '#a78bfa', '#f87171',
        '#fb923c', '#2dd4bf', '#e879f9', '#60a5fa', '#34d399',
        '#f472b6', '#facc15', '#38bdf8', '#c084fc', '#4ade80',
        '#fb7185',
    ]
    author_totals_sorted = sorted(author_totals.items(), key=lambda x: x[1], reverse=True)
    max_author_commits = author_totals_sorted[0][1] if author_totals_sorted else 1
    author_table_rows = "\n".join(
        f'<tr><td class="c rank">#{i+1}</td><td class="c"><span style="color:{author_palette[i % len(author_palette)]}">\u25cf</span> {a}</td><td class="c num">{c}</td>'
        f'<td class="c bar-cell"><div class="bar-fill" style="width:{c*100//max_author_commits}%;background:{author_palette[i % len(author_palette)]}"></div></td></tr>'
        for i, (a, c) in enumerate(author_totals_sorted)
    )

    # Hour chart
    hour_counts = data.get("hour_counts", None)
    hour_labels = json.dumps([f"{h:02d}:00" for h in range(24)])
    hour_values = json.dumps([hour_counts.get(h, 0) for h in range(24)] if hour_counts else [])

    # Weekday chart
    weekday_counts = data.get("weekday_counts", None)
    weekday_labels = json.dumps(WEEKDAY_NAMES)
    weekday_values = json.dumps([weekday_counts.get(d, 0) for d in range(7)] if weekday_counts else [])

    # Lines by author
    lines_data = data.get("lines", {})
    lines_authors = sorted(lines_data.keys(), key=lambda a: lines_data[a]["added"], reverse=True)
    lines_labels = json.dumps(lines_authors)
    lines_added = json.dumps([lines_data[a]["added"] for a in lines_authors])
    lines_removed = json.dumps([lines_data[a]["removed"] for a in lines_authors])

    # Lines summary
    total_added = sum(lines_data[a]["added"] for a in lines_authors)
    total_removed = sum(lines_data[a]["removed"] for a in lines_authors)

    # Most changed files (top 10) — colored by top-level folder
    file_changes = data.get("file_changes", {})
    top_files = file_changes.most_common(10) if hasattr(file_changes, 'most_common') else sorted(file_changes.items(), key=lambda x: x[1], reverse=True)[:10]
    files_labels = json.dumps([f[0] for f in top_files])
    files_values = json.dumps([f[1] for f in top_files])

    folder_palette = [
        '#39ff14', '#22d3ee', '#fbbf24', '#a78bfa', '#f87171',
        '#fb923c', '#2dd4bf', '#e879f9', '#60a5fa', '#34d399',
        '#f472b6', '#facc15',
    ]
    folder_color_map = {}
    folder_idx = 0
    files_colors = []
    for filepath, _ in top_files:
        parts = filepath.split("/")
        folder = parts[0] if len(parts) > 1 else "(root)"
        if folder not in folder_color_map:
            folder_color_map[folder] = folder_palette[folder_idx % len(folder_palette)]
            folder_idx += 1
        files_colors.append(folder_color_map[folder])
    files_colors_js = json.dumps(files_colors)

    # Legend entries for folder colors
    files_legend_html = " ".join(
        f'<span style="margin-right:1rem;font-size:0.75rem;color:var(--text-dim)">'
        f'<span style="color:{color}">\u25cf</span> {folder}</span>'
        for folder, color in folder_color_map.items()
    )

    # File ownership table
    ownership = data.get("ownership", {})
    sorted_ownership = sorted(ownership.items(), key=lambda x: sum(x[1].values()), reverse=True)[:15]
    ownership_rows = "\n".join(
        f'<tr><td class="c file">{file}</td><td class="c">{authors.most_common(1)[0][0]}</td><td class="c num">{authors.most_common(1)[0][1]}</td><td class="c num">{sum(authors.values())}</td></tr>'
        for file, authors in sorted_ownership
    )

    # Word frequency
    word_counter = data.get("words", {})
    most_common_words = word_counter.most_common(10) if hasattr(word_counter, 'most_common') else []
    word_labels = json.dumps([w[0] for w in most_common_words])
    word_values = json.dumps([w[1] for w in most_common_words])
    least_common_words = [
        (word, count) for word, count in sorted(word_counter.items(), key=lambda x: x[1])
        if not word.isdigit()
    ][:10] if word_counter else []
    least_words_rows = "\n".join(
        f'<tr><td class="c">{w}</td><td class="c num">{c}</td></tr>'
        for w, c in least_common_words
    )

    # New contributors table
    new_contributors = data.get("new_contributors", {})
    contributors_sorted = sorted(new_contributors.items(), key=lambda x: x[1])
    contributors_rows = "\n".join(
        f'<tr><td class="c">{a}</td><td class="c">{d}</td></tr>'
        for a, d in contributors_sorted
    )

    # Streak details
    streak_length = streak_data["best_streak"] if streak_data else "—"
    streak_range = f'{streak_data["best_start"]} to {streak_data["best_end"]}' if streak_data else "—"
    streak_active = streak_data["total_days_with_commits"] if streak_data else "—"

    # Avg commits per active day
    avg_per_day = f"{total_commits / streak_active:.1f}" if isinstance(streak_active, int) and streak_active > 0 else "—"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>pystat // {repo_name}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');
  :root {{
    --neon: #39ff14;
    --neon-dim: #22c55e;
    --neon-glow: rgba(57,255,20,0.15);
    --cyan: #22d3ee;
    --amber: #fbbf24;
    --red: #f87171;
    --bg: #0d1117;
    --surface: #161b22;
    --surface2: #1c2333;
    --border: #30363d;
    --border-bright: #484f58;
    --text: #e6edf3;
    --text-dim: #8b949e;
    --text-muted: #484f58;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'JetBrains Mono', 'Cascadia Code', 'Fira Code', monospace;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    font-size: 13px;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
  }}
  .wrap {{ max-width: 980px; margin: 0 auto; padding: 2rem 1.5rem; }}

  /* ── header ── */
  header {{
    border: 1px solid var(--border);
    background: var(--surface);
    padding: 2rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
  }}
  header .header-text {{ flex: 1; }}
  header .header-logos {{
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-shrink: 0;
  }}
  header .header-logos img.logo {{ height: 40px; width: auto; }}
  header .header-logos img.nat {{ height: 64px; width: auto; }}
  header .top-line {{
    color: var(--text-muted);
    font-size: 0.75rem;
    margin-bottom: 0.5rem;
  }}
  header h1 {{
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--neon);
    letter-spacing: -0.02em;
  }}
  header h1 span {{ color: var(--text-dim); font-weight: 400; }}
  header .meta {{
    margin-top: 0.75rem;
    font-size: 0.8rem;
    color: var(--text-dim);
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
  }}
  header .meta strong {{ color: var(--text); }}

  /* ── stat cards ── */
  .stats {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    margin-bottom: 1.5rem;
  }}
  .stat {{
    background: var(--surface);
    padding: 1.25rem 1rem;
    text-align: center;
  }}
  .stat .val {{
    font-size: 2rem;
    font-weight: 700;
    color: var(--neon);
    line-height: 1.1;
  }}
  .stat .lbl {{
    font-size: 0.65rem;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.35rem;
  }}
  .stat.alt .val {{ color: var(--cyan); }}
  .stat.warn .val {{ color: var(--amber); }}

  /* ── sections ── */
  section {{
    border: 1px solid var(--border);
    background: var(--surface);
    margin-bottom: 1.5rem;
  }}
  section .sec-head {{
    padding: 0.75rem 1.25rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }}
  section .sec-head h2 {{
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text);
  }}
  section .sec-head .tag {{
    font-size: 0.65rem;
    color: var(--neon);
    opacity: 0.7;
  }}
  section .sec-body {{ padding: 1.25rem; }}

  /* ── tables ── */
  table {{ width: 100%; border-collapse: collapse; font-size: 0.8rem; }}
  th {{
    text-align: left;
    padding: 0.4rem 0.6rem;
    color: var(--text-muted);
    border-bottom: 1px solid var(--border);
    font-weight: 500;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }}
  .c {{
    padding: 0.35rem 0.6rem;
    border-bottom: 1px solid var(--border);
    color: var(--text-dim);
  }}
  .c.num {{ text-align: right; font-variant-numeric: tabular-nums; color: var(--text); }}
  .c.rank {{ color: var(--text-muted); width: 2.5rem; }}
  .c.file {{ word-break: break-all; font-size: 0.75rem; }}
  .bar-cell {{ width: 35%; padding-right: 1rem; }}
  .bar-fill {{
    height: 6px;
    background: var(--neon);
    opacity: 0.5;
    min-width: 2px;
  }}

  /* ── two-col layout ── */
  .cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }}
  .cols > section {{ margin-bottom: 0; }}

  /* ── detail grid ── */
  .detail-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1px;
    background: var(--border);
  }}
  .detail-grid .di {{
    background: var(--surface2);
    padding: 1rem;
  }}
  .detail-grid .di .dl {{
    font-size: 0.65rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }}
  .detail-grid .di .dv {{
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
    margin-top: 0.2rem;
  }}
  .detail-grid .di .dv.glow {{ color: var(--neon); }}

  /* ── inline stats ── */
  .inline-stats {{
    display: flex;
    gap: 1.5rem;
    padding: 0.75rem 1.25rem;
    border-bottom: 1px solid var(--border);
    font-size: 0.75rem;
  }}
  .inline-stats span {{ color: var(--text-dim); }}
  .inline-stats strong {{ color: var(--neon); }}
  .inline-stats .del {{ color: var(--red); }}

  /* ── footer ── */
  footer {{
    text-align: center;
    padding: 1.5rem;
    font-size: 0.7rem;
    color: var(--text-muted);
    border-top: 1px solid var(--border);
    margin-top: 0.5rem;
  }}
  .no-data {{ color: var(--text-muted); font-size: 0.8rem; padding: 0.5rem 0; }}

  /* ── print ── */
  @media print {{
    body {{
      -webkit-print-color-adjust: exact; print-color-adjust: exact;
      font-size: 13px;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-rendering: optimizeLegibility;
    }}
    .wrap {{ padding: 1rem; max-width: 100%; }}
    .stats {{ grid-template-columns: repeat(4, 1fr); }}
    .cols {{ grid-template-columns: 1fr 1fr; }}
  }}
  @media (max-width: 700px) {{
    .stats {{ grid-template-columns: repeat(2, 1fr); }}
    .cols {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<div class="wrap">

<header>
  <div class="header-text">
    <div class="top-line">$ pystat --repo {repo_name} --since {since}{f" --until {until}" if until else ""}</div>
    <h1>{repo_name} <span>// git stats</span></h1>
    <div class="meta">
      <span>range <strong>{date_range}</strong></span>
      <span>generated <strong>{generated_at}</strong></span>
    </div>
  </div>
  <div class="header-logos">
    {"<img class='logo' src='" + logo_src + "' alt='ITK'>" if logo_src else ""}
    {"<img class='nat' src='" + nat_src + "' alt='NAT'>" if nat_src else ""}
  </div>
</header>

<div class="stats">
  <div class="stat"><div class="val">{total_commits}</div><div class="lbl">commits</div></div>
  <div class="stat alt"><div class="val">{total_contributors}</div><div class="lbl">contributors</div></div>
  <div class="stat warn"><div class="val">{streak_days}d</div><div class="lbl">longest streak</div></div>
  <div class="stat"><div class="val">{coauthored}</div><div class="lbl">co-authored</div></div>
</div>

<!-- Commits per Month -->
<section>
  <div class="sec-head"><h2>Commits per Month</h2><span class="tag">bar</span></div>
  <div class="sec-body"><canvas id="cpmChart"></canvas></div>
</section>

<!-- Commits by Author -->
<section>
  <div class="sec-head"><h2>Commits by Author</h2><span class="tag">stacked</span></div>
  <div class="sec-body"><canvas id="authorChart"></canvas></div>
</section>
<section>
  <div class="sec-head"><h2>Leaderboard</h2><span class="tag">{total_contributors} authors</span></div>
  <div class="sec-body" style="padding:0;">
    <table>
      <thead><tr><th></th><th>Author</th><th style="text-align:right">Commits</th><th></th></tr></thead>
      <tbody>{author_table_rows}</tbody>
    </table>
  </div>
</section>

<div class="cols">
<!-- Commit Activity by Hour -->
<section>
  <div class="sec-head"><h2>Activity by Hour</h2><span class="tag">24h</span></div>
  <div class="sec-body"><canvas id="hourChart"></canvas></div>
</section>

<!-- Busiest Weekday -->
<section>
  <div class="sec-head"><h2>Weekday</h2><span class="tag">7d</span></div>
  <div class="sec-body"><canvas id="weekdayChart"></canvas></div>
</section>
</div>

<!-- Lines by Author -->
<section>
  <div class="sec-head"><h2>Lines Changed</h2><span class="tag">insertions / deletions</span></div>
  <div class="inline-stats">
    <span>total added: <strong>+{total_added:,}</strong></span>
    <span>total removed: <strong class="del">-{total_removed:,}</strong></span>
    <span>net: <strong>{f"+{total_added - total_removed:,}" if total_added >= total_removed else f"{total_added - total_removed:,}"}</strong></span>
  </div>
  <div class="sec-body"><canvas id="linesChart"></canvas></div>
</section>

<!-- Most Changed Files -->
<section>
  <div class="sec-head"><h2>Hottest Files</h2><span class="tag">top 10</span></div>
  <div style="padding:0.5rem 1.25rem 0;">{files_legend_html}</div>
  <div class="sec-body"><canvas id="filesChart"></canvas></div>
</section>

<!-- File Ownership -->
<section>
  <div class="sec-head"><h2>File Ownership</h2><span class="tag">top 15</span></div>
  <div class="sec-body" style="padding:0;">
    <table>
      <thead><tr><th>File</th><th>Top Contributor</th><th style="text-align:right">Theirs</th><th style="text-align:right">Total</th></tr></thead>
      <tbody>{ownership_rows}</tbody>
    </table>
  </div>
</section>

<div class="cols">
<!-- Commit Message Words -->
<section>
  <div class="sec-head"><h2>Top Words</h2><span class="tag">commit msgs</span></div>
  <div class="sec-body"><canvas id="wordsChart"></canvas></div>
</section>

<!-- Least Frequent Words -->
<section>
  <div class="sec-head"><h2>Rare Words</h2><span class="tag">least used</span></div>
  <div class="sec-body" style="padding:0;">
    <table>
      <thead><tr><th>Word</th><th style="text-align:right">Count</th></tr></thead>
      <tbody>{least_words_rows}</tbody>
    </table>
  </div>
</section>
</div>

<!-- New Contributors -->
<section>
  <div class="sec-head"><h2>New Contributors</h2><span class="tag">first commit in range</span></div>
  <div class="sec-body" style="padding:0;">
    {"<div class='no-data' style='padding:1rem;'>No new contributors in this period.</div>" if not new_contributors else f'''<table>
      <thead><tr><th>Author</th><th>First Commit</th></tr></thead>
      <tbody>{contributors_rows}</tbody>
    </table>'''}
  </div>
</section>

<!-- Streak Details -->
<section>
  <div class="sec-head"><h2>Streak &amp; Activity</h2></div>
  <div class="sec-body" style="padding:0;">
    <div class="detail-grid">
      <div class="di"><div class="dl">Best Streak</div><div class="dv glow">{streak_length} days</div></div>
      <div class="di"><div class="dl">Streak Window</div><div class="dv">{streak_range}</div></div>
      <div class="di"><div class="dl">Active Days</div><div class="dv">{streak_active}</div></div>
      <div class="di"><div class="dl">Avg / Active Day</div><div class="dv">{avg_per_day}</div></div>
    </div>
  </div>
</section>

<footer>pystat // git repository statistics // generated {generated_at}<br>source: https://github.com/ITerativaKlubben/pystat</footer>

</div>

<script>
const NEON = '#39ff14';
const NEON_DIM = '#22c55e';
const CYAN = '#22d3ee';
const AMBER = '#fbbf24';
const RED = '#f87171';
const GRID = 'rgba(48,54,61,0.6)';
const TICK = '#8b949e';

Chart.defaults.font.family = "'JetBrains Mono', monospace";
Chart.defaults.font.size = 11;
Chart.defaults.color = TICK;
Chart.defaults.devicePixelRatio = 3;

const gridY = {{ color: GRID }};
const noGrid = {{ display: false }};
const noLegend = {{ legend: {{ display: false }} }};

// Per-bar color cycling palette
const PALETTE = ['#39ff14','#22d3ee','#fbbf24','#a78bfa','#f87171','#fb923c','#2dd4bf','#e879f9','#60a5fa','#34d399','#f472b6','#facc15'];
function cycle(data) {{ return data.map((_,i) => PALETTE[i % PALETTE.length]); }}

// Commits per Month
new Chart(document.getElementById('cpmChart'), {{
  type: 'bar',
  data: {{
    labels: {cpm_labels},
    datasets: [{{ data: {cpm_values}, backgroundColor: cycle({cpm_values}), borderRadius: 2 }}]
  }},
  options: {{ responsive: true, plugins: noLegend,
    scales: {{ y: {{ beginAtZero: true, grid: gridY }}, x: {{ grid: noGrid }} }}
  }}
}});

// Author stacked bar
new Chart(document.getElementById('authorChart'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps(months_sorted)},
    datasets: {author_datasets_js}
  }},
  options: {{ responsive: true,
    plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 10, padding: 8, font: {{ size: 10 }} }} }} }},
    scales: {{ x: {{ stacked: true, grid: noGrid }}, y: {{ stacked: true, beginAtZero: true, grid: gridY }} }}
  }}
}});

// Hour chart — gradient from cool to warm across 24h
const hourColors = {hour_values}.map((_,i) => {{
  const t = i / 23;
  if (t < 0.25) return '#60a5fa';      // night — blue
  if (t < 0.5) return '#fbbf24';       // morning — amber
  if (t < 0.75) return '#fb923c';      // afternoon — orange
  return '#a78bfa';                     // evening — purple
}});
new Chart(document.getElementById('hourChart'), {{
  type: 'bar',
  data: {{
    labels: {hour_labels},
    datasets: [{{ data: {hour_values}, backgroundColor: hourColors, borderRadius: 2 }}]
  }},
  options: {{ responsive: true, plugins: noLegend,
    scales: {{ y: {{ beginAtZero: true, grid: gridY }}, x: {{ grid: noGrid, ticks: {{ maxRotation: 90, font: {{ size: 9 }} }} }} }}
  }}
}});

// Weekday chart
const weekdayColors = ['#22d3ee','#39ff14','#fbbf24','#a78bfa','#fb923c','#f87171','#e879f9'];
new Chart(document.getElementById('weekdayChart'), {{
  type: 'bar',
  data: {{
    labels: {weekday_labels},
    datasets: [{{ data: {weekday_values}, backgroundColor: weekdayColors, borderRadius: 2 }}]
  }},
  options: {{ indexAxis: 'y', responsive: true, plugins: noLegend,
    scales: {{ x: {{ beginAtZero: true, grid: gridY }}, y: {{ grid: noGrid }} }}
  }}
}});

// Lines by author
new Chart(document.getElementById('linesChart'), {{
  type: 'bar',
  data: {{
    labels: {lines_labels},
    datasets: [
      {{ label: '++ added', data: {lines_added}, backgroundColor: NEON_DIM, borderRadius: 2 }},
      {{ label: '-- removed', data: {lines_removed}, backgroundColor: RED, borderRadius: 2 }}
    ]
  }},
  options: {{ indexAxis: 'y', responsive: true,
    plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 10, padding: 8, font: {{ size: 10 }} }} }} }},
    scales: {{ x: {{ beginAtZero: true, grid: gridY }}, y: {{ grid: noGrid }} }}
  }}
}});

// Most changed files — colored by folder
new Chart(document.getElementById('filesChart'), {{
  type: 'bar',
  data: {{
    labels: {files_labels},
    datasets: [{{ data: {files_values}, backgroundColor: {files_colors_js}, borderRadius: 2 }}]
  }},
  options: {{ indexAxis: 'y', responsive: true, plugins: noLegend,
    scales: {{ x: {{ beginAtZero: true, grid: gridY }}, y: {{ grid: noGrid, ticks: {{ font: {{ size: 9 }} }} }} }}
  }}
}});

// Word frequency chart
new Chart(document.getElementById('wordsChart'), {{
  type: 'bar',
  data: {{
    labels: {word_labels},
    datasets: [{{ data: {word_values}, backgroundColor: cycle({word_values}), borderRadius: 2 }}]
  }},
  options: {{ responsive: true, plugins: noLegend,
    scales: {{ y: {{ beginAtZero: true, grid: gridY }}, x: {{ grid: noGrid }} }}
  }}
}});

// Set @page size to actual content height to avoid dead space in PDF
window.addEventListener('beforeprint', () => {{
  const h = document.querySelector('.wrap').scrollHeight + 20;
  let style = document.getElementById('print-page-size');
  if (!style) {{
    style = document.createElement('style');
    style.id = 'print-page-size';
    document.head.appendChild(style);
  }}
  style.textContent = `@page {{ size: 210mm ${{h}}px; margin: 0; }}`;
}});
</script>
</body>
</html>"""
    return html


def _build_author_datasets(months, authors, author_monthly):
    """Build Chart.js dataset array for stacked author bar chart."""
    palette = [
        '#39ff14', '#22d3ee', '#fbbf24', '#a78bfa', '#f87171',
        '#fb923c', '#2dd4bf', '#e879f9', '#60a5fa', '#34d399',
        '#f472b6', '#facc15', '#38bdf8', '#c084fc', '#4ade80',
        '#fb7185',
    ]
    datasets = []
    for i, author in enumerate(authors):
        color = palette[i % len(palette)]
        values = [author_monthly.get(m, {}).get(author, 0) for m in months]
        datasets.append({
            "label": author,
            "data": values,
            "backgroundColor": color,
            "borderRadius": 1,
        })
    return json.dumps(datasets)


def write_report(html, output_path):
    """Write HTML string to file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
