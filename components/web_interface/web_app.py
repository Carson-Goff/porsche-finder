from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def main():
    df = app.config.get('DATAFRAME')
    return render_template('display.html', dataframe=df)