from flask import Flask, render_template, request, session, redirect, url_for
import os
from datetime import datetime, timedelta
from database import *

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta( minutes = 60 )

@app.route('/')
def main_page():
    Session = sessionmaker(bind = engine)
    s = Session()
    resume = s.query(Resume).all()
    return render_template('main_page.html' , resume = resume )

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect('/')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pass']
        Session = sessionmaker(bind=engine)
        s = Session()
        try:
            query = s.query(User).filter(User.username.in_([username]))
            result = query.first()
            if result.password == password:
                session['logged_in'] = True
                session['username'] = username
                session['access'] = result.access
                return redirect('/')
            else:
                error = 'نام کاربری یا رمز عبور اشتباه است'
                return render_template('login.html', error = error)

        except:
            error = 'نام کاربری یا رمز عبور اشتباه است'
            return render_template('login.html', error = error )

    return render_template('login.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        id = None
        username = request.form['username']
        password = request.form['pass']
        email = request.form['email']
        Session = sessionmaker(bind=engine)
        s = Session()
        try:
            query = s.query(User).filter(User.username.in_([username]))
            query1 = s.query(User).filter(User.email.in_([email]))
            result = query.first()
            result1 = query1.first()
            if result or result1:
                error = 'نام کاربری یا ایمیل وجود دارد!'
                return render_template('signup.html', error = error)           
            else:
                Session = sessionmaker(bind=engine)
                session = Session()
                user = User(id, username, password, email, 3)
                session.add(user)
                session.commit()
                return redirect('/login')
  
        except:            
            error = ''
            return render_template('signup.html', error = error)            

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['username'] = ''
    session['access'] = 0
    return main_page()

@app.route('/change-password', methods = ['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        password = request.form['pass']
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.username.in_([session['username']]))
        result = query.first()
        result.password = password
        s.commit()
        return redirect('/')
    
    return render_template('change_password.html')

@app.route('/add-resume', methods = ['GET', 'POST'])
def add_resume():
    if request.method == 'POST' and session['logged_in']:
        fname = request.form['fname']
        lname = request.form['lname']
        education = request.form['education']
        skill = request.form['skill']
        try:
            picture = request.files['picture']
            document = request.files['document']
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], picture.filename))
            document.save(os.path.join(app.config['UPLOAD_FOLDER'], document.filename))
        except:
            error = 'تمام فیلدها را پر کنید'
            return render_template('add_resume.html', error = error)
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.username.in_([session['username']]))
        result = query.first()
        uid = result.id
        sess = Session()
        resume = Resume(None, uid, fname, lname, education, picture.filename, document.filename, skill)
        sess.add(resume)
        sess.commit()
        return redirect('/')

    return render_template('add_resume.html')

@app.route('/resume-detail/<id>')
def resume_detail( id ):
    Session = sessionmaker(bind=engine)
    resume_session = Session()
    comment_session = Session()
    resume_query = resume_session.query(Resume).filter( Resume.id.in_([id]))
    resume_result = resume_query.first()
    comment_query = comment_session.query(Comment).filter( Comment.rid.in_([id]))
    comment_result = comment_query.all()
    return render_template('resume_detail.html', resume = resume_result, comment = comment_result )

@app.route('/add-comment<rid>' , methods = ['GET', 'POST'])
def add_comment(rid):
    comment = request.form['comment']
    Session = sessionmaker(bind=engine)
    resume_session = Session()
    add_comment_session = Session()
    comment_session = Session()
    user_session = Session()
    resume_query = resume_session.query(Resume).filter(Resume.id.in_([rid]))
    resume_result = resume_query.first()
    uid = user_session.query(User).filter(User.username.in_([session['username']])).first().id
    comm = Comment(None, uid, rid, comment)
    add_comment_session.add(comm)
    add_comment_session.commit()
    comment_query = comment_session.query(Comment).filter(Comment.rid.in_([rid]))
    comment_result = comment_query.all()
    return render_template('resume_detail.html', resume = resume_result, comment = comment_result)

@app.route('/show-resume/<id>', methods = ['GET', 'POST'])
def show_resume(id):
    Session = sessionmaker(bind=engine)
    resume_session = Session()
    resume_query = resume_session.query(Resume).filter(Resume.id.in_([id]))
    resume_result = resume_query.first()
    return render_template('show_resume.html', resume = resume_result)

@app.route('/edit-resume/<id>', methods = ['GET', 'POST'])
def edit_resume(id):
    if request.method == 'POST' and session['access'] == 1:
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(Resume).filter(Resume.id.in_([id]))
        result = query.first()
        education = request.form['education']
        skill = request.form['skill']
        try:
            document = request.files['document']
            document.save(os.path.join(app.config['UPLOAD_FOLDER'], document.filename))
            result.document = document.filename
        except:
            error = 'تمام فیلدها را پر کنید'
            return render_template('show_resume.html', error = error)

        result.education = education
        result.skill = skill
        s.commit()
        
    return redirect('/resume-detail/' + id)

@app.route('/document')
def document():
    # filename = 'uploads/document.pdf'
    return render_template('document.html')
    





if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run( debug = True )