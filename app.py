from flask import Flask , render_template,request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///doto.db"
db = SQLAlchemy(app)

class todo(db.Model):
    Sno = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(200) , nullable = False)
    desc = db.Column(db.String(500) , nullable = False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self) -> str:
       return f"{self.Sno}"


@app.cli.command()
def init_db():
    db.create_all()




@app.route('/' , methods = ['GET','POST'])
def hello_world():
    if request.method ==  'POST':
        title = request.form['title']
        desc = request.form['desc']
        Todo = todo(title = title , desc = desc)
        db.session.add(Todo)
        db.session.commit()
    allTodo = todo.query.all()
    print(allTodo)
    return render_template('index.html' , allTodo = allTodo)
    
@app.route('/show')
def products():
    allTodo = todo.query.all()
    print(allTodo)
    return 'this is products page'

@app.route('/update/<int:Sno>' ,methods = ['GET','POST'] )
def update(Sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        
        Todo = todo.query.filter_by(Sno=Sno).first()
        Todo.title = title
        Todo.desc = desc
        db.session.add(Todo)
        db.session.commit()
        return redirect("/")
        
    Todo = todo.query.filter_by(Sno=Sno).first()
    print(Todo)
    return render_template('update.html', todo = Todo)

@app.route('/delete/<int:Sno>')
def delete(Sno):
    Todo = todo.query.filter_by(Sno=Sno).first()
    db.session.delete(Todo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True , port = 5007)