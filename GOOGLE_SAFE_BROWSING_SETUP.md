# Google Safe Browsing Integration

PhishGuard now includes **Google Safe Browsing API** integration for real-time threat detection.

## What is Google Safe Browsing?

Google Safe Browsing is a service that provides security APIs to help protect users against phishing, malware, and other unsafe websites. It maintains a real-time database of unsafe web resources.

## Setup Instructions

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top
3. Click "NEW PROJECT"
4. Enter a project name (e.g., "PhishGuard")
5. Click "CREATE"

### Step 2: Enable Safe Browsing API

1. In the Google Cloud Console, search for "Safe Browsing API"
2. Click on "Safe Browsing API"
3. Click the "ENABLE" button
4. Wait for the API to be enabled (this may take a minute)

### Step 3: Create an API Key

1. Go to [APIs & Services > Credentials](https://console.cloud.google.com/apis/credentials)
2. Click "CREATE CREDENTIALS" at the top
3. Select "API Key"
4. Your API key will be displayed in a dialog box
5. Copy the key

### Step 4: Configure Your Environment

1. Open the `.env` file in your project root
2. Replace `YOUR_API_KEY_HERE` with your actual API key:
   ```
   GOOGLE_SAFE_BROWSING_API_KEY=AIzaSy_YOUR_ACTUAL_KEY_HERE
   ```
3. Save the file

### Step 5: Restart the Backend

1. Stop the running backend (Ctrl+C in the terminal)
2. Start it again:
   ```bash
   uvicorn app:app --reload --port 8000
   ```

## Features

The Google Safe Browsing API integration checks URLs for:

- **MALWARE**: URLs known to distribute malware
- **SOCIAL_ENGINEERING**: Phishing and social engineering attacks
- **POTENTIALLY_HARMFUL_APPLICATION**: URLs hosting potentially harmful applications
- **UNWANTED_SOFTWARE**: URLs hosting unwanted software

## Testing

Once configured, you can test the integration by:

1. Going to http://localhost:3000
2. Entering a suspicious URL
3. The results will show both XGBoost analysis and Google Safe Browsing results

## API Rate Limits

Google Safe Browsing API has rate limits:

- **Free tier**: 600 requests per minute
- Check [Google Cloud Pricing](https://cloud.google.com/safe-browsing/pricing) for more details

## Troubleshooting

### "Google Safe Browsing API key not configured"

This message appears when:
- No API key is set in the `.env` file
- The API key is set to `YOUR_API_KEY_HERE` (the default placeholder)

**Solution**: Follow the setup instructions above to get a real API key.

### "Error: API key is invalid"

This could mean:
- The API key is incorrect or expired
- The Safe Browsing API is not enabled for your project
- Your quota has been exceeded

**Solution**: 
1. Verify the API key in `.env`
2. Check that Safe Browsing API is enabled in Google Cloud Console
3. Monitor your API usage in the Cloud Console

### Slow Response Times

The Google Safe Browsing API may take a few seconds to respond. This is normal.

## Security Notes

- Keep your API key secret - never commit it to version control
- The `.env` file should be added to `.gitignore`
- Use environment variables in production instead of `.env` files

## Additional Resources

- [Google Safe Browsing Documentation](https://developers.google.com/safe-browsing)
- [Safe Browsing API Reference](https://developers.google.com/safe-browsing/v4)
- [Google Cloud Security Best Practices](https://cloud.google.com/security/best-practices)
