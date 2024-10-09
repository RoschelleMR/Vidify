from azure.cosmos import CosmosClient, PartitionKey
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

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
    partition_key=PartitionKey(path="/userId")
)

# Function to create or update user data
def upsert_user(user_data):
    container.upsert_item(user_data)

# Function to fetch a user by userId
def get_user(user_id):
    query = f"SELECT * FROM c WHERE c.userId='{user_id}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return items[0] if items else None