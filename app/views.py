from flask import render_template, flash, redirect, request,session
from app import app, db, models, admin
from flask_admin.contrib.sqla import ModelView
import datetime
from .forms import LoginUserForm, SignUpForm, PostForm
import json
from flask import jsonify
#IncomeForm, ExpenceForm, GoalForm

admin.add_view(ModelView(models.PostTable, db.session))
admin.add_view(ModelView(models.UserTable, db.session))
admin.add_view(ModelView(models.FollowingTable, db.session))


@app.route('/follow/<int:user_id>' , methods=['POST'])
def follow(user_id):
    

    current_user = session['user_id']
    follower = models.FollowingTable.query.filter_by(UserID = current_user, FolloweeID = user_id ).first()
    
    if follower:
        #delete folower from FolowerTable
        db.session.delete(follower)
        action = 'Unfollow'
    else:
        new_follower = models.FollowingTable(UserID = current_user, FolloweeID = user_id)
        db.session.add(new_follower)
        action = 'Follow'

    db.session.commit()

    return jsonify({ "status": "OK", "action": action })

    


@app.route('/profile/<int:user_id>')
def profile(user_id):
    current_user = models.UserTable.query.get( session['user_id'])
    user = models.UserTable.query.get_or_404(user_id)
    posts = models.PostTable.query.filter_by(user_id = user_id).all()

    follower = models.FollowingTable.query.filter_by(UserID = current_user.id, FolloweeID = user_id).first()

    return render_template('ProfilePage.html', user=user, posts=posts, current_user = current_user.id , follower = follower)

@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    post = models.PostTable.query.get_or_404(post_id)
    user_id = session["user_id"]
    existing_like = models.Likes.query.filter_by(user_id=user_id,post_id=post_id).first()
    
    # Increment the like count
    if existing_like:
        return jsonify( {"status" : "not OK"} )
    
    like = models.Likes(user_id = user_id, post_id = post_id )
    db.session.add(like)
    post.like_count += 1
    db.session.commit()

    # Return the updated like count as JSON
    return jsonify({"status" : 'OK' , "like_count": post.like_count})

@app.route('/AddPost',methods=['POST','GET'])
def AddPost():
    form = PostForm()

    if request.method == 'POST':
        content = request.form['content']

        new_post  = models.PostTable(content = form.content.data,
                                     user_id = session['user_id'])
        db.session.add(new_post)
        db.session.commit()
        return redirect('/UserMain')        

    ##Succsessreturn redirect('/');
    return render_template('AddPost.html', form = form)

@app.route('/SignUp',methods=['POST','GET'])
def SignUp():
    form = SignUpForm()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        new_user = models.UserTable(username = form.username.data,
                                    password = form.password.data)
        db.session.add(new_user)
        db.session.commit()
        #return redirect('/UserMain')
        flash("Sign Up Succsessfull",'alert alert-success')
        return redirect('/')

    return render_template('Signup.html', form=form)

@app.route('/redirect_to_SignUp', methods=['POST','GET'])
def redirect_to_SignUp():
    return redirect('/SignUp')

@app.route('/UserMain', methods=['GET'])
def  UserMain():

    UserName = session['username']
    posts = models.PostTable.query.all()
    likes_objects = models.Likes.query.filter_by(user_id=session['user_id']).all()
    likes = [like.post_id for like in likes_objects]




    return render_template('UserHome.html', UserName = UserName , posts=posts, likes = likes)


@app.route('/UserMainFollowers', methods=['GET'])
def  UserMainFollower():

    UserName = session['username']
    user_id = session['user_id']
    
    # Assuming you have a relationship between FollowingTable and UserTable, adjust as needed
    following_users = models.FollowingTable.query.filter_by(UserID=user_id).all()
    
    # Extract the user IDs of the users being followed
    following_user_ids = [following.FolloweeID for following in following_users]

    # Retrieve posts from the users being followed
    posts = models.PostTable.query.filter(models.PostTable.user_id.in_(following_user_ids)).all()

    # Retrieve liked posts by the currently logged-in user
    likes_objects = models.Likes.query.filter_by(user_id=user_id).all()
    likes = [like.post_id for like in likes_objects]

    # All_posts = models.PostTable.query.all()

    # Only Query the posts by the Folowee ID in the users Follower Table.

    #posts = models.PostTable.query.all()
    #likes_objects = models.Likes.query.filter_by(user_id=session['user_id']).all()
    #likes = [like.post_id for like in likes_objects]


    return render_template('UserHomeFollower.html', UserName = UserName , posts=posts, likes = likes)





