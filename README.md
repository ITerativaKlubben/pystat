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

By default it grabs stats for the current year. You can narrow it down with `--since` and `--until`:

```bash
python3 analyze.py --since 2024-01-01 --until 2024-12-31
python3 analyze.py --since 2023-06-15
```

If your repo lives somewhere else you can point to it:

```bash
python3 analyze.py --repo /path/to/your/repo
```
