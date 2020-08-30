import requests
from app import config
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Header, Depends, HTTPException

# importing ORM
from sqlalchemy.orm import Session
import crud, models, schemas


# class to receive client data to get api token 
class Client_auth(BaseModel):
    client_id: str
    client_secret: str


router = APIRouter()


@router.post("/spotify/api/token")
def get_spotify_api_token(client_auth: Client_auth):
    """
    Request api token from spotify 

    We will use this Bearer access token to login into other spotify apis

    current spotify documentation:

    https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow

    """
    url = "https://accounts.spotify.com/api/token"
    spotify_client_data = {
        "grant_type": "client_credentials",
        "client_id": client_auth.client_id, 
        "client_secret": client_auth.client_secret
    }

    response = requests.post(url, data=spotify_client_data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail = response.json() )

    return response.json()



@router.get("/spotify/artist/{spotify_search}")
def get_artist_data(spotify_search: str, Authorization: Optional[str] = Header(None),  db: Session = Depends(deps.get_db)):
    """
    Get Spotify Catalog information about artists that match a keyword string.

    Create Result from Spotify Data

    Require authentication
    """
    url = "https://api.spotify.com/v1/search?q=" + str(spotify_search) + "&type=artist&limit=40"
    headers = { "Authorization": Authorization}
    response = requests.get(url,headers=headers)

    db_result = crud.create_results()

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Pokemon not found")

    return response.json()