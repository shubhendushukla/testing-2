#some changes

from flask import Flask, request, render_template_string, send_file
from PIL import Image
import io

# Initialize the Flask application
app = Flask(__name__)

# Define the HTML template for the user interface.
# It includes a form to upload a file and uses Tailwind CSS for styling.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image to B&W Converter</title>
    <!-- Include Tailwind CSS for styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Use the Inter font from Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Apply the Inter font to the body */
        body {
            font-family: 'Inter', sans-serif;
        }
    </style>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen">
    <div class="bg-white p-8 rounded-2xl shadow-lg max-w-md w-full text-center m-4">
        <h1 class="text-2xl font-bold text-gray-800 mb-2">Image to B&W Converter</h1>
        <p class="text-gray-600 mb-6">Upload your image and we'll convert it to black and white for you.</p>
        
        <!-- The form for uploading the image. It sends a POST request to the same URL. -->
        <form method="post" enctype="multipart/form-data" class="space-y-6">
            <div>
                <!-- Custom styled file input button -->
                <label for="file-upload" class="relative cursor-pointer bg-white border border-gray-300 rounded-md px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 transition duration-150 ease-in-out">
                    <span>Choose a file</span>
                    <input id="file-upload" name="file" type="file" class="sr-only" accept="image/png, image/jpeg, image/gif" required>
                </label>
                <!-- This span will display the name of the chosen file -->
                <span id="file-name" class="ml-3 text-sm text-gray-500">No file chosen</span>
            </div>
            <button type="submit" class="w-full bg-indigo-600 text-white font-semibold py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out">
                Upload & Convert
            </button>
        </form>
    </div>

    <!-- A simple script to update the file name when a user selects a file -->
    <script>
        const fileInput = document.getElementById('file-upload');
        const fileNameSpan = document.getElementById('file-name');
        
        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                // Display the name of the first selected file
                fileNameSpan.textContent = fileInput.files[0].name;
            } else {
                // Reset if no file is chosen
                fileNameSpan.textContent = 'No file chosen';
            }
        });
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def upload_and_convert():
    """
    This function handles both GET and POST requests for the root URL.
    - GET: Displays the HTML upload form.
    - POST: Processes the uploaded image and returns the B&W version.
    """
    if request.method == 'POST':
        # --- File Handling ---
        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part in the request.', 400
        
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            return 'No file selected.', 400

        if file:
            try:
                # --- Image Processing ---
                # Open the uploaded image file using Pillow
                image = Image.open(file.stream)
                
                # Convert the image to grayscale ('L' mode stands for luminance)
                bw_image = image.convert('L')
                
                # --- In-Memory File Handling ---
                # Create a byte stream in memory to save the image
                # This avoids saving the file to disk on the server
                img_io = io.BytesIO()
                
                # Save the black and white image to the byte stream in JPEG format
                bw_image.save(img_io, 'JPEG')
                
                # Move the cursor to the beginning of the byte stream
                img_io.seek(0)
                
                # --- Send Response ---
                # Send the image file back to the browser
                return send_file(
                    img_io,
                    mimetype='image/jpeg',
                    as_attachment=False, # Set to True to download the file instead of displaying it
                    download_name='bw_image.jpg'
                )
            except Exception as e:
                # Handle potential errors during file processing
                return f"An error occurred: {e}", 500

    # For a GET request, just render the HTML template.
    return render_template_string(HTML_TEMPLATE)

# This block runs the app when the script is executed directly
if __name__ == '__main__':
    # Running in debug mode provides helpful error messages
    app.run(debug=True)

