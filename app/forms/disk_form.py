from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from ..models.Disk import Disk


class DiskForm(FlaskForm):
    name = StringField('Disk Name', validators=[DataRequired(), Length(max=250)])
    company_id = StringField('Company', validators=[Optional(), Length(max=250)])
    size = StringField('Size/Type', validators=[Optional(), Length(max=250)])
    sakisid = StringField('ID Code', validators=[Optional(), Length(max=250)])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Add Disk')

    def validate_name(self, field):
        if Disk.query.filter_by(name=field.data).first():
            raise ValidationError('Disk with this name already exists.')