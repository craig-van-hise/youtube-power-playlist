# Setup Guide for the Research Archive Bot

This guide provides step-by-step instructions for configuring the necessary external services and environment for the Research Archive Bot.

## 1. Google Cloud Console: Enable APIs

Before running the application, you must enable the following APIs in your Google Cloud project.

1.  Navigate to the [Google Cloud Console API Library](https://console.cloud.google.com/apis/library).
2.  Select your Google Cloud project.
3.  Search for and enable the following APIs:
    *   **YouTube Data API v3:** This is required for searching and retrieving video data from YouTube.
    *   **Vertex AI API:** This provides access to the Google Generative AI models (Gemini) for analyzing video metadata.

## 2. Credentials Configuration

The application requires two types of credentials: an **OAuth 2.0 Client ID** for user authorization (if accessing user-specific data, though for this project it's for the script to act on behalf of a user) and **Application Default Credentials** for server-side authentication with Google Cloud services like Firestore.

### OAuth 2.0 Client ID (`client_secrets.json`)

This is used by the `one_time_auth.py` script to authorize the application to access YouTube data on your behalf.

1.  Go to the [Credentials page](https://console.cloud.google.com/apis/credentials) in the Google Cloud Console.
2.  Click **+ CREATE CREDENTIALS** and select **OAuth client ID**.
3.  For the **Application type**, select **Desktop app**.
4.  Give it a name (e.g., "Research Archive Bot CLI").
5.  After creation, click the **DOWNLOAD JSON** button for the newly created client ID.
6.  Rename the downloaded file to `client_secrets.json`.
7.  Place this file in the root of the `research-archive-bot` directory.

### Application Default Credentials (for Firestore and other services)

For local development and ease of use, we recommend using the `gcloud` CLI to set up your Application Default Credentials. This method is more secure than downloading a service account key.

1.  **Install the gcloud CLI:** If you haven't already, [install the Google Cloud CLI](https://cloud.google.com/sdk/docs/install).
2.  **Login and Authenticate:** Run the following command in your terminal and follow the prompts to log in with your Google account:
    ```bash
    gcloud auth application-default login
    ```
    This command will store your credentials locally, and the `firebase-admin` SDK (and other Google Cloud libraries) will automatically detect and use them.

## 3. Firebase Setup: Enable Firestore

The project uses Firestore to store the archived video data.

1.  Go to the [Firebase Console](https://console.firebase.google.com/).
2.  Click **Add project** and select your existing Google Cloud project.
3.  Once your Firebase project is set up, go to the **Firestore Database** section in the left-hand menu.
4.  Click **Create database**.
5.  Choose **Native mode**.
6.  Select a location for your database.
7.  For the security rules, you can start with **test mode** for initial development, but be sure to secure your database before deploying a public-facing application.

## 4. Environment Variables (`.env` file)

Create a file named `.env` in the `research-archive-bot` directory by copying the `.env.example` file. Then, fill in the values for each variable.

```
# .env

# Your Google Cloud Project ID
GOOGLE_CLOUD_PROJECT="your-gcp-project-id"

# API key for the YouTube Data API
YOUTUBE_API_KEY="your-youtube-api-key"

# API key for the Gemini API
GEMINI_API_KEY="your-gemini-api-key"

# This is no longer needed if you use 'gcloud auth application-default login'
# GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"

# The email address of the user you are acting on behalf of
# (the same one you used in the 'gcloud auth' step)
GOOGLE_OAUTH_USER_EMAIL="your-email@example.com"
```

### Finding Your API Keys:

*   Go to the [Credentials page](https://console.cloud.google.com/apis/credentials) in the Google Cloud Console.
*   Your API keys will be listed under the "API Keys" section. If you don't have one, you can create one by clicking **+ CREATE CREDENTIALS** and selecting **API key**.
*   It's a good practice to restrict your API keys to the specific APIs they are used for (YouTube and Vertex AI).