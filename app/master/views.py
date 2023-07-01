from flask import Flask, make_response,jsonify,request,Blueprint
from flask_restful import Resource,Api
from app.userRegister.controller import insert_user,find_user
from app.userRegister.verification import Verification,emailVerification
from app import api
from app import mail
from flask_mail import Message
example_blueprint = Blueprint("example_blueprint",__name__)


class UserRegistration(Resource):
    def post(self):
        try:
            email = request.json.get("email","NA")
            password = request.json.get("password","NA")
            print("This is line 16",email,password)
            role = request.json.get("role",False)
            is_verify = request.json.get("is_verify",False)


            # Checking if email/password  is empty
            verify_obj = Verification()
            result = verify_obj.verify_email_password(email,password)
            if result != "Valid email password":
                return make_response(jsonify({"message":result}))

            #checking if emailid entred is correct
            object_of_email_verification = emailVerification()
            result_of_valid_email =object_of_email_verification.verfy_email(email)
            if not result_of_valid_email:
                return make_response(jsonify({"message":"Invalid Email"}))
            ######################################

            details_of_user = {"email": email, "password": password, "role": role, "is_verify": is_verify}

            results = insert_user(details_of_user)
            print(results)
            result = True
            if results == True:
                print("line1")
                msg = Message('Testing', sender='ap7788546@gmail.com', recipients=[email])
                print("line1")
                msg.body = "This is test mail"
                print("line1")
                mail.send(msg)
                print("line1")
                return make_response(jsonify({"message":"please check your mail for verification tokken"}))
            return make_response(jsonify({"message":"Partial"}))
            ######################################
        except Exception as e:
            return make_response(jsonify({"message":f"str{e}"}))



api.add_resource(UserRegistration, '/')
