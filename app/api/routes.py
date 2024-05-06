from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Chameleon, chameleon_schema, chameleons_schema

api = Blueprint('api', __name__, url_prefix='/api')

# Insert chameleon into database
@api.route('/chameleons', methods = ['POST'])
@token_required
def create_chameleon_data(current_user_token):
    name = request.json['name']
    sex = request.json['sex']
    dob = request.json['dob']
    dod = request.json['dod']
    dams_sire = request.json['dams_sire']
    sire = request.json['sire']
    dams= request.json['dams']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    chameleon = Chameleon(name, sex, dob, dod, dams_sire, sire, dams, user_token = user_token )

    db.session.add(chameleon)
    db.session.commit()

    response = chameleon_schema.dump(chameleon)
    return jsonify(response)

# Retrieve all chameleons
@api.route('/chameleons', methods = ['GET'])
@token_required
def get_chameleons(current_user_token):
    a_user = current_user_token.token
    chameleons = Chameleon.query.filter_by(user_token = a_user).all()
    response = chameleons_schema.dump(chameleons)
    return jsonify(response)

# Retrieve a single chameleon
@api.route('/chameleons/<id>', methods = ['GET'])
@token_required
def get_single_chameleon(current_user_token, id):
    chameleon = Chameleon.query.get(id)
    response = chameleon_schema.dump(chameleon)
    return jsonify(response)

# Update chameleon info
# 'PUT' is the replace command
@api.route('/chameleons/<id>', methods = ['POST','PUT'])
@token_required
def update_chameleon(current_user_token,id):
    chameleon = Chameleon.query.get(id) 
    chameleon.name = request.json['name']
    chameleon.sex = request.json['sex']
    chameleon.dob = request.json['dob']
    chameleon.dod = request.json['dod']
    chameleon.dams_sire = request.json['dams_sire']
    chameleon.sire = request.json['sire']
    chameleon.dams = request.json['dams']
    chameleon.user_token = current_user_token.token

    db.session.commit()
    response = chameleon_schema.dump(chameleon)
    return jsonify(response)

@api.route('/chameleons/<id>', methods = ['DELETE'])
@token_required
def delete_chameleon(current_user_token, id):
    chameleon = Chameleon.query.get(id)
    db.session.delete(chameleon)
    db.session.commit()
    response = chameleon_schema.dump(chameleon)
    return jsonify(response)