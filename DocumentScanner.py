from flask import Flask, render_template,request ,send_file,flash
import base64
import helperfunctions


app = Flask(__name__)

app.secret_key = "hereismysecretkey"




@app.route("/",methods = ["GET","POST"])
def index():
    if request.method == "POST":
        if request.files["pic"]:
            pic = request.files["pic"]
            img = base64.b64encode(pic.read())
            document = helperfunctions.ScanningImg(img)
            if document == False:
                flash("Lütfen Uyarıları Dikkate Alarak Tekrar Yükleyiniz!!")
            else:
                return send_file("Documents\scanned_img.jpg", as_attachment=True)

        else:
            flash("Henüz Bir Kağıt Yüklemediniz!")
            return render_template("index.html")
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)



