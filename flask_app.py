# from flask import Flask, jsonify
# from flask_cors import CORS
# #from flask import Flask, request, jsonify
# #from config import app


# app = Flask(__name__)
# CORS(app)

# @app.route('/')
# def hello_world():
#     return 'Hello world 2!'

# @app.route("/contacts", methods=["GET"])
# def get_contacts():
#     # contacts = Contact.query.all()
#     # json_contacts = list(map(lambda x: x.to_json(), contacts))
#     # print("Called get_contacts")
#     return jsonify({"contacts": [{"name": "Asbjorn"}]})