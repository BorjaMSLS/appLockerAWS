from flask import Flask, jsonify, request
from util import createUsersAPI, getLockersAPI, assignLockerAPI, findByEmailAPI, releaseLockerAPI, getLockerAttAPI, getUsersAPI, authenticateAPI, getPersonLockersAPI

application = Flask(__name__)
application.config['WTF_CSRF_ENABLED'] = False

@application.route('/hello')
def hello():
    return 'Hello, Aniti!'

@application.route('/newUser', methods = ['POST'])
def handle_user():
    data = request.json  # Assumes request data is in JSON format
    print(data)
    name_user = data['name']
    email_user = data['email']
    result = createUsersAPI(name_user,email_user)
    response = jsonify({'result': result})
    return response


@application.route('/getLockers/<center_id>', methods = ['GET'])
def handle_get_lockers(center_id):
     # Assumes request data is in JSON format
    result = getLockersAPI(center_id)
    return jsonify(result)

@application.route('/findByEmail/<search>', methods = ['GET'])
def handle_find_users(search):
     # Assumes request data is in JSON format
    result = findByEmailAPI(search)
    return jsonify(result)

@application.route('/getLockerAtt/<person_id>', methods = ['GET'])
def handle_get_locker_att(person_id):
     # Assumes request data is in JSON format
    result = getLockerAttAPI(person_id)
    return jsonify(result)

@application.route('/getPersonLockers/<person_email>', methods = ['GET'])
def handle_get_person_lockers(person_email):
     # Assumes request data is in JSON format
    result = getPersonLockersAPI(person_email)
    return jsonify(result)

@application.route('/authenticate/<email>/<passw>', methods = ['GET'])
def handle_get_auth(email, passw):
     # Assumes request data is in JSON format
    result = authenticateAPI(email, passw)
    return jsonify(result)

@application.route('/getUsers', methods = ['GET'])
def handle_get_users():
     # Assumes request data is in JSON format

    result = getUsersAPI()
    return jsonify(result)

@application.route('/assignLocker', methods = ['POST'])
def handle_locker_assign():
    data = request.json  # Assumes request data is in JSON format
    print(data)
    user_id = data['user_id']
    if 'locker_id' in data:
        result = assignLockerAPI(user_id,data['locker_id'])
    else:
        result = assignLockerAPI(user_id, "")

    response = jsonify({'result': result})
    return response

@application.route('/createFacility', methods = ['POST'])
def handle_facility():
    data = request.json  # Assumes request data is in JSON format
    print(data)
    name_facility = data['facilityName']
    address_facility = data['facilityAddress']
    city_facility = data['facilityCity']
    country_facility = data['facilityCountry']
    capacity_facility = data['facilityCapacity']
    result = createFacilityAPI(name_facility,city_facility,address_facility,country_facility,capacity_facility)
    response = jsonify({'result': result})
    return response

@application.route('/releaseLocker/<locker_id>', methods = ['POST'])
def handle_release_locker(locker_id):
     # Assumes request data is in JSON format
    result = releaseLockerAPI(locker_id)
    return jsonify(result)

if __name__ == '__main__':
    application.run()
