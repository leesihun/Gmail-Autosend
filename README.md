# Gmail-Autosend

A Python tool to automatically send emails with attachments and clipboard content using the Gmail API.

## Features
- Sends all files from a specified folder as email attachments
- Automatically attaches images from the clipboard (e.g., screenshots)
- Includes clipboard text in the email body
- Uses OAuth2 for secure Gmail authentication

## Requirements
- Python 3.7+
- Google API client libraries (`google-auth-oauthlib`, `google-api-python-client`)
- `pyperclip`, `Pillow`

## Setup

### 1. Clone the repository:
```bash
git clone https://github.com/leesihun/Gmail-Autosend.git
cd Gmail-Autosend
```

### 2. Install dependencies:
```bash
pip install google-auth-oauthlib google-api-python-client pyperclip Pillow
```

### 3. Obtain Google API Credentials (credentials.json):

#### Step 3.1: Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter a project name (e.g., "Gmail Autosend") and click "Create"

#### Step 3.2: Enable Gmail API
1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Gmail API" and click on it
3. Click "Enable"

#### Step 3.3: Create OAuth2 Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in required fields (App name, User support email, Developer contact)
   - Add your email to "Test users" if in testing mode
4. For Application type, select "Desktop application"
5. Give it a name (e.g., "Gmail Autosend Client")
6. Click "Create"
7. Download the JSON file and rename it to `credentials.json`
8. Place `credentials.json` in the project root directory

### 4. Configure the script:
- Edit the recipient email in `gmail_automation.py` (line 75):
  ```python
  to = "your-recipient@example.com"  # Change this to your target email
  ```
- Optionally, change the folder path (line 62):
  ```python
  FOLDER_PATH = r'./item'  # Change this to your desired folder
  ```

## Usage

### Option 1: Run Python Script
1. Place files you want to send in the `item/` folder
2. Copy any image or text to your clipboard (optional)
3. Run the script:
   ```bash
   python gmail_automation.py
   ```

### Option 2: Use Pre-built Executable
1. Download `gmail_automation.exe` from the repository
2. Place your `credentials.json` in the same folder as the executable
3. Create an `item/` folder and place files you want to send
4. Double-click `gmail_automation.exe` to run

## First Run Authentication
- The first time you run the script, it will:
  1. Open a browser window for Google authentication
  2. Ask you to sign in to your Google account
  3. Request permission to send emails via Gmail
  4. Create a `token.json` file for future use
- Subsequent runs will use the saved `token.json` and won't require browser authentication

## File Structure
```
Gmail-Autosend/
├── gmail_automation.py      # Main Python script
├── gmail_automation.exe     # Pre-built executable
├── credentials.json         # Your Google API credentials (create this)
├── token.json              # Auto-generated after first auth (don't share)
├── item/                   # Folder containing files to send
│   ├── file1.pdf
│   ├── image.png
│   └── ...
└── README.md
```

## Security Notes
- Never share your `credentials.json` or `token.json` files
- These files contain sensitive authentication information
- The repository excludes these files via `.gitignore` for security
- If you suspect your credentials are compromised, revoke them in Google Cloud Console

## Troubleshooting
- **"File not found" error**: Ensure `credentials.json` is in the same directory as the script
- **"Access denied" error**: Check that Gmail API is enabled and OAuth consent screen is configured
- **"Invalid credentials" error**: Re-download `credentials.json` from Google Cloud Console
- **"Token expired" error**: Delete `token.json` and run the script again to re-authenticate

## License
MIT License 