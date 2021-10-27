from flask import Flask, render_template, request
from flaskext.mysql import MySQL
from werkzeug.utils import redirect

app = Flask(__name__)

#konfigurasi mysql
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'db_kontak'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app) 
conn = mysql.connect()

#routing
@app.route('/') #menampilkan data
def index():
   cursor = conn.cursor()
   sql = 'select * from kontak'
   cursor.execute(sql)
   hasil = cursor.fetchall()

   return render_template('index.html', data=hasil)

@app.route('/tambah', methods = ['GET', 'POST'])
def tambah():
   if request.method == 'POST': #simpan data
      _nama = request.values.get('nama')
      _kategori = request.values.get('kategori')

      sql = "insert into kontak(nama, kategori) values (%s, %s)"
      data = (_nama, _kategori)
      
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()

      return redirect('/')

   else: #menampilkan form
      return render_template('tambah_kontak.html')   

@app.route('/hapus/<_id>') #menampilkan data
def hapus_kontak(_id):
   cursor = conn.cursor()
   sql = 'delete from kontak where id = %s'
   data = (_id)
   cursor.execute(sql, data)
   conn.commit()

   return redirect('/')   

@app.route('/ubah/<_id>') #menampilkan data
def ubah_kontak(_id):
   cursor = conn.cursor()
   sql = 'select * from kontak where id = %s'
   data = (_id)
   cursor.execute(sql, data)
   hasil = cursor.fetchone()

   return render_template('ubah_kontak.html', data=hasil)

@app.route('/perbarui', methods = ['POST'])
def perbarui_kontak():
   _id = request.values.get('id')
   _nama = request.values.get('nama')
   _kategori = request.values.get('kategori')

   sql = "update kontak set nama = %s, kategori = %s where id = %s"
   data = (_nama, _kategori, _id)
   
   cursor = conn.cursor()
   cursor.execute(sql, data)
   conn.commit()

   return redirect('/')
