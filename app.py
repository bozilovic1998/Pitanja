from flask import Flask, render_template, url_for, request, redirect, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash


con=mysql.connector.connect(
		host='localhost',
		port='3308',
		user='root',
		passwd='',
		database='baza_pitanja'
	)

mycursor = con.cursor(dictionary=True)

app = Flask(__name__)

app.secret_key='tajni_kljuc'

#-----------------------------------------------> Login <-------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def Login():
	if request.method=='GET':
		return render_template('login.html')
	elif request.method=='POST':
		forma=request.form
		upit="SELECT * FROM korisnik WHERE korisnicko_ime=%s"
		vrednost=(forma['korisnicko_ime'],)
		mycursor.execute(upit, vrednost)
		korisnik=mycursor.fetchone()
		print(korisnik)
		if(korisnik is not None):
			if check_password_hash(korisnik['lozinka'], forma['lozinka']):
				session['ulogovani_korisnik']=str(korisnik)
				return redirect(url_for('Opsti_deo'))
			else:
				flash("Pogrešna lozinka!")
				return redirect(request.referrer)
		else:
			flash("Korisnik sa navedenim korisičkim imenom ne postoji.")
			return redirect(request.referrer)

@app.route('/admin_login', methods=['GET', 'POST'])
def Admin_Login():
	if request.method=='GET':
		return render_template("admin_login.html")
	elif request.method=='POST':
		forma=request.form
		upit="SELECT * FROM admin WHERE korisnicko_ime=%s"
		vrednost=(forma['korisnicko_ime'],)
		mycursor.execute(upit, vrednost)
		admin=mycursor.fetchone()
		if(admin is not None):
			if (admin['lozinka'] == forma['lozinka']):
				session['ulogovani_admin']=str(admin)
				return redirect(url_for('Korisnici'))
			else:
				flash("Pogrešna lozinka!")
				return redirect(request.referrer)
		else:
			flash("Administrator sa navedenim korisičkim imenom ne postoji.")
			return redirect(request.referrer)

def Logged():
 if 'ulogovani_korisnik' in session:
 	return True
 else:
 	return False

def Logged_Admin():
 if 'ulogovani_admin' in session:
 	return True
 else:
 	return False

@app.route('/logout')
def Logout():
	session.pop('ulogovani_korisnik', None)
	return redirect(url_for('Login'))

@app.route('/logout_admin')
def Logout_Admin():
	session.pop('ulogovani_admin', None)
	return redirect(url_for('Admin_Login'))

@app.route('/')
def Home():
	return render_template("login.html")


#-----------------------------------------------> Pitanja <-------------------------------------------------------

@app.route('/opsti_deo', methods = ['GET', 'POST'])
def Opsti_deo():
	if Logged():
		mycursor.execute("SELECT MIN(broj_pitanja) AS Broj_Pitanja_Min FROM opsti_deo_pitanja")
		minimum = mycursor.fetchone()
		mycursor.execute("SELECT MAX(broj_pitanja) AS Broj_Pitanja_Max FROM opsti_deo_pitanja")
		maximum = mycursor.fetchone()
		con.commit()
		return render_template("opsti_deo.html", minimum=minimum, maximum=maximum)
	else:
		return redirect(url_for("Login"))

@app.route('/tds_pitanja')
def Tds_Pitanja():
	if Logged():
		mycursor.execute("SELECT MIN(broj_pitanja) AS Broj_Pitanja_Min FROM tds_pitanja")
		minimum = mycursor.fetchone()
		mycursor.execute("SELECT MAX(broj_pitanja) AS Broj_Pitanja_Max FROM tds_pitanja")
		maximum = mycursor.fetchone()
		con.commit()
		return render_template("tds_pitanja.html",minimum=minimum, maximum=maximum)
	else:
		return redirect(url_for("Login"))

@app.route('/b_pitanja')
def B_Pitanja():
	if Logged():
		mycursor.execute("SELECT MIN(broj_pitanja) AS Broj_Pitanja_Min FROM b_pitanja")
		minimum = mycursor.fetchone()
		mycursor.execute("SELECT MAX(broj_pitanja) AS Broj_Pitanja_Max FROM b_pitanja")
		maximum = mycursor.fetchone()
		con.commit()
		return render_template("b_pitanja.html",minimum=minimum, maximum=maximum)
	else:
		return redirect(url_for("Login"))	

