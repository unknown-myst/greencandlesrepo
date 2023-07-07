import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from greencandles import app, db, bcrypt
from greencandles.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from greencandles.models import User, Post,Stockbasics
from flask_login import login_user, current_user, logout_user, login_required


from flask import jsonify
from greencandles.utils import import_data_from_csv,return_stocks_info,return_csv,pie_data
app.app_context().push()



@app.route("/home")
def home():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route("/")
@app.route("/home2")
def home2():    
    return render_template('home2.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('user/register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('portfolio'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('user/login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home2'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('user/account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('post/create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post/post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('post/create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))




@app.route("/portfolio")
@login_required
def portfolio():
    form = UpdateAccountForm()
    form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('dashboard/portfolio.html',image_file=image_file, form=form)


@app.route("/algotrading")
@login_required
def algotrading():
    form = UpdateAccountForm()
    form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('dashboard/algotrading.html',image_file=image_file, form=form)


@app.route("/market")
@login_required
def market():
    form = UpdateAccountForm()
    form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('dashboard/market.html',image_file=image_file, form=form)



@app.route("/strategy")
@login_required
def strategy():
    form = UpdateAccountForm()
    form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('dashboard/strategy.html',image_file=image_file, form=form)

@app.route("/stocks/")
@login_required
def stocks1():
    stock_symbol = 'MRF.NS'
    form = UpdateAccountForm()
    form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('dashboard/stocks.html',image_file=image_file, form=form,stock_symbol=stock_symbol)


@app.route("/stocks/<endpoint>")
@login_required
def stocks(endpoint):
    stock_symbol = endpoint
    form = UpdateAccountForm()
    form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('dashboard/stocks.html',image_file=image_file, form=form,stock_symbol=stock_symbol)


@app.route("/profile")
@login_required
def profile():
    form = UpdateAccountForm()
    form.username.data = current_user.username
    form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('dashboard/profile.html', title='Account',
                           image_file=image_file, form=form)



@app.route('/getStockInfo/<endpoint>',methods=['GET'])
def get_stocks_info(endpoint):
    symbol = endpoint
    info = return_stocks_info(symbol)
    # info = str(type(info))
    return jsonify(info)


@app.route('/getChartData/<endpoint>',methods=['GET'])
def get_chart_data(endpoint):
    symbol = endpoint
    info = return_csv(symbol)        
    return jsonify(info)

@app.route('/getPieData/<endpoint>',methods=['GET'])
def get_pie_data(endpoint):
    info = pie_data(endpoint)
    return jsonify(info)


@app.route('/getListData', methods=['GET'])
def get_list_data():
    csv_file_path = os.path.join(app.root_path, 'static', 'data','setup', 'final2kcomps.csv')
    
    try:
        data = Stockbasics.query.all()
        if len(data) == 0:
            import_data_from_csv(csv_file_path)
        print('inside try')
    except:
        db.create_all()
        import_data_from_csv(csv_file_path)
        data = Stockbasics.query.all()
        print('inside except')
    
    list_of_all = []
    for i in data:
        list_of_all.append(f'{i.company} ({i.symbol})')
    json_data = jsonify(list_of_all)
    return json_data




@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'),404



@app.errorhandler(403)
def error_404(error):
    return render_template('errors/404.html'),403


@app.errorhandler(500)
def error_404(error):
    return render_template('errors/404.html'),500
