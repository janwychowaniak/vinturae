# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Vinturae is a CLI tool that fetches and displays YouTube video, playlist, and channel statistics using the YouTube Data API v3. It's a single-file Python application (`vinturae.py`).

## Running

```bash
# Requires VINTURAE_YOUTUBE_API_KEY in .env (next to the script) or environment

# With uv (no install step needed — dependencies declared inline via PEP 723):
./vinturae.py -v VIDEO_ID              # single video
./vinturae.py -v ID1 -v ID2            # multiple videos
./vinturae.py -p PLAYLIST_ID           # playlist with its videos
./vinturae.py -c CHANNEL_ID            # channel info
./vinturae.py -c @handle               # channel by @handle
./vinturae.py -v ID -p ID -c ID        # combine freely
./vinturae.py -p PLAYLIST_ID -n 200    # fetch up to 200 items

# Or with plain Python (after pip install -r requirements.txt):
python vinturae.py -v VIDEO_ID
```

No test suite or linter is configured.

## Architecture

All code lives in `vinturae.py` (~550 lines). The structure follows a pattern of paired Fetcher + Domain classes per YouTube resource type:

- **YouTube** — Lazy-initialized API client wrapper
- **Video / VideoStats / VideoDataFetcher / VideoStatsFormatter** — Fetch video data, compute per-day metrics and engagement ratios, format as aligned table
- **PersonExtractor** — Sends video descriptions to an LLM via OpenRouter to extract person names (opt-in, requires `VINTURAE_OPENROUTER_API_KEY`); shows in-place `<N/total>` progress counter
- **Playlist / PlaylistFetcher** — Fetch playlist metadata + video IDs (paginated, configurable via `-n`, default 100)
- **Channel / ChannelFetcher** — Fetch channel stats, uploads playlist, and related playlists (paginated, configurable via `-n`, default 100); supports `@handle` resolution via `forHandle` API parameter

Entry point: `if __name__ == '__main__'` block uses argparse, then calls `serve_videos_stats()`, `serve_playlist_stats()`, or `serve_channel_stats()` based on flags.

Data flow: CLI args → Fetcher (API call) → Domain object (parsed data + computed properties) → Formatter/`__str__` → stdout.

## Key Details

- Domain classes use lazy-computed `@property` fields for derived metrics (age_days, per-day rates, ratios)
- Optional API fields (commentCount, likeCount, language) are handled with `None` propagation throughout
- ISO 8601 durations are parsed with regex in `Video.formatted_duration`
- API key loaded via `python-dotenv` from `.env` in the script's own directory (not CWD), so the script can be invoked from anywhere (variable: `VINTURAE_YOUTUBE_API_KEY`)
- Optional OpenRouter integration: `VINTURAE_OPENROUTER_API_KEY` enables person name extraction from descriptions; `VINTURAE_OPENROUTER_MODEL` overrides the default model (`anthropic/claude-sonnet-4`)
- Type hints on all function/method signatures using Python 3.12 syntax (`X | None`, `list[str]`, `tuple[...]`); `yt_api` params left untyped (dynamic google API client)
- Dependencies declared inline via PEP 723 script metadata (for `uv run`) and also in `requirements.txt`; packages: `google-api-python-client`, `python-dotenv`, `openrouter`
- Requires Python 3.11+
