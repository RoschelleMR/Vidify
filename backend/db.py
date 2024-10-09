from azure.cosmos import CosmosClient, PartitionKey
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

from google import oauth2
from google.auth.transport.requests import Request

# Load environment variables from the .env file
load_dotenv()

# Cosmos DB credentials (from the Azure portal)
COSMOS_URI =  os.getenv("COSMOS_URI")
COSMOS_KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = "vidify-db"
CONTAINER_NAME = "users"

# Initialize Cosmos client
client = CosmosClient(url=COSMOS_URI, credential=COSMOS_KEY)

# Create database if not exists
database = client.create_database_if_not_exists(DATABASE_NAME)

# Create or get the container
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME,
    partition_key=PartitionKey(path="/id")
)

# Function to create or update user data
def upsert_user(user_data):
    container.upsert_item(user_data)

# Function to fetch a user by userId
def get_user(user_id):
    query = f"SELECT * FROM c WHERE c.userId='{user_id}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return items[0] if items else None

def fetch_user_credentials(user_id):
    """Fetch the user's OAuth2 credentials from CosmosDB and refresh if needed."""
    try:
        # Query the CosmosDB container to fetch user data
        user_item = container.read_item(item=user_id, partition_key=user_id)
        
        # Extract Google OAuth credentials from the user document
        google_credentials = user_item.get('google_credentials', {})

        # Ensure necessary fields are available
        if all(k in google_credentials for k in ('access_token', 'refresh_token', 'token_uri', 'client_id', 'client_secret')):
            credentials = oauth2.credentials.Credentials(
                token=google_credentials['access_token'],
                refresh_token=google_credentials['refresh_token'],
                token_uri=google_credentials['token_uri'],
                client_id=google_credentials['client_id'],
                client_secret=google_credentials['client_secret'],
                scopes=google_credentials['scopes']
            )

            # If the token is expired, refresh it
            if credentials.expired:
                credentials.refresh(Request())

                # Save the new access token back to the database
                google_credentials['access_token'] = credentials.token
                container.upsert_item(user_item)  # Update the user document with the new access token

            return google_credentials
        else:
            raise Exception("Missing credentials in user data")
    except Exception as e:
        print(f"Error fetching or refreshing user credentials: {e}")
        return None