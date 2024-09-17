# utils.py

from google.auth.transport import requests
from google.oauth2 import id_token

GOOGLE_CLIENT_ID = ["840477817407-fudv992qklqqln48ggmpk0na5o76ni5n.apps.googleusercontent.com","840477817407-c2slaq8uhp8d5jpdd81plvg960j6aam7.apps.googleusercontent.com"]
def VerifyGoogleToken(token):
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )    
        return idinfo,True
    except ValueError as e:
        # Invalid token
        print(f'Error verifying Google ID token: {e}')
        return None,False
        