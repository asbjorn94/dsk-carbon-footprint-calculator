from flask import request, jsonify
from config import app, db
from models import Contact #Should eventually be removed, but kept for testing purposes

import json
from utils import Utils

@app.route("/get_footprint", methods=["POST"])
def get_footprint():
    # print("request.json: " + str(request.json))
    
    loaded_request: dict = request.json
    response = Utils.parse_recipe_items(loaded_request.get('request'))
    return json.dumps(response)

    # if request.json.get("product") == "Opskrift":
    #     return panda_db.to_json(orient = "records")
    # else:
    #     return (
    #         jsonify({"Error": "Bad request"}),400
    #     )

# with app.app_context():
#     db.create_all()

# @app.route("/contacts", methods=["GET"])
# def get_contacts():
#     contacts = Contact.query.all()
#     json_contacts = list(map(lambda x: x.to_json(), contacts))
#     return jsonify({"contacts": json_contacts})

# @app.route("/create_contact", methods=["POST"])
# def create_contact():
#     first_name = request.json.get("firstName")
#     last_name = request.json.get("lastName")
#     email = request.json.get("email")

#     if not first_name or not last_name or not email:
#         return (
#             jsonify({"message": "You must include a first name, last name and email"}),400
#         )

#     new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
#     try:
#         db.session.add(new_contact)
#         db.session.commit()
#     except Exception as e:
#         return jsonify({"message": str(e)}), 400

#     return jsonify({"message": "User created!"}), 201

# @app.route("/add_five", methods=["POST"])
# def add_five():
#     number = request.json.get("value")
#     return_value = int(number) + 5

#     return jsonify({"return_value": return_value}), 201




# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()

#     app.run(debug=True)