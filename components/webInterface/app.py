import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def main():
    df = app.config.get('DATAFRAME')
    if df is not None:
        df_html = df.to_html(classes='table table-striped', index=False)  # Convert to HTML
    else:
        df_html = "<p>No data available</p>"
    return render_template('display.html', tables=[df_html])

if __name__ == '__main__':
    app.run(debug=True)
