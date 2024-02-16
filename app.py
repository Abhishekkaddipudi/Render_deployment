from flask import Flask, send_file, request
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

@app.route('/age_image', methods=['GET'])
def age_image():
    age = request.args.get('age', type=int)
    if age is None:
        return 'Please provide an age parameter in the URL', 400

    # Create a blank image with white background
    width, height = 200, 100
    background_color = (255, 255, 255)
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)

    # Define font and text color
    font = ImageFont.truetype(os.path.join("fonts", "arial.ttf"), 36)
    text_color = (0, 0, 0)

    # Calculate text position
    text = f"Age: {age}"
    text_width, text_height = draw.textsize(text, font=font)
    position = ((width - text_width) / 2, (height - text_height) / 2)

    # Draw text on image
    draw.text(position, text, fill=text_color, font=font)

    # Save image to a temporary file
    img_path = 'temp_age_image.png'
    img.save(img_path)

    # Return the image file as a response
    return send_file(img_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
