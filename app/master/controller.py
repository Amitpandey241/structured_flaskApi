from app import mongo

def insert_user(user_detail):
    try:
        """here query_to_insert_user_in_db.acknowledged gives
           status which is boolean value.
         """
        email = user_detail['email']
        # print(email)
        find_email= mongo.db.user.find_one({'email':email})
        # print(find_email)
        if not find_email:
            status=mongo.db.user.insert_one(user_detail)

            reesult = True if status.acknowledged else False
            return reesult
        else:
            return False
    except Exception as e:
        return str(e)

"""This code is to test insert_user fucntion"""
# test_data = {"email" :"Amit pandey", "passsword": "djnfjsdnfa"}
# print(insert_user(test_data))

def find_user(user_details):
    try:
        result =  mongo.db.user.find_one(user_details)

        if result:
            return True
        else:
            return False
    except Exception as e:
        return str(e)