from flask import Flask, render_template

app = Flask(__name__)

#renderizando o home.html
#layout é a forma base de todas as páginas(como se fosse uma classe abstrata)
#as outras páginas vão herdar do layout
@app.route("/")
def homeP():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)