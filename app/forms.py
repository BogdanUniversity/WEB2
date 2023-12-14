from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField , PasswordField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms import ValidationError
from app import models

# In this document we define forms for data to be added to databases

"""
def name_check_goal(form, field):
    name = field.data
    record = models.Goals.query.filter_by(goal_name=name).first()
    if record:
        raise ValidationError("This Goal Name is in Use")


def name_check_income(form, field):
    name = field.data
    record = models.Incomes.query.filter_by(income_name=name).first()
    if record:
        raise ValidationError("This Income Name is in Use")


def name_check_expences(form, field):
    name = field.data
    record = models.Expences.query.filter_by(expence_name=name).first()
    if record:
        raise ValidationError("This Expence Name is in Use")
"""
class PostForm(FlaskForm):
    content = StringField('content')

class LoginUserForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

class SignUpForm(FlaskForm):
    username = StringField('username')
    password = StringField('password')
    
     
""""
class IncomeForm(FlaskForm):
    income_name = StringField('income_name', validators=[DataRequired(),
                                                         name_check_income])
    income_type = SelectField('income_type', choices=[('salary', 'Salary'),
                                                      ('gift', 'Gift')],
                              validators=[DataRequired()])

    income_amount = FloatField('integer_amount',
                               validators=[DataRequired(),
                                           NumberRange(
                                               min=0.01,
                                               max=1000000000,
                                               message="The Amount is Invalid"
                                               )])


class ExpenceForm(FlaskForm):
    expence_name = StringField('expence_name',
                               validators=[DataRequired(),
                                           name_check_expences])
    expence_type = SelectField('expence_type',
                               choices=[('food', 'Food'),
                                        ('entertainment', 'Entertainment'),
                                        ('bills', 'Bills'),
                                        ('other', 'Other')],
                               validators=[DataRequired()])
    expence_amount = FloatField('expence_amount',
                                validators=[DataRequired(),
                                            NumberRange(
                                                min=0.01,
                                                max=1000000000,
                                                message="The Amount is Invalid"
                                                )])


class GoalForm(FlaskForm):
    goal_name = StringField('goal_name',
                            validators=[name_check_goal,
                                        Optional(strip_whitespace=True)])
    goal_amount = FloatField('goal_amounmt',
                             validators=[DataRequired(),
                                         NumberRange(
                                             min=0.01,
                                             max=1000000000,
                                             message="The Amount is Invalid"
                                             )])
"""