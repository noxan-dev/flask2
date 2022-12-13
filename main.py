import os
import smtplib
from flask import Flask, render_template, flash, redirect, url_for, request
from forms import ContactForm
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
from datetime import datetime


cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
cache.init_app(app)
csrf = CSRFProtect(app)

# app.config['TESTING'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ['RECAPTCHA_PUBLIC_KEY']
app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ['RECAPTCHA_PRIVATE_KEY']

MAIL_USERNAME = 'chaimmalek@gmail.com'
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']


@app.template_filter('remove_dashes')
def remove_dashes(string):
    return string.replace('-', ' ')


@app.template_filter('upper')
def upper(string):
    return string.title()


@app.route('/', methods=['GET', 'POST'])
# @cache.cached(timeout=60)
def redesign():
    year = datetime.now().year
    form = ContactForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            message = form.message.data
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
                smtp.sendmail(from_addr=email,
                              to_addrs=MAIL_USERNAME,
                              msg='Subject: New Message from {}\n\n{}\nFrom: {}'.format(name, message, email)
                              )
            flash('Message sent!')
            return redirect(url_for('redesign'))
    return render_template('indexV2.html', year=year, form=form)


@app.route('/about')
@cache.cached(timeout=60)
def about():
    return render_template('about.html')


@app.route('/gallery')
@cache.cached(timeout=60)
def gallery():
    images_file = os.listdir('./static/images/gallery')
    return render_template('gallery.html', images=images_file)



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
