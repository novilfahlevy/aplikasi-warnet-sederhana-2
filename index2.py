from prettytable import PrettyTable
import pwinput
tabel = PrettyTable()

print("==================================================")
print("                 T O K O   B A J U                ")
print("       S I S T E M   I N F O R M A S I   B        ")
print("==================================================")
print("                   KELOMPOK 7                     ")
print("   Hadi Prasetiyo                    2109116070   ")
print("   Anisa Fitri                       2109116081   ")
print("   Muhammad Indra Buana              2109116084   ")
print("==================================================")

#LOGIN ADMIN
admin = {"usernameadmin" : ["admin", "admin2"],
        "passwordadmin" : ["admin", "admin2"],
        "kesempatanadmin" : 3
    }
#LOGIN USER
user = {"username": ["iyok","ibe", "anisa"],
        "password": ["2002", "777", "123"],
        "kesempatan" : 3
    }
#LIST DIDALAM TABEL
toko={"list baju" : ["baju batik","baju polos","baju sablon"],
    "harga" : [120000, 85000, 95000],
    "stok barang" : [120, 100, 110]
    }

#PRINT TABEL
tabel.field_names = ["no","list baju","harga","stok barang"]

#INPUT DATA
def data_baju(no,bb,bp,bs):
    toko.get("no").append(no)
    toko.get("list baju").append(bb)
    toko.get("harga").append(bp)
    toko.get("stok barang").append(bs)

#UBAH DATA
def ubah_data(cariin,bpw,sbw):
    toko.get("harga")[cariin]=bpw
    toko.get("stok barang")[cariin]=sbw

#BUAT DATA
def btable():
    tabel.clear_rows()
    for i in range(len(toko.get("list baju"))):
        tabel.add_row([i+1,toko.get("list baju")[i],toko.get("harga")[i],toko.get("stok barang")[i]])

#HAPUS DATA
def hapusdatabaju(hapusbaju):
  toko.get("list baju").pop(hapusbaju)
  toko.get("harga").pop(hapusbaju)
  toko.get("stok barang").pop(hapusbaju)

#MENU LOGIN
def pilih_login():
    print("""
    ===============================
    == SILAHKAN PILIH MENU LOGIN ==
    ===============================
    | 1. Karyawan                 |
    | 2. Pelanggan                |
    | 3. Buat Akun                |
    | 4. EXIT                     |
    ===============================
    """)

#MENU MEMBUAT AKUN
def menubuatakun():
    print("""
    =============================
    ====== PILIH TIPE AKUN ======
    =============================
    |  1. Karyawan              |
    |  2. Pelanggan             |
    |  3. KEMBALI KE MENU LOGIN |
    =============================
    """)

#MENU USER
def menuuser():
    print("""
    =========================================
    ============ SELAMAT DATANG =============
    ============== TOKO BAJU ================
    ======= TERKECE TERKEREN DI DUNIA =======
    =========================================
    | 1. TAMPILKAN STOK                      |
    | 2. PILIH BAJU YANG INGIN DIBELI        |
    | 3. KEMBALI KE MENU LOGIN               |
    =========================================
    """)

#MENU ADMIN
def menuadmin():
    print("""
    ===============================
    ====== SELAMAT BEKERJA ========
    ===============================
    | 1. TAMPILKAN STOK BAJU      |
    | 2. INPUT BAJU               |
    | 3. UBAH HARGA DAN STOK BAJU |
    | 4. HAPUS                    |
    | 5. KEMBALI KE MENU LOGIN    |
    ===============================
    """)


