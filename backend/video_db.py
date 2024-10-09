import datetime
import uuid
from azure.cosmos import CosmosClient, PartitionKey
from azure.storage.blob import BlobServiceClient, ContentSettings
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Initialize Azure Blob Service Client
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connect_str)



# Cosmos DB credentials (from the Azure portal)
COSMOS_URI =  os.getenv("COSMOS_URI")
COSMOS_KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = "vidify-db"
CONTAINER_NAME = "videos"

# Initialize Cosmos client
client = CosmosClient(url=COSMOS_URI, credential=COSMOS_KEY)

# Create database if not exists
database = client.create_database_if_not_exists(DATABASE_NAME)

# Create or get the container
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME,
    partition_key=PartitionKey(path="/id")
)

def upload_video_to_blob(file_path, user_id, blob_name):
    try:
        # Create a blob client in the 'videos' container
        blob_client = blob_service_client.get_blob_client(container="videos", blob=f"{user_id}/{blob_name}")
        
        # check if the blob exists
        if blob_client.exists():
            print(f"Blob {blob_name} already exists")
            return blob_client.url
        
        # Set the Content-Type and Content-Disposition
        content_settings = ContentSettings(
            content_type='video/mp4', 
        )
        
        # Upload the video to Azure Blob
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, content_settings=content_settings)

        print(f"Uploaded {blob_name} successfully")
        return blob_client.url  # Return the URL to store in CosmosDB
    except Exception as ex:
        print(f"Error uploading video: {ex}")
        return None
    
def store_video_metadata(user_id, video_url, video_title):
    try:
        video_data = {
            'id': str(uuid.uuid4()),  # Unique ID for the video
            'user_id': user_id,  # The ID of the user who generated the video
            'title': video_title,
            'url': video_url,
            'created_at': str(datetime.datetime.now())
        }
        
        container.create_item(body=video_data)
        print("Video metadata stored successfully in CosmosDB")
    except Exception as e:
        print(f"Error storing video metadata: {e}")
        
def get_user_videos(user_id):
    try:
        # Query CosmosDB for videos associated with the user_id
        query = f"SELECT * FROM c WHERE c.user_id = @user_id"
        parameters = [{"name": "@user_id", "value": user_id}]
        
        # Execute the query
        videos = list(container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

        print(f"Found {len(videos)} videos for user {user_id}")
        return videos
    
    except Exception as e:
        print(f"Error retrieving videos for user {user_id}: {e}")
        return []
    
def delete_video_from_blob(user_id, blob_name):
    try:
        # Create a blob client for the video
        blob_client = blob_service_client.get_blob_client(container="videos", blob=f"{user_id}/{blob_name}")

        # Check if the blob exists
        if blob_client.exists():
            blob_client.delete_blob()
            print(f"Deleted blob {blob_name} successfully.")
            return True
        else:
            print(f"Blob {blob_name} does not exist.")
            return False
        
    except Exception as e:
        print(f"Error deleting blob: {e}")
        return False
    
def delete_video_metadata(video_id, blob_name):
    print(f"Deleting video metadata with id {video_id} from CosmosDB")
    try:
        # Query to find the video by its video_id
        query = f"SELECT * FROM c WHERE c.id = @video_id"
        parameters = [{"name": "@video_id", "value": video_id}]
        
        # Query the container for the video item
        video_items = list(container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        print('Here is the video items:', video_items)

        if not video_items:
            print(f"Video with id {video_id} not found.")
            return False

        # Assuming the video_id is unique, so we delete the first (and only) item
        video_item = video_items[0]
        
        
        # Delete the video item from CosmosDB
        container.delete_item(item=video_id, partition_key=blob_name)
        print(f"Deleted video metadata with id {video_id} from CosmosDB.")
        return True

    except Exception as e:
        print(f"Error deleting video metadata: {e}")
        return False
    

def delete_video(user_id, video_id, blob_name):
    # Delete from Blob Storage
    blob_deleted = delete_video_from_blob(user_id, blob_name)
    
    # Delete from CosmosDB
    if blob_deleted:
        metadata_deleted = delete_video_metadata(video_id, video_id)
        if metadata_deleted:
            return True
    return False