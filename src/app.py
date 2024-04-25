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
    print(members)
    if members is None:
        return jsonify({"error": "No members found"}), 404

    return jsonify(members), 200
        

@app.route('/member', methods=['POST'])
def add_member():
    data = request.json
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    
    first_name = data.get('first_name')
    age = data.get('age')
    if not first_name or not age:
        return jsonify({"error": "Missing required fields"}), 400
    
   
    add = jackson_family.add_member(data)
    return jsonify(add), 201

@app.route('/member/<int:id>', methods=['GET'])
def get_member_by_id(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Member not found"}), 404

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member_by_id(id):
    member = jackson_family.delete_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Member not found"}), 404

if __name__ == "__main__":
    # Definir el puerto en el que se ejecutará la aplicación
    PORT = int(os.environ.get('PORT', 3000))

    # Iniciar la aplicación Flask
    app.run(host='0.0.0.0', port=PORT, debug=True)

