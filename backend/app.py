import json
from flask import Flask, Response, request, session
import requests
from dotenv import load_dotenv
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import os, pathlib
import google
import jwt
from flask_cors import CORS

from db import upsert_user


# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
cors = CORS(app)

# Config for CORS
app.config['Access-Control-Allow-Origin'] = '*'
app.config["Access-Control-Allow-Headers"]="Content-Type"

# To allow Http traffic for local dev
app.secret_key = os.getenv('FLASK_SECRET_KEY')
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" 

AUTH_FOLDER = 'auth/'
CLIENT_SECRETS_FILE = os.path.join(AUTH_FOLDER, 'client_secrets.json')
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid']
REDIRECT_URI = 'http://localhost:5000/auth/google/callback'
ALGORITHM = os.getenv("ALGORITHM")
BACKEND_URL=os.getenv("BACKEND_URL")
FRONTEND_URL=os.getenv("FRONTEND_URL")

#database connection
# connect_db()


flow = Flow.from_client_secrets_file(
    client_secrets_file=CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)

# JWT generation function
def generate_JWT(payload):
    encoded_jwt = jwt.encode(payload, app.secret_key, algorithm=ALGORITHM)
    return encoded_jwt

# Login required decorator to protect routes
def login_required(function):
    def wrapper(*args, **kwargs):
        encoded_jwt = request.headers.get("Authorization").split("Bearer ")[1]
        if encoded_jwt is None:
            return abort(401)
        else:
            return function()
    return wrapper


# OAuth2 callback route
@app.route('/auth/google/callback')
def google_callback():

    
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    # Create a session to request Google services
    request_session = requests.session()
    token_request = google.auth.transport.requests.Request(session=request_session)
    
    # Verify the Google ID token
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID,
        clock_skew_in_seconds=10
    )
    session["google_id"] = id_info.get("sub")  # Store Google ID in session

    # Generate JWT
    del id_info['aud']  # Removing 'aud' field to prevent any errors
    
    user_data = {
            "id": id_info.get("sub"),
            "name": id_info.get("name"),
            "email": id_info.get("email"),
            "profile_picture": id_info.get("picture")
    }
    
    # Store user data in Cosmos DB
    upsert_user(user_data)
    
    jwt_token = generate_JWT(id_info)
    
    # Redirect user to the frontend with JWT in the query params
    return redirect(f"{FRONTEND_URL}?jwt={jwt_token}")


# Google OAuth2 login route
@app.route("/auth/google")
def login():
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    session["state"] = state  # Store state in session
    return redirect(authorization_url)

    
# Logout route to clear the session
@app.route("/logout")
def logout():
    session.clear()  # Clear session
    return Response(
        response=json.dumps({"message": "Logged out"}),
        status=202,
        mimetype='application/json'
    )
    
# Protected route that requires login
@app.route("/home", methods=["GET"])
@login_required
def home_page_user():
    encoded_jwt = request.headers.get("Authorization").split("Bearer ")[1]
    try:
        decoded_jwt = jwt.decode(encoded_jwt, app.secret_key, algorithms=[ALGORITHM])
        print(decoded_jwt)
    except Exception as e:
        return Response(
            response=json.dumps({"message": "Decoding JWT Failed", "exception": e.args}),
            status=500,
            mimetype='application/json'
        )
    return Response(
        response=json.dumps(decoded_jwt),
        status=200,
        mimetype='application/json'
    )



if __name__ == "__main__":
    app.run(debug=True, port=5000)