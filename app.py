from flask import Flask, request, send_file, render_template, Response
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import date, datetime
import os
from werkzeug.wsgi import FileWrapper

app_name = 'Filler Image'

app = Flask(__name__)

app.config['STATIC_URL_PATH'] = '/static'

@app.route('/')
def home():
    # Retrieve the parameters from the form data
    width = request.args.get('w')
    height = request.args.get('h')
    text = request.args.get('text')
    color = "#e8e8ea"
    font_path = os.path.join(app.static_folder, "fonts", 'Arial.ttf')

    if width and height:
        try:
            width = int(width)
            height = int(height)
        except ValueError:
            return "Error: Width and height must be integers."
        # Generate the image using the provided parameters
        # You can use libraries like Pillow or OpenCV to create the image

        # Return the generated image to the user
        # You can save the image temporarily or generate it on-the-fly using BytesIO

        # Create a new image with the specified width, height, and color
        image = Image.new('RGB', (width, height), color)

        # Create a draw object
        draw = ImageDraw.Draw(image)

        # Calculate the text dimensions
        if not text:
            text = f"{width} x {height}"
        font_size = min(int(width) // len(text), int(height) // 10)  # Calculate the font size as a ratio
        font = ImageFont.truetype(font_path, size=font_size)  # Specify your desired font and size
        text_width, text_height = draw.textsize(text, font=font)

        # Calculate the position to center the text
        x = (int(width) - text_width) // 2
        y = (int(height) - text_height) // 2

        # Write the text on the image
        draw.text((x, y), text, font=font, fill=(51, 51, 51, 1))  # Specify the text color

        # Add boiler text at the bottom
        boiler_text = request.host
        boiler_font_size = font_size // 2
        boiler_font = ImageFont.truetype(font_path, size=boiler_font_size)
        boiler_text_width, boiler_text_height = draw.textsize(boiler_text, font=boiler_font)
        boiler_x = 16
        boiler_y = int(height) - boiler_text_height - boiler_font_size
        draw.text((boiler_x, boiler_y), boiler_text, font=boiler_font, fill=(51, 51, 51, 1))

        # Save the image to a BytesIO object
        image_io = BytesIO()
        image.save(image_io, 'JPEG')
        image_io.seek(0)
    
        # Create a FileWrapper around the BytesIO object
        wrapper = FileWrapper(image_io)

        return Response(wrapper, mimetype='image/jpeg')
    
    else:
        return render_template('index.html', DOMAIN=request.host, date=datetime.today().year, app_name=app_name)
