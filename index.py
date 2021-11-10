from prettytable import PrettyTable
from datetime import date, datetime, time, timedelta
import os
import json
import getpass

def waktu_sekarang() :
  return datetime.now().strftime('%H:%M')

def tanggal_sekarang(format = "-") :
  return date.today().strftime(f'%d{format}%m{format}%Y')

def buat_file_database_json(database) :
  # buat file database jika tidak ada
  file_database = open('database.json', 'a')

  if file_database :
    if os.path.getsize('database.json') == 0 :
      file_database.write(json.dumps(database))
      file_database.close()

buat_file_database_json({
  "pengguna": [
    {"id": 1, "username": "admin", "password": "admin", "role": "admin"},
    {"id": 3, "username": "admin2", "password": "admin2", "role": "admin"}
  ],
  "pelanggan": [
    { "id": 1, "nama": "Novil", "tanggal_bergabung": tanggal_sekarang() },
    { "id": 2, "nama": "Rizki Perdana", "tanggal_bergabung": tanggal_sekarang() },
    { "id": 3, "nama": "Ibnu Praditya", "tanggal_bergabung": tanggal_sekarang() },
  ],
  "billing": [
    {
      "id": 1,
      "id_pelanggan": 2,
      "tanggal": tanggal_sekarang(),
      "waktu_mulai": '13:00',
      "waktu_selesai": '14:00',
      "harga": 8000,
      'total_harga': 8000
    },
  ],
  "pengaturan": [
    { "id": 1, "harga_perjam": 8000 }
  ]
})

def timpa_db(data) :
  file_database = open('database.json', 'w')
  file_database.write(json.dumps(data))
  file_database.close()
  
def get(field = False) :
  file_database = open('database.json')
  data = json.loads(file_database.read())
  file_database.close()

  return data[field] if field != False else data

def get_by_id(field, id) :
  data = get(field)
  for i in range(len(data)) :
    if data[i]['id'] == id :
      return data[i]
  
  return False

def get_last_id(field) :
  data_db = sorted(get(field), key=lambda data: data['id'], reverse=True)
  return data_db[0]['id'] if len(data_db) > 0 else False

def create(field, data) :
  data_db = get()
  data_db[field] = get(field)
  data_db[field].append(data)

  timpa_db(data_db)

def update(field, data) :
  id = data['id']
  data_db = get_by_id(field, id)

  if data_db :
    for i in data['data'] :
      if i != 'id' and (i in data_db) :
        data_db[i] = data['data'][i]

    db = get()
    for i in range(len(db[field])) :
      if db[field][i]['id'] == id :
        db[field][i] = data_db
    
    timpa_db(db)

def delete(field, id) :
  data_db = get()
  data_db[field] = list(filter(lambda data: data['id'] != id, data_db[field]))

  timpa_db(data_db)

# ============================================================================================================================== #

def hapus_billing() :
  tampilkan_billing()

  id_billing = int(input('ID : '))
  billing = get_by_id('billing', id_billing)

  if billing :
    delete('billing', id_billing)
    tampilkan_billing()
    print(f'billing dengan ID {id_billing} berhasil dihapus')
  else :
    print('Mohon masukan ID billing yang tersedia')
    return halaman_billing()

def edit_billing() :
  print()
  tampilkan_billing()

  id = int(input('ID billing : '))
  billing = get_by_id('billing', id)

  pelanggan = get_by_id('pelanggan', billing['id_pelanggan'])
  nama_pelanggan = pelanggan['nama']
  id_pelanggan_lama = pelanggan['id']
  id_pelanggan = input(f'ID pelanggan ({id_pelanggan_lama}, {nama_pelanggan}) : ') or id_pelanggan_lama
  id_pelanggan = int(id_pelanggan)

  tanggal = tanggal_sekarang()
  waktu_mulai_lama = billing['waktu_mulai']
  waktu_selesai_lama = billing['waktu_selesai']
  waktu_mulai = input(f'Waktu mulai ({waktu_mulai_lama}) : ') or waktu_mulai_lama
  waktu_selesai = input(f'Waktu selesai ({waktu_selesai_lama}) : ') or waktu_selesai_lama

  harga_perjam = get('pengaturan')[0]['harga_perjam']
  durasi = datetime.strptime(waktu_selesai, '%H:%M') - datetime.strptime(waktu_mulai, '%H:%M')
  total_harga = int(get('pengaturan')[0]['harga_perjam'] * int(durasi.seconds / 3600))

  if get_by_id('pelanggan', id_pelanggan) :
    update('billing', {
      'id': id,
      'data': {
        'id_pelanggan': id_pelanggan,
        'tanggal': tanggal,
        'waktu_mulai': waktu_mulai,
        'waktu_selesai': waktu_selesai,
        'harga': harga_perjam,
        'total_harga': total_harga
      }
    })
    tampilkan_billing()
    print('Billing telah edit')
  else :
    print('ID pelanggan tidak ditemukan')
    return tambah_billing()

