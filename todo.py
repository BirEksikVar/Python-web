from flask import Flask,render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy 
import urllib.parse
#1.yol____mssql
#params = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=DalmaDerine-;DATABASE=todoapp;UID=sa;PWD=istatistik")

app = Flask(__name__)
app.secret_key="dene"


#sqlite3 __ile baglanma
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/DalmaDerine/Desktop/todoapp/todo.db'
#mssql __e BAĞLANMAmssql+pyodbc://user:pwd@server/database?driver=SQL+Server"
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://sa:istatistik@DalmaDerine/todoapp?driver=SQL+Server"
"""
1.yol__msql
app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
"""
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos = todos)

@app.route("/complete/<string:id>")
def complete(id):
    todo = Todo.query.filter_by(id=id).first()
    """
    if todo.complete == True:
        todo.complete == False
    else:
        todo.complete == True
    #yerine
    """
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deletetodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/add",methods=["POST"])
def addTodo():
    title = request.form.get("title")
    if len(title)==0:
        flash("Lütfen bir başlık giriniz","danger")
        return redirect(url_for("index"))
    else:
        newTodo = Todo(title = title,complete=False)
        db.session.add(newTodo)
        db.session.commit()
        return redirect(url_for("index"))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

