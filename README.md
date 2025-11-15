# Screenshot XPath element and send to Telegram

This small script captures a screenshot of an element on a webpage (by XPath) using Selenium and sends it to a Telegram chat using a bot.

Files:
- `take_screenshot_send_telegram.py` - main script
- `requirements.txt` - Python dependencies

Usage (PowerShell):

1. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2. Set environment variables (or pass `--token` and `--chat` args)

```powershell
$env:TELEGRAM_BOT_TOKEN = "<your-bot-token>"
$env:TELEGRAM_CHAT_ID = "<your-chat-id>"
```

3. Run script

```powershell
python .\take_screenshot_send_telegram.py
```

Optional arguments:
- `--url` : page URL to load (default the sensibull page)
- `--xpath`: XPath of element to capture
- `--token`, `--chat`: override env vars
- `--caption`: photo caption to send

Notes:
- If the element is inside an iframe or blocked by a modal, the script may need small modifications to switch to the frame or dismiss the modal.
- If the element appears after async loads, increase `--timeout`.
