from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from ..models.Company import Company
from . import DISK_SIZE_CHOICES


class CompanyForm(FlaskForm):
    name = StringField('Όνομα', validators=[DataRequired(), Length(max=250)])
    labels_size = SelectField('Μέγεθος ετικέτας', choices=DISK_SIZE_CHOICES, coerce=int, default=45, validators=[Optional()])
    info = TextAreaField('Πληροφορίες', validators=[Optional()])
    submit = SubmitField('Αποθήκευση')

    def validate_name(self, field):
        existing = Company.query.filter_by(name=field.data, labels_size=self.labels_size.data).first()
        if existing and existing.company_id != getattr(self, 'editing_id', None):
            raise ValidationError('Υπάρχει ήδη εταιρεία με αυτό το όνομα και μέγεθος ετικέτας.')
