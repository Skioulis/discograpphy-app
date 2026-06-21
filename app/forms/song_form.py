from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FieldList, FormField, BooleanField
from wtforms.validators import DataRequired, Length, Optional

class PersonSongForm(FlaskForm):
    person_name = StringField('Πρόσωπο', validators=[Optional()])
    isSinger = BooleanField('Ερμηνεία', default=False)
    isComposer = BooleanField('Σύνθεση', default=False)
    isSongwriter = BooleanField('Στίχοι', default=False)
    isMusician = BooleanField('Μουσική', default=False)

class SongForm(FlaskForm):
    title = StringField('Τίτλος', validators=[DataRequired(), Length(max=250)])
    lyrics = TextAreaField('Στίχοι', validators=[Optional()])
    notes = TextAreaField('Σημειώσεις', validators=[Optional()])
    disk_name = StringField('Δίσκος', validators=[Optional(), Length(max=250)])
    persons = FieldList(FormField(PersonSongForm), min_entries=1)
    submit = SubmitField('Αποθήκευση')
