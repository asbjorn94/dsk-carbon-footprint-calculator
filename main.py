from flask import request, jsonify
from config import app, db
from models import Contact

with app.app_context():
    db.create_all()

@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    print("Called get_contacts")
    return jsonify({"contacts": json_contacts})

@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return (
            jsonify({"message": "You must include a first name, last name and email"}),400
        )

    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "User created!"}), 201

@app.route("/add_five", methods=["POST"])
def add_five():
    number = request.json.get("value")
    return_value = int(number) + 5

    return jsonify({"return_value": return_value}), 201

# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()

#     app.run(debug=True)