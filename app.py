from flask import Flask, send_file, request, render_template,jsonify
from PIL import Image, ImageDraw
from datetime import datetime
import io
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
messages = []
@app.route('/')
def home():
    # This route serves the form to the user.
    return render_template('index.html')

@app.route('/chat')
def index():
    return render_template('chat.html', messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    username = request.form['username']
    message = request.form['message']
    if username and message:
        messages.append({'username': username, 'message': message})
        socketio.emit('new_message', {'username': username, 'message': message})
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Username and message are required'})

@app.route('/year', methods=['GET'])
def age_image():
    # Extracts the year from the query parameter.
    year = request.args.get('year', type=int)
    if year is None:
        # If year is not provided or not convertible to int, return an error message.
        return 'Please provide a year parameter in the URL', 400
    
    # Calculate age based on the provided year.
    age = get_age(year)

    # Create an image with the calculated age.
    img = create_age_image(age)
    
    # Return the image file as a response.
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return send_file(img_buffer, mimetype='image/png')

def get_age(year):
    try:
        
        birthyear = int(year)
    except ValueError:
        # This part of the code might not be reached due to the type=int in request.args.get,
        # but it's here as a safeguard.
        return 'Invalid year format. Please provide a four-digit number.'


    current_year = datetime.now().year

    return current_year - birthyear

def create_age_image(age):
    # Create a blank image with white background.
    width, height = 21, 21  # Adjusted for better visibility.
    img = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    text_color = (0, 0, 0, 255)
    if age < 1 and age > datetime.now().year:
        return "Invalid year"
    text = f"{age}"
    # Use a simpler approach for text position since dynamic calculation might not be necessary for simple use cases.
    position = (width // 4, height // 4)  # Adjust as needed for text alignment.
    draw.text(position, text, fill=text_color)
    return img

if __name__ == '__main__':
    socketio.run(app, debug=True,host='0.0.0.0')
