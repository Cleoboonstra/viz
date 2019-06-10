from flask import Flask, render_template, request
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)

df = pd.read_csv("data/cars.csv")

# Create the main plot
def create_figure(df):
    myData = df.head()
    return myData

# Index page
@app.route('/')
def index():
    var2 = create_figure(df)
    var3 = var2.info()
    return render_template("embed.html", var2=var2, var3=var3)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)