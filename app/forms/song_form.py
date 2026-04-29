from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FieldList, FormField, BooleanField
from wtforms.validators import DataRequired, Length, Optional

class PersonSongForm(FlaskForm):
    person_name = StringField('Person', validators=[Optional()])
    isSinger = BooleanField('Singer', default=False)
    isComposer = BooleanField('Composer', default=False)
    isSongwriter = BooleanField('Songwriter', default=False)
    isMusician = BooleanField('Musician', default=False)

class SongForm(FlaskForm):
    title = StringField('Song Title', validators=[DataRequired(), Length(max=250)])
    lyrics = TextAreaField('Lyrics', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])
    disk_name = StringField('Disk', validators=[Optional(), Length(max=250)])
    persons = FieldList(FormField(PersonSongForm), min_entries=1)
    submit = SubmitField('Add Song')
