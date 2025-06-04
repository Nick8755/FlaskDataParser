from flask import Flask, render_template, redirect, url_for, request
import os

'''
Flask - main framework)
render_template - to load and render HTML templates
redirect, url_for - to handle redirects and URL generation
request - handles incoming form data, including uploaded files
os - to handle file system operations
'''

app = Flask(__name__) # Create a Flask application instance

UPLOAD_FOLDER = 'uploads' # Folder to save uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # We tell Flask to use this folder for uploads
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Create the upload folder if it doesn't already exist

# Function to check if the uploaded file has a .dat extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == "dat"
    # Check if the file has a .dat extension
    # "example.dat".rsplit('.',1) -> ['example', 'dat']
    # lower() - to lowercase the file extension for case-insensitive


# Create function for 10 equaly spaced data points from each section
def select_10_data_points(data_points):
    n = len(data_points)
    if n <= 10:
        return data_points  # No need to sample if list is already short

    step = n/9 # 9 intervals give 10 points
    indices = [round(i * step) for i in range(10)]  # Get 10 target indices
    indices = [min(i, n-1) for i in indices] # Make sure we don’t go out of bounds

    return [data_points[i] for i in indices] # Return selected data_points


# Create the main route for Uploading the file
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST': # Handle file upload (upload button clicked)
        if 'file' not in request.files: # Check if 'file' part is in the request
            return "No file part in the request", 400 # error if no file missing

        file = request.files['file'] # obtain the file from the request

        if file.filename == '': # Check if the file has empty name
            return "No selected file", 400 # error if file name is empty

        if file and allowed_file(file.filename): # existing file and allowed extension
            filename = file.filename # Get the filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # Create the full path to save the file
            file.save(file_path) # Save the file to the upload folder
            return redirect(url_for('parse_file', filename=filename)) # # Redirect to results page
        else: # If the file is not allowed
            return "Invalid file type. Only .dat files are allowed.", 400 # error for invalid file type

    return render_template('index.html') # Render the index.html template for GET request


# Route for parsing and displaying results
@app.route('/parse/<filename>')
def parse_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # Full path to the uploaded file

    if not os.path.exists(file_path):
        return f"File doesn't exist", 404 #
    try:
        with open(file_path, 'rb') as f:
            parsed_sections = parse_dat_file(f) # Parse file contents
    except Exception as e:
        return f"Error when reading a file: {str(e)}", 500 # Error while reading/parsing file

    return render_template('result.html', sections=parsed_sections, filename=filename) # Show parsed data

# Function to parse the .dat file into sections, metadata, and data points
def parse_dat_file(file_stream):
    content = file_stream.read().decode('utf-8') # Read file contents as text
    sections = [] # List to hold parsed sections
    raw_sections = content.split('&') # Split file into sections using '&' as separator

    for raw_section in raw_sections:
        data_points = [] # numeric data_points
        metadata = [] # metadata

        lines = raw_section.strip().split('\n') # Split section into lines
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 2:
                try:
                    x = float(parts[0]) # Convert first part to float
                    y = float(parts[1]) # Convert second part to float
                    data_points.append((x,y)) # If succesfull, append as a tuple (x, y) to data_points
                except ValueError:
                    metadata.append(line.strip()) # If not, save as metadata
            else:
                metadata.append(line.strip()) # Any line not containing two values is metadata

        sampled = select_10_data_points(data_points) # Select 10 equidistant data points

        # Create a section dictionary with data points and metadata
        sections.append({
            'data_points': sampled,
            'metadata': metadata
        })
    return sections # Return all parsed sections

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)