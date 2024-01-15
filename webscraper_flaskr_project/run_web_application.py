from news_scraper.main import create_app
import webbrowser
from threading import Timer

#Opens the localhost in a webbrowser
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

#Create the application from main, turn off debugging
app = create_app()
app.debug = False

#Start the localhost browser in 0.5 seconds and run the app to be hosted
Timer(0.5, open_browser).start()
app.run(host='0.0.0.0', port=5000)
