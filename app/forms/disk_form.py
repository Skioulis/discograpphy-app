from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from . import DISK_SIZE_CHOICES
from ..models.Disk import Disk


class DiskForm(FlaskForm):
    name = StringField('Όνομα', validators=[DataRequired(), Length(max=250)])
    company_id = SelectField('Εταιρεία', coerce=int, validators=[DataRequired()])
    labels_size = SelectField('Μέγεθος ετικέτας', choices=DISK_SIZE_CHOICES, coerce=int, default=45, validators=[Optional()])
    sakisid = StringField('Κωδικός', validators=[Optional(), Length(max=250)])
    notes = TextAreaField('Σημειώσεις', validators=[Optional()])
    submit = SubmitField('Αποθήκευση')

    def validate_name(self, field):
        existing = Disk.query.filter_by(name=field.data).first()
        if existing and existing.disk_id != getattr(self, 'editing_id', None):
            raise ValidationError('Υπάρχει ήδη δίσκος με αυτό το όνομα.')