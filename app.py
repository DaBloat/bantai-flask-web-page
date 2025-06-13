from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def homepage():
    greet = {'AM':'Good Morning', 'PM':'Good Afternoon'}
    stats = {
        'greet': greet[datetime.now().strftime("%p")],
        'user': 'Admin'
    }
    return render_template('index.html', stat=stats)

if __name__ == '__main__':
    app.run(debug=True)
