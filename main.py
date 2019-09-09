from flask import Flask, request, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_, select

app= Flask(__name__)
app.config['SECRET_KEY']='unique'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employeedatabase.db'


db= SQLAlchemy(app)

class Employee(db.Model):
   
   id = db.Column(db.Integer, primary_key = True)

   name = db.Column(db.String(100), nullable=False)

   designation = db.Column(db.String(100), nullable=False)  

   addr = db.Column(db.String(200), nullable=False)

   phone = db.Column(db.String(10), nullable=False, unique=True)

   def __repr__(self):
      return '<Employee: {}>'.format(self.name)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/disp", methods=["GET","POST"])
def disp_all():
    return render_template("list.html",employee= Employee.query.all())

@app.route('/show_all')
def show_all():
    return render_template('show_all.html', employee= Employee.query.all() )


@app.route("/add", methods=["GET", "POST"])
def add():
    return render_template("add.html")

@app.route("/add_employee", methods=["GET","POST"])
def add_emp():
    if request.method == 'POST':
      if not request.form['name'] or not request.form['designation'] or not request.form['addr']or not request.form['phone']:
         flash('Please enter all the fields', 'error')
      else:
         username = request.form['name']
         count = Employee.query.filter(Employee.name == username).count()
         if count <= 0:
             emp = Employee(name=request.form['name'], designation= request.form['designation'],addr=request.form['addr'], phone=request.form['phone'])
             db.session.add(emp)
             db.session.commit()
             flash('Record was successfully added')
         else:
             flash('User Already Exist')
 
         return redirect(url_for('show_all'))
    return render_template('add.html')
    

@app.route("/delete", methods=["GET","POST"])
def delete():   
    return render_template("delete.html",employee= Employee.query.all())
    

@app.route("/delete_emp/<int:id>", methods=["GET","POST"])
def delete_emp(id): 
    res = db.session.query(Employee).filter(Employee.id==id).first() 
    db.session.delete(res)
    db.session.commit()    
    flash('Deleted successfully')
    return redirect(url_for('delete'))

@app.route("/search", methods=["GET","POST"])
def search():   
   return render_template("search.html")


@app.route("/results", methods = ['GET', 'POST'])
def search_advanced():
    if request.method == 'GET':
       result = request.args.get('query')
       print(result)

       qry = Employee.query.filter(or_((Employee.name.contains(result)),(Employee.designation.contains(result)),(Employee.phone.contains(result))))
       count = qry.count();
       if count > 0:
          return render_template('view.html', employee= qry.all())

    return render_template('search.html')



if __name__ == "__main__":
    db.create_all()   
    app.run(debug=True)
