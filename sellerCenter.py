# IMPORT
from os import system
from datetime import datetime
import re
import mysql.connector
import random

# DATABASE
sellerCenter = mysql.connector.connect(host="localhost", username="root", password="", database="seller_center")
cursorSC = sellerCenter.cursor(buffered=True)

indonesia = mysql.connector.connect(host="localhost", username="root", password="", database="indonesia")
cursorI = indonesia.cursor(buffered=True)

courier = mysql.connector.connect(host="localhost", username="root", password="", database="courier")
cursorC = courier.cursor(buffered=True)

# CLASS
class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class Penjual:
    def __init__(self, email, namaToko, noTelp):
        self.email = email
        self.namaToko = namaToko
        self.alamat = Alamat
        self.noTelp = noTelp
        self.ratingToko = 0.0
        self.saldo = 0
        self.statusToko = "Buka"

    def setAlamat(self, alamat):
        self.alamat = alamat

    def tambahAlamat(self, alamat):
        self.alamat = alamat
        query = "INSERT INTO alamat (Email, Jenis, Provinsi, Kabupaten, Kecamatan, Kelurahan, Alamat, KodePos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        value = (self.email, "penjual", self.alamat.provinsi, self.alamat.kabupaten,
                 self.alamat.kecamatan, self.alamat.kelurahan, self.alamat.alamat, self.alamat.kodePos)
        cursorSC.execute(query, value)
        sellerCenter.commit()

    def updateStatus(self):
        query = "UPDATE penjual SET StatusToko = %s WHERE Email = %s"
        value = (self.statusToko, self.email)
        cursorSC.execute(query, value)
        sellerCenter.commit()

    def bukaToko(self):
        self.statusToko = "Buka"
        self.updateStatus()
        print("\nToko telah dibuka.")
        input()

    def tutupToko(self):
        self.statusToko = "Tutup"
        self.updateStatus()
        print("\nToko telah ditutup.")
        input()

class Alamat:
    def __init__(self, email, provinsi, kabupaten, kecamatan, kelurahan, alamat, kodePos):
        self.email = email
        self.provinsi = provinsi
        self.kabupaten = kabupaten
        self.kecamatan = kecamatan
        self.kelurahan = kelurahan
        self.alamat = alamat
        self.kodePos = kodePos

class Produk:
    def __init__(self, email, namaProduk, kodeProduk, harga, berat, kategori, deskripsi, stok, kondisi):
        self.email = email
        self.namaProduk = namaProduk
        self.kodeProduk = kodeProduk
        self.harga = harga
        self.berat = berat
        self.kategori = kategori
        self.deskripsi = deskripsi
        self.stok = stok
        self.rating = 0.0
        self.jumlahTerjual = 0
        self.kondisi = kondisi

    # untuk memasukkan data yang diinput ke dalam database
    def tambahProduk(self, produk):
        query = "INSERT INTO produk (Email, NamaProduk, KodeProduk, Harga, Berat, Kategori, Deskripsi, Stok, Rating, JumlahTerjual, Kondisi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        value = (self.email, produk.namaProduk, produk.kodeProduk, produk.harga, produk.berat, produk.kategori,
                 produk.deskripsi, produk.stok, produk.rating, produk.jumlahTerjual, produk.kondisi)
        cursorSC.execute(query, value)
        sellerCenter.commit()
        print("\nProduk telah berhasil ditambahkan.")
        input()

class Variasi:
    def __init__(self, kodeProduk, tipeVariasi):
        self.kodeProduk = kodeProduk
        self.tipeVariasi = tipeVariasi
        self.subVariasi = []

class SubVariasi(Variasi):
    def __init__(self, kodeProduk, tipeVariasi, subVariasi, stokSubVariasi):
        super().__init__(kodeProduk, tipeVariasi)
        self.subVariasi = subVariasi
        self.stokSubVariasi = stokSubVariasi

class Pesanan:
    def __init__(self, email, emailPembeli, noTelpPembeli, noPesanan, waktuPesanan, metodePembayaran, hargaPesanan, kurir, noResi):
        self.email = email
        self.emailPembeli = emailPembeli
        self.noTelpPembeli = noTelpPembeli
        self.alamatPembeli = Alamat
        self.noPesanan = noPesanan
        self.waktuPesanan = waktuPesanan
        self.metodePembayaran = metodePembayaran
        self.hargaPesanan = hargaPesanan
        self.kurir = kurir
        self.noResi = noResi
        self.status = "Belum Bayar"

    # alamat yang ada berdasarkan dari database yang sudah diinput, yaitu database bernama sellerCenter
    def tambahAlamatPembeli(self, alamatPembeli):
        self.alamatPembeli = alamatPembeli
        query = "INSERT INTO alamat (Email, Jenis, Provinsi, Kabupaten, Kecamatan, Kelurahan, Alamat, KodePos) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        value = (self.emailPembeli, "pembeli", self.alamatPembeli.provinsi, self.alamatPembeli.kabupaten,
                 self.alamatPembeli.kecamatan, self.alamatPembeli.kelurahan, self.alamatPembeli.alamat, self.alamatPembeli.kodePos)
        cursorSC.execute(query, value)
        sellerCenter.commit()

class ProdukPesanan:
    def __init__(self, noPesanan, kodeProduk, kuantitas, subtotal):
        self.noPesanan = noPesanan
        self.kodeProduk = kodeProduk
        self.kuantitas = kuantitas
        self.subtotal = subtotal

