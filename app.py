from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def expand_url(url):
    session = requests.Session()  # so connections are recycled
    resp = session.head(url, allow_redirects=True)
    return resp.url

@app.route('/', methods=['GET', 'POST'])
def index():
    long_url = ''
    if request.method == 'POST':
        short_url = request.form.get('url')
        long_url = expand_url(short_url)
    return render_template('index.html', long_url=long_url)

if __name__ == '__main__':
    app.run()