from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class DiskLabelForm(FlaskForm):
    label = StringField('Label Text', validators=[DataRequired()])
    company_id = SelectField('Company', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Disk Label')
