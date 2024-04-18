"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    if members:
        return jsonify(members), 200
    else:
        return jsonify({"error": "No members found"}), 404

@app.route('/members', methods=['POST'])
def add_member():
    data = request.json
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    
    first_name = data.get('first_name')
    age = data.get('age')
    if not first_name or not age:
        return jsonify({"error": "Missing required fields"}), 400
    
    lucky_numbers = data.get('lucky_numbers', [])
    jackson_family.add_member(first_name, age, lucky_numbers)
    
    response_body = {
        "message": "Member added successfully",
        "member": {
            "first_name": first_name,
            "age": age,
            "lucky_numbers": lucky_numbers
        }
    }
    
    return jsonify(response_body), 201

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member_by_id(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Member not found"}), 404

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member_by_id(member_id):
    member = jackson_family.delete_member(member_id)
    if member:
        return jsonify({"message": "Member deleted successfully"}), 200
    else:
        return jsonify({"error": "Member not found"}), 404

if __name__ == '__main__':
    # Agregar tres miembros de la familia al iniciar la aplicación
    jackson_family.add_member("John Jackson", 33, [7, 13, 22])
    jackson_family.add_member("Jane Jackson", 35, [10, 14, 3])
    jackson_family.add_member("Jimmy Jackson", 5, [1])

    # Definir el puerto en el que se ejecutará la aplicación
    PORT = int(os.environ.get('PORT', 3000))

    # Iniciar la aplicación Flask
    app.run(host='0.0.0.0', port=PORT, debug=True)

