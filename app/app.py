import os, signal, sqlite3, datetime, uuid
from pages import PAGES
from flask import Flask, render_template, request, redirect, url_for, jsonify, g, abort

app = Flask(__name__)
DB = os.environ.get("DB_PATH", "/data/hospital.db")
SLOTS = ["10:00","10:20","10:40","11:00","11:20","11:40","12:00","12:20","12:40"]
DOCTORS = [
    (1,"Dr. Anita Sharma","General Medicine","Mon-Sat, 10:00-13:00"),
    (2,"Dr. Rakesh Verma","Cardiology","Mon, Wed, Fri, 10:00-13:00"),
    (3,"Dr. Neha Singh","Pediatrics","Mon-Sat, 10:00-13:00"),
    (4,"Dr. Imran Khan","Orthopedics","Tue, Thu, Sat, 10:00-13:00"),
    (5,"Dr. Sunita Rao","Gynecology","Mon-Fri, 10:00-13:00"),
]

def db():
    if "db" not in g:
        os.makedirs(os.path.dirname(DB), exist_ok=True)
        g.db = sqlite3.connect(DB, timeout=10)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close(_):
    d = g.pop("db", None)
    if d: d.close()

def init():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    c = sqlite3.connect(DB)
    c.executescript("""
    CREATE TABLE IF NOT EXISTS doctors(id INTEGER PRIMARY KEY,name TEXT,dept TEXT,hours TEXT);
    CREATE TABLE IF NOT EXISTS appointments(
      ref TEXT PRIMARY KEY, doctor_id INT, date TEXT, slot TEXT,
      patient TEXT, phone TEXT, reason TEXT, created TEXT,
      UNIQUE(doctor_id,date,slot));""")
    c.executemany("INSERT OR IGNORE INTO doctors VALUES(?,?,?,?)", DOCTORS)
    c.commit(); c.close()
init()

def doctor(i):
    d = db().execute("SELECT * FROM doctors WHERE id=?", (i,)).fetchone()
    if not d: abort(404)
    return d

@app.route("/")
def home(): return render_template("home.html", doctors=DOCTORS)

@app.route("/facilities")
def facilities(): return render_template("facilities.html")

@app.route("/contact")
def contact(): return render_template("contact.html")

@app.route("/doctors")
def doctors(): return render_template("doctors.html", doctors=DOCTORS)

@app.route("/book", methods=["GET","POST"])
def book():
    docs = db().execute("SELECT * FROM doctors").fetchall()
    today = datetime.date.today()
    mx = today + datetime.timedelta(days=14)
    f = {"doctor_id": request.args.get("doctor", ""), "date": request.args.get("date", ""), "slot": "", "patient": "", "phone": "", "reason": ""}
    err = None
    if request.method == "POST":
        f = {k: request.form.get(k, "").strip() for k in f}
        try:
            d = datetime.date.fromisoformat(f["date"])
            if not (today <= d <= mx): err = "Choose a date within the next 14 days."
            elif d.weekday() == 6: err = "OPD is closed on Sundays."
        except ValueError: err = "Choose a valid date."
        if not err and f["slot"] not in SLOTS: err = "Choose a time slot."
        if not err and (len(f["patient"]) < 2 or not f["phone"].isdigit() or len(f["phone"]) != 10):
            err = "Enter the patient's name and a 10-digit mobile number."
        if not err:
            doc = doctor(f["doctor_id"])
            ref = "OPD-" + uuid.uuid4().hex[:6].upper()
            try:
                db().execute("INSERT INTO appointments VALUES(?,?,?,?,?,?,?,?)",
                  (ref, doc["id"], f["date"], f["slot"], f["patient"], f["phone"], f["reason"], datetime.datetime.now().isoformat()))
                db().commit()
                return redirect(url_for("confirm", ref=ref))
            except sqlite3.IntegrityError:
                err = "That slot was just taken. Pick another time."
    return render_template("book.html", docs=docs, f=f, err=err, slots=SLOTS, today=today, mx=mx)

@app.route("/slots")
def slots():
    taken = [r["slot"] for r in db().execute("SELECT slot FROM appointments WHERE doctor_id=? AND date=?",
             (request.args.get("doctor"), request.args.get("date")))]
    return jsonify([s for s in SLOTS if s not in taken])

@app.route("/appointment/<ref>")
def confirm(ref):
    a = db().execute("SELECT a.*, d.name dname, d.dept FROM appointments a JOIN doctors d ON d.id=a.doctor_id WHERE ref=?", (ref,)).fetchone()
    if not a: abort(404)
    return render_template("confirm.html", a=a)

@app.route("/health")
def health():
    try:
        db().execute("SELECT 1").fetchone()
        return jsonify(status="ok"), 200
    except Exception as e:
        return jsonify(status="down", error=str(e)), 503

@app.route("/api/appointments")
def api_list():
    rows = db().execute("SELECT ref,doctor_id,date,slot FROM appointments ORDER BY date,slot").fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/crash", methods=["POST"])
def crash():  # demo only: stops the container's main process
    if os.environ.get("ENABLE_CRASH") != "1": abort(404)
    os.kill(os.getppid(), signal.SIGTERM)
    return "crashing", 202


@app.route("/<slug>")
def page(slug):
    if slug not in PAGES: abort(404)
    t, intro, secs = PAGES[slug]
    return render_template("page.html", title=t, intro=intro, secs=secs)

@app.route("/manage", methods=["GET","POST"])
def manage():
    a, msg = None, None
    if request.method == "POST":
        ref = request.form.get("ref","").strip().upper(); ph = request.form.get("phone","").strip()
        q = "SELECT a.*, d.name dname, d.dept FROM appointments a JOIN doctors d ON d.id=a.doctor_id WHERE ref=? AND phone=?"
        a = db().execute(q, (ref, ph)).fetchone()
        if not a: msg = "No booking matches that number and mobile. Check both and try again."
        elif request.form.get("action") == "cancel":
            db().execute("DELETE FROM appointments WHERE ref=?", (ref,)); db().commit()
            a, msg = None, "Your booking " + ref + " is cancelled and the slot is free again."
    return render_template("manage.html", a=a, msg=msg)

@app.errorhandler(404)
def nf(_): return render_template("page.html", title="Page not found", intro="That page does not exist. Use the menu or go back home.", secs=[]), 404

@app.after_request
def headers(r):
    r.headers["X-Content-Type-Options"] = "nosniff"; r.headers["X-Frame-Options"] = "DENY"
    r.headers["Referrer-Policy"] = "same-origin"
    return r

@app.route("/appointment/<ref>/receipt")
def receipt(ref):
    a = db().execute("SELECT a.*, d.name dname, d.dept FROM appointments a JOIN doctors d ON d.id=a.doctor_id WHERE ref=?", (ref,)).fetchone()
    if not a: abort(404)
    html = render_template("receipt.html", a=a, phone=("XXXXXX" + a["phone"][-4:]),
                           now=datetime.datetime.now().strftime("%d %b %Y, %I:%M %p"),
                           auto_print=request.args.get("print") == "1")
    r = app.response_class(html, mimetype="text/html")
    if request.args.get("download") == "1":
        r.headers["Content-Disposition"] = f"attachment; filename=receipt-{a['ref']}.html"
    return r
