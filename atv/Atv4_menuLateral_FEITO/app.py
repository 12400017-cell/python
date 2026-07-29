from flask import Flask, render_template

app = Flask(__name__)

#renderizando o home.html
#layout é a forma base de todas as páginas(como se fosse uma classe abstrata)
#as outras páginas vão herdar do layout
@app.route("/")
def homeP():
    return render_template("home.html")

@app.route("/page1")
def  pag1():
    return render_template("page1.html")

@app.route("/page2")
def  pag2():
    return render_template("page2.html")

if __name__ == '__main__':
    app.run(debug=True)