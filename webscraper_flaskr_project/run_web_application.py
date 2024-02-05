from news_scraper.main import create_app
import webbrowser
from threading import Timer
import nltk

# Download NLTK resources
nltk.download('stopwords')
nltk.download('punkt')

def open_browser():
    """
    Opens the default web browser with the specified URL.

    This function is called by the Timer to open the browser window.

    Args:
        None

    Returns:
        None
    """
    webbrowser.open_new("http://127.0.0.1:5000")

# Create the Flask app
app = create_app()
app.debug = False

# Start a Timer to open the browser after a delay
Timer(0.5, open_browser).start()

# Run the Flask app
app.run(host='0.0.0.0', port=5000)
