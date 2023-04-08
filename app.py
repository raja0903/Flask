from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    #time=db.Column(db.DateTime,default=datetime.utcnow)
     
    def __repr__(self) -> str:
        return f'{self.sno}-{self.title}'
    

@app.route('/',methods=['POST','GET'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()
    return render_template("index.html",alltodo=alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    alltodo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(alltodo)
    db.session.commit()
    return redirect('/')
    
    

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        mn=Todo.query.filter_by(sno=sno).first()
        mn.title=title
        mn.desc=desc
        db.session.add(mn)
        db.session.commit()
        return redirect('/')
    alltodo=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",alltodo=alltodo)

if __name__=='__main__':
    app.run(debug=True)