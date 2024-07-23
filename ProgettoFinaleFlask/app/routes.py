import hashlib
from . import app
from flask import Flask, abort, flash,render_template,redirect,request, send_from_directory, url_for,session,jsonify
from .models import db,User,Transaction

# Home --> °Dashboard generale
#                 (Login)
#             /             \
#            /               \
#     Grafico IN/OUT      STIME E REMINDER

def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password.encode('utf-8'))
    return hash_object.hexdigest()


@app.route("/")
def index():
    if 'username' in session:
        u = session['username']
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        utente = User.query.filter_by(username=request.form['username']).first()
        if not utente:
            flash("Utente non trovato,Redirect alla registrazione")
            return redirect(url_for('signup'))

        #u = request.form['username']
        # NOn controllo la password
        # p = hash_password(request.form['password'])
        #if hash_password(request.form['username']) == utente.password:
        session['username'] = request.form['username']
        session['iduser'] = utente.iduser
        return redirect(url_for('index'))

        utente = User(username = u , password = p)
        db.session.add(utente)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        utente = User.query.filter_by(username=request.form['username']).first()
        if utente:
            return flash("Username già utilizzato")
        u = request.form['username']
        p = hash_password(request.form['password'])
        utente = User(username = u , password = p)
        db.session.add(utente)
        db.session.commit()
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('iduser',None)

    return redirect(url_for('login'))


@app.route('/process', methods=['POST']) 
def process():  
    dati = []
    for i,j in request.form.items():
      dati.append(j)
    print(f"POST {dati}")
    #transizione = Transaction(iduser=session['iduser'],ammontare = dati[1],
    #                                  data = dati[2],tipo = dati[3],spesa_guada = dati[4])
    dati[4] = float(dati[4])
    #if dati[1] == 'expense':
    #    dati[4] = -dati[4]
    transizione = Transaction(iduser=session['iduser'],ammontare = dati[4],
                                      data = dati[3],tipo = dati[2],spesa_guada = dati[1])
    db.session.add(transizione)
    db.session.commit()
    return ''


# def calcolo(valore): 
#     if valore == "income":
#         valore = session['ammontare']
#     else:
#         valore = -session['ammontare']
#     return valore


@app.route('/index')
def home():
    if 'username' not in session:
        return redirect('/login')
    movimenti = Transaction.query.filter_by(iduser=session['iduser']).all()
    income = 0
    expenses = 0
    for movimento in movimenti:
        if movimento.spesa_guada == 'expense':
            expenses += movimento.ammontare
        else:
            income += movimento.ammontare
    return render_template('index.html', income=income, expenses=expenses)
    
@app.route('/images/<path:path>')
def static_images(path):
    return send_from_directory('images',path)

@app.route('/css/<path:path>')
def staitc_css(path):
    return send_from_directory('css',path)

@app.route('/js/<path:path>')
def static_js(path):
    return send_from_directory('js',path)

@app.route('/transaction')
def transaction():
    return render_template('transaction.html')

@app.route('/history')
@app.route('/transactionhistory')
def history():
    dati = []
    transizione = Transaction.query.filter_by(iduser=session['iduser']).all()
    transizione = transizione
    for j in transizione:
      dati.append(j)
    print(dati)
    return render_template('history.html',dati = dati)


# def insert_db():
#     for i,j in request.form.items():
#         db.session.add(j)


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#   # If the user made a POST request, create a new user
#     if request.method == "POST":
#         user = User(username=request.form.get("username"),
#                      password=request.form.get("password"))
#         # Add the user to the database
#         db.session.add(user)
#         # Commit the changes made
#         db.session.commit()
#         # Once user account created, redirect them
#         # to login route (created later on)
#         return redirect(url_for("login"))
#     # Se sono in GET carico il form di login.
#     return render_template('login.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         u = User(username=request.form['username'],
#                     password=request.form['password'])
#         db.session.add(u)
#         db.session.commit()
#     return render_template('register.html')

# @app.route('/updateuser/<int:p_id>', methods=['GET', 'POST'])
# def update(u_id):
#     u = User.query.get_or_404(u_id)
#     if request.method == 'POST':
#         u.nome = request.form['username']
#         u.anni = request.form['password']
#         db.session.add(u)
#         db.session.commit()
#     return render_template('edit.html', User=User)

# # Nota: tipicamente non si attiva anche GET per evitare
# # cancellazioni accidentali.
# @app.route('/delete/<int:p_id>', methods=['GET', 'POST'])
# def delete(u_id):
#     u = User.query.get_or_404(u_id)
#     db.session.delete(u)
#     db.session.commit()

