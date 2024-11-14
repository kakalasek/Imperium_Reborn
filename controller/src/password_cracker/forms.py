from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, FileField
from wtforms.validators import DataRequired

class JohnForm(FlaskForm):
    file = FileField('File with Hashes', validators=[DataRequired()])
    format = SelectField('Hash Format', choices=[('descrypt', 'Descrypt'), 
                                                 ('bsdicrypt', 'Bsdicrypt'),
                                                 ('md5crypt', 'MD5crypt'),
                                                 ('bcrypt', 'BCrypt'),
                                                 ('lm', 'LM'),
                                                 ('afs', 'AFS'),
                                                 ('tripcode', 'Tripcode')])
    attack_type = SelectField('Attack Type', choices=[('dictionary', 'Dictionary'), 
                                                      ('bruteforce', 'Bruteforce')])
    dictionary = FileField('Dictionary File')
    submit = SubmitField('Crack')