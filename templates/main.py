from flask import Flask, render_template
app = Flask(__name__, template_folder='../templates')


@app.route("/")
def initial():
    return render_template("welcome.html")


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


@app.route("/data_page")
def data_page():
    return render_template("data_page.html")


if __name__ == "__main__":
    app.run(debug=True)
# render_template將會找尋html檔案傳送給使用者
