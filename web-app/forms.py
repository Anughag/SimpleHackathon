from flask_wtf import FlaskForm
from flask_wtf import Form
from wtforms import StringField, TextField, SubmitField, IntegerField,TextAreaField,RadioField,SelectField, DecimalField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import ValidationError
import pandas as pd 



class PredictForm(FlaskForm):
   num1=TextAreaField('Defect Description')
   choices=SelectField(u'Type of Defect', choices=[('Business Logic', 'Business Logic'), ('UI', 'UI')])
   submit = SubmitField('Find the Similarities')
   pd = "" # this variable is used to send information back to the front page



class DefectPrediction(FlaskForm):
   efforts=DecimalField('Efforts')
   plannedCP=DecimalField('Planned CP')
   teamExpertise=SelectField(u'Team Expertise',choices=[('1','Expert'),('2','Skillfull'),('3','Intermediate'),('4','Average'),('5','Below Average')])
   complexityFactor=DecimalField('Complexity Factor')
   submit=SubmitField('Defect Prediction')
   result=""