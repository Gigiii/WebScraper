from news_scraper.main import create_app
import webbrowser
from threading import Timer


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

app = create_app()
app.debug = False
Timer(0.5, open_browser).start()
app.run(host='0.0.0.0', port=5000)
