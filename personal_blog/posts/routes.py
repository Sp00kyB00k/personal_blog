import os
from flask import render_template, redirect, url_for, \
    flash, request, abort, current_app
from flask_login import current_user, login_required
from ..decorators import permission_required
from . import posts
from .forms import PostForm, CommentForm
from ..models import Permission, Post, Comment, Category
from .. import db


@posts.route('/<category>')
def filter_on_category(category):
    page = request.args.get('page', type=int)
    category = Category.query.filter_by(name=category).first_or_404()
    pagination = category.posts.paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'])
    posts = pagination.items
    return render_template('index.html', pagination=pagination, posts=posts)


@posts.route("/new", methods=['GET', 'POST'])
@login_required
@permission_required(Permission.WRITE)
def write_post():
    form = PostForm()
    print(form.body.data)
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        f = form.body.data.read().decode('utf-8')
        post = Post(title=form.title.data,
                    body=f,
                    author=current_user._get_current_object())
        post.category = Category.query.get(form.category.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template('posts/edit_post.html', form=form,
                           legend="Write your Post!")


@posts.route("/<int:id>", methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('posts.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('posts/post.html', title=post.title, posts=[post],
                           form=form, comments=comments, pagination=pagination)


@posts.route("/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user and \
            not current_user.can(Permission.ADMIN):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.category = Category.query.get(form.category.data)
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', id=id))
    elif request.method == 'GET':
        form.category.data = "Linux"
        form.title.data = post.title
        form.body.data = post.body
    return render_template('posts/edit_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/<int:id>/delete", methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))