@app.route('/c_pitanja')
def C_Pitanja():
	if Logged():
		mycursor.execute("SELECT MIN(broj_pitanja) AS Broj_Pitanja_Min FROM c_pitanja")
		minimum = mycursor.fetchone()
		mycursor.execute("SELECT MAX(broj_pitanja) AS Broj_Pitanja_Max FROM c_pitanja")
		maximum = mycursor.fetchone()
		con.commit()
		return render_template("c_pitanja.html",minimum=minimum, maximum=maximum)
	else:
		return redirect(url_for("Login"))


@app.route('/prikaz_opsti_deo', methods = ['GET', 'POST'])
def Prikaz_opsti_deo():
	if Logged():
		prvo=request.form['prvo']
		drugo=request.form['drugo']
		trece=request.form['trece']
		cetvrto=request.form['cetvrto']
		peto=request.form['peto']
		while prvo not in (drugo, trece, cetvrto, peto) and drugo not in (prvo, trece, cetvrto, peto) and trece not in (prvo, drugo, cetvrto, peto) and cetvrto not in (prvo, drugo, trece, peto) and peto not in (prvo, drugo, trece, cetvrto):
			mycursor.execute("SELECT * FROM opsti_deo_pitanja WHERE broj_pitanja=%s UNION SELECT * FROM opsti_deo_pitanja WHERE broj_pitanja=%s UNION SELECT * FROM opsti_deo_pitanja WHERE broj_pitanja=%s UNION SELECT * FROM opsti_deo_pitanja WHERE broj_pitanja=%s UNION SELECT * FROM opsti_deo_pitanja WHERE broj_pitanja=%s", (prvo, drugo, trece, cetvrto, peto))
			pitanja = mycursor.fetchall()
			con.commit()
			return render_template('prikaz_opsti_deo.html', pitanja = pitanja)
		else:
			flash("Morate uneti različite brojeve pitanja.")
			return redirect(request.referrer)

	else:
		return redirect(url_for("Login"))


@app.route('/prikaz_tds_pitanja', methods=['GET','POST'])
def Prikaz_tds_pitanja():
	if Logged():
		prvo=request.form['prvo']
		drugo=request.form['drugo']
		trece=request.form['trece']
		cetvrto=request.form['cetvrto']
		peto=request.form['peto']
		while prvo not in (drugo, trece, cetvrto, peto) and drugo not in (prvo, trece, cetvrto, peto) and trece not in (prvo, drugo, cetvrto, peto) and cetvrto not in (prvo, drugo, trece, peto) and peto not in (prvo, drugo, trece, cetvrto):
			mycursor.execute("SELECT * FROM tds_pitanja WHERE broj_pitanja=%s UNION SELECT * FROM tds_pitanja WHERE broj_pitanja=%s UNION SELECT * FROM tds_pitanja WHERE broj_pitanja=%s UNION SELECT * FROM tds_pitanja WHERE broj_pitanja=%s UNION SELECT * FROM tds_pitanja WHERE broj_pitanja=%s", (prvo, drugo, trece, cetvrto, peto))
			pitanja = mycursor.fetchall()
			con.commit()
			return render_template('prikaz_tds_pitanja.html', pitanja = pitanja)
		else:
			flash("Morate uneti različite brojeve pitanja.")
			return redirect(request.referrer)
	else:
		return redirect(url_for("Login"))

@app.route('/prikaz_b_pitanja', methods=['GET','POST'])
def Prikaz_b_pitanja():
	if Logged():
		prvo=request.form['prvo']
		drugo=request.form['drugo']
		trece=request.form['trece']
		cetvrto=request.form['cetvrto']
		peto=request.form['peto']
		while prvo not in (drugo, trece, cetvrto, peto) and drugo not in (prvo, trece, cetvrto, peto) and trece not in (prvo, drugo, cetvrto, peto) and cetvrto not in (prvo, drugo, trece, peto) and peto not in (prvo, drugo, trece, cetvrto):
			mycursor.execute("SELECT * FROM b_pitanja WHERE broj_pitanja=%s UNION SELECT * FROM b_pitanja WHERE broj_pitanja=%s UNION SELECT * FROM b_pitanja WHERE broj_pitanja=%s UNION SELECT * FROM b_pitanja WHERE broj_pitanja=%s UNION SELECT * FROM b_pitanja WHERE broj_pitanja=%s", (prvo, drugo, trece, cetvrto, peto))
			pitanja = mycursor.fetchall()
			con.commit()
			return render_template('prikaz_b_pitanja.html', pitanja = pitanja)
		else:
			flash("Morate uneti različite brojeve pitanja.")
			return redirect(request.referrer)
	else:
		return redirect(url_for("Login"))


