from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import user

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(120),nullable=False,unique=True)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users=User.query.all()
    return render_template ('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    username=request.form['username']
    email=request.form['email']
    new_user=User(username=username,email=email)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_user(id):
    user=User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def edit_user(id):
    user = User.query.get_or_404(id)
    return render_template('edit.html', user=user)

@app.route('/update/<int:id>', methods=['POST'])
def update_user(id):
    user = User.query.get(id)
    user.username = request.form['username']
    user.email = request.form['email']
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug= True)