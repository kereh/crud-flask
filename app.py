# Author : Kereh
# Github : https://www.github.com/kereh

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    session,
    request,
    flash,
)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "watashiwaronarudodesu"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_orang_2.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Orang(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(20))
    umur = db.Column(db.String(20))
    alamat = db.Column(db.String(50))

    def __init__(self, nama, umur, alamat):
        self.nama = nama
        self.alamat = alamat
        self.umur = umur

@app.route('/')
def index():
    getAllOrang = Orang.query.all()
    check = len(getAllOrang)
    return render_template('index.html', title="Data Orang", row=getAllOrang, check=check)

@app.route("/tambah")
def tambah():
    return render_template("tambah.html", title="Tambah Data")

@app.route("/proses_tambah", methods=["POST", "GET"])
def proses_tambah():
    getAllOrang = Orang.query.all()
    nama = request.form["nama"]
    umur = request.form["umur"]
    alamat = request.form["alamat"]
    try:
        check_nama = len(nama)
        check_umur = len(umur)
        check_alamat = len(alamat)
        if check_nama == 0:
            return redirect(url_for("tambah"))
        if check_umur == 0:
            return redirect(url_for("tambah"))
        if check_alamat == 0:
            return redirect(url_for("tambah"))
        for x in getAllOrang:
            if nama == x.nama:
                flash(f'Nama {nama} sudah di pakai')
                return redirect(url_for("index"))
        data = Orang(nama, umur, alamat)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for("index"))
    except Exception as e:
        return "error"

@app.route("/hapus/<id>")
def hapus(id):
    getId = Orang.query.get(id)
    db.session.delete(getId)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<id>", methods=["POST", "GET"])
def edit(id):
    get = Orang.query.filter_by(id=id).first()
    row = get
    return render_template("edit.html", row=get,title=f"Edit Data {row.nama}")

@app.route("/edit_proc/<id>", methods=["POST", "GET"])
def edit_proc(id):
    all = Orang.query.all()
    get = Orang.query.filter_by(id=id).first()
    get.nama = request.form["nama"]
    get.umur = request.form["umur"]
    get.alamat = request.form["alamat"]
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