@app.route('/prikaz_c_pitanja', methods=['GET','POST'])
def Prikaz_c_pitanja():
	if Logged():
		prvo=request.form['prvo']
		drugo=request.form['drugo']
		trece=request.form['trece']
		cetvrto=request.form['cetvrto']
		peto=request.form['peto']
		while prvo not in (drugo, trece, cetvrto, peto) and drugo not in (prvo, trece, cetvrto, peto) and trece not in (prvo, drugo, cetvrto, peto) and cetvrto not in (prvo, drugo, trece, peto) and peto not in (prvo, drugo, trece, cetvrto):
			mycursor.execute("SELECT * FROM c_pitanja WHERE broj_pitanja=%s UNION SELECT * FROM c_pitanja WHERE broj_pitanja=%s UNION SELECT * FROM c_pitanja WHERE broj_pitanja=%s UNION SELECT * FROM c_pitanja WHERE broj_pitanja=%s UNION SELECT * FROM c_pitanja WHERE broj_pitanja=%s", (prvo, drugo, trece, cetvrto, peto))
			pitanja = mycursor.fetchall()
			con.commit()
			return render_template('prikaz_c_pitanja.html', pitanja = pitanja)
		else:
			flash("Morate uneti različite brojeve pitanja.")
			return redirect(request.referrer)
	else:
		return redirect(url_for("Login"))

#-----------------------------------------------> Administrator - korisnici <-------------------------------------------------------

@app.route('/novi_korisnik', methods=['GET', 'POST'])
def Novi_Korisnik():

	if Logged_Admin():

		if request.method == 'GET':
			return render_template('admin_korisnici.html')
		elif request.method == 'POST':
			forma = request.form
			upit = "INSERT INTO korisnik (korisnicko_ime, lozinka, email) VALUES (%s, %s, %s)"
			hash_lozinka = generate_password_hash(forma['lozinka'])
			vrednosti = (forma['korisnicko_ime'],hash_lozinka, forma['email'])
			mycursor.execute(upit, vrednosti)
			flash("Novi korisnik je uspešno dodat.")
			con.commit()
			return redirect(url_for('Korisnici'))
	else:
		return redirect(url_for("Admin_Login"))

@app.route('/admin_korisnici')
def Korisnici():

	if Logged_Admin():
		upit = "SELECT * FROM korisnik"
		mycursor.execute(upit)
		korisnici = mycursor.fetchall()
		return render_template('admin_korisnici.html', korisnici = korisnici)
	else:
		return redirect(url_for("Admin_Login"))

@app.route('/korisnik_izmena', methods=['GET', 'POST'])
def Korisnik_Izmena():

	if Logged_Admin():

		if request.method == 'POST':
			id_data = request.form['id']
			korisnicko_ime = request.form['korisnicko_ime']
			email = request.form['email']
			lozinka = generate_password_hash(request.form['lozinka'])
			mycursor.execute("UPDATE korisnik SET korisnicko_ime=%s, lozinka=%s, email=%s WHERE id=%s", (korisnicko_ime, lozinka, email, id_data))
			flash("Izmena je uspešno izvršena.")
			con.commit()
			return redirect(url_for('Korisnici'))
	else:
		return redirect(url_for("Admin_Login"))		

@app.route('/korisnik_brisanje/<string:id_data>', methods = ['GET', 'POST'])
def Korisnik_Brisanje(id_data):

	if Logged_Admin():

		mycursor = con.cursor()
		upit= "DELETE FROM korisnik WHERE id = %s"
		vrednost = (id_data,)
		mycursor.execute(upit, vrednost)
		flash("Korisnik je obrisan.")
		con.commit()
		return redirect(url_for('Korisnici'))
	else:
		return redirect(url_for("Admin_Login"))	

#-----------------------------------------------> Administrator - pitanja <-------------------------------------------------------

@app.route('/admin_opsti_deo', methods = ['GET', 'POST'])
def Admin_opsti_deo():
	if Logged_Admin():

		upit = "SELECT * FROM opsti_deo_pitanja"
		mycursor.execute(upit)
		pitanja = mycursor.fetchall()
		upit="SELECT MAX(broj_pitanja) AS broj_pitanja FROM opsti_deo_pitanja"
		mycursor.execute(upit)
		br = mycursor.fetchone()
		return render_template('admin_opsti_deo.html', pitanja = pitanja, br=br)
	else:
		return redirect(url_for("Admin_Login"))	

