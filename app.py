from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

GARENA_API_URL = "https://shop.garena.my/api/auth/player_id_login"

HEADERS = {
    "sec-ch-ua-platform": "\"Android\"",
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Infinix X6837 Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.7727.55 Mobile Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "sec-ch-ua": "\"Android WebView\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"",
    "Content-Type": "application/json",
    "sec-ch-ua-mobile": "?1",
    "Origin": "https://shop.garena.my",
    "X-Requested-With": "mark.via.gp",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://shop.garena.my/?channel=202953",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": (
        "source=mb; region=MY; language=en; "
        "mspid2=5a0d9bcdd4dfc077158dcebd20bd0035; "
        "_fbp=fb.1.1777226630722.236627174334749579; "
        "datadome=mWe_SuotviZaUJY6jNlmjo6nyuxArpSTftTi5IDEvpn6n6gsZZRv7xO0e_nQ4UEq6N0Zf7TPkZUHkgFdinG6SsLRlwmRuT8wGj_U10ZVeDmbsIhkbRRracgoME2~8TLV"
    ),
    "Connection": "keep-alive",
}

APP_IDS = {
    "BD": 100067,
    "MY": 100067,
    "SG": 100067,
    "TH": 100067,
    "ID": 100067,
    "PH": 100067,
    "VN": 100067,
    "TW": 100067,
}


@app.route("/<region>/player-info", methods=["GET"])
def player_info(region):
    region = region.upper()

    uid = request.args.get("uid")
    if not uid:
        return jsonify({"error": "uid parameter is required"}), 400

    app_id = APP_IDS.get(region, 100067)

    payload = {
        "app_id": app_id,
        "login_id": uid
    }

    try:
        response = requests.post(
            GARENA_API_URL,
            json=payload,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code != 200:
            return jsonify({"error": f"Garena API returned status {response.status_code}"}), 502

        data = response.json()

        nickname = data.get("nickname")
        if not nickname:
            return jsonify({"error": "Player not found or invalid UID"}), 404

        return jsonify({"nickname": nickname})

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request to Garena API timed out"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "ok",
        "usage": "GET /<region>/player-info?uid=<player_uid>",
        "example": "/BD/player-info?uid=2815662785",
        "supported_regions": list(APP_IDS.keys())
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
