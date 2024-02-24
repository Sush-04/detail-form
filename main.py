from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'emp'
}

# Function to connect to MySQL database
def connect_to_database():
    try:
        cnx = mysql.connector.connect(**mysql_config)
        print("Connected to mysql")
        return cnx
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

@app.route('/')
def index():
   return render_template('index.html')

# Route to insert employee data into MySQL
@app.route('/add_employee', methods=['POST'])
def add_employee():
    try:
        data = request.get_json()
        print(data)
        if data:
            conn = connect_to_database()
            print("connected to db")
            if conn:
                print("enters")
                cursor = conn.cursor()
                print("cursor connected")
                query = "INSERT INTO details (name, empid, dept, dob, gender, designation, salary,experience,lang) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
                employee_values = (
                    data['name'], data['empid'], data['dept'], data['dob'], data['gender'],
                    data['role'], data['salary'],data['experience'],data['lang']
                )
                print(employee_values)
                cursor.execute(query, employee_values)
                print("inserted")

                conn.commit()
                cursor.close()
                conn.close()
                return jsonify({'message': 'Employee details added successfully'})
            else:
                print("Failed")
                return jsonify({'error': 'Failed to connect to the database'})
        else:
            return jsonify({'error': 'No data provided'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
