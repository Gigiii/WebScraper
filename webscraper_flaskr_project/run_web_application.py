from news_scraper.main import create_app
from database.queries import purgeKeywords, init_db
import webbrowser

init_db()
purgeKeywords()
app = create_app()
app.debug = False
webbrowser.open_new("http://127.0.0.1:5000/")
app.run(host='0.0.0.0', port=5000)