# FUNCTION
def detailPesanan(penjual, nomor, menu, customQuery):
    clear()
    # cari pesanan di urutan ke-nomor
    query = ""
    if customQuery != "":
        query = customQuery
    else:
        if menu == "Pesanan Masuk":
            query = "SELECT * FROM pesanan WHERE Email = '%s'" % penjual.email
        elif menu == "Menunggu Pembayaran":
            query = "SELECT * FROM pesanan WHERE Email = '%s' AND Status = '%s'" % (penjual.email, menu)
        elif menu == "Perlu Dikirim":
            query = "SELECT * FROM pesanan WHERE Email = '%s' AND Status = '%s'" % (penjual.email, menu)
        elif menu == "Dalam Perjalanan":
            query = "SELECT * FROM pesanan WHERE Email = '%s' AND Status = '%s'" % (penjual.email, menu)
        elif menu == "Pesanan Selesai":
            query = "SELECT * FROM pesanan WHERE Email = '%s' AND Status = 'Selesai'" % (penjual.email)
        elif menu == "Pesanan Batal":
            query = "SELECT * FROM pesanan WHERE Email = '%s' AND Status = 'Dibatalkan'" % (penjual.email)
    cursorSC.execute(query)
    crpsnn = cursorSC.fetchall()
    # ambil nomor pesanan 
    query = "SELECT * FROM pesanan WHERE Email = '%s' AND NoPesanan = '%s'" % (
        penjual.email, crpsnn[nomor - 1][3])
    cursorSC.execute(query)
    psnn = cursorSC.fetchone()

    print("{:23s}: {}".format("Status", psnn[15]))
    
    print("{:24s}: {}".format("\nEmail Pembeli", psnn[1]))
    print("{:23s}: {}".format("Nomor Telepon Pembeli", psnn[2]))
    
    print("{:24s}: {}".format("\nWaktu Dibuat", psnn[4]))
    psnn5, psnn6, psnn7 = "", "", ""
    if psnn[5] == None:
        psnn5 = "-"
    else:
        psnn5 = psnn[5]
    if psnn[6] == None:
        psnn6 = "-"
    else:
        psnn6 = psnn[6]
    if psnn[7] == None:
        psnn7 = "-"
    else:
        psnn7 = psnn[7]
    print("{:23s}: {}".format("Waktu Dibayar", psnn5))
    print("{:23s}: {}".format("Waktu Dikirim", psnn6))
    print("{:23s}: {}".format("Waktu Selesai", psnn7))

    print("\nProduk")
    query = "SELECT * FROM produk_pesanan WHERE NoPesanan = '%s'" % (crpsnn[nomor - 1][3])
    cursorSC.execute(query)
    prdkpsnn = cursorSC.fetchall()
    print("+%s+%s+%s+%s+%s+%s+%s+%s+%s+%s+%s+" % (("-" * 5), ("-" * 13), ("-" * 22), ("-" * 11), ("-" * 11), ("-" * 7), ("-" * 17), ("-" * 9), ("-" * 12), ("-" * 17), ("-" * 11)))
    print("| {:<3} | {:<11} | {:<20} | {:<9} | {:<9} | {:<5} | {:<15} | {:<7} | {:<10} | {:<15} | {:<9} |".format('No.', 'Kode Produk', 'Nama Produk', 'Harga', 'Kuantitas', 'Berat', 'Kategori', 'Kondisi', 'Variasi', 'Sub Variasi', 'Subtotal'))
    print("+%s+%s+%s+%s+%s+%s+%s+%s+%s+%s+%s+" % (("-" * 5), ("-" * 13), ("-" * 22), ("-" * 11), ("-" * 11), ("-" * 7), ("-" * 17), ("-" * 9), ("-" * 12), ("-" * 17), ("-" * 11)))
    for x in range(len(prdkpsnn)):
        prdkpsnn9 = ""
        if prdkpsnn[x][9] == None:
            prdkpsnn9 = "-"
        else:
            prdkpsnn9 = prdkpsnn[x][9]
        prdkpsnn10 = ""
        if prdkpsnn[x][10] == None:
            prdkpsnn10 = "-"
        else:
            prdkpsnn10 = prdkpsnn[x][10]
        print("| {:<3} | {:<11} | {:<20} | {:<9} | {:<9} | {:<5} | {:<15} | {:<7} | {:<10} | {:<15} | {:<9} |".format(x + 1, prdkpsnn[x][2], prdkpsnn[x][3][0:20], prdkpsnn[x][4], prdkpsnn[x][8], prdkpsnn[x][5], prdkpsnn[x][6][0:15], prdkpsnn[x][7], prdkpsnn9, prdkpsnn10, str(int(prdkpsnn[x][4]) * int(prdkpsnn[x][8]))))
        print("+%s+%s+%s+%s+%s+%s+%s+%s+%s+%s+%s+" % (("-" * 5), ("-" * 13), ("-" * 22), ("-" * 11), ("-" * 11), ("-" * 7), ("-" * 17), ("-" * 9), ("-" * 12), ("-" * 17), ("-" * 11)))
    

    print("{:24s}: {}".format("\nSubtotal Produk", psnn[8]))
    print("{:23s}: {}".format("Ongkos Kirim", psnn[9]))
    print("{:23s}: {}".format("Biaya Penanganan", psnn[10]))
    print("{:23s}: {}".format("Total Harga", psnn[11]))
    
    print("{:24s}: {}".format("\nKurir", psnn[13]))
    psnn14 = ""
    if psnn[14] == None:
        psnn14 = "-"
    else:
        psnn14 = psnn[14]
    print("{:23s}: {}".format("Nomor Resi", psnn14))
    
    print("{:24s}: {}".format("\nMetode Pembayaran", psnn[12]))

    print("")
    pilihan = ["Menu Utama"]
    if psnn[15] == "Perlu Dikirim":
        pilihan.append("Atur Pengiriman")
    if psnn[15] == "Menunggu Pembayaran":
        pilihan.append("Batalkan Pesanan")
    for x in range(len(pilihan)):
        print(f"{x}. {pilihan[x]}")
    pilihanMenu = int(input("Input: "))
    while pilihanMenu < 0 or pilihanMenu > len(pilihan):
        print("\nMasukkan input yang benar.")
        pilihanMenu = int(input("Input: "))
    if pilihanMenu == 0:
        dashboard(penjual)
    else:
        # perlu dikirim
        if pilihanMenu == 1 and pilihan[pilihanMenu] == "Atur Pengiriman":
            noResi = input("\nMasukkan Nomor Resi: ")
            query = "SELECT COUNT(*) FROM received WHERE NoResi = '%s'" % noResi
            cursorC.execute(query)
            noResiValid = cursorC.fetchone()
            if noResi == "":
                detailPesanan(penjual, nomor, menu, "")
            while noResi != "" and noResiValid[0] != 1:
                print("Nomor resi tidak valid. Silakan masukkan nomor resi yang valid.")
                noResi = input("\nMasukkan Nomor Resi: ")
                if noResi == "":
                    detailPesanan(penjual, nomor, menu, "")
                else:
                    query = "SELECT COUNT(*) FROM received WHERE NoResi = '%s'" % noResi
                    cursorC.execute(query)
                    noResiValid = cursorC.fetchone()
            if noResiValid[0] == 1:
                print("\nNomor resi valid.")
                query = "UPDATE pesanan SET NoResi = %s, WaktuDikirim = %s, Status = 'Dalam Perjalanan' WHERE Email = %s AND NoPesanan = %s"
                dt = datetime.now()
                value = (str(noResi), str(dt)[0:19], penjual.email, crpsnn[nomor - 1][3])
                cursorSC.execute(query, value)
                sellerCenter.commit()
                print("Pesanan sedang dalam perjalanan.")
                input()
                detailPesanan(penjual, nomor, menu, "")

        # menunggu pembayaran
        # -h perlu dikirim tidak bisa dibatalkan karena membutuhkan pengembalian biaya, yang belum bisa dilakukan oleh sistem ini
        elif pilihanMenu == 1 and pilihan[pilihanMenu] == "Batalkan Pesanan":
            print("\nAnda yakin ingin membatalkan pesanan ini? (y/n)")
            answer = input("Input: ")
            while answer != "y" and answer != "n":
                print("\nMasukkan input yang benar.")
                answer = input("Input: ")

            if answer == "y":
                query = "UPDATE pesanan SET Status = 'Dibatalkan' WHERE Email = %s AND NoPesanan = %s"
                value = (penjual.email, crpsnn[nomor - 1][3])
                cursorSC.execute(query, value)
                sellerCenter.commit()
                print("\nPesanan berhasil dibatalkan.")
                input()
                detailPesanan(penjual, nomor, menu, "")
            elif answer == "n":
                detailPesanan(penjual, nomor, menu, "")

def tabelPesanan(penjual, menu, customQuery):
    query = ""
    if customQuery != "":
        query = customQuery
    else:
        if menu == "Pesanan Masuk":
            query = "SELECT * FROM pesanan WHERE Email = '%s'" % penjual.email
        elif menu == "Menunggu Pembayaran":
            query = "SELECT * FROM pesanan WHERE Email = '%s' AND Status = '%s'" % (penjual.email, menu)
        elif menu == "Perlu Dikirim":
            query = "SELECT * FROM pesanan WHERE Email = '%s' AND Status = '%s'" % (penjual.email, menu)
        elif menu == "Dalam Perjalanan":
            query = "SELECT * FROM pesanan WHERE Email = '%s' AND Status = '%s'" % (penjual.email, menu)
        elif menu == "Pesanan Selesai":
            query = "SELECT * FROM pesanan WHERE Email = '%s' AND Status = 'Selesai'" % (penjual.email)
        elif menu == "Pesanan Batal":
            query = "SELECT * FROM pesanan WHERE Email = '%s' AND Status = 'Dibatalkan'" % (penjual.email)
    cursorSC.execute(query)
    psnn = cursorSC.fetchall()
    if len(psnn) == 0:
        print("\nBelum ada pesanan.")
        print("0. Menu Utama")

    # untuk merapihkan tampilan
    else:
        print("\n+%s+%s+%s+%s+%s+%s+%s+" % (("-" * 5), ("-" * 22),
              ("-" * 22), ("-" * 15), ("-" * 11), ("-" * 17), ("-" * 22)))
        print("| {:<3} | {:<20} | {:<20} | {:<13} | {:<9} | {:<15} | {:<20} |".format(
            'No.', 'Email Pembeli', 'Waktu Dibuat', 'Jumlah Produk', 'Total', 'Kurir', 'Status'))
        print("+%s+%s+%s+%s+%s+%s+%s+" % (("-" * 5), ("-" * 22), ("-" * 22), ("-" * 15), ("-" * 11),
              ("-" * 17), ("-" * 22)))

        for x in range(len(psnn)):
            query = f"SELECT Kuantitas FROM produk_pesanan WHERE NoPesanan = {psnn[x][3]}"
            cursorSC.execute(query)
            kuantitas = cursorSC.fetchall()
            jumlahProduk = 0
            for y in range(len(kuantitas)):
                jumlahProduk += kuantitas[y][0]

            print("| {:<3} | {:<20} | {:<20} | {:<13} | {:<9} | {:<15} | {:<20} |".format(
                x + 1, psnn[x][1][0:20], str(psnn[x][4]), jumlahProduk, psnn[x][11], psnn[x][13], psnn[x][15]))
            print("+%s+%s+%s+%s+%s+%s+%s+" % (("-" * 5), ("-" * 22), ("-" * 22), ("-" * 15), ("-" * 11),
                                              ("-" * 17), ("-" * 22)))
        print("0. Menu Utama")
        query = "SELECT COUNT(*) FROM pesanan WHERE Email = '%s'" % penjual.email
        cursorSC.execute(query)
        jumlahPesanan = cursorSC.fetchone()
        return jumlahPesanan[0]

