from prettytable import PrettyTable
from datetime import date, datetime, timedelta
from termcolor import colored
import platform
import pwinput
import json
import csv
import os

if platform.system() == 'windows' :
  os.system('color')

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
  return data_db[0]['id'] if len(data_db) > 0 else 0

def create(field, data) :
  data_db = get()
  data_db[field] = get(field)

  data['id'] = get_last_id(field) + 1
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

def get_user_by_role(role) :
  return list(filter(lambda user: user['role'] == role, get('user')))

# ============================================================================================================================== #

def cek_billing_masih_berlaku(id_billing) :
  billing = get_by_id('billing', id_billing)
  tanggal = billing['tanggal']
  waktu_selesai = billing['waktu_selesai']

  return f'{tanggal} {waktu_selesai}' > f'{tanggal_sekarang()} {waktu_sekarang()}'

def hapus_billing(pesan_error = False) :
  tampilkan_billing()

  if pesan_error :
    print(pesan_error)

  id_billing = int(input('ID : '))
  billing = get_by_id('billing', id_billing)

  if billing :
    delete('billing', id_billing)
    tampilkan_billing()
    print(colored(f'billing dengan ID {id_billing} berhasil dihapus', 'green'))
  else :
    return hapus_billing(colored('ID billing tidak ditemukan', 'red'))

def edit_billing(pesan_error = False) :
  print()
  tampilkan_billing()

  if pesan_error :
    print(pesan_error)

  try :
    id_billing = int(input('ID billing : '))
    billing = get_by_id('billing', id_billing)
  except ValueError :
    return edit_billing(colored('ID billing tidak ditemukan', 'red'))

  if billing :
    member = get_by_id('member', billing['id_member'])
    id_member = member['id']

    pc_lama = get_by_id('pc', billing['id_pc'])
    id_pc_lama = pc_lama['id']
    label_pc_lama = pc_lama['label']

    try :
      id_pc = input(f'ID PC ({label_pc_lama}) : ') or id_pc_lama
      id_pc = int(id_pc)
      pc = get_by_id('pc', id_pc)

      if cek_pc_masih_dipakai(id_pc) and (id_pc != id_pc_lama) :
        return tambah_billing(colored('PC masih dipakai', 'red'))
    except ValueError :
      return edit_billing(colored('ID PC tidak ditemukan', 'red'))

    if pc :
      tanggal = tanggal_sekarang()
      waktu_mulai_lama = billing['waktu_mulai']
      waktu_selesai_lama = billing['waktu_selesai']
      waktu_mulai = input(f'Waktu mulai ({waktu_mulai_lama}) : ') or waktu_mulai_lama
      waktu_selesai = input(f'Waktu selesai ({waktu_selesai_lama}) : ') or waktu_selesai_lama

      try :
        harga_perjam = pengaturan("harga_perjam")
        durasi = datetime.strptime(waktu_selesai, '%H:%M') - datetime.strptime(waktu_mulai, '%H:%M')
        total_harga = int(harga_perjam * int(durasi.seconds / 3600))
      except ValueError :
        return edit_billing(colored('Format waktu tidak tepat', 'red'))

      update('billing', {
        'id': id_billing,
        'data': {
          'id_pc': id_pc,
          'id_member': id_member,
          'tanggal': tanggal,
          'waktu_mulai': waktu_mulai,
          'waktu_selesai': waktu_selesai,
          'harga': harga_perjam,
          'total_harga': total_harga
        }
      })
      
      tampilkan_billing()
      print(colored(f'Billing dengan ID {id_billing} telah edit', 'green'))
    else :
      return edit_billing(colored('ID PC tidak ditemukan', 'red'))
  else :
    return edit_billing(colored('ID billing tidak ditemukan', 'red'))

