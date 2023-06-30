import logging
from app import app,api,jwt
from app.master.controller  import insert_user,read,delete_user,update_users_age,find_user,find_user_details
from flask import Flask,request,make_response,jsonify,Blueprint
from flask_restful import Resource,Api
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from logging import FileHandler,WARNING




example_blueprint = Blueprint("example_blueprint",__name__)
logger = logging.getLogger(__name__)
file_handler = FileHandler('/home/amitpandey/Desktop/structured_flaskApi/app/logs/errors.txt')
file_handler.setLevel(WARNING)
app.logger.addHandler(file_handler)

class UserRegeister(Resource):
    def post(self):
        try:
            username = request.json.get("username", "NA")

            password = request.json.get("password", "NA")
            age = request.json.get("age", 0)
            val = {"username": username, "password": password, "age": age}
            if username in ["NA", ""] or password in ["NA", ""]:
                return make_response(jsonify({"message":"You might have not entered your name or password"}))
            else:
                results = find_user({"username":username})
                if results==True:
                    return make_response(jsonify({"message":f"Username {username} allready present"}))

                elif results ==False:
                    results = insert_user(val)
                    return make_response(jsonify({"message":"Succefully register!"}))
                else:
                    return make_response(jsonify({"message": "Please Try again later!"}), 400)

        except Exception as e:
            logger.error(e)
class Login(Resource):
    def post(self):
        #cursor = mycollection.find()
        username = request.json.get("username")
        password = request.json.get("password")
        User_name_login = username
        #db.Users.find({username: "Amit"}, password: "password"})
        findquery = {"username": username, "password": password}
        projection = {"username": 1,"age":1, "_id": 0}
        cursor = read(findquery,projection)
        user_details = cursor
        try:
            if user_details:
                user_name = user_details.get('username')
                access_token = create_access_token(identity=user_name)
                return make_response(jsonify({"message": f"Succefully logged in! {user_name}  ","access_token":access_token}))
            else:
                return jsonify({"message": f"User {username} is not Register!!"})
        except Exception as e:
            return jsonify({"error": str(e)})

class UpdateAge(Resource):
    @jwt_required()
    def post(self):
         try:
             username =request.json.get("username","NA")
             password = request.json.get("password","NA")
             age = request.json.get("age","NA")
             find_user_detail = find_user_details(username,password)

             if find_user_detail["username"] == username and find_user_detail["password"] == password:
                find_by = {"username":username,"password":password}
                update_field = {"$set":{"age":age}}
                current_user = get_jwt_identity()
                print(current_user)
                query = update_users_age(find_by,update_field)

                ackknowlegement_from_query = query[0]
                status_to_check_number_of_match = query[1]
                if ackknowlegement_from_query == True and status_to_check_number_of_match>0:
                    return jsonify({"message": f"Age updated for {username}"})
                else:
                    return jsonify({"message": "Error in updating!! Please check username!"})
             else:
                 return make_response(jsonify({"message":"Please check username or password"}))
         except Exception as e:
             # import traceback
             # print(traceback.print_exc())
             return jsonify({"error": str(e)})

class DeleteUser(Resource):
    @jwt_required()
    def post(self):
        username= request.json.get("username")
        password = request.json.get("password")
        find_user_detail = find_user_details(username,password)
        print(find_user_detail,"This is username: ",username,"this is password: ",password)
        if find_user_detail['username'] == username and find_user_detail['password'] == password:
            find = {"username":username,"password":password}
            query_response = delete_user(find)
            try:
                if query_response == 0:
                    return jsonify({"message": "No Such user exists"})
                else:
                    current_user = get_jwt_identity()
                    print(current_user)
                    return jsonify({"message": "User deleted sucessfully!"})
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            return make_response(jsonify({"message":f"This is no such user {username}"}))

api.add_resource(UserRegeister,'/register')
api.add_resource(Login,"/login")
api.add_resource(UpdateAge,"/update")
api.add_resource(DeleteUser,"/delete")

