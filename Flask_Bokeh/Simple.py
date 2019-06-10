from flask import Flask, render_template
app = Flask(__name__)

test = "Hello, test"

# Create the main plot
def create_figure(test):
    var1 = "This is var1: " + test
    return var1

# Index page
@app.route('/')
def index():
    var2 = create_figure(test)
    var3 = "This is var3"
    return render_template("simple.html", var2=var2, var3=var3)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)