def detailProduk(penjual, nomor, customQuery):
    query = ""
    if customQuery != "":
        query = customQuery
    else:
        query = "SELECT * FROM produk WHERE Email = '%s'" % (penjual.email)
    cursorSC.execute(query)
    prdk = cursorSC.fetchall()
    x = nomor - 1
    print(prdk[x][1])
    line()

    print("{:24s}: {}".format("\nHarga Produk", prdk[x][3]))
    print("{:23s}: {}".format("Jumlah Terjual", prdk[x][9]))
    print("{:23s}: {}".format("Rating Produk", prdk[x][8]))
    print("{:23s}: {}".format("Stok Produk", prdk[x][7]))
    print("{:23s}: {}".format("Kode Produk", prdk[x][2]))
    print("{:23s}: {}".format("Kategori Produk", prdk[x][5]))
    print("{:23s}: {}kg".format("Berat Produk", prdk[x][4]))
    print("{:23s}: {}".format("Deskripsi Produk", prdk[x][6]))
    print("{:23s}: {}".format("Kondisi Produk", prdk[x][10]))

    # updute semua variasi produk
    query = "SELECT * FROM variasi WHERE KodeProduk = '%s'" % (prdk[x][2])
    cursorSC.execute(query)
    vrs = cursorSC.fetchall()
    if len(vrs) != 0:
        for i in vrs:
            print("\nVariasi Produk")
            query = "SELECT * FROM sub_variasi WHERE KodeProduk = '%s' AND TipeVariasi = '%s'" % (  # tampilin variasi produk dari database
                prdk[x][2], i[1])
            cursorSC.execute(query)
            sbVrs = cursorSC.fetchall()
            print(f"{i[1]}:")
            for j in sbVrs:
                print(f"- {j[2]}")
                print(f"  Stok: {j[3]}")


# tampilan untuk ubah produk
    print("""\n0. Menu Utama
1. Ubah Produk
2. Hapus Produk""")
    fitur = int(input("Input: "))
    while fitur < 0 or fitur > 2:
        print("\nMasukkan input yang benar.")
        fitur = int(input("Input: "))
    if fitur == 0:
        dashboard(penjual)
    else:
        if fitur == 1:
            formUbah(penjual, prdk[x][2])
        elif fitur == 2:
            query = "DELETE FROM produk WHERE Email = '%s' AND KodeProduk = '%s'" % (
                penjual.email, prdk[x][2])
            cursorSC.execute(query)
            sellerCenter.commit()
            print("Produk telah berhasil dihapus")
            input()
        dashboard(penjual)

def tabelProduk(penjual, customQuery):
    query = ""
    if customQuery != "":
        query = customQuery
    else:
        query = "SELECT * FROM produk WHERE Email = '%s'" % penjual.email
    cursorSC.execute(query)
    prdk = cursorSC.fetchall()
    if len(prdk) == 0:
        print("\nAnda belum menambahkan produk.")
        print("0. Menu Utama")

    # untuk merapihkan tampilan
    else:
        print("\n+%s+%s+%s+%s+%s+%s+%s+%s+%s+%s+%s+" % (("-" * 5), ("-" * 13), ("-" * 22),
              ("-" * 11), ("-" * 7), ("-" * 17), ("-" * 32), ("-" * 10), ("-" * 8), ("-" * 16), ("-" * 9)))
        print("| {:<3} | {:<11} | {:<20} | {:<9} | {:<5} | {:<15} | {:<30} | {:<8} | {:<6} | {:<14} | {:<7} |".format(
            'No.', 'Kode Produk', 'Nama Produk', 'Harga', 'Berat', 'Kategori', 'Deskripsi', 'Stok', 'Rating', 'Jumlah Terjual', 'Kondisi'))
        print("+%s+%s+%s+%s+%s+%s+%s+%s+%s+%s+%s+" % (("-" * 5), ("-" * 13), ("-" * 22), ("-" * 11),
              ("-" * 7), ("-" * 17), ("-" * 32), ("-" * 10), ("-" * 8), ("-" * 16), ("-" * 9)))
        for x in range(len(prdk)):
            print("| {:<3} | {:<11} | {:<20} | {:<9} | {:<5} | {:<15} | {:<30} | {:<8} | {:<6} | {:<14} | {:<7} |".format(
                x + 1, prdk[x][2], prdk[x][1][0:20], prdk[x][3], str(prdk[x][4]) + "kg", prdk[x][5][0:15], prdk[x][6][0:30], prdk[x][7], prdk[x][8], prdk[x][9], prdk[x][10]))
        print("+%s+%s+%s+%s+%s+%s+%s+%s+%s+%s+%s+" % (("-" * 5), ("-" * 13), ("-" * 22), ("-" * 11),
              ("-" * 7), ("-" * 17), ("-" * 32), ("-" * 10), ("-" * 8), ("-" * 16), ("-" * 9)))
        print("0. Menu Utama")
        query = "SELECT COUNT(*) FROM produk WHERE Email = '%s'" % penjual.email
        cursorSC.execute(query)
        jumlahProduk = cursorSC.fetchone()
        return jumlahProduk[0]