def tambah_billing(pesan_error = False) :
  print()
  tampilkan_member()

  if pesan_error :
    print(pesan_error)

  try :
    id_member = int(input('ID member : '))
  except ValueError :
    return tambah_billing(colored('ID member tidak ditemukan', 'red'))
  
  try :
    id_pc = int(input('ID PC : '))

    if cek_pc_masih_dipakai(id_pc) :
      return tambah_billing(colored('PC masih dipakai'))
  except ValueError :
    return tambah_billing(colored('ID PC tidak ditemukan', 'red'))

  if get_by_id('member', id_member) and get_by_id('pc', id_pc) :
    try :
      durasi = int(input('Durasi (jam) : '))
    except ValueError :
      return tambah_billing(colored('Masukan durasi berdasarkan jam', 'red'))

    waktu_mulai = datetime.now()
    waktu_selesai = waktu_mulai + timedelta(hours=durasi)
    tanggal = tanggal_sekarang()

    waktu_mulai = waktu_mulai.strftime('%H:%M')
    waktu_selesai = waktu_selesai.strftime('%H:%M')

    harga_perjam = pengaturan("harga_perjam")
    total_harga = harga_perjam * int((datetime.strptime(waktu_selesai, '%H:%M') - datetime.strptime(waktu_mulai, '%H:%M')).seconds / 3600)

    create('billing', {
      'id_pc': id_pc,
      'id_member': id_member,
      'tanggal': tanggal,
      'waktu_mulai': waktu_mulai,
      'waktu_selesai': waktu_selesai,
      'harga': harga_perjam,
      'total_harga': total_harga
    })

    tampilkan_billing()
    print(colored('Billing telah ditambahkan', 'green'))
  else :
    return tambah_billing(colored('ID member tidak ditemukan', 'red'))

def data_billing(billing, color = True) :
  data = []

  for i in range(len(billing)) :
    id_billing = billing[i]['id']
    member = get_by_id('member', billing[i]['id_member'])
    pc = get_by_id('pc', billing[i]['id_pc'])
    waktu_mulai = billing[i]['waktu_mulai']
    waktu_selesai = billing[i]['waktu_selesai']
    harga = billing[i]['harga']
    durasi = datetime.strptime(waktu_selesai, '%H:%M') - datetime.strptime(waktu_mulai, '%H:%M')
    total_harga = int(billing[i]['harga'] * (durasi.seconds / 3600))

    data.append([
      id_billing,
      pc['label'] if pc else colored('[PC Telah Terhapus]', 'yellow'),
      member['nama'] if member else colored('[Member Telah Terhapus]', 'yellow'),
      billing[i]['tanggal'],
      f'{waktu_mulai} - {waktu_selesai}',
      durasi,
      f"Rp {'{:0,.0f}'.format(harga)}",
      f"Rp {'{:0,.0f}'.format(total_harga)}",
      (colored('Masih Berlaku', 'green') if color else 'Masih Berlaku') if cek_billing_masih_berlaku(id_billing) else 'Selesai'
    ])

  return data

def tampilkan_billing() :
  print()
  print('Daftar Billing :')

  tabel = PrettyTable()
  tabel.field_names = ['ID', 'PC', 'Nama member', 'Tanggal', 'Waktu', 'Durasi (jam)', 'Harga', 'Total Harga', 'Status']

  billing = get('billing')
  tabel.add_rows(data_billing(billing))

  print(tabel)

def pilihan_menu_halaman_billing(tampilkan_menu = True) :
  try :
    print()
    if tampilkan_menu :
      print('== Menu Billing ==')
      print('[1] Tampilkan billing')
      print('[2] Tambah billing')
      print('[3] Edit billing')
      print('[4] Hapus billing')
      print('[0] Kembali')
    
    pilihan = int(input('Pilih (pilih 99 untuk menampilkan menu) : '))

    if pilihan == 99 :
      return pilihan_menu_halaman_billing()

    return pilihan
  except ValueError :
    print(colored('Pilihan tidak tersedia', 'red'))
    return pilihan_menu_halaman_billing()

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
    return halaman_operator()
  else :
    print(colored('Pilihan tidak ditemukan', 'red'))
    return halaman_billing()

# ============================================================================================================================== #

def hapus_member(pesan_error = False) :
  tampilkan_member()

  if pesan_error :
    print(pesan_error)  

  id_member = int(input('ID : '))
  member = get_by_id('member', id_member)

  if member :
    delete('member', id_member)
    tampilkan_member()
    print(colored(f'member dengan ID {id_member} berhasil dihapus', 'green'))
  else :
    return hapus_member(colored('ID member tidak ditemukan', 'red'))

