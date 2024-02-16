from flask import Flask, send_file, request
from PIL import Image, ImageDraw

from datetime import datetime
import io

app = Flask(__name__)

@app.route('/year', methods=['GET'])
def age_image():
    year = request.args.get('year', type=int)
    if year is None:
        return 'Please provide an year parameter in the URL', 400
    age=get_age(year)

    # Create a blank image with white background
    width, height = 21, 21
    img = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Define font and text color
   
    text_color = (0, 0, 0,255)

    # Calculate text position
    text = f"{age}"
    text_bbox = draw.textbbox((0, 0), text)
    position = ((width - (text_bbox[2] - text_bbox[0])) / 2, (height - (text_bbox[3] - text_bbox[1])) / 2)

    # Draw text on image
    draw.text(position, text, fill=text_color, )

    # Save image to a temporary file
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    # Return the image file as a response
    return send_file(img_buffer, mimetype='image/png')

def get_age(year):
    # Extract the "birthyear" parameter from the URL query string
    birthyear_str=year
    if not birthyear_str:
        return """'error': 'Please provide a birthyear parameter as a four-digit number'"""

    try:
        birthyear = int(birthyear_str)
    except ValueError:
        return """'error': 'Invalid year format. Please provide a four-digit number.'"""

    current_year = datetime.now().year
    age = current_year - birthyear
    
    return  age

if __name__ == '__main__':
    app.run(debug=True)
