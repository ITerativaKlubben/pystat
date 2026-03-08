# pystat

Janky little script that pulls commit statistics from the ITK Project Web repo. Mostly written by AI, not pretty, but it works.

## Setup

Clone this repo next to your ITK Project Web fork so the folder structure looks someting like this:

```
.
├── itk_website
└── pystat
```

Then set up a venv and install deps:

```bash
cd pystat
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python3 analyze.py
```

This generates `pystat_report.html` — a self-contained dark-themed HTML report with interactive Chart.js graphs, summary cards, leaderboards, and more. The ITK logo and default NAT are embedded automatically.

By default it grabs stats for the current year. You can narrow it down with `--since` and `--until`:

```bash
python3 analyze.py --since 2024-01-01 --until 2024-12-31
python3 analyze.py --since 2023-06-15
```

If your repo lives somewhere else you can point to it:

```bash
python3 analyze.py --repo /path/to/your/repo
```

You can also change the output filename:

```bash
python3 analyze.py --output stats_2024.html
```

## GitHub API

By default pystat pulls data straight from the GitHub API — commits, PRs, issues, CI runs, contributor profiles, the whole thing. The local git clone is only used as a fallback.

Drop a `.env` file in the project root:

```
GITHUB_TOKEN=github_pat_...
```

You need a fine-grained personal access token scoped to the org/repo with read access to Contents, Pull requests, Issues, and Actions.

The repo slug is auto-detected from the git remote, but you can override it:

```bash
python3 analyze.py --github-repo ITerativaKlubben/website
```

If you want to skip the API and use local git history instead:

```bash
python3 analyze.py --local
```

No token, no `.env`, no problem — it just falls back to local git automatically.

## Printing to PDF

The report is designed for printing as a single continuous page with no breaks. To get the best result:

1. Open `pystat_report.html` in a browser
2. Press `Ctrl+P` (or `Cmd+P`)
3. Set margins to **None**
4. Make sure **Background graphics** is enabled (keeps the dark theme)
5. Save as PDF

The charts render at 3x resolution for sharp output.

## Export to PNG

Convert the report to a single tall PNG image (great for sharing on Discord):

```bash
playwright install chromium  # first time only
python3 to_png.py
```

This creates `pystat_report.png` at 2x resolution. You can tweak it:

```bash
python3 to_png.py --width 1200 --scale 3.0
python3 to_png.py custom_report.html -o output.png
```