def edit_member(pesan_error = False) :
  tampilkan_member()

  if pesan_error :
    print(pesan_error)

  id_member = int(input('ID : '))
  member = get_by_id('member', id_member)

  if member :
    nama_lama = member['nama']
    nama = input(f'Nama ({nama_lama}) : ') or nama_lama

    update('member', {
      'id': id_member,
      'data': { 'nama': nama }
    })

    tampilkan_member()
    print(colored(f'Member dengan ID {id_member} telah diedit', 'green'))
  else :
    return edit_member(colored('ID member tidak ditemukan', 'red'))

def tambah_member() :
  print()

  nama = input('Nama : ')
  tanggal_bergabung = tanggal_sekarang()

  create('member', { 'nama': nama, 'tanggal_bergabung': tanggal_bergabung })
  tampilkan_member()
  print(colored('Member telah ditambahkan', 'green'))

def tampilkan_member() :
  print()
  print('Daftar member :')

  tabel = PrettyTable()
  tabel.field_names = ['ID', 'Nama', 'Tanggal Bergabung']

  member = get('member')
  for i in range(len(member)) :
    tabel.add_row([
      member[i]['id'],
      member[i]['nama'],
      member[i]['tanggal_bergabung']
    ])

  print(tabel)

def pilihan_menu_halaman_member(tampilkan_menu = True) :
  try :
    print()
    if tampilkan_menu :
      print('== Menu Member ==')
      print('[1] Tampilkan member')
      print('[2] Tambah member')
      print('[3] Edit member')
      print('[4] Hapus member')
      print('[0] Kembali')
    
    pilihan = int(input('Pilih (99 untuk menampilkan menu) : '))

    if pilihan == 99 :
      return pilihan_menu_halaman_member()
    
    return pilihan
  except ValueError :
    print(colored('Pilihan tidak tersedia', 'red'))
    return pilihan_menu_halaman_member()

def halaman_member(tampilkan_menu = True) :
  pilihan = pilihan_menu_halaman_member(tampilkan_menu)
  if pilihan == 1 :
    tampilkan_member()
    return halaman_member(False)
  elif pilihan == 2 :
    tambah_member()
    return halaman_member(False)
  elif pilihan == 3 :
    edit_member()
    return halaman_member(False)
  elif pilihan == 4 :
    hapus_member()
    return halaman_member(False)
  elif pilihan == 0 :
    return halaman_operator()
  else :
    print(colored('Pilihan tidak tersedia', 'red'))
    return halaman_member()

# ============================================================================================================================== #

def pilihan_menu_halaman_operator() :
  try :
    print()
    print('== Halaman Operator ==')
    print('[1] Billing')
    print('[2] Member')
    print('[0] Keluar')

    piilhan = int(input('Pilih : '))
    return piilhan
  except ValueError :
    print(colored('Pilihan tidak tersedia', 'red'))
    return pilihan_menu_halaman_operator()

def halaman_operator() :
  try :
    pilihan = pilihan_menu_halaman_operator()
    if pilihan == 1 :
      return halaman_billing()
    elif pilihan == 2 :
      return halaman_member()
    elif pilihan == 0 :
      return aplikasi()
    else :
      print(colored('Pilihan tidak tersedia', 'red'))
      return halaman_operator()
  except KeyboardInterrupt :
    print()
    return halaman_operator()

def login_operator() :
  print()
  
  try :
    username = input('Username: ')
    password = pwinput.pwinput(mask='*')
    operator = get_user_by_role('operator')
  except KeyboardInterrupt :
    return aplikasi()

  for i in range(len(operator)) :
    if username == operator[i]['username'] and password == operator[i]['password'] :
      return True
  
  print(colored('Username atau password tidak benar', 'red'))
  return login_operator()

# ============================================================================================================================== #