def tambah_billing() :
  print()
  tampilkan_pelanggan()

  id = get_last_id('billing')
  id_pelanggan = int(input('ID pelanggan : '))
  tanggal = tanggal_sekarang()
  waktu_mulai = input(f'Waktu mulai ({waktu_sekarang()}) : ') or waktu_sekarang()
  waktu_selesai = input('Waktu selesai : ')

  harga_perjam = get('pengaturan')[0]['harga_perjam']
  durasi = datetime.strptime(waktu_selesai, '%H:%M') - datetime.strptime(waktu_mulai, '%H:%M')
  total_harga = int(get('pengaturan')[0]['harga_perjam'] * int(durasi.seconds / 3600))

  if get_by_id('pelanggan', id_pelanggan) :
    create('billing', {
      'id': id + 1,
      'id_pelanggan': id_pelanggan,
      'tanggal': tanggal,
      'waktu_mulai': waktu_mulai,
      'waktu_selesai': waktu_selesai,
      'harga': harga_perjam,
      'total_harga': total_harga
    })
    tampilkan_billing()
    print('Billing telah ditambahkan')
  else :
    print('ID pelanggan tidak ditemukan')
    return tambah_billing()


def tampilkan_billing() :
  print()
  print('Daftar Billing :')

  tabel = PrettyTable()
  tabel.field_names = ['No', 'ID', 'Nama Pelanggan', 'Tanggal', 'Waktu', 'Durasi (jam)', 'Harga', 'Total Harga']

  billing = get('billing')
  for i in range(len(billing)) :
    pelanggan = get_by_id('pelanggan', billing[i]['id_pelanggan'])
    waktu_mulai = billing[i]['waktu_mulai']
    waktu_selesai = billing[i]['waktu_selesai']
    harga = billing[i]['harga']
    durasi = datetime.strptime(waktu_selesai, '%H:%M') - datetime.strptime(waktu_mulai, '%H:%M')
    total_harga = int(billing[i]['harga'] * (durasi.seconds / 3600))

    tabel.add_row([
      i + 1,
      billing[i]['id'],
      pelanggan['nama'] or '[Pelanggan Telah Terhapus]',
      billing[i]['tanggal'],
      f'{waktu_mulai} - {waktu_selesai}',
      durasi,
      f'Rp {harga}',
      f'Rp {total_harga}',
    ])

  print(tabel)

def pilihan_menu_halaman_billing(tampilkan_menu = True) :
  print()
  if tampilkan_menu :
    print('== Halaman Billing ==')
    print('[1] Tampilkan Billing')
    print('[2] Tambah Billing')
    print('[3] Edit Billing')
    print('[4] Hapus Billing')
    print('[0] Kembali')

  return int(input('Pilih : '))

def halaman_billing(tampilkan_menu = True) :
  pilihan = pilihan_menu_halaman_billing(tampilkan_menu)
  if pilihan == 1 :
    tampilkan_billing()
    return halaman_billing(False)
  elif pilihan == 2 :
    tambah_billing()
    return halaman_billing(False)
  elif pilihan == 3 :
    edit_billing()
    return halaman_billing(False)
  elif pilihan == 4 :
    hapus_billing()
    return halaman_billing(False)
  elif pilihan == 0 :
    return halaman_user()
  else :
    print('Mohon pilih pilihan yang tersedia')
    return halaman_billing()

# ============================================================================================================================== #

