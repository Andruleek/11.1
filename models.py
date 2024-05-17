from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
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

@app.route('/')
def home():
    return 'Welcome to the Contacts App!'

@app.route('/contacts', methods=['POST'])
def create_contact():
    data = request.get_json()
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
    return jsonify({'message': 'Contact created successfully'}), 201

@app.route('/contacts/<contact_id>', methods=['GET'])
def get_contact(contact_id):
    contact = Contact.query.get(contact_id)
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404
    contact_data = {
        'id': contact.id,
        'first_name': contact.first_name,
        'last_name': contact.last_name,
        'email': contact.email,
        'phone_number': contact.phone_number,
        'birthday': contact.birthday.strftime('%Y-%m-%d'),
        'additional_data': contact.additional_data
    }
    return jsonify(contact_data), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# Command-line interface for interacting with the contacts database
while True:
    command = input("Введіть команду: ").lower()

    if command == "hello":
        print("How can I help you?")

    elif command.startswith("add"):
        parts = command.split()
        if len(parts) == 6:  # There are 6 parts because 'split()' divides by spaces, and your data has 5 fields
            first_name = parts[1]
            last_name = parts[2]
            email = parts[3]
            phone_number = parts[4]
            birthday = parts[5]
            # Save the contact to the database
            with app.app_context():
                new_contact = Contact(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    birthday=birthday
                )
                db.session.add(new_contact)
                db.session.commit()
                print(f"Контакт {first_name} з номером {phone_number} успішно додано!")
        else:
            print("Формат команди неправильний. Використовуйте: add [ім'я] [прізвище] [електронна пошта] [номер телефону] [дата народження]")

    elif command == "exit":
        print("До побачення!")
        break

    else:
        print("Невідома команда. Спробуйте ще раз.")
