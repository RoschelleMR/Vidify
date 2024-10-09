#!/usr/bin/python

import http.client as httplib
import tempfile

import httplib2
import os
import random
import sys
import time

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from google import oauth2
from azure.storage.blob import BlobServiceClient


# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
  httplib.IncompleteRead, httplib.ImproperConnectionState,
  httplib.CannotSendRequest, httplib.CannotSendHeader,
  httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

AUTH_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'auth')
CLIENT_SECRETS_FILE = os.path.join(AUTH_FOLDER, 'client_secrets.json')

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


CATEGORY_ID = "22"  # Default category ID for People & Blogs
PRIVACY_STATUS = "private"  # Default privacy status for videos
TAGS = ["AmItheAsshole", "AITA", "Reddit", "shorts"]  # Default tags for videos


# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

# Initialize the BlobServiceClient with your connection string
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connect_str)


def get_authenticated_service(user_credentials):
  
  credentials = oauth2.credentials.Credentials(
        token=user_credentials['access_token'],
        refresh_token=user_credentials['refresh_token'],
        token_uri=user_credentials['token_uri'],
        client_id=user_credentials['client_id'],
        client_secret=user_credentials['client_secret'],
        scopes=user_credentials['scopes']
  )
  
  # Build the YouTube service using the user credentials
  return build(
      YOUTUBE_API_SERVICE_NAME,
      YOUTUBE_API_VERSION,
      credentials=credentials
  )


def download_blob_to_tempfile(blob_url):
    """Download the blob from Azure to a temporary file and return the file path."""
    # Parse the blob URL to extract the container and blob name
    container_name = blob_url.split("/")[3]
    blob_name = "/".join(blob_url.split("/")[4:])

    # Create a blob client
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_file_path = temp_file.name

    # Download the blob data to the temporary file
    with open(temp_file_path, "wb") as download_file:
        blob_data = blob_client.download_blob()
        blob_data.readinto(download_file)

    return temp_file_path
  

def upload_video(video_path, title, desc,  user_credentials, tags=TAGS, category_id=CATEGORY_ID, privacy_status=PRIVACY_STATUS):

   youtube = get_authenticated_service(user_credentials=user_credentials)

   request_body = dict(
       snippet = dict(
           title = title,
           description = desc,
           tags = tags,
           categoryId = category_id
        ),
        status = dict(
            privacyStatus = privacy_status,
            selfDeclaredMadeForKids = False
        )
    )
   
   local_video_path = download_blob_to_tempfile(video_path)
   
   media = MediaFileUpload(local_video_path, chunksize=-1, resumable=True)
   
   # Call the API's videos.insert method to create and upload the video.
  
   request = youtube.videos().insert(
       part=",".join(request_body.keys()),
       body=request_body,
       media_body=media
    )
   
   
   
   resumable_upload(request)




# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(insert_request):
  response = None
  error = None
  retry = 0
  while response is None:
    try:
      print("Uploading file...")
      status, response = insert_request.next_chunk()
      if response is not None:
        if 'id' in response:
          print ("Video id '%s' was successfully uploaded." % response['id'])
        else:
          exit("The upload failed with an unexpected response: %s" % response)
    except HttpError as e:
      if e.resp.status in RETRIABLE_STATUS_CODES:
        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                             e.content)
      else:
        raise
    except RETRIABLE_EXCEPTIONS as e:
      error = "A retriable error occurred: %s" % e

    if error is not None:
      print(error)
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      print ("Sleeping %f seconds and then retrying..." % sleep_seconds)
      time.sleep(sleep_seconds)
