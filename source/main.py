from flask import request, jsonify
from .config import app
import json
from .utils import Utils

@app.route("/get_footprint", methods=["POST"])
def get_footprint():
    # print("request.json: " + str(request.json))

    loaded_request: dict = request.json
    response = Utils.parse_recipe_items(loaded_request.get('request'))

    print(f"""
        response before getting returned in json.dumps: \n
        {response}
        \n
        """)

    return json.dumps(response)