@app.route('/opsti_deo_izmena', methods=['GET', 'POST'])
def Opsti_deo_izmena():

	if Logged_Admin():

		if request.method == 'POST':
			id_data = request.form['id']
			broj_pitanja = request.form['broj_pitanja']
			text_pitanja = request.form['text_pitanja']
			odgovor_jedan = request.form['odgovor_jedan']
			odgovor_dva = request.form['odgovor_dva']
			odgovor_tri = request.form['odgovor_tri']
			odgovor_cetiri = request.form['odgovor_cetiri']
			mycursor.execute("UPDATE opsti_deo_pitanja SET text_pitanja=%s, broj_pitanja=%s, odgovor_jedan=%s, odgovor_dva=%s, odgovor_tri=%s, odgovor_cetiri=%s WHERE id=%s", (text_pitanja, broj_pitanja, odgovor_jedan, odgovor_dva, odgovor_tri, odgovor_cetiri, id_data))
			flash("Izmena je uspešno izvršena.")
			con.commit()
			return redirect(url_for('Admin_opsti_deo'))
	else:
		return redirect(url_for("Admin_Login"))

@app.route('/novo_opsti_deo', methods=['GET', 'POST'])
def Novo_opsti_deo():

	if Logged_Admin():

		if request.method == 'GET':
			return render_template('admin_opsti_deo.html')
		elif request.method == 'POST':
			forma = request.form
			upit = "INSERT INTO opsti_deo_pitanja (broj_pitanja, text_pitanja, odgovor_jedan, odgovor_dva, odgovor_tri, odgovor_cetiri) VALUES (%s, %s, %s, %s, %s, %s)"
			vrednosti = (forma['broj_pitanja'], forma['text_pitanja'], forma['odgovor_jedan'], forma['odgovor_dva'], forma['odgovor_tri'], forma['odgovor_cetiri'])
			mycursor.execute(upit, vrednosti)
			flash("Novo pitanje je uspešno dodato.")
			con.commit()
			return redirect(url_for('Admin_opsti_deo'))
	else:
		return redirect(url_for("Admin_Login"))			


@app.route('/admin_tds_pitanja', methods = ['GET', 'POST'])
def Admin_tds_pitanja():

	if Logged_Admin():

		upit = "SELECT * FROM tds_pitanja"
		mycursor.execute(upit)
		pitanja = mycursor.fetchall()
		upit="SELECT MAX(broj_pitanja) AS broj_pitanja FROM tds_pitanja"
		mycursor.execute(upit)
		br = mycursor.fetchone()
		return render_template('admin_tds_pitanja.html', pitanja = pitanja, br=br)
	else:
		return redirect(url_for("Admin_Login"))	

@app.route('/tds_pitanja_izmena', methods=['GET', 'POST'])
def Tds_pitanja_izmena():

	if Logged_Admin():

		if request.method == 'POST':
			id_data = request.form['id']
			broj_pitanja = request.form['broj_pitanja']
			text_pitanja = request.form['text_pitanja']
			odgovor_jedan = request.form['odgovor_jedan']
			odgovor_dva = request.form['odgovor_dva']
			odgovor_tri = request.form['odgovor_tri']
			mycursor.execute("UPDATE tds_pitanja SET text_pitanja=%s, broj_pitanja=%s, odgovor_jedan=%s, odgovor_dva=%s, odgovor_tri=%s WHERE id=%s", (text_pitanja, broj_pitanja, odgovor_jedan, odgovor_dva, odgovor_tri, id_data))
			flash("Izmena je uspešno izvršena.")
			con.commit()
			return redirect(url_for('Admin_tds_pitanja'))
	else:
		return redirect(url_for("Admin_Login"))		

@app.route('/novo_tds_pitanje', methods=['GET', 'POST'])
def Novo_tds_pitanje():

	if Logged_Admin():

		if request.method == 'GET':
			return render_template('admin_tds_pitanja.html')
		elif request.method == 'POST':
			forma = request.form
			upit = "INSERT INTO tds_pitanja (broj_pitanja, text_pitanja, odgovor_jedan, odgovor_dva, odgovor_tri) VALUES (%s, %s, %s, %s, %s)"
			vrednosti = (forma['broj_pitanja'], forma['text_pitanja'], forma['odgovor_jedan'], forma['odgovor_dva'], forma['odgovor_tri'])
			mycursor.execute(upit, vrednosti)
			flash("Novo pitanje je uspešno dodato.")
			con.commit()
			return redirect(url_for('Admin_tds_pitanja'))
	else:
		return redirect(url_for("Admin_Login"))		

@app.route('/admin_b_pitanja')
def Admin_b_pitanja():
	if Logged_Admin():

		upit = "SELECT * FROM b_pitanja"
		mycursor.execute(upit)
		pitanja = mycursor.fetchall()
		upit="SELECT MAX(broj_pitanja) AS broj_pitanja FROM b_pitanja"
		mycursor.execute(upit)
		br = mycursor.fetchone()
		return render_template('admin_b_pitanja.html', pitanja = pitanja,br=br)
	else:
		return redirect(url_for("Admin_Login"))

