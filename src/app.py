"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the Jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        # Cambiar la estructura del miembro para que use 'name' en lugar de 'first_name' y 'last_name'
        member_dict = {
            "id": member["id"],
            "name": member["first_name"],  # Puedes elegir cómo combinar el nombre
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }
        return jsonify(member_dict), 200
    return jsonify({"message": "Member not found"}), 404

@app.route('/member', methods=['POST'])
def add_member():
    member_data = request.get_json()
    if not member_data or 'first_name' not in member_data or 'age' not in member_data or 'lucky_numbers' not in member_data:
        return jsonify({"message": "Invalid data"}), 400  # Cambia a 400

    jackson_family.add_member(member_data)
    return jsonify({"message": "Member created successfully", "member": member_data}), 201

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = jackson_family.get_member(id)
    if not member:
        return jsonify({"message": "Member not found"}), 404

    jackson_family.delete_member(id)
    return jsonify({"done": True}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