def formUbah(penjual, id):
    namaProduk = input("{:24s}: ".format("\nNama Produk"))
    if namaProduk == "":
        pass
    # jika nama produk yang diinput kurang dari 5 atau lebih dari 50 maka akan menampilkan pesan yang sudah dibuat
    else:
        while len(namaProduk) < 5 or len(namaProduk) > 50:
            if len(namaProduk) < 5:
                print("Panjang nama produk minimal 5.")
            if len(namaProduk) > 50:
                print("Panjang nama produk maskimal 50.")
            namaProduk = input("{:24s}: ".format("\nNama Produk"))
        # untuk mengupdate nama produk ke database
        query = "UPDATE produk SET NamaProduk = %s WHERE Email = %s AND KodeProduk = %s"
        value = (namaProduk, penjual.email, id)
        cursorSC.execute(query, value)
        sellerCenter.commit()
        print("Produk telah berhasil diubah.")

    # menampilkan harga produk
    hargaProduk = input("{:23s}: ".format("Harga Produk"))
    if hargaProduk == "":
        pass
    # harga minimal 99 dan maksimal 999999999
    else:
        while int(hargaProduk) < 99 or int(hargaProduk) > 999999999:
            if int(hargaProduk) < 99:
                print("Harga produk minimal 99.")
            if int(hargaProduk) > 999999999:
                print("Harga produk maskimal 999999999.")
            hargaProduk = input("{:24s}: ".format("\nHarga Produk"))

        # untuk mengupdate harga produk ke database
        query = "UPDATE produk SET Harga = %s WHERE Email = %s AND KodeProduk = %s"
        value = (int(hargaProduk), penjual.email, id)
        cursorSC.execute(query, value)
        sellerCenter.commit()
        print("Produk telah berhasil diubah.")

    # menampilkan berat produk
    beratProduk = input("{:23s}: ".format("Berat Produk"))
    if beratProduk == "":
        pass

    # berat produk minimal 0.01 dan maksimal 10 kg
    else:
        while float(beratProduk) < 0.01 or float(beratProduk) > 10:
            if float(beratProduk) < 0.01:
                print("Berat produk minimal 0.01.")
            if float(beratProduk) > 10:
                print("Berat produk maskimal 10.")
            beratProduk = input("{:24s}: ".format("\nBerat Produk"))

        # untuk mengupdate berat produk ke database
        query = "UPDATE produk SET Berat = %s WHERE Email = %s AND KodeProduk = %s"
        value = (float(beratProduk), penjual.email, id)
        cursorSC.execute(query, value)
        sellerCenter.commit()
        print("Produk telah berhasil diubah.")

    # menampilkan kategori
    ktgr = []
    print("\nKategori Produk")
    query = "SELECT Nama FROM kategori"
    cursorSC.execute(query)
    for i in cursorSC:
        ktgr.append(i[0])
    for i in range(len(ktgr)):
        print("%s. %s" % (i + 1, ktgr[i]))
    kategori = input("Input: ")
    if kategori == "":
        pass
    else:
        while int(kategori) < 1 or int(kategori) > len(ktgr):  # input kategori jika tidak sesuai
            print("\nMasukkan input yang benar.")
            kategori = input("Input: ")
        kategori = ktgr[int(kategori) - 1]
        # updute kategori produk ke database
        query = "UPDATE produk SET Kategori = %s WHERE Email = %s AND KodeProduk = %s"
        value = (kategori, penjual.email, id)
        cursorSC.execute(query, value)
        sellerCenter.commit()

        # updute semua yang ada di kode produk
        query = "SELECT id FROM kategori WHERE Nama = '%s'" % kategori
        cursorSC.execute(query)
        ktgrID = cursorSC.fetchone()[0]
        kodeProduk = f"{ktgrID}{id[1:10]}"
        # updute kode produk ke database
        query = "UPDATE produk SET KodeProduk = %s WHERE KodeProduk = %s"
        value = (kodeProduk, id)
        cursorSC.execute(query, value)
        # updute variasi ke database
        query = "UPDATE variasi SET KodeProduk = %s WHERE KodeProduk = %s"
        value = (kodeProduk, id)
        cursorSC.execute(query, value)
        # updute sub_variasi ke database
        query = "UPDATE sub_variasi SET KodeProduk = %s WHERE KodeProduk = %s"
        value = (kodeProduk, id)
        cursorSC.execute(query, value)
        sellerCenter.commit()

        print("Produk telah berhasil diubah.")

    # tampilan untk input deskripsi produk
    deskripsiProduk = input("{:24s}: ".format("\nDeskripsi Produk"))
    if deskripsiProduk == "":
        pass
    else:
        # input panjang deskripsi produk harus kurang dari 10 dan maks 255
        while (len(deskripsiProduk) < 10 or len(deskripsiProduk) > 255) and deskripsiProduk != "":
            if len(deskripsiProduk) < 10:
                print("Panjang deskripsi produk minimal 10.")
            if len(deskripsiProduk) > 255:
                print("Panjang deskripsi produk maskimal 255.")
            deskripsiProduk = input("{:24s}: ".format("\nDeskripsi Produk"))
        # updute deskripsi produk ke dalam database
        query = "UPDATE produk SET Deskripsi = %s WHERE Email = %s AND KodeProduk = %s"
        value = (deskripsiProduk, penjual.email, id)
        cursorSC.execute(query, value)
        sellerCenter.commit()
        print("Produk telah berhasil diubah.")

    # tampilan input untuk stok produk
    stokProduk = input("{:23s}: ".format("Stok Produk"))
    if stokProduk == "":
        pass
    else:
        # input stok produk min 1 atau maks 999999
        while int(stokProduk) < 1 or int(stokProduk) > 999999:
            if int(stokProduk) < 1:
                print("Stok produk minimal 1.")
            if int(stokProduk) > 999999:
                print("Stok produk maskimal 999999.")
            stokProduk = input("{:24s}: ".format("\nStok Produk"))
        # updute stok produk ke dalam database
        query = "UPDATE produk SET Stok = %s WHERE Email = %s AND KodeProduk = %s"
        value = (int(stokProduk), penjual.email, id)
        cursorSC.execute(query, value)
        sellerCenter.commit()
        print("Produk telah berhasil diubah.")

    # tampilan untuk input bagaimana kondisi produk yang akan dijual
    print("""\nKondisi
1. Baru
2. Bekas""")
    kondisi = input("Input: ")
    if kondisi == "":
        pass
    else:
        # untuk input kondisi produk antara baru atau bekas
        while int(kondisi) < 1 or int(kondisi) > 2:
            print("\nMasukkan input yang benar.")
            kondisi = input("Input: ")
        if int(kondisi) == 1:
            kondisi = "Baru"
        elif int(kondisi) == 2:
            kondisi = "Bekas"
        # updute kondisi produk kedalam database
        query = "UPDATE produk SET Kondisi = %s WHERE Email = %s AND KodeProduk = %s"
        value = (kondisi, penjual.email, id)
        cursorSC.execute(query, value)
        sellerCenter.commit()
        print("Produk telah berhasil diubah.")
        input()
    
    query = "SELECT * FROM variasi WHERE KodeProduk = '%s'" % (id)
    cursorSC.execute(query)
    vrs = cursorSC.fetchall()
    if len(vrs) != 0:
        for i in vrs:
            print("\nVariasi Produk")
            query = "SELECT * FROM sub_variasi WHERE KodeProduk = '%s' AND TipeVariasi = '%s'" % (  # tampilin variasi produk dari database
                id, i[1])
            cursorSC.execute(query)
            sbVrs = cursorSC.fetchall()
            print(f"{i[1]}:")
            for j in sbVrs:
                print(f"- {j[2]}")
                stokSV = input("  Stok: ")
                if stokSV == "":
                    pass
                else:
                    while int(stokSV) < 1 or int(stokSV) > 999999:
                        if int(stokSV) < 1:
                            print("\nStok sub variasi produk minimal 1.")
                        if int(stokSV) > 999999:
                            print("\nStok sub variasi produk maskimal 999999.")
                        stokSV = input("  Stok: ")
                    query = f"UPDATE sub_variasi SET Stok = {stokSV} WHERE KodeProduk = '{id}' AND TipeVariasi = '{i[1]}' AND SubVariasi = '{j[2]}'"
                    cursorSC.execute(query)
                    sellerCenter.commit()
                    print("Produk telah berhasil diubah.")
                    input()

def dashboard(penjual):
    clear()
    print("Pusat Penjual {Nama E-Commerce}")
    line()

# status toko
    if penjual.statusToko == "Buka":
        notStatus = "Tutup"
    elif penjual.statusToko == "Tutup":
        notStatus = "Buka"

    print(f"""\n{penjual.namaToko}
Status Toko: {penjual.statusToko}
Saldo Anda: {penjual.saldo}

Pesanan
1. Pesanan Masuk
2. Cari Pesanan
3. Menunggu Pembayaran
4. Perlu Dikirim
5. Dalam Perjalanan
6. Pesanan Selesai
7. Pesanan Batal

Produk
8. Produk di Toko Saya
9. Cari Produk
10. Tambah Produk
11. Ubah Produk
12. Hapus Produk

Toko
13. Atur Jasa Kirim
14. Informasi Toko Saya
15. {notStatus} Toko

16. Log Out""")

# untuk tampilan input yang akan dipilih di menu penjual
    menu = int(input("Input: "))
    while menu < 1 or menu > 16:
        print("\nMasukkan input yang benar.")
        menu = int(input("Input: "))

    if menu == 1:
        pesanan(penjual, "Pesanan Masuk")
    elif menu == 2:
        cariPesanan(penjual)
    elif menu == 3:
        pesanan(penjual, "Menunggu Pembayaran")
    elif menu == 4:
        pesanan(penjual, "Perlu Dikirim")
    elif menu == 5:
        pesanan(penjual, "Dalam Perjalanan")
    elif menu == 6:
        pesanan(penjual, "Pesanan Selesai")
    elif menu == 7:
        pesanan(penjual, "Pesanan Batal")
    elif menu == 8:
        produkSaya(penjual)
    elif menu == 9:
        cariProduk(penjual)
    elif menu == 10:
        tambahProduk(penjual)
    elif menu == 11:
        ubahProduk(penjual)
    elif menu == 12:
        hapusProduk(penjual)
    elif menu == 13:
        aturJasaKirim(penjual)
    elif menu == 14:
        informasiToko(penjual)
    elif menu == 15:
        aturStatusToko(penjual, notStatus)
    elif menu == 16:
        logOut(penjual)

def pesanan(penjual, menu):
    clear()
    print(menu)
    line()

    jumlah = tabelPesanan(penjual, menu, "")
    print("\nPilih pesanan yang ingin ditampilkan.")
    tampil = int(input("Input: "))
    if jumlah != None:
        while tampil < 0 or tampil > jumlah:
            print("\nMasukkan input yang benar.")
            tampil = int(input("Input: "))
    else:
        while tampil != 0:
            print("\nMasukkan input yang benar.")
            tampil = int(input("Input: "))
    if tampil == 0:
        dashboard(penjual)
    else:
        detailPesanan(penjual, tampil, menu, "")

