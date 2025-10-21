from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Instagram Info API is running!"}

@app.get("/insta")
def insta_user(username: str = Query(..., description="Instagram username")):
    try:
        url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return JSONResponse(
                content={"error": "Failed to fetch user info"},
                status_code=resp.status_code
            )

        data = resp.json()

        # कुछ useful fields निकालना
        user = data.get("graphql", {}).get("user", {})
        if not user:
            return {"error": "User not found or private"}

        result = {
            "username": user.get("username"),
            "full_name": user.get("full_name"),
            "biography": user.get("biography"),
            "followers": user.get("edge_followed_by", {}).get("count"),
            "following": user.get("edge_follow", {}).get("count"),
            "posts": user.get("edge_owner_to_timeline_media", {}).get("count"),
            "profile_pic": user.get("profile_pic_url_hd"),
            "profile_url": f"https://instagram.com/{username}",
            "is_private": user.get("is_private"),
            "is_verified": user.get("is_verified")
        }
        return result

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)