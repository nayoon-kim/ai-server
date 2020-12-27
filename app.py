from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',title='AI-SERVER')

@app.route('/<pagename>')
def hello(pagename):
    return pagename

@app.route('/animal')
def animal():
    return render_template('animal.html')

@app.route('/dog')
def dog():
    return render_template('dog.html')
if __name__ == '__main__':
    app.run(debug=True)
