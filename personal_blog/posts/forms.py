from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = TextAreaField("Title", validators=[DataRequired()])
    body = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("submit")