def hapus_pelanggan() :
  tampilkan_pelanggan()

  id_pelanggan = int(input('ID : '))
  pelanggan = get_by_id('pelanggan', id_pelanggan)

  if pelanggan :
    delete('pelanggan', id_pelanggan)
    tampilkan_pelanggan()
    print(f'Pelanggan dengan ID {id_pelanggan} berhasil dihapus')
  else :
    print('Mohon masukan ID pelanggan yang tersedia')
    return hapus_pelanggan()

def edit_pelanggan() :
  tampilkan_pelanggan()

  id_pelanggan = int(input('ID : '))
  pelanggan = get_by_id('pelanggan', id_pelanggan)

  if pelanggan :
    nama_lama = pelanggan['nama']
    nama = input(f'Nama ({nama_lama}) : ') or nama_lama

    update('pelanggan', {
      'id': id_pelanggan,
      'data': { 'nama': nama }
    })

    tampilkan_pelanggan()
    print(f'Pelanggan dengan ID {id_pelanggan} telah diedit')
  else :
    print('Mohon masukan ID pelanggan yang tersedia')
    return edit_pelanggan()

def tambah_pelanggan() :
  print()

  id = get_last_id('pelanggan')
  nama = input('Nama : ')
  tanggal_bergabung = tanggal_sekarang()

  create('pelanggan', { 'id': id + 1, 'nama': nama, 'tanggal_bergabung': tanggal_bergabung })
  tampilkan_pelanggan()
  print('Pelanggan telah ditambahkan')

def tampilkan_pelanggan() :
  print()
  print('Daftar Pelanggan :')

  tabel = PrettyTable()
  tabel.field_names = ['No', 'ID', 'Nama', 'Tanggal Bergabung']

  pelanggan = get('pelanggan')
  for i in range(len(pelanggan)) :
    tabel.add_row([
      i + 1,
      pelanggan[i]['id'],
      pelanggan[i]['nama'],
      pelanggan[i]['tanggal_bergabung']
    ])

  print(tabel)

def pilihan_menu_halaman_pelanggan(tampilkan_menu = True) :
  print()
  if tampilkan_menu :
    print('== Halaman Pelanggan ==')
    print('[1] Tampilkan Pelanggan')
    print('[2] Tambah Pelanggan')
    print('[3] Edit Pelanggan')
    print('[4] Hapus Pelanggan')
    print('[0] Kembali')

  return int(input('Pilih : '))

def halaman_pelanggan(tampilkan_menu = True) :
  pilihan = pilihan_menu_halaman_pelanggan(tampilkan_menu)
  if pilihan == 1 :
    tampilkan_pelanggan()
    return halaman_pelanggan(False)
  elif pilihan == 2 :
    tambah_pelanggan()
    return halaman_pelanggan(False)
  elif pilihan == 3 :
    edit_pelanggan()
    return halaman_pelanggan(False)
  elif pilihan == 4 :
    hapus_pelanggan()
    return halaman_pelanggan(False)
  elif pilihan == 0 :
    return halaman_user()
  else :
    print('Mohon pilih pilihan yang tersedia')
    return halaman_pelanggan()

# ============================================================================================================================== #

def pilihan_menu_halaman_user() :
  print()
  print('== Halaman user ==')
  print('[1] Billing')
  print('[2] Pelanggan')
  print('[0] Keluar')

  return int(input('Pilih : '))

def halaman_user() :
  pilihan = pilihan_menu_halaman_user()
  if pilihan == 1 :
    return halaman_billing()
  elif pilihan == 2 :
    return halaman_pelanggan()
  elif pilihan == 0 :
    return aplikasi()
  else :
    print('Mohon pilih pilihan yang tersedia')
    return halaman_user()

def login_user() :
  username = input('Username : ')
  password = getpass.getpass('Password : ')
  pengguna = get('pengguna')

  for i in range(len(pengguna)) :
    if username == pengguna[i]['username'] and password == pengguna[i]['password'] :
      return True
  
  print('Username atau password tidak benar\n')
  return login_user()

# ============================================================================================================================== #

def aplikasi() :
  while True :
    print()
    print('Anda sebagai')
    print('[1] User')
    print('[2] Admin')
    print('[0] Keluar')

    pilihan = int(input('Pilih : '))
    print()

    if pilihan == 1 :
      if login_user() :
        halaman_user()
        return
    elif pilihan == 0 :
      print('\n\nBye ^^')
      return

try :
  aplikasi()
except KeyboardInterrupt :
  print('\n\nBye ^^')