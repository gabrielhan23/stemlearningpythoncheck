from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
import uuid, json
from pathlib import Path
import glob, os, shutil

from files.setup import *
from files.databases import *
from files.forms import *
from files.functions import *
from files.questions import *

@app.route('/', methods=['GET', 'POST'])
def home():
  if current_user.is_authenticated:
    return redirect(url_for("questions"))
  else:
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
      return redirect(url_for("questions"))
    form = LoginForm()
    if form.validate_on_submit():
      user = User.query.filter_by(username=form.username.data.lower()).first()
      if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user)
        flash("You have been logged in", "success")
        return redirect(url_for("questions"))
      else:
        flash("Incorrect username or password.", "danger")
    return render_template("login.html", form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
      return redirect(url_for("questions"))
    form = RegistrationForm()
    if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
      user = User(username=form.username.data.lower(), password=hashed_password)
      db.session.add(user)
      db.session.commit()
      
      login_user(user)
      flash("You have successfuly made an account.", "success")
      return redirect(url_for("questions"))
    return render_template("signup.html", form=form)

@app.route('/questions', methods=['GET', 'POST'])
@login_required
def questions():
    return render_template("questions.html", questions=questionsMaster, passed=current_user.passed)

@app.route('/questions/<num>', methods=['GET', 'POST'])
@login_required
def questionPage(num):
    if str(num) in questionsMaster:
      theQuestion = questionsMaster[str(num)]
      Path("files/code/"+current_user.username).mkdir(parents=True, exist_ok=True)
      f = open("files/code/"+current_user.username+"/"+num+".py", "a")
      f.close()
      f = open("files/code/"+current_user.username+"/"+num+".py", "r")
      answer = f.read()
      form = QuestionForm(code=answer)
      if form.validate_on_submit():
        # form.code.data
        if "import" in form.code.data and "files" in form.code.data and "from" in form.code.data:
          flash("You failed :(. This is why: " + "Import Error", "danger")
          return render_template("question.html", question=questionsMaster[str(num)], form=form)
        f = open("files/code/"+current_user.username+"/"+num+".py", "w")
        f.write(form.code.data)
        f.close()
        for x in theQuestion[2]:
          result = checkQuestion(current_user.username+"/"+num,x[0],x[1])
          if result[0] == False:
            flash("You failed :(. This is why: " + result[1], "danger")
            return render_template("question.html", question=questionsMaster[str(num)], form=form)
        
        if current_user.passed and theQuestion[0] in current_user.passed.split(";"):
          print("done already")
        elif current_user.passed:
          current_user.passed += ";"+theQuestion[0]
          db.session.commit()
        else:
          current_user.passed = theQuestion[0]
          db.session.commit()
        flash("You have successfuly answered the question!", "success")
        return redirect(url_for("questions"))
      if current_user.passed and theQuestion[0] in current_user.passed:
        flash("You have already completed this problem.", "info")
      return render_template("question.html", question=questionsMaster[str(num)], form=form)
    else:
      return render_template("error.html")

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
  if current_user.username == "admin":
    users = User.query.all()
    tasks = questionsMaster
    return render_template("admin.html", users=users, tasks=tasks)
  return render_template("error.html")

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  form = AccountForm()
  if form.validate_on_submit():
    if bcrypt.check_password_hash(current_user.password, form.oldpassword.data):
      hashed_password = bcrypt.generate_password_hash(form.newpassword.data).decode("utf-8")
      current_user.password = hashed_password
      db.session.commit()
      flash("Your password has been changed", "success")
      return redirect(url_for("questions"))
    else:
      flash("Old password incorrect.", "danger")
  return render_template("account.html", form=form, username=current_user.username)

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
  if current_user.username == "admin":
    form = AdminPasswordForm()
    user = User.query.filter_by(username=username).first()
    code = {}
    path = 'files/code/'+username
    for filename in glob.glob(os.path.join(path, '*.py')):
      with open(os.path.join(os.getcwd(), filename), 'r') as f:
        code[os.path.basename(f.name)] = f.read()
    if form.validate_on_submit():
      user.password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
      db.session.commit()
      flash("Changed password for student.", "success")
      return redirect(url_for("admin"))
    return render_template("user.html", user=user, form=form, questions=questionsMaster, code=code)
  return render_template("error.html")

@app.route('/deleteuser', methods=['POST'])
@login_required
def deleteuser():
  if current_user.username == "admin":
    user = User.query.filter_by(username=request.form['username']).first()
    db.session.delete(user)
    db.session.commit()
    if os.path.isdir("files/code/"+request.form['username']):
      shutil.rmtree("files/code/"+request.form['username'])
    flash("Deleted user", "success")
    return redirect(url_for("admin"))
  return render_template("error.html")

@app.route('/signout', methods=['POST'])
@login_required
def signout():
  logout_user()
  flash("You have been logged out", "success")
  return redirect(url_for("login"))

@app.route('/changeusernames', methods=['GET','POST'])
@login_required
def changeusernames():
  if current_user.username == "admin":
    for user in User.query.all():
      #if user.username == "darrennchangg ":
        # user.username = "darrennchangg"
      print("hello")
    db.session.commit()
    print(User.query.all())
    flash("Deleted spaces", "success")
    return redirect(url_for("login"))
  return render_template("error.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