def cek_pc_masih_dipakai(id_pc) :
  billing_dengan_pc_ini = list(filter(lambda b: b['id_pc'] == id_pc, get('billing')))
  for i in range(len(billing_dengan_pc_ini)) :
    if cek_billing_masih_berlaku(billing_dengan_pc_ini[i]['id']) :
      return True
  
  return False

def hapus_pc(pesan_error = False) :
  tampilkan_pc()

  if pesan_error :
    print(pesan_error)  

  id_pc = int(input('ID : '))
  pc = get_by_id('pc', id_pc)

  if pc :
    delete('pc', id_pc)
    tampilkan_pc()
    print(colored(f'PC dengan ID {id_pc} berhasil dihapus', 'green'))
  else :
    return hapus_pc(colored('ID pc tidak ditemukan', 'red'))

def edit_pc(pesan_error = False) :
  tampilkan_pc()

  if pesan_error :
    print(pesan_error)

  id_pc = int(input('ID : '))
  pc = get_by_id('pc', id_pc)

  if pc :
    label_lama = pc['label']
    label = input(f'label ({label_lama}) : ') or label_lama

    update('pc', {
      'id': id_pc,
      'data': { 'label': label }
    })

    tampilkan_pc()
    print(colored(f'PC dengan ID {id_pc} telah diedit', 'green'))
  else :
    return edit_pc(colored('ID pc tidak ditemukan', 'red'))

def tambah_pc() :
  print()

  label = input('Label PC : ')

  create('pc', { 'label': label })
  tampilkan_pc()
  print(colored('PC telah ditambahkan', 'green'))

def tampilkan_pc() :
  print()
  print('Daftar pc :')

  tabel = PrettyTable()
  tabel.field_names = ['ID', 'Label', 'Status']

  pcs = get('pc')
  for i in range(len(pcs)) :
    tabel.add_row([
      pcs[i]['id'],
      pcs[i]['label'],
      colored('Masih Dipakai', 'yellow') if cek_pc_masih_dipakai(pcs[i]['id']) else 'Kosong'
    ])

  print(tabel)

def pilihan_menu_halaman_pc(tampilkan_menu = True) :
  try :
    print()
    if tampilkan_menu :
      print('== Menu PC ==')
      print('[1] Tampilkan pc')
      print('[2] Tambah pc')
      print('[3] Edit pc')
      print('[4] Hapus pc')
      print('[0] Kembali')
    
    pilihan = int(input('Pilih (99 untuk menampilkan menu) : '))

    if pilihan == 99 :
      return pilihan_menu_halaman_pc()
    
    return pilihan
  except ValueError :
    print(colored('Pilihan tidak tersedia', 'red'))
    return pilihan_menu_halaman_pc()

def halaman_pc(tampilkan_menu = True) :
  pilihan = pilihan_menu_halaman_pc(tampilkan_menu)
  if pilihan == 1 :
    tampilkan_pc()
    return halaman_pc(False)
  elif pilihan == 2 :
    tambah_pc()
    return halaman_pc(False)
  elif pilihan == 3 :
    edit_pc()
    return halaman_pc(False)
  elif pilihan == 4 :
    hapus_pc()
    return halaman_pc(False)
  elif pilihan == 0 :
    return halaman_admin()
  else :
    print(colored('Pilihan tidak tersedia', 'red'))
    return halaman_pc()

# ============================================================================================================================== #

def hapus_user(pesan_error = False) :
  tampilkan_user(role='operator')

  if pesan_error :
    print(pesan_error)

  id_user = int(input('ID : '))
  user = get_by_id('user', id_user)

  if user and user['role'] != 'admin' :
    delete('user', id_user)
    tampilkan_user()
    print(colored(f'User dengan ID {id_user} berhasil dihapus', 'green'))
  else :
    return hapus_user(colored('ID user tidak ditemukan', 'red'))

def tambah_user() :
  print()

  username = input('Username: ')
  password = pwinput.pwinput(mask="*")
  role = input('Role (admin/operator): ').lower()

  if role not in ['admin', 'operator'] :
    print(colored('Role tidak sesuai', 'red'))
    return tambah_user()

  create('user', { 'username': username, 'password': password, 'role': role })
  tampilkan_user()
  print(colored('User telah ditambahkan', 'green'))

