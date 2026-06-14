from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from . import DISK_SIZE_CHOICES
from ..models.Disk import Disk


class DiskForm(FlaskForm):
    name = StringField('Disk Name', validators=[DataRequired(), Length(max=250)])
    company_id = SelectField('Company', coerce=int, validators=[DataRequired()])
    labels_size = SelectField('Labels Size', choices=DISK_SIZE_CHOICES, coerce=int, default=45, validators=[Optional()])
    sakisid = StringField('ID Code', validators=[Optional(), Length(max=250)])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Add Disk')

    def validate_name(self, field):
        existing = Disk.query.filter_by(name=field.data).first()
        if existing and existing.disk_id != getattr(self, 'editing_id', None):
            raise ValidationError('Disk with this name already exists.')