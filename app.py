from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import razorpay
import uuid
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')  # Use environment variable for secret key
db = SQLAlchemy(app)

# Replace with your Razorpay API keys
RAZORPAY_API_KEY = os.environ.get('RAZORPAY_API_KEY', 'rzp_test_UASg8QDyHDXQkz')
RAZORPAY_API_SECRET = os.environ.get('RAZORPAY_API_SECRET', 'im3zYBK6PuIoZ6dS1LhlMQDj')

class Item(db.Model):
    barcode = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'search' in request.form:
            barcode = request.form['barcode']
            item = Item.query.filter_by(barcode=barcode).first()
            if item:
                session.setdefault('items', [])
                if not any(i['barcode'] == item.barcode for i in session['items']):
                    session['items'].append({'barcode': item.barcode, 'name': item.name, 'price': item.price})
                    flash('Item added to cart!')
                else:
                    flash('Item already in cart.')
            else:
                flash('Item not found.')
        elif 'add' in request.form:
            try:
                new_item = Item(
                    barcode=request.form['new_barcode'],
                    name=request.form['new_name'],
                    price=float(request.form['new_price'])  # Ensure price is a float
                )
                db.session.add(new_item)
                db.session.commit()
                flash('Item added successfully!')
            except ValueError:
                flash('Invalid price entered. Please enter a valid number.')
            except Exception as e:
                flash(f'Error adding item: {str(e)}')

    items = session.get('items', [])
    total_price = sum(item['price'] for item in items)

    return render_template('index.html', items=items, total_price=total_price)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/payment', methods=['POST'])
def payment():
    if 'items' not in session or not session['items']:
        flash('No items in cart.')
        return redirect(url_for('index'))

    total_price = sum(item['price'] for item in session['items'])

    client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET))

    # Generate a receipt ID that is exactly 40 characters long
    receipt_id = str(uuid.uuid4()).replace('-', '')[:40]  # Remove dashes and slice to 40 characters

    order_data = {
        'amount': int(total_price * 100),  # Amount in paise
        'currency': 'INR',
        'receipt': receipt_id,  # Use the generated receipt ID
        'payment_capture': 1
    }

    try:
        response = client.order.create(order_data)
        order_id = response['id']
        order_options = {
            'key': RAZORPAY_API_KEY,
            'amount': response['amount'],
            'currency': response['currency'],
            'name': 'Your Company',
            'description': 'Order for items in your cart',
            'order_id': order_id,
            'handler': url_for('verify', _external=True),
            'theme': {
                'color': '#F37254'
            }
        }
        return render_template('payment.html', order_options=order_options)
    except Exception as e:
        flash(f'Error creating payment: {str(e)}')
        return redirect(url_for('index'))

@app.route('/verify', methods=['POST'])
def verify():
    response = request.form
    payment_id = response.get('razorpay_payment_id')
    order_id = response.get('razorpay_order_id')
    signature = response.get('razorpay_signature')

    client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET))
    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })
        flash('Payment successful! Your order will be processed shortly.')
        session.pop('items', None)  # Clear the cart after successful payment
        return redirect(url_for('index'))
    except Exception as e:
        flash('Payment verification failed. Please try again.')
        return redirect(url_for('index'))

@app.route('/print_receipt', methods=['GET'])
def print_receipt():
    if 'items' not in session or not session['items']:
        flash('No items in cart to print receipt.')
        return redirect(url_for('index'))

    items = session['items']
    total_price = sum(item['price'] for item in items)

    return render_template('receipt.html', items=items, total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)























# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from flask_sqlalchemy import SQLAlchemy
# import razorpay
# import uuid
# import os

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')  # Use environment variable for secret key
# db = SQLAlchemy(app)

# # Replace with your Razorpay API keys
# RAZORPAY_API_KEY = os.environ.get('RAZORPAY_API_KEY', 'rzp_test_UASg8QDyHDXQkz')
# RAZORPAY_API_SECRET = os.environ.get('RAZORPAY_API_SECRET', 'im3zYBK6PuIoZ6dS1LhlMQDj')

# class Item(db.Model):
#     barcode = db.Column(db.String(20), primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Float, nullable=False)

#     def __repr__(self):
#         return f'<Item {self.name}>'

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if 'search' in request.form:
#             barcode = request.form['barcode']
#             item = Item.query.filter_by(barcode=barcode).first()
#             if item:
#                 session.setdefault('items', [])
#                 if not any(i['barcode'] == item.barcode for i in session['items']):
#                     session['items'].append({'barcode': item.barcode, 'name': item.name, 'price': item.price})
#                     flash('Item added to cart!')
#                 else:
#                     flash('Item already in cart.')
#             else:
#                 flash('Item not found.')
#         elif 'add' in request.form:
#             try:
#                 new_item = Item(
#                     barcode=request.form['new_barcode'],
#                     name=request.form['new_name'],
#                     price=float(request.form['new_price'])  # Ensure price is a float
#                 )
#                 db.session.add(new_item)
#                 db.session.commit()
#                 flash('Item added successfully!')
#             except ValueError:
#                 flash('Invalid price entered. Please enter a valid number.')
#             except Exception as e:
#                 flash(f'Error adding item: {str(e)}')

#     items = session.get('items', [])
#     total_price = sum(item['price'] for item in items)

#     return render_template('index.html', items=items, total_price=total_price)

# @app.before_request
# def create_tables():
#     db.create_all()

# @app.route('/payment', methods=['POST'])
# def payment():
#     if 'items' not in session or not session['items']:
#         flash('No items in cart.')
#         return redirect(url_for('index'))

#     total_price = sum(item['price'] for item in session['items'])

#     client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET))

#     order_data = {
#         'amount': int(total_price * 100),  # Amount in paise
#         'currency': 'INR',
#         'receipt': 'receipt_id_' + str(uuid.uuid4())[:40],
#         'payment_capture': 1
#     }

#     try:
#         response = client.order.create(order_data)
#         order_id = response['id']
#         order_options = {
#             'key': RAZORPAY_API_KEY,
#             'amount': response['amount'],
#             'currency': response['currency'],
#             'name': 'Your Company',
#             'description': 'Order for items in your cart',
#             'order_id': order_id,
#             'handler': url_for('verify', _external=True),
#             'theme': {
#                 'color': '#F37254'
#             }
#         }
#         return render_template('payment.html', order_options=order_options)
#     except Exception as e:
#         flash(f'Error creating payment: {str(e)}')
#         return redirect(url_for('index'))

# @app.route('/verify', methods=['POST'])
# def verify():
#     response = request.form
#     payment_id = response.get('razorpay_payment_id')
#     order_id = response.get('razorpay_order_id')
#     signature = response.get('razorpay_signature')

#     client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET))
#     try:
#         client.utility.verify_payment_signature({
#             'razorpay_order_id': order_id,
#             'razorpay_payment_id': payment_id,
#             'razorpay_signature': signature
#         })
#         flash ('Payment successful! Your order will be processed shortly.')
#         session.pop('items', None)  # Clear the cart after successful payment
#         return redirect(url_for('index'))
#     except Exception as e:
#         flash('Payment verification failed. Please try again.')
#         return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)