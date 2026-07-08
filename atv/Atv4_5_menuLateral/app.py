from flask import Flask, render_template

app = Flask(__name__)

#renderizando o layout.html
@app.route("/")
def homeP():
    return render_template("layout.html")

if __name__ == '__main__':
    app.run(debug=True)