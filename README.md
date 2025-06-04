# FlaskDataParser
A simple Flask-based web application for uploading and parsing `.dat` files.

# Features
- Upload `.dat` files via a web interface
- Split content into sections using the `&` separator
- Extract numeric pairs (data points) and metadata
- Display 10 equally spaced data points from each section
- Simple HTML interface

# Installation and Launch
1. Clone the repository:
   ```bash
   git clone https://github.com/Nick8755/FlaskDataParser.git
   cd FlaskDatParser
   
2. Create and activate a virtual environment:
    ```bash
    python3 -m venv .venv # for macOS/Linux
    source .venv/bin/activate # for macOS/Linux
    
    python -m venv .venv # for Windows
    .venv\Scripts\activate   # for Windows
    
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
   
4. Run the Flask application:
    ```bash
    python app.py
    
5. Open your web browser and go to http://127.0.0.1:5000

Project Structure:

FlaskDatParser/
├── app.py                # main application code
├── requirements.txt      # dependency list
├── .gitignore            # ignored files and folders
├── static/               # CSS styles
│   └── styles.css
├── templates/            # HTML templates
│   ├── index.html
│   └── result.html
├── uploads/              # folder for uploaded .dat files
└── .venv/                # virtual environment (ignored by Git)

Notes:
All .dat files are saved to the uploads/ folder
.gitignore is configured to exclude unnecessary system and build files
Recommended Python version: 3.10+