def cariPesanan(penjual):
    clear()
    print("Cari Pesanan")
    line()

    query = ""

    print("""\nCari berdasarkan*:
1. Nomor Pesanan
2. Nama Produk
3. Kode Produk""")
    berdasarkan = int(input("Input: "))
    while berdasarkan < 1 or berdasarkan > 3:
        print("\nMasukkan input yang benar.")
        berdasarkan = int(input("Input: "))

    keyword = input("\nMasukkan kata kunci*: ")
    while keyword == "":
        keyword = input("\nMasukkan kata kunci*: ")
    if berdasarkan == 1:
        query = f"SELECT * FROM pesanan WHERE Email = '{penjual.email}' AND NoPesanan = {keyword}"
    else:
        if berdasarkan == 2:
            queryTemp = f"SELECT DISTINCT NoPesanan FROM produk_pesanan WHERE Email = '{penjual.email}' AND NamaProduk LIKE '%{keyword}%'"
        elif berdasarkan == 3:
            queryTemp = f"SELECT DISTINCT NoPesanan FROM produk_pesanan WHERE Email = '{penjual.email}' AND KodeProduk LIKE '%{keyword}%'"
        cursorSC.execute(queryTemp)
        noPesanan = cursorSC.fetchall()
        query = f"SELECT * FROM pesanan WHERE Email = '{penjual.email}' AND NoPesanan IN ("
        for x in range(len(noPesanan)):
            if x != len(noPesanan) - 1:
                query += f"{noPesanan[x][0]}, "
            else:
                query += f"{noPesanan[x][0]}"
        query += ")"
        
    # opsional
    if berdasarkan != 1:
        print("""\nUrutkan Berdasarkan:
1. Tanggal Dibuat
2. Total Harga""")
        urutBerdasar = int(input("Input: "))
        while urutBerdasar != "" and (urutBerdasar < 1 or urutBerdasar > 2):
            print("\nMasukkan input yang benar.")
            urutBerdasar = int(input("Input: "))
        if urutBerdasar == 1:
            query += " ORDER BY WaktuDibuat"
        if urutBerdasar == 2:
            query += " ORDER BY TotalHarga"
        
        if urutBerdasar != "":
            if urutBerdasar == 1:
                print("""\nUrutkan Dari:
1. Terbaru hingga Terlama
2. Terlama hingga Terbaru""")
            if urutBerdasar == 2:
                print("""\nUrutkan Dari:
1. Terbesar hingga Terkecil
2. Terkecil hingga Terbesar""")
            urutkan = int(input("Input: "))
            while urutkan < 1 or urutkan > 2:
                print("\nMasukkan input yang benar.")
                urutkan = int(input("Input: "))
            if urutkan == 1:
                query += " DESC"
            if urutkan == 2:
                query += " ASC"

    queryTemp = f"SELECT * FROM pesanan WHERE Email = '{penjual.email}'"
    cursorSC.execute(queryTemp)
    jumlahPesanan = cursorSC.fetchall()

    if len(jumlahPesanan) != 0:
        cursorSC.execute(query)
        pesanan = cursorSC.fetchall()
        if len(pesanan) != 0:
            clear()
            tabelPesanan(penjual, "", query)
            print("\nPilih pesanan yang ingin ditampilkan.")
            tampil = int(input("Input: "))
            while tampil < 0 or tampil > len(pesanan):
                print("\nMasukkan input yang benar.")
                tampil = int(input("Input: "))
            if tampil == 0:
                dashboard(penjual)
            clear()
            detailPesanan(penjual, tampil, "", query)
        else:
            print("\nPesanan tidak ditemukan.")
            input()
            dashboard(penjual)
    else:
        print("\nAnda belum menerima pesanan.")
        input()
        dashboard(penjual)

def produkSaya(penjual):
    clear()
    print("Produk Saya")
    line()

    jumlah = tabelProduk(penjual, "")
    if (jumlah != 0):  # tampilan input untuk memilih produk yang akan ditampilkan
        print("\nPilih produk yang ingin ditampilkan.")
    tampil = int(input("Input: "))
    # tampilan jika input yang di masukkan salah
    if jumlah != None:
        while tampil < 0 or (tampil > jumlah):
            print("\nMasukkan input yang benar.")
            tampil = int(input("Input: "))
    else:
        while tampil != 0:
            print("\nMasukkan input yang benar.")
            tampil = int(input("Input: "))
    if tampil == 0:
        dashboard(penjual)
    else:
        clear()
        detailProduk(penjual, tampil, "")

def cariProduk(penjual):
    clear()
    print("Cari Produk")
    line()

    query = ""

    print("""\nCari berdasarkan*:
1. Nama
2. Kode
3. Kategori""")
    berdasarkan = int(input("Input: "))
    while berdasarkan < 1 or berdasarkan > 3:
        print("\nMasukkan input yang benar.")
        berdasarkan = int(input("Input: "))

    if berdasarkan != 3:
        keyword = input("\nMasukkan kata kunci*: ")
        while keyword == "":
            keyword = input("\nMasukkan kata kunci*: ")
        if berdasarkan == 1:
            query = f"SELECT * FROM produk WHERE Email = '{penjual.email}' AND NamaProduk LIKE '%{keyword}%'"
        elif berdasarkan == 2:
            query = f"SELECT * FROM produk WHERE Email = '{penjual.email}' AND KodeProduk LIKE '%{keyword}%'"
    else:
        queryTemp = "SELECT Nama FROM kategori"
        cursorSC.execute(queryTemp)
        pilihan = cursorSC.fetchall()
        for x in range(len(pilihan)):
            print(f"{x + 1}. {pilihan[x][0]}")
        kategori = int(input("Input: "))
        while kategori < 1 or kategori > len(pilihan):
            print("\nMasukkan input yang benar.")
            kategori = int(input("Input: "))
        query = f"SELECT * FROM produk WHERE Email = '{penjual.email}' AND Kategori = '{pilihan[kategori - 1][0]}'"
        
    # opsional
    print("""\nUrutkan Berdasarkan:
1. Stok
2. Jumlah Terjual""")
    urutBerdasar = int(input("Input: "))
    while urutBerdasar != "" and (urutBerdasar < 1 or urutBerdasar > 2):
        print("\nMasukkan input yang benar.")
        urutBerdasar = int(input("Input: "))
    if urutBerdasar == 1:
        query += " ORDER BY Stok"
    if urutBerdasar == 2:
        query += " ORDER BY JumlahTerjual"
    
    if urutBerdasar != "":
        print("""\nUrutkan Dari:
1. Terbesar hingga Terkecil
2. Terkecil hingga Terbesar""")
        urutkan = int(input("Input: "))
        while urutkan < 1 or urutkan > 2:
            print("\nMasukkan input yang benar.")
            urutkan = int(input("Input: "))
        if urutkan == 1:
            query += " DESC"
        if urutkan == 2:
            query += " ASC"
    
    queryTemp = f"SELECT * FROM produk WHERE Email = '{penjual.email}'"
    cursorSC.execute(queryTemp)
    jumlahProduk = cursorSC.fetchall()

    if len(jumlahProduk) != 0:
        cursorSC.execute(query)
        produk = cursorSC.fetchall()
        if len(produk) != 0:
            clear()
            tabelProduk(penjual, query)
            print("\nPilih produk yang ingin ditampilkan.")
            tampil = int(input("Input: "))
            while tampil < 0 or tampil > len(produk):
                print("\nMasukkan input yang benar.")
                tampil = int(input("Input: "))
            if tampil == 0:
                dashboard(penjual)
            clear()
            detailProduk(penjual, tampil, query)
        else:
            print("\nProduk tidak ditemukan.")
            input()
            dashboard(penjual)
    else:
        print("\nAnda belum menambahkan produk.")
        input()
        dashboard(penjual)

