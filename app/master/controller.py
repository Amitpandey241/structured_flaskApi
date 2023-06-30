from app import mongo

def insert_user(user_detail):
    try:
        """here query_to_insert_user_in_db.acknowledged gives
           status which is boolean value.
         """
        username = user_detail['username']
        # print(username)
        find_username= mongo.db.users.find_one({'username':username})

        if not find_username:
            status=mongo.db.users.insert_one(user_detail)

            reesult = True if status.acknowledged else False
            return reesult
        else:
            return False
    except Exception as e:
        return str(e)
# test_data = {"username": "Amit444", "password": "abc123"}
# print(insert_user(test_data))

def find_user(user_details):
    try:
        result =  mongo.db.users.find_one(user_details)

        if result:
            return True
        else:
            return False
    except Exception as e:
        return str(e)

# test_data = {"username": "Amit"}
# print(find_user(test_data))

def read(a, b, **kwargs):
    # findquery = {"username": username, "password": password}
    # projection = {"username": 1, "age": 1, "_id": 0}
    try:
        cursor =mongo.db.users.find_one(a, b)
        return cursor
    except Exception as e:
        return {str(e)}
# test_data = {"username": "Amit", "password": "abc123"}
# projection ={"username":1, "password":1,"_id":0}
# print(read(test_data,projection))

def delete_user(username):
    try:
        query = mongo.db.users.delete_one(username)
        return query.deleted_count
    except Exception as e:
        return {str(e)}

# test_data = {"username": "Amit444", "password": "abc123"}
# projection ={"username":1, "password":1,"_id":0}
# print(delete(test_data))


def update_users_age(find, update):
    # a represents match{}
    # b represents projection
    # find = {"username": username}
    # update = {"$set": {"age": age}}
    try:
        query = mongo.db.users.update_one(find, update)
        ack = query.acknowledged
        match = query.modified_count
        return [ack, match]
    except Exception as e:
        return {str(e)}
# n = {"username":"Amit"}
# # insert(n)
# up = {"$set":{"age":24}}
# u = updatee(n,up)
# print(u)
def find_user_details(username,password):
    try:
        query_to_find_user_details = mongo.db.users.find_one({"username":username,"password":password},{"username":1,"password":1,"_id":0})
        print(query_to_find_user_details)
        return query_to_find_user_details
    except Exception as e:
        return str(e)

# user_name = "Amit1"
# password = "password"
# find_user_details(user_name,password)
