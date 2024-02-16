from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

@app.route('/get_age', methods=['GET'])
def get_age():
    # Extract the "birthyear" parameter from the URL query string
    birthyear_str = request.args.get('birthyear', '')
    if not birthyear_str:
        return jsonify({'error': 'Please provide a birthyear parameter as a four-digit number'}), 400

    try:
        birthyear = int(birthyear_str)
    except ValueError:
        return jsonify({'error': 'Invalid year format. Please provide a four-digit number.'}), 400

    current_year = datetime.now().year
    age = current_year - birthyear
    
    return jsonify({'age': age})

if __name__ == '__main__':
    app.run(debug=True)
