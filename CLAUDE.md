# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Vinturae is a CLI tool that fetches and displays YouTube video, playlist, and channel statistics using the YouTube Data API v3. It's a single-file Python application (`vinturae.py`).

## Running

```bash
# Requires VINTURAE_YOUTUBE_API_KEY in .env or environment
pip install -r requirements.txt

python vinturae.py -v VIDEO_ID              # single video
python vinturae.py -v ID1 -v ID2            # multiple videos
python vinturae.py -p PLAYLIST_ID           # playlist with its videos
python vinturae.py -c CHANNEL_ID            # channel info
python vinturae.py -v ID -p ID -c ID        # combine freely
```

No test suite or linter is configured.

## Architecture

All code lives in `vinturae.py` (~470 lines). The structure follows a pattern of paired Fetcher + Domain classes per YouTube resource type:

- **YouTube** — Lazy-initialized API client wrapper
- **Video / VideoStats / VideoDataFetcher / VideoStatsFormatter** — Fetch video data, compute per-day metrics and engagement ratios, format as aligned table
- **Playlist / PlaylistFetcher** — Fetch playlist metadata + video IDs (pagination capped at 50)
- **Channel / ChannelFetcher** — Fetch channel stats, uploads playlist, and related playlists

Entry point: `if __name__ == '__main__'` block uses argparse, then calls `serve_videos_stats()`, `serve_playlist_stats()`, or `serve_channel_stats()` based on flags.

Data flow: CLI args → Fetcher (API call) → Domain object (parsed data + computed properties) → Formatter/`__str__` → stdout.

## Key Details

- Domain classes use lazy-computed `@property` fields for derived metrics (age_days, per-day rates, ratios)
- Optional API fields (commentCount, likeCount, language) are handled with `None` propagation throughout
- ISO 8601 durations are parsed with regex in `Video.formatted_duration`
- API key loaded via `python-dotenv` from `.env` file (variable: `VINTURAE_YOUTUBE_API_KEY`)
- Dependencies: `google-api-python-client`, `python-dotenv`