def tambahProduk(penjual):
    clear()
    print("Tambah Produk")
    line()

    namaProduk = input("{:24s}: ".format("\nNama Produk*"))
    while len(namaProduk) < 5 or len(namaProduk) > 50:
        if len(namaProduk) < 5:
            print("Panjang nama produk minimal 5.")
        if len(namaProduk) > 50:
            print("Panjang nama produk maskimal 50.")
        namaProduk = input("{:24s}: ".format("\nNama Produk*"))

    hargaProduk = int(input("{:23s}: ".format("Harga Produk*")))
    while hargaProduk < 99 or hargaProduk > 999999999:
        if hargaProduk < 99:
            print("Harga produk minimal 99.")
        if hargaProduk > 999999999:
            print("Harga produk maskimal 999999999.")
        hargaProduk = int(input("{:24s}: ".format("\nHarga Produk*")))

    beratProduk = float(input("{:23s}: ".format("Berat Produk*")))
    while beratProduk < 0.01 or beratProduk > 10:
        if beratProduk < 0.01:
            print("Berat produk minimal 0.01.")
        if beratProduk > 10:
            print("Berat produk maskimal 10.")
        beratProduk = float(input("{:24s}: ".format("\nBerat Produk*")))

    ktgr = []
    print("\nKategori Produk*")
    query = "SELECT Nama FROM kategori"
    cursorSC.execute(query)
    for i in cursorSC:
        ktgr.append(i[0])
    for i in range(len(ktgr)):
        print("%s. %s" % (i + 1, ktgr[i]))
    kategori = int(input("Input: "))
    while kategori < 1 or kategori > len(ktgr):
        print("\nMasukkan input yang benar.")
        kategori = int(input("Input: "))
    kategori = ktgr[kategori - 1]
    query = "SELECT id FROM kategori WHERE Nama = '%s'" % kategori
    cursorSC.execute(query)
    ktgrID = cursorSC.fetchone()[0]

    kode = random.randint(100000000, 999999999)
    query = "SELECT KodeProduk FROM produk WHERE Email = '%s'" % (
        penjual.email)
    cursorSC.execute(query)
    for i in cursorSC:
        if kode == int(i[0][1:10]):
            kode = random.randint(100000000, 999999999)
    kodeProduk = f"{ktgrID}{kode}"

    deskripsiProduk = input("{:24s}: ".format("\nDeskripsi Produk*"))
    while len(deskripsiProduk) < 10 or len(deskripsiProduk) > 255:
        if len(deskripsiProduk) < 10:
            print("Panjang deskripsi produk minimal 10.")
        if len(deskripsiProduk) > 255:
            print("Panjang deskripsi produk maskimal 255.")
        deskripsiProduk = input("{:24s}: ".format("\nDeskripsi Produk*"))

    print("""\nKondisi*
1. Baru
2. Bekas""")
    kondisi = int(input("Input: "))
    while kondisi < 1 or kondisi > 2:
        print("\nMasukkan input yang benar.")
        kondisi = int(input("Input: "))
    if kondisi == 1:
        kondisi = "Baru"
    elif kondisi == 2:
        kondisi = "Bekas"

    vrs, sbVrs = [], []
    while True:
        variasi = input("{:24s}: ".format("\nVariasi Produk"))
        if variasi == "":
            break
        else:
            while len(variasi) < 3 or len(variasi) > 10:
                if len(variasi) < 3:
                    print("Panjang variasi produk minimal 3.")
                if len(variasi) > 10:
                    print("Panjang variasi produk maskimal 10.")
                variasi = input("{:23s}: ".format("Variasi Produk"))
            vrs.append(Variasi(kodeProduk, variasi))

            jumlahSubVariasi = 0
            while True:
                subVariasi = input("{:24s}: ".format("\nSub Variasi Produk"))
                while subVariasi != "" and len(subVariasi) > 15:
                    print("Panjang sub variasi produk maskimal 15.")
                    subVariasi = input("{:23s}: ".format("Sub Variasi Produk"))

                if jumlahSubVariasi < 2 and subVariasi == "":
                    while subVariasi == "":
                        print("Jumlah sub variasi produk minimal 2.")
                        subVariasi = input(
                            "{:24s}: ".format("\nSub Variasi Produk"))
                        while subVariasi != "" and len(subVariasi) > 15:
                            print("Panjang sub variasi produk maskimal 15.")
                            subVariasi = input(
                                "{:23s}: ".format("Sub Variasi Produk"))

                if (jumlahSubVariasi == 2 or jumlahSubVariasi > 2) and subVariasi == "":
                    break

                if subVariasi != "":
                    stokSubVariasi = int(
                        input("{:24s}: ".format("\nStok Sub Variasi Produk*")))
                    while stokSubVariasi < 1 or stokSubVariasi > 999999:
                        if stokSubVariasi < 1:
                            print("Stok sub variasi produk minimal 1.")
                        if stokSubVariasi > 999999:
                            print("Stok sub variasi produk maskimal 999999.")
                        stokSubVariasi = int(
                            input("{:24s}: ".format("\nStok Sub Variasi Produk*")))

                    sbVrs.append(SubVariasi(kodeProduk, variasi,
                                 subVariasi, stokSubVariasi))

                    jumlahSubVariasi += 1

    stokProduk = 0
    if len(vrs) != 0:
        for i in vrs:
            query = "INSERT INTO variasi (KodeProduk, TipeVariasi) VALUES (%s, %s)"
            value = (i.kodeProduk, i.tipeVariasi)
            cursorSC.execute(query, value)
            sellerCenter.commit()
        for i in sbVrs:
            query = "INSERT INTO sub_variasi (KodeProduk, TipeVariasi, SubVariasi, Stok) VALUES (%s, %s, %s, %s)"
            value = (i.kodeProduk, i.tipeVariasi,
                     i.subVariasi, i.stokSubVariasi)
            cursorSC.execute(query, value)
            sellerCenter.commit()
            stokProduk += i.stokSubVariasi
    else:
        stokProduk = int(input("{:23s}: ".format("Stok Produk*")))
        while stokProduk < 1 or stokProduk > 999999:
            if stokProduk < 1:
                print("Stok produk minimal 1.")
            if stokProduk > 999999:
                print("Stok produk maskimal 999999.")
            stokProduk = int(input("{:24s}: ".format("\nStok Produk*")))

    produk = Produk(penjual.email, namaProduk, kodeProduk, hargaProduk,
                    beratProduk, kategori, deskripsiProduk, stokProduk, kondisi)
    produk.tambahProduk(produk)
    dashboard(penjual)

def ubahProduk(penjual):
    clear()
    print("Ubah Produk")
    line()

    tabelProduk(penjual, "")
    print("\nPilih produk yang ingin diubah.")
    ubah = int(input("Input: "))
    while ubah < 0 or ubah > tabelProduk(penjual, ""):
        print("\nMasukkan input yang benar.")
        ubah = int(input("Input: "))

    clear()
    print("Ubah Produk")
    line()

    query = "SELECT * FROM produk WHERE Email = '%s'" % (penjual.email)
    cursorSC.execute(query)
    prdk = cursorSC.fetchall()

    formUbah(penjual, prdk[ubah - 1][2])
    dashboard(penjual)

def hapusProduk(penjual):
    clear()
    print("Hapus Produk")
    line()

    tabelProduk(penjual, "")
    print("\nPilih produk yang ingin dihapus.")
    hapus = int(input("Input: "))
    while hapus < 0 or hapus > tabelProduk(penjual, ""):
        print("\nMasukkan input yang benar.")
        hapus = int(input("Input: "))

    if hapus == 0:
        pass
    else:
        query = "SELECT * FROM produk WHERE Email = '%s'" % (penjual.email)
        cursorSC.execute(query)
        prdk = cursorSC.fetchall()

        query = "DELETE FROM produk WHERE KodeProduk = '%s'" % prdk[hapus - 1][2]
        cursorSC.execute(query)
        sellerCenter.commit()

        query = "DELETE FROM variasi WHERE KodeProduk = '%s'" % prdk[hapus - 1][2]
        cursorSC.execute(query)
        sellerCenter.commit()

        query = "DELETE FROM sub_variasi WHERE KodeProduk = '%s'" % prdk[hapus - 1][2]
        cursorSC.execute(query)
        sellerCenter.commit()

        print("Produk telah berhasil dihapus.")
        input()
    dashboard(penjual)

