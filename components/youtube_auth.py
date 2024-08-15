import os
from google.oauth2.service_account import Credentials

# # Path to the auth folder
# AUTH_FOLDER = os.path.join(os.path.dirname(__file__), 'auth')

# Adjust the path to the auth folder in the root directory
AUTH_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'auth')

# Load client secrets from the auth folder
def load_credentials():
    """
    Load the client secrets from the auth folder and return the credentials object.
    """
    secrets_file = os.path.join(AUTH_FOLDER, 'client_secrets.json')
    credentials = Credentials.from_service_account_file(secrets_file)
    return credentials

# Example usage
if __name__ == '__main__':
    credentials = load_credentials()
    print("Credentials loaded successfully.")