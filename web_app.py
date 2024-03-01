from flask import Flask, render_template
from components.app import run_daily_job

app = Flask(__name__)

def setup_app(app):
    dataframe = run_daily_job()
    app.config['DATAFRAME'] = dataframe

@app.route("/")
def main():
    if 'DATAFRAME' not in app.config:
        setup_app(app)
    df = app.config.get('DATAFRAME')
    return render_template('display.html', dataframe=df if df is not None else "No data available.")

if __name__ == '__main__':
    app.run(debug=True)
