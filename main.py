from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ⚙️ Function: Fetch Instagram profile info
def get_insta_info(username):
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "X-IG-App-ID": "936619743392459"  # Public Instagram Web App ID
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return {"error": f"Profile '{username}' not found or private."}

        user = r.json()["data"]["user"]

        info = {
            "username": user["username"],
            "full_name": user.get("full_name", ""),
            "bio": user.get("biography", ""),
            "followers": user["edge_followed_by"]["count"],
            "following": user["edge_follow"]["count"],
            "posts": user["edge_owner_to_timeline_media"]["count"],
            "profile_pic": user["profile_pic_url_hd"],
            "private": user["is_private"],
            "verified": user["is_verified"]
        }

        return info

    except Exception as e:
        return {"error": str(e)}


# 🚀 Route: /insta-info?username=
@app.route('/insta-info', methods=['GET'])
def insta_info():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username parameter is required ❗"}), 400

    info = get_insta_info(username)
    return jsonify(info)


# 🏁 Default route
@app.route('/')
def home():
    return jsonify({
        "message": "📸 Instagram Profile Info API is running!",
        "usage": "/insta-info?username=USERNAME"
    })


# 🌍 Run local
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
