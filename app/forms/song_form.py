from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, FieldList, FormField, BooleanField
from wtforms.validators import DataRequired, Length, Optional

AUDIO_EXTENSIONS = ['mp3']
IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp']

class PersonSongForm(FlaskForm):
    person_name = StringField('Καλλιτέχνης', validators=[Optional()])
    isSinger = BooleanField('Ερμηνεία', default=False)
    isComposer = BooleanField('Σύνθεση', default=False)
    isSongwriter = BooleanField('Στίχοι', default=False)
    isMusician = BooleanField('Μουσική', default=False)

class SongForm(FlaskForm):
    title = StringField('Τίτλος', validators=[DataRequired(), Length(max=250)])
    audio_file = FileField('Αρχείο ήχου (mp3)', validators=[
        Optional(), FileAllowed(AUDIO_EXTENSIONS, 'Επιτρέπονται μόνο αρχεία mp3.')])
    image_file = FileField('Εικόνα', validators=[
        Optional(), FileAllowed(IMAGE_EXTENSIONS, 'Επιτρέπονται μόνο αρχεία εικόνας.')])
    lyrics = TextAreaField('Στίχοι', validators=[Optional()])
    notes = TextAreaField('Σημειώσεις', validators=[Optional()])
    disk_name = StringField('Δίσκος', validators=[Optional(), Length(max=250)])
    persons = FieldList(FormField(PersonSongForm), min_entries=1)
    submit = SubmitField('Αποθήκευση')
