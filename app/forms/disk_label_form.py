from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class DiskLabelForm(FlaskForm):
    label = StringField('Κείμενο ετικέτας', validators=[DataRequired()])
    company_id = SelectField('Εταιρεία', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Αποθήκευση')
