from random import randrange
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from SashiDo WebHook handler"

@app.route("/webhook", methods=['POST'])
def webhook():
    result = {}
    request_content = request.get_json(force=True)
    current_user = request_content['object']

    make_a_payment = current_user.get('payment', False)

    if make_a_payment == 'try':
        user_id = current_user['objectId']
        is_payment_success = make_payment(user_id)

        if is_payment_success:
            current_user['payment'] = 'success'
            current_user['plan'] = 'paid'
        else:
            current_user['payment'] = 'fail'
            current_user['plan'] = 'cancelled'

    result = {"success": current_user}

    return jsonify(result)

def make_payment(user_id):
    # Here we'll implement payment logic
    # for now we'll just fake it :)
    rand = randrange(1,20)
    is_success = randrange(1,20) % 2 == 0

    if is_success:
        return True
    else:
        return False


if __name__ == "__main__":
    app.run(host="localhost", port=4040)
