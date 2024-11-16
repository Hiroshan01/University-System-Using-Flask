from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'Hiroshan1999'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # user root
app.config['MYSQL_PASSWORD'] = ''  # password is null
app.config['MYSQL_DB'] = 'college'  # DB name 

mysql = MySQL(app)

# Root route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        try: #handle error
            email = request.form['email']
            password = request.form['password']

            cur = mysql.connection.cursor()
            # Fetch the admin user usingg email
            cur.execute("SELECT * FROM admin WHERE email = %s", (email,))
            admin_user = cur.fetchone()
            cur.close()

            print("check -->",admin_user)  

            # Check admin credi..
            if admin_user and admin_user[0] == password:  
                return redirect(url_for('admin_panel'))  # Redirect to admin panel
            else:
                flash('Invalid email or password.')
                return redirect(url_for('index'))  # Redirect to home if failed
        except Exception as e:
            flash('An error occurred: ' + str(e))
            return redirect(url_for('index'))  # Redirect to home on error

    return render_template('admin.html')  # Render the admin login form

@app.route('/adminPanal')
def admin_panel():
       cur = mysql.connection.cursor() #interact with DB
       cur.execute("SELECT * FROM students") #fetch all record from students table
       students = cur.fetchall() #retrive all the rows & store in student veri...
       return render_template('adminPanal.html', students=students) 

#registration
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        telephone = request.form['telephone']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students(name, email, course, telephone) VALUES(%s, %s, %s, %s)", (name, email, course, telephone))
        mysql.connection.commit()
        cur.close()  # Close the cursor
        return redirect(url_for('index'))  # Redirect to the index page after successful registration
    
    return render_template('registration.html')  # Render the registration form for GET requests
 
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    cur = mysql.connection.cursor() #create cursor object to execute query
    cur.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cur.fetchone()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        telephone = request.form['telephone']
        cur.execute("UPDATE students SET name = %s, email = %s, course = %s, telephone = %s WHERE id = %s", (name, email, course, telephone, id))
        mysql.connection.commit()
        return redirect(url_for('admin_panel'))
    return render_template('update_student.html', student=student)
    
    
@app.route('/delete/<int:id>', methods=['GET'])
def delete_student(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('admin_panel'))



if __name__ == '__main__':
    app.run(debug=True)
