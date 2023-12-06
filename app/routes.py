from flask import render_template, url_for, flash, redirect, request
# importing form
#⭐⭐⭐⭐
# from PACKAGE_NAME.MODULE_NAME
from app.forms import RegistrationForm, LoginForm   
from app import app,db,bcrypt
# importing models #⭐⭐⭐⭐
from app.models import User, Post

#for login
from flask_login import login_user, current_user, logout_user, login_required
# current_user to remember the current user
# logout_user to forget the current user

#To update the data and image of the user
from app.forms import UpdateAccountForm

#help to created random hex
import secrets

# To make sure the file is uploaded in the same format that is in the file is in PNG then the export will be in PNG and similarly
import os

# help to resize our image -> pip install Pillow
from PIL import Image

# to import postform from post.py
from app.forms import PostForm
# to display the 304-forbiden error
from flask import abort



# # some data - which is a list of dictionary
# posts = [
#     {
#         'author': 'Corey Schafer',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'April 20, 2018'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'April 21, 2018'
#     }
# ]

#having multiple routes for same page
#dont forget to change the function name
@app.route("/")
@app.route("/home")
def home():

    #take all the POST from the DB and display on home screen
    # posts = Post.query.all()
    # above display all the post on single page
    # 1= default page no, type=int-> throw error if someone try other than integer in url to access the page
    page = request.args.get('page', 1, type=int)
    # passing a query page=page
    # posts = Post.query.paginate(per_page=5, page=page)
    # lets order by date in descending order
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return  render_template("home.html", var_name=posts)

#having different route
#dont forget to change the function name
@app.route("/about")
def about():
    return render_template("about.html", title_name="About")

#⭐⭐⭐⭐
#                       this route can handle both "get" and "post" request
@app.route("/register", methods=["POST", "GET"])
def register(): 

    #If you are already logged in once and you click again on register or login page then it will automatically redirect you to the home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    #creating an instance of our form and passing it                      here
    form = RegistrationForm()
    #to validate the user
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        #flash display msg                                 bootstrap class
        flash('Your account has been created! You are now able to log in', 'success')
        # once the user is created and validated theb redirect to home page
        return redirect(url_for('login'))
    return render_template("register.html", title_name="Register", form = form)


#⭐⭐⭐⭐
@app.route("/login", methods=["POST", "GET"])
def login():

    #If you are already logged in once and you click again on register or login page then it will automatically redirect you to the home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))


    #creating an instance of our form and passing it                here
    form = LoginForm()
    if form.validate_on_submit():
        # test data
        # if form.email.data == 'kg@gmail.com' and form.password.data == '123':
        #     flash('You have been logged in!', 'success')  
        #     return redirect(url_for('home'))
        # else:
        #     flash('Login Unsuccessful. Please check username and password', 'danger')



        # lets query the db to see that the user exist
        user = User.query.filter_by(email=form.email.data).first()

        # checking the db pass and the pass they enter
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #          take the user , remember check box 
            login_user(user, remember=form.remember.data)

            # earlier in url if you access \account -> http://127.0.0.1:5000/login?next=%2Faccount -> it will take you login - once login - it will take you to home - if you want to access acc then you need to click to acc then you can see your account-
            # now in url if you access \account -> http://127.0.0.1:5000/login?next=%2Faccount -> it will take you login - once login - it will take you directly to acc

            # here "next" is a query parameter and to access the q we need to use "request"
            # args is a dictionary 
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

        
    return render_template("login.html", title_name="Login", form = form)



#logout route
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# to save pic data
def save_picture(form_picture):

    # to randomise the name of file upload
    random_hex = secrets.token_hex(8)

    # this os Returns two thing the file name and extension that is jpeG PNG -> It take input as the file name that the user has uploaded
    # f_name, f_ext = os.path.splitext(form_picture.filename)

    # We won't be using the variable file name so if you want to throw away any variable name then you can replace the variable name with an "_"
    _, f_ext = os.path.splitext(form_picture.filename)

    # Combining the random X and the File extension
    picture_fn = random_hex + f_ext

    # Now we need to give the path where we are saving the image
    # os.path.join() This basically creates the entire path from the system to the static folder to the hexcode generated plus its extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # how to resize our image (this will save both original and resize image in your folder)
    #              tuple
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # saving the new resize image
    i.save(picture_path)

    return picture_fn



@app.route("/account", methods=['GET', 'POST'])
# decorator - now our extension knows that we need to login to access the route(if you try to access the route without loging in the you will see nothing) but we need to also tell our extension where our login route is located -> go to __init__ and add "login_manager.login_view = 'login'"
@login_required
def account():
    # Creating an instance of the updated form
    form = UpdateAccountForm()
    # method
    if form.validate_on_submit():

        # to check if there is a pic data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            # updating current pic
            current_user.image_file = picture_file

        # updating info
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    
    elif request.method == 'GET':
        # will display existing data in boxes
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    # going to that route where img is present
    # "image_file" this var name should be same as created in models
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    #                                                      passing the img file into our template
    return render_template('account.html', title_name='Account', image_file=image_file, form=form)




# from app.forms import PostForm

# CRUD OP for posts
@app.route("/post/new", methods=['GET', 'POST'])
# in order to create a new post user must login in first that is y the following decorator is added
@login_required
def new_post():

    #creating and instance of our form
    form = PostForm()

    # VALIDATE THE FORM ONCE ITS PASTED
    if form.validate_on_submit():
        # adding data to oir database
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    #                                                  passing the instance of form, legend-> heading
    return render_template('create_post.html', title_name='New Post', form=form, legend='New Post')


# we can add variable in our routes -> <int:post_id>
@app.route("/post/<int:post_id>")
def post(post_id):
    # fetch this post if it exist
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title_name=post.title, post=post)


# from flask import abort

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
# require login
def update_post(post_id):

    #if the post exist with that id(this mainly give erroe when you name changes in url)
    post = Post.query.get_or_404(post_id)

    # only the user who created the post can update the post
    if post.author != current_user:
        abort(403)
    # creating an instance of the form 
    form = PostForm()

    if form.validate_on_submit():

        # overwrite the post content
        post.title = form.title.data
        post.content = form.content.data
        # no need to add() because we have over written above
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    
    # since we are updating the post we need to see what the previous title and post was
    # if the req is a get req then show the existing title and content
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title_name='Update Post', form=form, legend='Update Post')


# deleting a post from
# will only accept POST requests
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):

    #confirm post exist and it belongs to the current user
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    #deleting post 
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))



# home page pe jo post dikh rahe usme me name hai vo ek link hai - so by clicking that link we should be able to see all the posts uploadedby that user
@app.route("/user/<string:username>")
def user_posts(username):

    #take all the POST from the DB and display on home screen
    # posts = Post.query.all()
    # above display all the post on single page
    # 1= default page no, type=int-> throw error if someone try other than integer in url to access the page
    page = request.args.get('page', 1, type=int)

    # getting the first particular user
    user = User.query.filter_by(username=username).first_or_404()


    # passing a query page=page
    # posts = Post.query.paginate(per_page=5, page=page)
    # lets order by date in descending order
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    # filering by user
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)

    return render_template('user_posts.html', var_name=posts, user=user)

