from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    df = app.config.get('DATAFRAME')
    print(df)
    return render_template('display.html', dataframe=df if df is not None else "No data available.")

if __name__ == '__main__':
    app.run(debug=True)