@app.route('/b_pitanja_izmena', methods=['GET', 'POST'])
def B_pitanja_izmena():

	if Logged_Admin():

		if request.method == 'POST':
			id_data = request.form['id']
			broj_pitanja = request.form['broj_pitanja']
			text_pitanja = request.form['text_pitanja']
			odgovor_jedan = request.form['odgovor_jedan']
			odgovor_dva = request.form['odgovor_dva']
			odgovor_tri = request.form['odgovor_tri']
			mycursor.execute("UPDATE b_pitanja SET broj_pitanja=%s, text_pitanja=%s, odgovor_jedan=%s, odgovor_dva=%s, odgovor_tri=%s WHERE id=%s", (broj_pitanja, text_pitanja, odgovor_jedan, odgovor_dva, odgovor_tri, id_data))
			flash("Izmena je uspešno izvršena.")
			con.commit()
			return redirect(url_for('Admin_b_pitanja'))
	else:
		return redirect(url_for("Admin_Login"))		

@app.route('/novo_b_pitanje', methods=['GET', 'POST'])
def Novo_b_pitanje():

	if Logged_Admin():

		if request.method == 'GET':
			return render_template('admin_b_pitanja.html')
		elif request.method == 'POST':
			forma = request.form
			upit = "INSERT INTO b_pitanja (broj_pitanja, text_pitanja, odgovor_jedan, odgovor_dva, odgovor_tri) VALUES (%s, %s, %s, %s, %s)"
			vrednosti = (forma['broj_pitanja'], forma['text_pitanja'], forma['odgovor_jedan'], forma['odgovor_dva'], forma['odgovor_tri'])
			mycursor.execute(upit, vrednosti)
			flash("Novo pitanje je uspešno dodato.")
			con.commit()
			return redirect(url_for('Admin_b_pitanja'))
	else:
		return redirect(url_for("Admin_Login"))		

@app.route('/admin_c_pitanja')
def Admin_c_pitanja():
	if Logged_Admin():

		upit = "SELECT * FROM c_pitanja"
		mycursor.execute(upit)
		pitanja = mycursor.fetchall()
		upit="SELECT MAX(broj_pitanja) AS broj_pitanja FROM c_pitanja"
		mycursor.execute(upit)
		br = mycursor.fetchone()
		return render_template('admin_c_pitanja.html', pitanja = pitanja,br=br)
	else:
		return redirect(url_for("Admin_Login"))


@app.route('/c_pitanja_izmena', methods=['GET', 'POST'])
def C_pitanja_izmena():

	if Logged_Admin():

		if request.method == 'POST':
			id_data = request.form['id']
			broj_pitanja = request.form['broj_pitanja']
			text_pitanja = request.form['text_pitanja']
			odgovor_jedan = request.form['odgovor_jedan']
			odgovor_dva = request.form['odgovor_dva']
			odgovor_tri = request.form['odgovor_tri']
			mycursor.execute("UPDATE c_pitanja SET broj_pitanja = %s, text_pitanja=%s, odgovor_jedan=%s, odgovor_dva=%s, odgovor_tri=%s WHERE id=%s", (broj_pitanja, text_pitanja, odgovor_jedan, odgovor_dva, odgovor_tri, id_data))
			flash("Izmena je uspešno izvršena.")
			con.commit()
			return redirect(url_for('Admin_c_pitanja'))
	else:
		return redirect(url_for("Admin_Login"))		

@app.route('/novo_c_pitanje', methods=['GET', 'POST'])
def Novo_c_pitanje():

	if Logged_Admin():

		if request.method == 'GET':
			return render_template('admin_c_pitanja.html')
		elif request.method == 'POST':
			forma = request.form
			upit = "INSERT INTO c_pitanja (broj_pitanja, text_pitanja, odgovor_jedan, odgovor_dva, odgovor_tri) VALUES (%s, %s, %s, %s, %s)"
			vrednosti = (forma['broj_pitanja'], forma['text_pitanja'], forma['odgovor_jedan'], forma['odgovor_dva'], forma['odgovor_tri'])
			mycursor.execute(upit, vrednosti)
			flash("Novo pitanje je uspešno dodato.")
			con.commit()
			return redirect(url_for('Admin_c_pitanja'))
	else:
		return redirect(url_for("Admin_Login"))
		
		
app.run(debug=True)

