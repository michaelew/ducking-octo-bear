#!/usr/bin/env python
from flask import Flask, render_template, request, flash
from forms import ContactForm, Unsubscribe, Home
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap
import dataset

mail = Mail()

app = Flask(__name__)
Bootstrap(app)

app.secret_key = '9sef7s98fe79se8f7s9e8f98fh7fgj98f'

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'your@gmail.com'
app.config["MAIL_PASSWORD"] = 'yourpassword'

mail.init_app(app)

db = dataset.connect('sqlite:///site.db')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = Home()
    
    if request.method == 'GET':
        return render_template('home.html', form=form)
    
    if not form.validate():
        flash('Form is not correctly filled out. ')
        return render_template('home.html', form=form)

    table = db['subscriber']

    if table.find_one(invite=form.invite.data):
        table.insert(dict(subscriber=form.email.data))
        return 'Your email has been submitted for approval. Make sure you look out for an interview email from our staff.'

    return 'Your invite code cannot be found. Please contact the person who provided it to you.'

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required. ')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender='yoursending_email@gmail.com', recipients=['email@sentto.com'])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)

            return render_template('contact.html', success=True)

    elif request.method == 'GET':
        return render_template('contact.html', form=form)

@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
    form = Unsubscribe()

    if request.method == 'POST':
        if form.validate() == False:
            flash('Form must be filled out correctly. ')
            return render_template('unsubscribe.html', form=form)
        else:
            table = db['unsub']
            table.insert(dict(unsubscribed=form.email.data))
            return 'You have been unsubscribed.'

    elif request.method == 'GET':
        return render_template('unsubscribe.html', form=form)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

if __name__ == '__main__':
    app.run(debug=True)

