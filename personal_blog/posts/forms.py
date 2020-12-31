from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = TextAreaField("Title", validators=[DataRequired()])
    body = PageDownField("Content", validators=[DataRequired()])
    submit = SubmitField("submit")


class CommentForm(FlaskForm):
    body = StringField("", validators=[DataRequired()])
    submit = SubmitField('Submit')
