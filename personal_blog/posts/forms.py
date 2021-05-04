from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TextAreaField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from personal_blog.models import Category


class PostForm(FlaskForm):
    category = SelectField("Category", coerce=str)
    title = TextAreaField("Title", validators=[DataRequired()])
    body = FileField("Content",
                     validators=[FileRequired(),
                                 FileAllowed(["md"], "Only MarkDown Files")])
    submit = SubmitField("submit")

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(
                                     Category.name).all()]


class CommentForm(FlaskForm):
    body = StringField("", validators=[DataRequired()])
    submit = SubmitField('Submit')
