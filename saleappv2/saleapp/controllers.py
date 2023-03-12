from flask import render_template, request, redirect, session, jsonify
from flask_wtf.recaptcha import validators

from saleapp import app, dao, admin, login, utils
from flask_login import login_user, logout_user, login_required
from saleapp.decorators import annonymous_user
import cloudinary.uploader
from flask_wtf import FlaskForm, RecaptchaField
from twilio.rest import Client
import random
from wtforms.validators import DataRequired, Email
from wtforms import StringField, TextAreaField, SubmitField
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials



def index():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    products = dao.load_products(cate_id, kw)

    return render_template('index.html', products=products)


def details(product_id):
    p = dao.get_product_by_id(product_id)
    return render_template('details.html', product=p)


def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


class ContactForm1(FlaskForm):
    recaptcha = RecaptchaField()


class ContactForm(FlaskForm):
    recaptcha = RecaptchaField(validators=[validators.Recaptcha(message='Invalid reCAPTCHA.')])


def register():
    err_msg = ''
    form = ContactForm()
    if request.method.__eq__('POST') and request.form.get('g-recaptcha-response'):
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=password,
                             phonenumber = request.form['numPhone'],
                             avatar=avatar)

                return redirect('/login')
            except:
                err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg, form=form)



@annonymous_user
def login_my_user():
    form = ContactForm()
    if request.method.__eq__('POST') and request.form.get('g-recaptcha-response'):
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            n = request.args.get("next")
            return redirect(n if n else '/')

    return render_template('login.html', form=form)


def logout_my_user():
    logout_user()
    return redirect('/login')



def cart():
    # session['cart'] = {
    #     "1": {
    #         "id": "1",
    #         "name": "iPhone 13",
    #         "price": 13000,
    #         "quantity": 2
    #     },
    #     "2": {
    #         "id": "2",
    #         "name": "iPhone 14",
    #         "price": 13000,
    #         "quantity": 2
    #     }
    # }

    return render_template('cart.html')


def add_to_cart():
    key = app.config['CART_KEY']
    cart = session[key] if key in session else {}

    data = request.json
    id = str(data['id'])

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        name = data['name']
        price = data['price']

        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


def update_cart(product_id):
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart and product_id in cart:
        cart[product_id]['quantity'] = int(request.json['quantity'])

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


def delete_cart(product_id):
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart and product_id in cart:
        del cart[product_id]

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


@login_required
def pay():
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart:
        try:
            dao.save_receipt(cart=cart)
        except Exception as ex:
            print(str(ex))
            return jsonify({"status": 500})
        else:
            del session[key]

    return jsonify({"status": 200})


def comments(product_id):
    data = []
    for c in dao.load_comments(product_id=product_id):
        data.append({
            'id': c.id,
            'content': c.content,
            'created_date': str(c.created_date),
            'user': {
                'name': c.user.name,
                'avatar': c.user.image
            }
        })

    return jsonify(data)


def add_comment(product_id):
    try:
        c = dao.save_comment(product_id=product_id, content=request.json['content'])
    except:
        return jsonify({'status': 500})

    return jsonify({
        'status': 204,
        'comment': {
            'id': c.id,
            'content': c.content,
            'created_date': str(c.created_date),
            'user': {
                'name': c.user.name,
                'avatar': c.user.image
            }
        }
    })


# Thông tin tài khoản Twilio

def send_otp():
    account_sid = 'AC99204c3540a27bd83aede03e43b83312'
    auth_token = '6660059774e9c35882ef7e4fa354ec56'
    client = Client(account_sid, auth_token)
    otp = random.randint(100000, 999999)
    message = client.messages.create(
        messaging_service_sid='MG32639fd52b8605ff78a55e2f7d7f3651',
        body=f'Hiếu test otp {otp}',
        to='+84359505026'
    )

    print(message.sid)
    print(otp)
