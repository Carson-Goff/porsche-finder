from flask import Flask, render_template
import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

from app import run_daily_job

def create_app():
    app = Flask(__name__)
    run_daily_job()

    @app.route("/")
    def main():
        df = app.config.get('DATAFRAME')
        print("DataFrame in Flask route:", df)
        return render_template('display.html', dataframe=df if df is not None else pd.DataFrame())

    return app


if __name__ == '__main__':
    create_app().run(debug=True)