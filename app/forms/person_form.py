from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from ..models.Person import Person

class PersonForm(FlaskForm):
    name = StringField('Όνομα', validators=[DataRequired(), Length(max=250)])
    notes = TextAreaField('Σημειώσεις', validators=[Optional()])
    submit = SubmitField('Αποθήκευση')

    def validate_name(self, field):
        existing = Person.query.filter_by(name=field.data).first()
        if existing and existing.person_id != getattr(self, 'editing_id', None):
            raise ValidationError('Υπάρχει ήδη καλλιτέχνης με αυτό το όνομα.')
