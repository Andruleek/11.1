import cmd
from flask import Flask
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

class ContactCLI(cmd.Cmd):
    prompt = 'contacts> '

    def do_hello(self, arg):
        print("How can I help you?")

    def do_add(self, arg):
        parts = arg.split()
        if len(parts) == 5:
            first_name, last_name, email, phone_number, birthday = parts
            with app.app_context():
                try:
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
                except Exception as e:
                    db.session.rollback()
                    print(f"Failed to add contact: {e}")
        else:
            print("Формат команди неправильний. Використовуйте: add [ім'я] [прізвище] [електронна пошта] [номер телефону] [дата народження]")

    def do_exit(self, arg):
        print("До побачення!")
        return True

if __name__ == '__main__':
    ContactCLI().cmdloop()