@app.route('/', methods=['POST','GET'])
def home():

    session.pop('user_id', None)
    session.pop('username', None)

    form = LoginUserForm()
    if request.method == 'POST':

        # Links up the data from the form fields
        username = form.username.data
        password = form.password.data

        # Find the Username from the DataBase, compare the Password to the input Password
        user = models.UserTable.query.filter_by(username=username).first()
        if user.password == password:

            # Redirect User to the MainPage
            flash("Logging In",'alert alert-success')
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect('/UserMain')
        
        else:
            flash("Incorecct Log In" , 'alert alert-warning')
            return redirect('/')


    return render_template('WebHome.html', form=form)



"""
@app.route('/redirect_to_goal', methods=['GET'])
def redirect_to_goal():
    return redirect('/goal')


@app.route('/', methods=['GET'])
def home():
    home = {'description': 'Welcome to Finance Manager.'}
    goal = models.Goals.query.all()

    if not goal:
        goal = None

    IncomeRecords = models.Incomes.query.all()
    ExpenceRecords = models.Expences.query.all()

    IncomeTotal = 0
    ExpenceTotal = 0

    for income in IncomeRecords:
        IncomeTotal += income.income_amount

    for expence in ExpenceRecords:
        ExpenceTotal += expence.expence_amount

    Savings = IncomeTotal - ExpenceTotal

    return render_template('home.html', title='Home',
                           home=home, goal=goal, Savings=Savings,
                           IncomeTotal=IncomeTotal,
                           ExpenceTotal=ExpenceTotal)


@app.route('/delete_record_expence/<int:record_id>', methods=['POST', 'GET'])
def delete_record_expence(record_id):

    record = models.Expences.query.get(record_id)
    db.session.delete(record)
    db.session.commit()
    return redirect('/listE')


@app.route('/delete_record_income/<int:record_id>', methods=['POST', 'GET'])
def delete_record_income(record_id):

    record = models.Incomes.query.get(record_id)
    db.session.delete(record)
    db.session.commit()
    return redirect('/listI')


@app.route('/clear_incomes', methods=['POST'])
def clear_incomes():

    Records = models.Incomes.query.all()

    for income in Records:
        db.session.delete(income)
    db.session.commit()
    return redirect('/listI')


@app.route('/clear_expences', methods=['POST'])
def clear_expences():

    Records = models.Expences.query.all()

    for expence in Records:
        db.session.delete(expence)
    db.session.commit()
    return redirect('/listE')


@app.route('/delete_goal', methods=['POST'])
def delete_goal():

    goal = models.Goals.query.all()

    # If The Goal Exists
    if goal is not None:
        db.session.delete(goal[0])
        db.session.commit()

    return redirect('/')


@app.route('/placeholder', methods=['POST'])
def placeholder():
    placeholder = {'description': 'This WebPage is under construction !!!'}
    return render_template('placeholder.html',
                           title='Under Construction',
                           placeholder=placeholder)


@app.route('/listI', methods=['GET', 'POS'])
def listI():
    list = {'description': 'You Can view your Incomes here!!!'}
    records = models.Incomes.query.all()

    totalIncome = 0
    for record in records:
        totalIncome += record.income_amount

    return render_template('listI.html', title="Incomes",
                           list=list, records=records,
                           totalIncome=totalIncome)


@app.route('/listE', methods=['GET', 'POS'])
def listE():
    list = {'description': 'You Can view your Expences here!!!'}
    records = models.Expences.query.all()
    totalExpence = 0

    for record in records:
        totalExpence += record.expence_amount

    return render_template('listE.html', title="Expences",
                           list=list, records=records,
                           totalExpence=totalExpence)


@app.route('/incomeEdit/<int:record_id>', methods=['GET', 'POST'])
def incomeEdit(record_id):

    record = models.Incomes.query.get(record_id)
    form = IncomeForm(obj=record)

    if form.validate_on_submit():
        record.income_type = form.income_type.data
        record.income_amount = form.income_amount.data
        db.session.commit()
        flash("Correctly Edited the Income", 'alert alert-success')

    # There is a issue with the errors getting flashed on page load
    # Could not figure out why that is happening, so i removed them for now

    # else:
    #    flash("There is an Error in your submission!",'alert alert-danger')
    #    for attributes,errors in form.errors.items():
    #        for error in errors:
    #            flash(f"{error}" , 'alert alert-warning')

    return render_template('incomeEdit.html', title="IncomeEdit",
                           record=record, form=form)


@app.route('/expenceEdit/<int:record_id>', methods=['POST'])
def expenceEdit(record_id):

    record = models.Expences.query.get(record_id)
    form = ExpenceForm(obj=record)
    if request.method == 'POST':
        if form.validate_on_submit():
            # This Pulls the Record we are Editing
            record.expence_name = form.expence_name.data
            record.expence_type = form.expence_type.data
            record.expence_amount = form.expence_amount.data
            db.session.commit()
            flash("Correctly Edited the Expence", 'alert alert-success')

        # There is a issue with the errors getting flashed on page load
        # Could not figure out why that is happening, so i removed them for now

        # else:
        #   flash("There is an Error in your submission!",'alert alert-danger')
        #   for attributes,errors in form.errors.items():
        #       for error in errors:
        #           flash(f"{error}" , 'alert alert-warning')

    return render_template('expenceEdit.html', title="ExpencesEdit",
                           record=record, form=form)


@app.route('/incomes', methods=['GET', 'POST'])
def incomes():
    form = IncomeForm()
    if form.validate_on_submit():

        # Adds the Data to the DataBase
        new_income = models.Incomes(income_name=form.income_name.data,
                                    income_type=form.income_type.data,
                                    transaction_date=datetime.datetime.utcnow(),
                                    income_amount=form.income_amount.data)
        db.session.add(new_income)
        db.session.commit()
        flash(f"A new Income: {form.income_name.data} Correctly Added",
              'alert alert-success')

    elif request.method == 'POST':
        flash("There is an Error in your submission!", 'alert alert-danger')
        for attributes, errors in form.errors.items():
            for error in errors:
                flash(f"{error}", 'alert alert-warning')
    return render_template('income.html', title='Incomes', form=form)


@app.route('/expences', methods=['GET', 'POST'])
def expences():
    form = ExpenceForm()
    if form.validate_on_submit():
        new_expence = models.Expences(expence_name=form.expence_name.data,
                                      expence_type=form.expence_type.data,
                                      transaction_date=datetime.datetime.utcnow(),
                                      expence_amount=form.expence_amount.data)
        db.session.add(new_expence)
        db.session.commit()
        flash(f"A new Expence: {form.expence_name.data} Correctly Adde!",
              'alert alert-success')

    elif request.method == 'POST':
        flash("There is an Error in your submission!", 'alert alert-danger')
        for attributes, errors in form.errors.items():
            for error in errors:
                flash(f"{error}", 'alert alert-warning')

    return render_template('expence.html', title='Expence', form=form)


@app.route('/goal', methods=['GET', 'POST'])
def goal():

    # This will check if a first record is present,
    #  if it is it will delete it before setting up a new goal,
    #  this will stop from entering more than one goal
    goals = models.Goals.query.all()
    form = GoalForm()

    if not goals:
        goalPresent = False
    else:
        goalPresent = True
    if form.validate_on_submit():
        if not goals:

            goal = models.Goals(goal_name=form.goal_name.data,
                                goal_amount=form.goal_amount.data)
            db.session.add(goal)
            db.session.commit()
            flash("Correctly Added a New Goal!", 'alert alert-success')

        else:
            goals[0].goal_name = form.goal_name.data
            goals[0].goal_amount = form.goal_amount.data
            db.session.commit()
            flash(f"Correctly Edited the Goal to {form.goal_name.data}",
                  'alert alert-success')

    elif request.method == 'POST':
        flash("There is an Error in your submission!", 'alert alert-danger')
        for attributes, errors in form.errors.items():
            for error in errors:
                flash(f"{error}", 'alert alert-warning')

    return render_template('goal.html', title='Goal Manager', form=form,
                           goalPresent=goalPresent)
"""