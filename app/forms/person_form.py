from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from ..models.Person import Person

class PersonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=250)])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Add Person')

    def validate_name(self, field):
        if Person.query.filter_by(name=field.data).first():
            raise ValidationError('A person with this name already exists.')
