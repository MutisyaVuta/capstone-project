from flask import Blueprint,jsonify,request

from flask_jwt_extended import create_access_token,JWTManager

from flask_jwt_extended import jwt_required, get_jwt_identity,unset_jwt_cookies

from . import db,bcrypt

from datetime import timedelta,datetime,timezone

from .models import User

import json


auth_blueprint=Blueprint('auth',__name__)#name of blue print
#signing up route
@auth_blueprint.route("/signup",methods=["POST"])
def signup():
    body=request.get_json()
    name=body.get('name')
    email=body.get('email')
    admn_no=body.get('admn_no')  
    password=body.get('password')

    ## Validation
    if not email or not password or not name:
        return jsonify({'message':"Required field missing"}),400
    
    if len(email)<4:
        return jsonify({'message':"Email too short"}),400
    
    if len(name)<4:
        return jsonify({'message':"Name too short"}),400
    
    if len(password)<4:
        return jsonify({'message':"Password too short"}),400
    
    if len(admn_no)<4:
        return jsonify({'message':"admission too short"}),400
    
    existing_member=User.query.filter_by(email=email).first()

    if existing_member:
        return jsonify({'message':f"Email already in use {email}"}),400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf8')
    
    member=User(name=name,email=email,password=hashed_password,admn_no=admn_no )
    db.session.add(member)
    db.session.commit()
    return jsonify({"message":"Sign up success"}),201

@auth_blueprint.route("/login",methods=["POST"])
def login():
    body=request.get_json()
    email=body.get('email')
    password=body.get('password')

        ## Validation
    if not email or not password:
        return jsonify({'message':"Required field missing"}),400
    user=User.query.filter_by(email=email).first()

 
    if not user:
        return jsonify({'message':"User not found"}),400
    
    
    pass_ok=bcrypt.check_password_hash(user.password.encode('utf-8'),password)
    
    if not pass_ok:
        return jsonify({"message":"Invalid password"}),401

    expires=datetime.utcnow()+timedelta(hours=24)
    ##access token
    access_token=create_access_token(identity={"id":user.id,"name":user.name,"role":"cats and dogs"},expires_delta=(expires-datetime.utcnow()))
   
    
    return jsonify({'user':user.details(),'token':access_token})

@auth_blueprint.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    user_data = [user.details() for user in users]
    return jsonify({'users': user_data})

@auth_blueprint.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    user_id = get_jwt_identity()["id"]
    response = jsonify({"msg": "User logged out successfully"})
    unset_jwt_cookies(response)
    return response, 200