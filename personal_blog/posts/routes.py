from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from ..decorators import permission_required
from . import posts
from .forms import PostForm
from ..models import Permission, Post
from .. import db


@posts.route("/new", methods=['GET', 'POST'])
@login_required
@permission_required(Permission.WRITE)
def write_post():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template('posts/create_post.html', form=form)


@posts.route("/<int:id>")
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('posts/_post.html', title=post.title, post=post)


@posts.route("/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', id=id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
    return render_template('posts/create_post.html', title='Update Post',
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