def tampilkan_user(role=None) :
  print()
  print('Daftar user :')

  tabel = PrettyTable()
  tabel.field_names = ['ID', 'Username', 'Role']

  users = get('user')
  for i in range(len(users)) :
    if role != None :
      if users[i]['role'] == role :
        tabel.add_row([users[i]['id'], users[i]['username'], users[i]['role']])
    else :
      tabel.add_row([users[i]['id'], users[i]['username'], users[i]['role']])

  print(tabel)

def pilihan_menu_halaman_user(tampilkan_menu = True) :
  try :
    print()
    if tampilkan_menu :
      print('== Menu User ==')
      print('[1] Tampilkan user')
      print('[2] Tambah user')
      print('[3] Hapus user')
      print('[0] Kembali')
    
    pilihan = int(input('Pilih (99 untuk menampilkan menu) : '))

    if pilihan == 99 :
      return pilihan_menu_halaman_user()
    
    return pilihan
  except ValueError :
    print(colored('Pilihan tidak tersedia', 'red'))
    return pilihan_menu_halaman_user()

def halaman_user(tampilkan_menu = True) :
  pilihan = pilihan_menu_halaman_user(tampilkan_menu)
  if pilihan == 1 :
    tampilkan_user()
    return halaman_user(False)
  elif pilihan == 2 :
    tambah_user()
    return halaman_user(False)
  elif pilihan == 3 :
    hapus_user()
    return halaman_user(False)
  elif pilihan == 0 :
    return halaman_admin()
  else :
    print(colored('Pilihan tidak tersedia', 'red'))
    return halaman_user()

# ============================================================================================================================== #

def laporan_csv() :
  billing = get('billing')

  dari_tanggal = input('Dari tanggal [dd-mm-yyyy] (opsional) : ')
  if dari_tanggal != '' :
    try:
      datetime.strptime(dari_tanggal, "%d-%m-%Y")
    except ValueError :
      print(colored('Format tanggal tidak tepat', 'red'))
      return laporan_csv()
  
  sampai_tanggal = input('Sampai tanggal [dd-mm-yyyy] (opsional) : ')
  if sampai_tanggal != '' :
    try:
      datetime.strptime(sampai_tanggal, "%d-%m-%Y")
    except ValueError or EOFError :
      print(colored('Format tanggal tidak tepat', 'red'))
      return laporan_csv()

  if dari_tanggal == '' and sampai_tanggal != '' :
    billing = list(filter(lambda b: b['tanggal'] <= sampai_tanggal, billing))
  elif dari_tanggal != '' and sampai_tanggal == '' :
    billing = list(filter(lambda b: b['tanggal'] >= dari_tanggal, billing))
  elif dari_tanggal != '' and sampai_tanggal != '' :
    billing = list(filter(lambda b: b['tanggal'] >= dari_tanggal and b['tanggal'] <= sampai_tanggal, billing))

  # sumber https://www.pythontutorial.net/python-basics/python-write-csv-file/
  with open('siwarnet_laporan.csv', 'w') as f :
    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    writer.writerows(data_billing(billing, color=False))

  print()
  print(colored(f'Laporan telah tersimpan di {colored(os.path.dirname(os.path.abspath(__file__)) + "/siwarnet_laporan.csv", "yellow")}', 'green'))
  return halaman_admin()

# ============================================================================================================================= #

def pengaturan(nama_pengaturan) :
  return get('pengaturan')[0][nama_pengaturan]

def pengaturan_harga_perjam() :
  try :
    harga_lama = pengaturan("harga_perjam")
    harga = input(f'Harga perjam (Rp {"{:0,.0f}".format(harga_lama)}) : ') or harga_lama
    harga = int(harga)

    update('pengaturan', {
      'id': 1,
      'data': { 'harga_perjam': harga }
    })

    print(colored('Pengaturan harga perjam berhasil diubah', 'green'))
    return halaman_pengaturan()
  except ValueError :
    print(colored('Input tidak valid', 'red'))
    return pengaturan_harga_perjam()

