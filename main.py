from flask import request, jsonify
from config import app, db
import json
from utils import Utils

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

    # if request.json.get("product") == "Opskrift":
    #     return panda_db.to_json(orient = "records")
    # else:
    #     return (
    #         jsonify({"Error": "Bad request"}),400
    #     )

# with app.app_context():
#     db.create_all()

# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()

#     app.run(debug=True)