def aturJasaKirim(penjual):
    clear()
    print("Atur Jasa Kirim")
    line()

    print("\nTekan 'y' untuk memilih jasa kirim.\nTekan 'n' untuk menghapus jasa kirim.\nTekan enter untuk melewati\n")
    jasaKirim = ['JNE', 'J&T', 'siCepat',
                 'Lion Parcel', 'Anteraja', 'Pos Indonesia']
    pilihanJK = []

    query = "SELECT COUNT(*) FROM jasa_kirim WHERE EmailPenjual = '%s'" % penjual.email
    cursorSC.execute(query)
    jumlahJasaKirim = cursorSC.fetchone()
    if jumlahJasaKirim[0] != 0:
        dJasaKirim = "SELECT * FROM jasa_kirim WHERE EmailPenjual = '%s'" % (penjual.email)
        cursorSC.execute(dJasaKirim)
        terpilih = cursorSC.fetchall()
        for i in range(len(terpilih)):
            pilihanJK.append(terpilih[i][1])

    pilihanJKBaru = pilihanJK.copy()

    for i in jasaKirim:
        pilihan = i
        for j in pilihanJK:
            if j == i:
                pilihan += " (y)"
        print(pilihan)
        pilih = input("Input: ")
        if i != jasaKirim[len(jasaKirim) - 1]:
            print("")
        if pilih == 'y' and i not in pilihanJK:
            pilihanJKBaru.append(i)
            print(f"Jasa kirim {i} ditambahkan.\n")
        elif pilih == 'y' and i in pilihanJK:
            print(f"Jasa kirim {i} sudah ditambahkan.\n")
        elif pilih == 'n' and i not in pilihanJK:
            print(f"Jasa kirim {i} belum ditambahkan.\n")
        elif pilih == 'n' and i in pilihanJK:
            pilihanJKBaru.remove(i)
            print(f"Jasa kirim {i} dihapus.\n")
    
    pilihanJK.sort()
    pilihanJKBaru.sort()

    if pilihanJK != pilihanJKBaru:
        # cek apakah ada yang dihapus
        for i in pilihanJK:
            if i not in pilihanJKBaru:
                query = f"DELETE FROM jasa_kirim WHERE EmailPenjual = '{penjual.email}' AND Nama = '{i}'"
                cursorSC.execute(query)
                sellerCenter.commit()
        
        # cek apakah ada yang ditambah
        for i in pilihanJKBaru:
            if i not in pilihanJK:
                query = "INSERT INTO jasa_kirim (EmailPenjual, Nama) VALUES (%s, %s)"
                value = (penjual.email, i)
                cursorSC.execute(query, value)
                sellerCenter.commit()
        
        print("\nJasa kirim telah diperbarui.")
        
    input()
    dashboard(penjual)

def informasiToko(penjual):
    clear()
    print("Informasi Toko Saya")
    line()

    dUser = "SELECT * FROM user WHERE Email = '%s'" % (penjual.email)
    dPenjual = "SELECT * FROM penjual WHERE Email = '%s'" % (penjual.email)
    dAlamat = "SELECT * FROM alamat WHERE Email = '%s'" % (penjual.email)
    dJasaKirim = "SELECT * FROM jasa_kirim WHERE EmailPenjual = '%s'" % (
        penjual.email)

    cursorSC.execute(dPenjual)
    pnjl = cursorSC.fetchone()
    print("{:24s}: {}".format("\nNama Toko", pnjl[1]))

    cursorSC.execute(dUser)
    user = cursorSC.fetchone()
    print("{:23s}: {}".format("Email", user[0]))

    print("{:23s}: {}".format("Nomor Telepon Toko", pnjl[2]))
    print("{:23s}: {}".format("Rating Toko", pnjl[3]))

    print("\nAlamat:")
    cursorSC.execute(dAlamat)
    alamat = cursorSC.fetchone()
    print("{:23s}: {}".format("Provinsi", alamat[2]))
    print("{:23s}: {}".format("Kabupaten", alamat[3]))
    print("{:23s}: {}".format("Kecamatan", alamat[4]))
    print("{:23s}: {}".format("Kelurahan", alamat[5]))
    print("{:23s}: {}".format("Alamat", alamat[6]))
    print("{:23s}: {}".format("Kode Pos", alamat[7]))

    print("\nJasa Kirim:")
    cursorSC.execute(dJasaKirim)
    jasaKirim = cursorSC.fetchall()
    for i in range(len(jasaKirim)):
        print(f"{i + 1}. {jasaKirim[i][1]}")

    input()
    dashboard(penjual)

def aturStatusToko(penjual, notStatus):
    if notStatus == "Tutup":
        query = "UPDATE penjual SET StatusToko = 'Tutup' WHERE Email = '%s'" % (penjual.email)
        cursorSC.execute(query)
        sellerCenter.commit()
        penjual.tutupToko()
    elif notStatus == "Buka":
        query = "UPDATE penjual SET StatusToko = 'Buka' WHERE Email = '%s'" % (penjual.email)
        cursorSC.execute(query)
        sellerCenter.commit()
        penjual.bukaToko()
    dashboard(penjual)

def logOut(penjual):
    clear()
    print("Anda yakin ingin Log Out? (y/n)")
    answer = input("Input: ")
    while answer != "y" and answer != "n":
        print("\nMasukkan input yang benar.")
        answer = input("Input: ")

    if answer == "y":
        del penjual
        signInUp()
    elif answer == "n":
        dashboard(penjual)

def newStore(user):
    prvns, kbptn, kcmtn, klrhn = [], [], [], []
    prvnsID, kbptnID, kcmtnID, klrhnID = "", "", "", ""

    clear()
    print("Atur Toko Anda")
    line()

    namaToko = input("{:23s}: ".format("\nNama Toko"))
    while len(namaToko) < 5 or len(namaToko) > 30:
        if len(namaToko) < 5:
            print("Panjang nama toko minimal 5.")
        if len(namaToko) > 30:
            print("Panjang nama toko maskimal 30.")

        namaToko = input("{:24s}: ".format("\nNama Toko"))

    print("\nAlamat")
    print("Provinsi")
    query = "SELECT name FROM provinces"
    cursorI.execute(query)
    for i in cursorI:
        prvns.append(i[0].title())
    for i in range(len(prvns)):
        print("%s. %s" % (i + 1, prvns[i]))
    provinsi = int(input("Input: "))
    while provinsi < 1 or provinsi > len(prvns):
        print("\nMasukkan input yang benar.")
        provinsi = int(input("Input: "))
    provinsi = prvns[provinsi - 1].title()
    query = "SELECT id FROM provinces WHERE name = '%s'" % provinsi
    cursorI.execute(query)
    prvnsID = cursorI.fetchone()[0]

    print("\nKabupaten")
    query = "SELECT name FROM regencies WHERE province_id = '%d'" % int(
        prvnsID)
    cursorI.execute(query)
    for i in cursorI:
        kbptn.append(i[0].title())
    for i in range(len(kbptn)):
        print("%s. %s" % (i + 1, kbptn[i]))
    kabupaten = int(input("Input: "))
    while kabupaten < 1 or kabupaten > len(kbptn):
        print("\nMasukkan input yang benar.")
        kabupaten = int(input("Input: "))
    kabupaten = kbptn[kabupaten - 1].title()
    query = "SELECT id FROM regencies WHERE name = '%s'" % kabupaten
    cursorI.execute(query)
    kbptnID = cursorI.fetchone()[0]

    print("\nKecamatan")
    query = "SELECT name FROM districts WHERE regency_id = %d" % int(kbptnID)
    cursorI.execute(query)
    for i in cursorI:
        kcmtn.append(i[0].title())
    for i in range(len(kcmtn)):
        print("%s. %s" % (i + 1, kcmtn[i]))
    kecamatan = int(input("Input: "))
    while kecamatan < 1 or kecamatan > len(kcmtn):
        print("\nMasukkan input yang benar.")
        kecamatan = int(input("Input: "))
    kecamatan = kcmtn[kecamatan - 1].title()
    query = "SELECT id FROM districts WHERE name = '%s'" % kecamatan
    cursorI.execute(query)
    kcmtnID = cursorI.fetchone()[0]

    print("\nKelurahan")
    query = "SELECT name FROM villages WHERE district_id = %d" % int(kcmtnID)
    cursorI.execute(query)
    for i in cursorI:
        klrhn.append(i[0].title())
    for i in range(len(klrhn)):
        print("%s. %s" % (i + 1, klrhn[i]))
    kelurahan = int(input("Input: "))
    while kelurahan < 1 or kelurahan > len(klrhn):
        print("\nMasukkan input yang benar.")
        kelurahan = int(input("Input: "))
    kelurahan = klrhn[kelurahan - 1].title()
    query = "SELECT id FROM villages WHERE name = '%s'" % kelurahan
    cursorI.execute(query)

    alamat = input("{:24s}: ".format("\nAlamat"))
    while len(alamat) < 10 or len(alamat) > 30:
        if len(alamat) < 10:
            print("Panjang alamat minimal 10.")
        if len(alamat) > 30:
            print("Panjang alamat maskimal 30.")

        alamat = input("{:24s}: ".format("\nAlamat"))

    try:
        kodePos = int(input("{:23s}: ".format("Kode Pos")))
    except ValueError:
        print("Kode pos harus berupa angka.")

    while len(str(kodePos)) != 5:
        if len(str(kodePos)) != 5:
            print("Kode pos harus sepanjang 5 digit.")
        kodePos = int(input("{:24s}: ".format("\nKode Pos")))

    noTelp = input("{:24s}: ".format("\nNo. Telepon"))
    while len(noTelp) < 11 or len(noTelp) > 13:
        if len(noTelp) < 11:
            print("Panjang nomor telepon minimal 11.")
        if len(noTelp) > 13:
            print("Panjang nomor telepon maskimal 13.")

        noTelp = input("{:24s}: ".format("\nNo. Telepon"))

    penjual = Penjual(user.email, namaToko, noTelp)
    query = "INSERT INTO penjual (Email, NamaToko, NoTelp, RatingToko, Saldo, StatusToko) VALUES (%s, %s, %s, %s, %s, %s)"
    value = (penjual.email, penjual.namaToko, penjual.noTelp,
             penjual.ratingToko, penjual.saldo, penjual.statusToko)
    cursorSC.execute(query, value)
    sellerCenter.commit()

    penjual.tambahAlamat(Alamat(penjual.email, provinsi,
                         kabupaten, kecamatan, kelurahan, alamat, kodePos))

    dashboard(penjual)