while True :
    try :
        pilih_login()
        while True:
            try:  
                choose=int(input("Silahkan Pilih Menu Login : ")) # PILIH LOGIN
                if choose>4:
                    print("Pilihan tidak tersedia, masukkan pilihan yang tersedia")
                break
            except:
                print("Masukkan Angka")
                
        #LOGIN ADMIN
        if choose == 1 :
            usernameadmin = input ("Masukkan Username : ") # MASUKKAN USERNAME, AKAN MENGULANG JIKA USERNAME ATAU PASSWORD SALAH
            passwordadmin = pwinput.pwinput("Masukkan Password : ") # MASUKKAN PASSWORD, AKAN MENGULANG JIKA USERNAME ATAU PASSWORD SALAH
            search = admin.get("usernameadmin").index(usernameadmin)
            if admin.get("usernameadmin")[search] == usernameadmin and admin.get("passwordadmin")[search] == passwordadmin and admin["kesempatanadmin"] >0: 
                print("Login Berhasil")
                aplikasi_adminberjalan = True
                while aplikasi_adminberjalan:
                    menuadmin()
                    btable()
                    while True:
                        try:  
                            select=int(input("Silahkan Pilih Menu :"))
                            if select>5:
                                print("Pilihan tidak tersedia, masukkan pilihan yang tersedia")
                            break
                        except:
                            print("Masukkan Angka")
                    
                    if select == 1: # JIKA DIPILIH 1, MAKA AKAN MENAMPILKAN STOK BAJU
                        btable()
                        print(tabel)

                    elif select == 2: # JIKA DIPILIH 2, MAKA AKAN MENAMBAHKAN BAJU
                        while True:
                            while True:
                                try:
                                    bb=str(input("Nama baju : "))
                                    cariin = toko.get("list baju").index(bb) 
                                    print("Maaf baju telah terdaftar")
                                except :
                                    break
                            cek=0
                            while True:
                                if bb=="":
                                    print("masukkan nama baju")
                                    cek=0
                                    bb=input("Nama baju : ")
                                elif bb[cek]==" ":
                                    print("masukkan huruf didepan")
                                    cek=0
                                    bb=input("Nama baju : ")
                                elif bb[cek]!=" ":
                                    break
                                elif cek>=len(bb)-1:
                                    cek=0
                                    bb=input("Nama baju : ")
                                else:
                                    cek+=1
                            if all(namabaju.isalpha() or namabaju.isspace() or namabaju.isnumeric()  for namabaju in bb):
                                
                                while True:
                                    try:
                                        bp= int(input("Harga : "))
                                        if bp>=0:
                                            break
                                        else:
                                            print("masukkan dengan benar")
                                    except:
                                        print("Masukkan Angka")

                                while True:
                                    try:
                                        bs= int(input ("Stok Barang : "))
                                        if bs>=0:
                                            break
                                        else:
                                            print("masukkan dengan benar")
                                    except:
                                        print("Masukkan Angka")

                            toko.get("list baju").append(bb)
                            toko.get("harga").append(bp)
                            toko.get("stok barang").append(bs)
                            no = len(toko.get("list baju"))
                            tabel.add_row([no,bb,bp,bs])
                            print(tabel)
                            break
                    
                    elif select == 3: # JIKA DIPILIH 3, MAKA AKAN MENGUBAH HARGA DAN STOK BAJU
                        btable()
                        print(tabel)
                        while True:
                            ub = int(input("No. Baju yang ingin diubah : "))
                            if ub>0:
                                break
                            else:
                                print("angka yang anda masukkan 0/minus")
                        while True:
                            try:
                                bpw = int(input("Masukkan harga baju terbaru : "))
                                if bpw>=0:    
                                    break
                                else:
                                     print("masukkan dengan benar")
                            except:
                                print("Masukkan Angka")
                        while True:
                            try:
                                sbw = int(input("Masukkan stok baju terbaru : "))
                                if sbw>=0:
                                    break
                                else:
                                     print("masukkan dengan benar")
                            except:
                                print("Masukkan Angka")
                        
                        print()
                        ubah_data(ub-1,bpw,sbw)
                        btable()
                        print(tabel)

                    elif select == 4: # JIKA DIPILIH 4, MAKA AKAN MENGHAPUS STOK BAJU, YANG DIHAPUS SESUAI URUTAN
                        btable()
                        print(tabel)
                        while True:
                            hb = int(input("No. Baju yang ingin dihapus : "))
                            if hb>0:
                                break
                            else:
                                print("angka yang anda masukkan 0/minus")
                        
                        print()
                        hapusdatabaju(hb-1)
                        btable()
                        print(tabel)

                    elif select == 5 : # JIKA DIPILIH 5, MAKA PROGRAM AKAN BERHENTI
                        print("Terima Kasih")
                        break
            
            else :
                print("login gagal, Password anda salah")
                wrong = admin["kesempatanadmin"] - 1
                admin["kesempatanadmin"] = wrong
                print("kesempatan anda login sisa :", admin["kesempatanadmin"])

        #LOGIN USER
        elif choose == 2 :
            username = input ("Masukkan Username : ") # MASUKKAN USERNAME, AKAN MENGULANG JIKA USERNAME ATAU PASSWORD SALAH
            password = pwinput.pwinput("Masukkan Password : ") # MASUKKAN PASSWORD, AKAN MENGULANG JIKA USERNAME ATAU PASSWORD SALAH
            cariin = user.get("username").index(username)
            if user.get("username")[cariin] == username and user.get("password")[cariin] == password and user["kesempatan"] >0: 
                print("Login Berhasil")
                aplikasi_userberjalan = True
                while aplikasi_userberjalan:
                    menuuser()
                    btable()
                    while True:
                        try:  
                            pilih=int(input("Pilih Menu : ")) # PILIH INPUT MENU
                            if pilih>3:
                                print("Pilihan tidak tersedia, masukkan pilihan yang tersedia")
                            break
                        except:
                            print("Masukkan Angka")
                        
                    if pilih == 1: # JIKA DIPILIH 1, MAKA AKAN MENAMPILKAN STOK BAJU
                        btable()
                        print(tabel)

                    elif pilih == 2: # JIKA PILIH 2, MAKA AKAN MEMBELI BAJU
                        tabel_hasil = PrettyTable()
                        tabel_hasil.field_names = ["baju", "harga", "jumlah baju", "jumlah total"]

                        baju = toko.get("list baju")
                        total = 0

                        btable()
                        print(tabel)

                        for index_baju in range(len(baju)) :
                            while True:
                                try:
                                    while True:
                                        jumlah = int (input (f"Masukkan Jumlah {baju[index_baju]} yang ingin dibeli = "))
                                        if jumlah>=0:
                                            break
                                        else:
                                            print("Masukkan stok dengan benar")
                                    if toko["stok barang"][index_baju] >= jumlah :
                                        harga = toko.get("harga")[index_baju]
                                        total_harga = harga * jumlah

                                        tabel_hasil.add_row([baju[index_baju], harga, jumlah, total_harga])
                                        total = total + total_harga

                                        toko["stok barang"][index_baju] = toko["stok barang"][index_baju] - jumlah
                                        break
                                    else :
                                        print("Stok Baju Tidak Cukup")
                                except:
                                    print("Masukkan Angka")
                            
                        print(tabel_hasil)

                        if total>500000 :
                            total = total - total*0.05
                            print("Jumlah yang harus dibayarkan : ", "Rp.", total)
                        else :
                            print("Jumlah yang harus dibayarkan : ", "Rp.", total)

                        print("Bayar")
                        while True:
                            try:
                                Bayar = int(input("Masukkan Jumlah Nominal Uang :"))
                                if Bayar > total and Bayar>=0:
                                    Kembalian = Bayar - total
                                    print("Kembalian anda", "Rp.", Kembalian)
                                    print("Terima Kasih Telah Berbelanja")
                                    break
                                else:
                                    print("Maaf uang anda tidak cukup, Silahkan masukkan ulang nominal uang anda")   
                            except :
                                print("Masukkan Angka")

                    elif pilih == 3 : # JIKA DIPILIH 3, MAKA PROGRAM AKAN KEMBALI KE MENU LOGIN
                        print("Terima Kasih")
                        break
            
            else :
                print("login gagal, Password anda salah")
                salah = user["kesempatan"] - 1
                user["kesempatan"] = salah
                print("kesempatan anda login sisa :", user["kesempatan"])

        #REGISTER
        elif choose == 3: 
            menubuatakun()
            while True:
                try:
                    buat_akun = int(input("Pilih tipe akun yang ingin dibuat   : "))
                    if buat_akun>3:
                        print("Maaf pilihan tidak tersedia, masukkan pilihan yang tersedia")
                    break
                except:
                    print("Masukkan Angka")
            
            #REGISTER AKUN ADMIN
            if buat_akun == 1 :
                while True:  
                    akunkaryawanbaru = input("Masukkan Username Admin Yang Anda Inginkan : ")
                    if akunkaryawanbaru in admin.get("usernameadmin"):
                        print("Maaf Username Yang Anda Pilih Sudah Terdaftar\nSilahkan Masukkan Username Yang Lain")
                        break
                    else:
                        passwordkaryawanbaru = pwinput.pwinput("Masukkan password yang anda inginkan : ")
                        admin.get("usernameadmin").append(akunkaryawanbaru)
                        admin.get("passwordadmin").append(passwordkaryawanbaru)
                        print("Anda Telah Berhasil Register !")
                        print("Silahkan Coba Akun Baru")
                        break
            
            #REGISTER AKUN USER
            elif buat_akun == 2:
                while True:
                    akunpelangganbaru = input("Masukkan Username Pelanggan Yang Anda Inginkan : ")
                    if akunpelangganbaru in user.get("username"):
                        print("Maaf Username Yang Anda Pilih Sudah Terdaftar\nSilahkan Masukkan Username Yang Lain")
                        break
                    else:
                        passwordpelangganbaru = pwinput.pwinput("Masukkan password yang anda inginkan : ")
                        user.get("username").append(akunpelangganbaru)
                        user.get("password").append(passwordpelangganbaru)
                        print("Anda Telah Berhasil Register !")
                        print("Silahkan Coba Akun Baru")
                        break
            
            #KEMBALI KE MENU LOGIN
            elif buat_akun == 3:
                print("Terima Kasih")
        
        #KELUAR DARI PROGRAM
        elif choose == 4:
            print("===> Terima Kasih Telah Berbelanja <===")
            print(" ===> SEMOGA HARIMU MENYENANGKAN <===")
            exit()
    
    #JIKA SALAH MEMASUKAN USERNAME ATAU PASSWORD
    except ValueError :
        print("Maaf Pilihan atau Username Tidak Tersedia")