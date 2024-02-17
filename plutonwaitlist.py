from flask import Flask, render_template, request
import mysql.connector
import logging

app = Flask(__name__)

# Function to connect to the MySQL database
def connect_db():
    try:
        return mysql.connector.connect(
            host='sql5.freesqldatabase.com',
            user='sql5684687',
            password='x4ckaRmGd5',
            database='sql5684687'
        )
    except Exception as e:
        logging.error("Database connection failed: %s", e)
        return None

# Define your Flask routes here
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_email', methods=['POST'])
def submit_email():
    if request.method == 'POST':
        email = request.form['email']
        if email:
            conn = connect_db()
            if conn:
                try:
                    cursor = conn.cursor()
                    # Insert the email into the database
                    cursor.execute("INSERT INTO emails (email) VALUES (%s)", (email,))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    message = "Email submitted successfully!"
                except Exception as e:
                    message = "An error occurred while inserting email: " + str(e)
            else:
                message = "Failed to connect to the database. Please try again later."
        else:
            message = "Email cannot be empty!"
        return render_template('message.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)