from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    additional_data = db.Column(db.String(200))

    def __init__(self, first_name, last_name, email, phone_number, birthday, additional_data=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.birthday = datetime.strptime(birthday, '%Y-%m-%d')
        self.additional_data = additional_data

class ContactForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[DataRequired()])
    additional_data = StringField('Additional Data', validators=[Length(max=200)])

@app.route('/')
def home():
    return 'Ласкаво просимо до програми Контакти!'

@app.route('/contacts', methods=['POST'])
def create_contact_api():
    data = request.get_json()
    try:
        new_contact = Contact(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone_number=data['phone_number'],
            birthday=data['birthday'],
            additional_data=data.get('additional_data')
        )
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({'message': 'Контакт успішно створено'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/contacts/form', methods=['GET', 'POST'])
def create_contact_form():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            new_contact = Contact(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                birthday=form.birthday.data.strftime('%Y-%m-%d'),
                additional_data=form.additional_data.data
            )
            db.session.add(new_contact)
            db.session.commit()
            flash('Contact created successfully!', 'success')
            return redirect(url_for('create_contact_form'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to create contact: {e}', 'danger')
    return render_template('create_contact.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

