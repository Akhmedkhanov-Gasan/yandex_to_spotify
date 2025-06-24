# Yandex Music → Spotify Sync

This Python script synchronizes your liked tracks from Yandex Music to a single Spotify playlist. It fetches newly liked tracks on Yandex Music and adds only those not already present in your Spotify playlist.

## Features

- Fetches liked tracks from Yandex Music using an OAuth token
- Searches for each track on Spotify and retrieves its URI
- Creates (or finds) a private Spotify playlist named `Yandex Music`
- Adds only new tracks—avoiding duplicates
- Can be scheduled (e.g., via cron or Task Scheduler) for continuous synchronization

## Prerequisites

- Python 3.7 or higher
- Yandex Music OAuth token (from web DevTools or other method)
- Spotify Developer account credentials
- A local loopback redirect URI (e.g., `http://127.0.0.1:8888/callback`)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/yandex-to-spotify-sync.git
   cd yandex-to-spotify-sync
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   # macOS/Linux
   source venv/bin/activate
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a **``** file** in the project root with the following variables:

   ```env
   # Spotify API
   SPOTIPY_CLIENT_ID=your_spotify_client_id
   SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
   
   # Yandex Music
   YANDEX_TOKEN=your_yandex_oauth_token
   ```

## Spotify App Setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Create a new app and copy the **Client ID** and **Client Secret**.
3. Under **Edit Settings**, add your redirect URI:
   - `http://127.0.0.1:8888/callback`
   - Or `http://[::1]:8888/callback` for IPv6
4. Save the settings.

## Obtaining a Yandex Music OAuth Token

To extract your Yandex Music token via your browser:

1. (Optional) Open your browser's DevTools and on the **Network** tab enable throttling if desired.
2. Navigate to the following authorization URL:
   ```
   https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d
   ```
3. Log in if prompted and grant access to the application.
4. After authorization, your browser will briefly redirect to a URL like:
   ```
   https://music.yandex.ru/#access_token=AQAAAAAYc***&token_type=bearer&expires_in=31535645
   ```
   You need to quickly copy this entire URL before it redirects again.
5. Extract the token string after `access_token=` and before `&`, and set it as your `YANDEX_TOKEN`.

## Usage

```bash
python yandex_to_spotify.py
```

Upon running, the script will:

1. Load your tokens and credentials from `.env`
2. Fetch liked tracks from Yandex Music
3. Create or find the `Yandex Music` playlist on Spotify
4. Search for and add new tracks
5. Print the number of newly added tracks

## Scheduling

To keep your Spotify playlist up-to-date, schedule the script:

- **Cron (Linux/macOS)**

  ```cron
  0 * * * * /path/to/venv/bin/python /path/to/yandex_to_spotify.py >> /path/to/logfile.log 2>&1
  ```

- **Task Scheduler (Windows)**

  1. Create a basic task pointing to `python.exe`
  2. Add arguments: `C:\path\to\yandex_to_spotify.py`
  3. Set the trigger (e.g., hourly)

## Troubleshooting

- **Module not found**: Ensure your virtual environment is activated and dependencies are installed.
- **Yandex token missing**: Re-extract the `Authorization` value from DevTools Network request headers on `music.yandex.ru`.
- **Spotify OAuth errors**: Verify your redirect URI matches exactly what is registered in the Spotify Developer Dashboard.

## License

This project is released under the MIT License.

