from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from ..models.Company import Company

class CompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired(), Length(max=250)])
    labels_size = SelectField('Labels Size', choices=[(33, '33'), (45, '45'), (78, '78')], coerce=int, default=45, validators=[Optional()])
    info = TextAreaField('Information', validators=[Optional()])
    submit = SubmitField('Add Company')

    def validate_name(self, field):
        if Company.query.filter_by(name=field.data).first():
            raise ValidationError('Company with this name already exists.')
