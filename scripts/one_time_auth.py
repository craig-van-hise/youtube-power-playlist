
import os
from google_auth_oauthlib.flow import InstalledAppFlow

# This script is run once to authorize the application.

# The scopes must match the ones required by your application.
# For this example, we're keeping it general.
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    """Runs the OAuth 2.0 flow to get user credentials."""
    # The client_secrets.json file is required for this flow.
    # You must download it from your Google Cloud project credentials page.
    if not os.path.exists('client_secrets.json'):
        print("Error: client_secrets.json not found. Please download it from your Google Cloud project.")
        return

    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Save the credentials for the application to use.
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    print("Authorization successful. 'token.json' created.")

if __name__ == "__main__":
    main()
