from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore
import requests
import re

# Create Flask app
app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("portfolio-2f0e2-firebase-adminsdk-ri2yx-1b0dd47dda.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to add contact to Firestore
def add_contact(name, phone, email, reason):
    doc_ref = db.collection(u'contacts').document()
    doc_ref.set({
        u'name': name,
        u'phone': phone,
        u'email': email,
        u'reason': reason,
        u'date': datetime.now()
    })


# def get_projects():
#     api_url = f'https://api.github.com/users/dmdhrumilmistry/repos'
#     cards_list = requests.get(api_url).json()
#     return cards_list


def get_projects():
    user = "BlueSquare4"
    api_url = f'https://api.github.com/users/{user}/repos'
    repos_list = requests.get(api_url).json()
    return repos_list




# @app.errorhandler(Exception)
# def handle_exception(message):
#     return render_template('error.html', message="Bad Request"), 400


@app.errorhandler(404)
def err_404(message):
    return render_template('error.html', message='404 Page Not Found'), 404


@app.route('/')
def main_page():
    return render_template('index.html', title='AJ here!')


@app.route('/home')
def home():
    return render_template('base.html', title='Base')

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    contact_status = None

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        reason = request.form.get('reason', '').strip()

        # Check phone number
        if 10 <= len(phone) <= 13 and re.fullmatch(r'^([+]?[\s0-9]+)?(\d{3}|[(]?[0-9]+[)])?([-]?[\s]?[0-9])+$', phone):
            add_contact(name, phone, email, reason)
            contact_status = True
        else:
            contact_status = False

    return render_template('contact.html', title='Contact Page', contact_status=contact_status)


@app.route('/projects')
def projects_page():
    return render_template('projects.html', title="Projects", cards=get_projects())
