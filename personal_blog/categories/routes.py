from flask import render_template, current_app, request
from personal_blog.models import Category
from . import categories


@categories.route('/<category>')
def filter_on_category(category):
    page = request.args.get('page', type=int)
    category = Category.query.filter_by(name=category).first_or_404()
    pagination = category.posts.paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'])
    posts = pagination.items
    return render_template('index.html', pagination=pagination, posts=posts)
