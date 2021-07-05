from flask_wtf import FlaskForm
from wtforms import SelectField, HiddenField, FloatField, validators, SubmitField
from wtforms.validators import DataRequired


class MovimientosForm(FlaskForm):
    desde_moneda = SelectField('From', choices=['EUR'], validators = [DataRequired()])
    c1 = FloatField('Cantidad', validators=[DataRequired()])
    para_moneda = SelectField('To', [validators.Required()], choices=[])
    c2 = FloatField('Cantidad a adquirir', validators=None)
    preciounitario = FloatField('Cantidad comprada', validators=None)
    submit1 = SubmitField('Comprar')
    submit2 = SubmitField('Calcular')
