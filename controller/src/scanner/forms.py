from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField 
from wtforms.validators import DataRequired


class ScanForm(FlaskForm): 
    ip = StringField('IP Adress or Range',
                       validators=[DataRequired()])
    scan_type = SelectField("Scan Type", choices=[('-sS', 'Syn Scan'), 
                                                  ('-sV', 'Version Scan'), 
                                                  ('-O', 'System Scan'), 
                                                  ('-sF', 'Fin Scan'), 
                                                  ('-sU', 'UDP Scan'), 
                                                  ('-sT', 'Connect Scan')])
    no_ping = BooleanField("No Ping")
    randomize_hosts = BooleanField("Randomize Hosts")
    fragment_packets = BooleanField("Fragment Packets")
    submit = SubmitField('Scan')