def pilihan_menu_halaman_pengaturan() :
  try :
    print()
    print('== Pengaturan ==')
    print(f'[1] Harga Perjam (Rp {"{:0,.0f}".format(pengaturan("harga_perjam"))})')
    print('[0] Kembali')

    piilhan = int(input('Pilih : '))
    return piilhan
  except ValueError :
    print(colored('Pilihan tidak tersedia', 'red'))
    return pilihan_menu_halaman_pengaturan()

def halaman_pengaturan() :
  try :
    pilihan = pilihan_menu_halaman_pengaturan()
    if pilihan == 1 :
      return pengaturan_harga_perjam()
    elif pilihan == 0 :
      return halaman_admin()
    else :
      print(colored('Pilihan tidak tersedia', 'red'))
      return halaman_pengaturan()
  except KeyboardInterrupt :
    print()
    return halaman_admin()

# ============================================================================================================================== #

def pilihan_menu_halaman_admin() :
  try :
    print()
    print('== Halaman Admin ==')
    print('[1] PC')
    print('[2] User')
    print('[3] Pengaturan')
    print('[4] Laporan CSV')
    print('[0] Keluar')

    piilhan = int(input('Pilih : '))
    return piilhan
  except ValueError :
    print(colored('Pilihan tidak tersedia', 'red'))
    return pilihan_menu_halaman_admin()

def halaman_admin() :
  try :
    pilihan = pilihan_menu_halaman_admin()
    if pilihan == 1 :
      return halaman_pc()
    elif pilihan == 2 :
      return halaman_user()
    elif pilihan == 3 :
      return halaman_pengaturan()
    elif pilihan == 4 :
      return laporan_csv()
    elif pilihan == 0 :
      return aplikasi()
    else :
      print(colored('Pilihan tidak tersedia', 'red'))
      return halaman_admin()
  except KeyboardInterrupt :
    print()
    return halaman_admin()

def login_admin() :
  print()
  
  try :
    username = input('Username: ')
    password = pwinput.pwinput(mask='*')
    operator = get_user_by_role('admin')
  except KeyboardInterrupt :
    return aplikasi()

  for i in range(len(operator)) :
    if username == operator[i]['username'] and password == operator[i]['password'] :
      return True
  
  print(colored('Username atau password tidak benar', 'red'))
  return login_admin()

# ============================================================================================================================== #

def aplikasi() :
  while True :
    print()
    print('Anda sebagai')
    print('[1] Operator')
    print('[2] Admin')
    print('[0] Keluar')

    try :
      pilihan = int(input('Pilih : '))
    except ValueError :
      print(colored('Pilihan tidak tersedia', 'red'))
      return aplikasi()

    try :
      if pilihan == 1 :
        if login_operator() :
          halaman_operator()
          return
      elif pilihan == 2 :
        if login_admin() :
          halaman_admin()
          return
      elif pilihan == 0 :
        print('\n\nBye ^^')
        return
      else :
        print(colored('Pilihan tidak tersedia', 'red'))
    except KeyboardInterrupt :
      return aplikasi()

try :
  buat_file_database_json({
    "user": [
      {"id": 1, "username": "admin", "password": "admin", "role": "admin"},
      {"id": 3, "username": "op", "password": "op", "role": "operator"}
    ],
    "member": [
      { "id": 1, "nama": "Novil", "tanggal_bergabung": tanggal_sekarang() },
      { "id": 2, "nama": "Rizki Perdana", "tanggal_bergabung": tanggal_sekarang() },
      { "id": 3, "nama": "Ibnu Praditya", "tanggal_bergabung": tanggal_sekarang() },
    ],
    "billing": [
      {
        "id": 1,
        "id_member": 2,
        "id_pc": 1,
        "tanggal": tanggal_sekarang(),
        "waktu_mulai": '13:00',
        "waktu_selesai": '14:00',
        "harga": 8000,
        'total_harga': 8000
      },
    ],
    "pc": [
      { "id": 1, "label": "PC 1" }
    ],
    "pengaturan": [
      { "id": 1, "harga_perjam": 8000 }
    ]
  })
  aplikasi()
except KeyboardInterrupt :
  print('\n\nBye ^^')