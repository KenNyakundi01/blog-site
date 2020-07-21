from flask import render_template, redirect, url_for, abort, request
from .forms import BlogsiteForm, CommentForm, CategoryForm
from ..auth.forms import LoginForm
from . import main
from ..models import Blogsite, User, Comment
from flask_login import login_required, current_user

@main.route('/', methods=['GET', 'POST'])
def index():
    title = "Blogsite"
    movie_blogs = Blogsite.get_blogs(1)
    product_blogs = Blogsite.get_blogs(2)
    job_blogs = Blogsite.get_blogs(3)
    motivation_blogs = Blogsite.get_blogs(4)
    return render_template('main/index.html', title=title, movie_blogs=movie_blogs, product_blogs=product_blogs, job_blogs=job_blogs, motivation_blogs=motivation_blogs )


@main.route('/add', methods= ['GET', 'POST'])
@login_required
def add_Blogsite():
    form = BlogsiteForm()
    categories = Category.get_all_cats()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cate = request.form['category']
        Blogsite = Blogsite(title=title, content=content, category_id=cate, user=current_user)
        Blogsite.save_Blogsite()
        return redirect(url_for('main.index'))
    return render_template('main/create_Blogsite.html', Blogsite_form=form, categories=categories)

    # if form.validate_on_submit():
    #     title = form.title.data
    #     content = form.content.data
    #     category = form.category.data

@main.route('/Blogsite/<int:Blogsite_id>')
def display_Blogsite(Blogsite_id):
    Blogsite = Blogsite.get_Blogsite_by_id(Blogsite_id)
    comments= Comment.get_all_comments(Blogsite_id)
    return render_template('main/Blogsite.html', Blogsite=Blogsite, comments=comments)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(name = uname).first()

    if user is None:
        abort(404)
    return render_template('profile/profile.html', user=user)

@main.route('/user/<uname>/update', methods= ['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(name=uname).first()
    update_form = UpdateForm()
    if user is None:
        abort(404)

    if update_form.validate_on_submit():
        user.bio = update_form.bio.data
        User.update_user(user)
        return redirect(url_for('.profile', uname=user.name))
    return render_template('profile/update.html', update_form = update_form)

@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(name = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))

@main.route('/upvote/<int:Blogsite_id>')
@login_required
def upvote(Blogsite_id):
    Blogsite = Blogsite.query.filter_by(id = Blogsite_id).first()
    if Blogsite.upvotes is None:
        Blogsite.upvotes = 0
        Blogsite.upvotes += 1
    else:
        Blogsite.upvotes += 1
    db.session.commit()
    return redirect(url_for('main.index'))
    
    
@main.route('/downvote/<int:Blogsite_id>')
@login_required
def downvote(Blogsite_id):
    Blogsite = Blogsite.query.filter_by(id = Blogsite_id).first()
    if Blogsite.downvotes is None:
        Blogsite.downvotes = 0
        Blogsite.downvotes += 1
    else:
        Blogsite.downvotes += 1
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/Blogsite//comment/new/<int:Blogsite_id>', methods=['GET', 'POST'])
@login_required
def comment_Blogsite(Blogsite_id):
    comment_form = CommentForm()
    Blogsite= Blogsite.get_Blogsite_by_id(Blogsite_id)
    if comment_form.validate_on_submit():
        content = comment_form.content.data
        new_comment = Comment(content=content, Blogsite_id=Blogsite_id)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('main.display_Blogsite', Blogsite_id=Blogsite_id))
    return render_template('main/Blogsite_comment.html', form = comment_form, Blogsite=Blogsite)

