from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional

class SongForm(FlaskForm):
    title = StringField('Song Title', validators=[DataRequired(), Length(max=250)])
    notes = TextAreaField('Notes', validators=[Optional()])
    disk_id = SelectField('Add to Disk', coerce=int, validators=[Optional()])
    submit = SubmitField('Add Song')
