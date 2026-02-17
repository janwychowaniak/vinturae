# vinturae

A command-line tool to fetch and display statistics for YouTube videos, playlists, and channels using the YouTube Data API v3.

## Features

- Retrieve detailed statistics for individual videos, including views, likes, comments, publication date, language, and duration.
- Analyze entire playlists, showing aggregated video data.
- Get channel overviews with subscriber counts, video counts, and related playlists.
- Handles optional fields gracefully (e.g., missing statistics or language info).
- Formatted output for easy reading.
- Optional LLM-powered person name extraction from video descriptions (via OpenRouter).

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd vinturae
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Obtain a YouTube Data API v3 key from the [Google Cloud Console](https://console.cloud.google.com/).

4. Set the API key:
   - Create a `.env` file in the project root with:
     ```
     VINTURAE_YOUTUBE_API_KEY=your_api_key_here
     ```
   - Alternatively, set it as an environment variable:
     ```
     export VINTURAE_YOUTUBE_API_KEY=your_api_key_here
     ```

5. (Optional) To enable person name extraction from video descriptions, add an [OpenRouter](https://openrouter.ai/) API key:
   ```
   VINTURAE_OPENROUTER_API_KEY=your_api_key_here
   VINTURAE_OPENROUTER_MODEL=anthropic/claude-sonnet-4  # optional, this is the default
   ```

## Usage

Run the script with command-line arguments to specify videos, playlists, or channels.

### Options

- `-v VIDEO_ID`: Add one or more video IDs (can be repeated).
- `-p PLAYLIST_ID`: Add one or more playlist IDs (can be repeated).
- `-c CHANNEL_ID`: Add one or more channel IDs (can be repeated).

At least one of `-v`, `-p`, or `-c` must be provided.

With that you can:

- Fetch stats for a single video
- Fetch stats for multiple videos
- Analyze a playlist
- Get channel info
- Combine multiple types

## Requirements

- Python 3.8+
- YouTube Data API v3 key
- Internet connection for API calls

## License

MIT
