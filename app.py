from distutils.log import debug
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#Database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cam_master'

mysql = MySQL(app)

@app.route("/")
def hello_world():
      return jsonify({"status":"ok"})

#registration module
@app.route("/createUser", methods=['POST'])
def createUser():
    #fetching data from request
    socket_data = request.get_json()
    print(socket_data)

    #splitting the data
    first_name = socket_data['first_name']
    last_name = socket_data['last_name']
    email = socket_data['email']
    password = socket_data['password']

    #to connect to sql
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM user_data_master WHERE email = '%s'" %(email))

    # row_headers=[x[0] for x in cursor.description]
    row = cursor.fetchall()
    print(row)
    # json_data=[]
    # for result in row:
    #     json_data.append(dict(zip(row_headers,result)))
    #     print(json_data)

    # count = json_data[0]['COUNT(*)']
    count = row[0][0]
    if(count == 0):
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO user_data_master (first_name,last_name,email,password) VALUES ('%s','%s','%s','%s')"%(first_name,last_name,email,password))
        mysql.connection.commit()

        return jsonify({
            "status":"success",
            "statusCode":"200",
            "message" : "User created"
        })

    else:
        return jsonify({
            "status":"failure",
            "statusCode":"SC001",
            "message" : "User already exist"
        })

#login module
@app.route("/userLogin" , methods=['GET'])
def Login():
    socket_data = request.get_json()
    #print(socket_data)

    email = socket_data['email']
    password = socket_data['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM user_data_master WHERE email = '%s'" %(email))
    row = cursor.fetchall()
    count = row[0][0]

    if (count == 1):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT password FROM user_data_master WHERE email = '%s'" %(email))
        data = cursor.fetchall()
        pw = data[0][0]
        if (pw == password):
            return jsonify({
                "status":"success",
                "statusCode":"200",
                "message":"Login Successful"
            })
        else:
                return jsonify({
                "status":"failure",
                "statusCode":"SC001",
                "message":"Invalid Password"
            })

    else:
        return jsonify({
            "status":"failure",
            "statusCode":"SC001",
            "message":"No User Found"
        })

#username update module
@app.route("/userUpdate", methods=['PUT'])
def updateName():
    socket_data = request.get_json()

    email = socket_data['email']
    pwd = socket_data['password']
    newf = socket_data['new_fname']
    newl = socket_data['new_lname']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT count(*) FROM user_data_master WHERE email='%s' and password='%s'" %(email,pwd))
    data = cursor.fetchall()
    count = data[0][0]
    
    if(count == 1):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE user_data_master SET first_name ='%s', last_name = '%s' WHERE email='%s'" %(newf,newl,email))
        mysql.connection.commit()

        return jsonify({
            "status":"success",
            "statusCode":"200",
            "message":"Username updated"
        })
    else:
        return jsonify({
            "status":"failure",
            "statusCode":"SC001",
            "message":"Invalid Email or Password"
        })

#password update module
@app.route("/passUpdate", methods=['PUT'])
def updatePass():
    socket_data = request.get_json()

    email = socket_data['email']
    pwd = socket_data['old_pass']
    newpw = socket_data['new_pass']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT count(*) FROM user_data_master WHERE email='%s' and password='%s'" %(email,pwd))
    data = cursor.fetchall()
    count = data[0][0]
    
    if(count == 1):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE user_data_master SET password = '%s' WHERE email='%s'" %(newpw,email))
        mysql.connection.commit()

        return jsonify({
            "status":"success",
            "statusCode":"200",
            "message":"Password updated"
        })

    else:
        return jsonify({
            "status":"failure",
            "statusCode":"SC001",
            "message":"Invalid Email or Password"
        })

#user deletion module
@app.route("/accDel",methods=['DELETE'])
def accountDel():
    socket_data = request.get_json()

    email = socket_data['email']
    password = socket_data['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT count(*) FROM user_data_master WHERE email='%s' and password='%s'" %(email,password))
    data = cursor.fetchall()
    count = data[0][0]

    if(count == 1):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM user_data_master WHERE email='%s' and password='%s'" %(email,password))
        mysql.connection.commit()

        return jsonify({
            "status":"success",
            "statusCode":"200",
            "message":"User Deleted"
        })
    else:
        return jsonify({
            "status":"failure",
            "statusCode":"SC001",
            "message":"Invalid Email or Password"
        })

app.run(host="0.0.0.0",port=5080,debug = True)