def signUp():
    regexE = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    sSymbol = ['$', '@', '#', '%']

    clear()
    print("Sign Up")
    line()

    email = input("{:24s}: ".format("\nE-Mail"))
    query = "SELECT Email FROM user WHERE Email = '{}'".format(email)
    cursorSC.execute(query)
    while re.fullmatch(regexE, email) == None or len(email) < 10 or len(email) > 40 or cursorSC.fetchone():
        query = "SELECT Email FROM user WHERE Email = '{}'".format(email)
        cursorSC.execute(query)
        if cursorSC.fetchone():
            print("E-mail sudah terdaftar. Silakan Log In.")
            input()
            logIn()
        if re.fullmatch(regexE, email) == None:
            print("Masukkan e-mail dengan format yang benar.")
        if len(email) < 10:
            print("Panjang e-mail minimal 10.")
        if len(email) > 40:
            print("Panjang e-mail maksimal 40.")

        email = input("{:24s}: ".format("\nE-Mail"))
        query = "SELECT Email FROM user WHERE Email = '{}'".format(email)
        cursorSC.execute(query)

    password = input("{:23s}: ".format("Password"))
    while len(password) < 8 or len(password) > 20 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password) or not any(char.islower() for char in password) or not any(char in sSymbol for char in password):
        if len(password) < 8:
            print("Panjang password minimal 8.")
        if len(password) > 20:
            print("Panjang password maksimal 20.")
        if not any(char.isdigit() for char in password):
            print("Password harus memiliki setidaknya satu angka")
        if not any(char.isupper() for char in password):
            print("Password harus memiliki setidaknya satu huruf besar")
        if not any(char.islower() for char in password):
            print("Password harus memiliki setidaknya satu huruf kecil")
        if not any(char in sSymbol for char in password):
            print("Password harus memiliki setidaknya satu simbol ($, @, #, %)")

        password = input("{:24s}: ".format("\nPassword"))

    cPassword = input("{:23s}: ".format("Confirm Password"))
    while cPassword != password:
        print("Password tidak sesuai.")
        cPassword = input("{:24s}: ".format("\nConfirm Password"))

    user = User(email, password)

    query = "INSERT INTO user (Email, Password) VALUES (%s, %s)"
    value = (user.email, user.password)
    cursorSC.execute(query, value)

    sellerCenter.commit()

    newStore(user)

def logIn():
    clear()
    print("Log In")
    line()

    email = input("{:24s}: ".format("\nE-Mail"))
    query = "SELECT Email FROM user WHERE Email = '{}'".format(email)
    cursorSC.execute(query)
    while not cursorSC.fetchone():
        query = "SELECT Email FROM user WHERE Email = '{}'".format(email)
        cursorSC.execute(query)
        if not cursorSC.fetchone():
            print("E-mail belum terdaftar. Silakan Sign Up")
            input()
            signUp()
        email = input("{:24s}: ".format("\nE-Mail"))
        query = "SELECT Email FROM user WHERE Email = '{}'".format(email)
        cursorSC.execute(query)

    password = input("{:23s}: ".format("Password"))
    query = "SELECT Password FROM user WHERE Email = '%s' AND Password = '%s'" % (
        email, password)
    cursorSC.execute(query)
    while not cursorSC.fetchone():
        query = "SELECT Password FROM user WHERE Email = '%s' AND Password = '%s'" % (
            email, password)
        cursorSC.execute(query)
        if not cursorSC.fetchone():
            print("Password tidak sesuai.")

        password = input("{:24s}: ".format("\nPassword"))
        query = "SELECT Password FROM user WHERE Email = '%s' AND Password = '%s'" % (
            email, password)
        cursorSC.execute(query)

    user = User(email, password)

    query = "SELECT NamaToko FROM penjual WHERE Email = '%s'" % user.email
    cursorSC.execute(query)
    if not cursorSC.fetchone():
        newStore(user)
    else:
        query = "SELECT NamaToko FROM penjual WHERE Email = '%s'" % user.email
        cursorSC.execute(query)
        namaToko = cursorSC.fetchone()[0]
        query = "SELECT NoTelp FROM penjual WHERE Email = '%s'" % user.email
        cursorSC.execute(query)
        noTelp = cursorSC.fetchone()[0]
        penjual = Penjual(user.email, namaToko, noTelp)
        query = "SELECT RatingToko FROM penjual WHERE Email = '%s'" % user.email
        cursorSC.execute(query)
        penjual.ratingToko = cursorSC.fetchone()[0]
        query = "SELECT Saldo FROM penjual WHERE Email = '%s'" % user.email
        cursorSC.execute(query)
        penjual.saldo = cursorSC.fetchone()[0]
        query = "SELECT StatusToko FROM penjual WHERE Email = '%s'" % user.email
        cursorSC.execute(query)
        penjual.statusToko = cursorSC.fetchone()[0]

        query = "SELECT Provinsi FROM alamat WHERE Email = '%s'" % user.email
        cursorSC.execute(query)
        provinsi = cursorSC.fetchone()[0]
        query = "SELECT Kabupaten FROM alamat WHERE Email = '%s'" % user.email
        cursorSC.execute(query)
        kabupaten = cursorSC.fetchone()[0]
        query = "SELECT Kecamatan FROM alamat WHERE Email = '%s'" % user.email
        cursorSC.execute(query)
        kecamatan = cursorSC.fetchone()[0]
        query = "SELECT Kelurahan FROM alamat WHERE Email = '%s'" % user.email
        cursorSC.execute(query)
        kelurahan = cursorSC.fetchone()[0]
        query = "SELECT Alamat FROM alamat WHERE Email = '%s'" % user.email
        cursorSC.execute(query)
        alamat = cursorSC.fetchone()[0]
        query = "SELECT KodePos FROM alamat WHERE Email = '%s'" % user.email
        cursorSC.execute(query)
        kodePos = cursorSC.fetchone()[0]
        penjual.setAlamat(Alamat(penjual.email, provinsi,
                          kabupaten, kecamatan, kelurahan, alamat, kodePos))

        dashboard(penjual)

def signInUp():
    clear()
    print("Selamat datang di Pusat Penjual {Nama E-Commerce}")
    line()
    print("""\n1. Log In
2. Sign Up""")
    signInUp = int(input("Input: "))
    while signInUp < 1 or signInUp > 2:
        print("\nMasukkan input yang benar.")
        signInUp = int(input("Input: "))

    if signInUp == 1:
        logIn()
    elif signInUp == 2:
        signUp()

def clear():
    system('cls')

def line():
    print(("=" * 143))

# MAIN
signInUp()