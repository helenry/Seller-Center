-- seller_center
DROP DATABASE IF EXISTS seller_center;
CREATE DATABASE IF NOT EXISTS seller_center;

USE seller_center;

-- CREATE TABLE
CREATE TABLE user (
	Email VARCHAR(40) NOT NULL,
	Password VARCHAR(20) NOT NULL,
	PRIMARY KEY (Email)
);

CREATE TABLE jasa_kirim (
    EmailPenjual VARCHAR(40) NOT NULL,
    Nama TEXT NOT NULL
);

CREATE TABLE penjual (
	Email VARCHAR(40) NOT NULL,
    NamaToko TEXT NOT NULL,
    NoTelp TEXT NOT NULL,
    RatingToko FLOAT NOT NULL,
    Saldo INT(9) NOT NULL,
    StatusToko TEXT NOT NULL,
    PRIMARY KEY (Email)
);

CREATE TABLE alamat (
	Email VARCHAR(40) NOT NULL,
	Jenis TEXT NOT NULL,
    Provinsi TEXT NOT NULL,
    Kabupaten TEXT NOT NULL,
    Kecamatan TEXT NOT NULL,
    Kelurahan TEXT NOT NULL,
    Alamat TEXT NOT NULL,
    KodePos INT(5) NOT NULL,
    PRIMARY KEY (Email)
);

CREATE TABLE produk (
	Email VARCHAR(40) NOT NULL,
    NamaProduk TEXT NOT NULL,
    KodeProduk VARCHAR(10) NOT NULL,
    Harga INT(9) NOT NULL,
    Berat FLOAT NOT NULL,
    Kategori TEXT NOT NULL,
    Deskripsi TEXT NOT NULL,
    Stok INT(6) NOT NULL,
    Rating FLOAT NOT NULL,
    JumlahTerjual INT(9) NOT NULL,
    Kondisi TEXT NOT NULL,
	PRIMARY KEY (KodeProduk)
);

CREATE TABLE kategori (
    Id CHAR NOT NULL,
    Nama TEXT NOT NULL,
    PRIMARY KEY (Id)
);

CREATE TABLE variasi (
	KodeProduk VARCHAR(10) NOT NULL,
    TipeVariasi TEXT NOT NULL
);

CREATE TABLE sub_variasi (
	KodeProduk VARCHAR(10) NOT NULL,
    TipeVariasi TEXT NOT NULL,
    SubVariasi TEXT NOT NULL,
    Stok INT NOT NULL
);

CREATE TABLE pesanan (
	Email VARCHAR(40) NOT NULL,
    EmailPembeli VARCHAR(40) NOT NULL,
    NoTelpPembeli TEXT NOT NULL,
	NoPesanan INT NOT NULL AUTO_INCREMENT,
    WaktuDibuat TIMESTAMP NOT NULL,
    WaktuDibayar TIMESTAMP NULL,
    WaktuDikirim TIMESTAMP NULL,
    WaktuSelesai TIMESTAMP NULL,
    SubtotalProduk INT(9) NOT NULL,
    Ongkir INT(9) NOT NULL,
    BiayaPenanganan INT(9) NOT NULL,
    TotalHarga INT(9) NOT NULL,
    MetodePembayaran TEXT NOT NULL,
    Kurir TEXT NOT NULL,
    NoResi VARCHAR(15) NULL,
    Status TEXT NOT NULL,
	PRIMARY KEY (NoPesanan)
);

CREATE TABLE produk_pesanan (
    Email VARCHAR(40) NOT NULL,
    NoPesanan INT NOT NULL,
	KodeProduk VARCHAR(10) NOT NULL,
	NamaProduk TEXT NOT NULL,
	Harga INT NOT NULL,
	Berat FLOAT NOT NULL,
	Kategori TEXT NOT NULL,
	Kondisi TEXT NOT NULL,
    Kuantitas INT NOT NULL,
    Variasi TEXT NULL,
    SubVariasi TEXT NULL
);

-- INSERT INTO
INSERT INTO kategori (Id, Nama)
VALUES ('A', 'Pakaian Wanita'),
('B', 'Pakaian Pria'),
('C', 'Elektronik'),
('D', 'Makanan dan Minuman'),
('E', 'Perawatan dan Kecantikan'),
('F', 'Pakaian Anak'),
('G', 'Aksesoris Wanita'),
('H', 'Aksesoris Pria'),
('I', 'Sepatu Wanita'),
('J', 'Sepatu Pria'),
('K', 'Perlengkapan Rumah'),
('L', 'Hobi'),
('M', 'Olahraga'),
('N', 'Lainnya');

INSERT INTO `produk` (`Email`, `NamaProduk`, `KodeProduk`, `Harga`, `Berat`, `Kategori`, `Deskripsi`, `Stok`, `Rating`, `JumlahTerjual`, `Kondisi`) VALUES
('keziaagth@gmail.com', 'Laptop Acer', 'C558975381', 20000000, 3.5, 'Elektronik', 'lorem ipsum dolor sit amet', 122, 0, 0, 'Baru'),
('keziaagth@gmail.com', 'Kabel LAN 10 Meter', 'C568225879', '20000', '1', 'Elektronik', 'Kabel untuk menghubungkan 2 perangkat', '456', '0', 50, 'Baru'),
('keziaagth@gmail.com', 'Iphone 13 Pro Max', 'C607819193', 21300000, 2.4, 'Elektronik', 'Iphone adalah handphone yang cocok digunakan untuk orang-orang yang suka memotret moment', 89, 0, 4, 'Baru'),
('keziaagth@gmail.com', 'Logitech Keyboard', 'C633276583', 299000, 1.3, 'Elektronik', 'keyboard ini cocok digunakan oleh orang yang suka mengetik', 598000, 0, 0, 'Baru');

INSERT INTO `user` (`Email`, `Password`) VALUES
('feren@gmail.com', 'Asdfg12345$'),
('helen@gmail.com', 'Abcde%12345'),
('keziaagth@gmail.com', 'Asdfg12345$');

INSERT INTO `penjual` (`Email`, `NamaToko`, `NoTelp`, `RatingToko`, `Saldo`, `StatusToko`) VALUES
('feren@gmail.com', 'EnterKomputer', '089765435267', 0, 0, 'Buka'),
('helen@gmail.com', 'Alfamart', '08912345678', 0, 0, 'Buka'),
('keziaagth@gmail.com', 'Avo Skin', '0897654321]', 0, 0, 'Tutup');

INSERT INTO `sub_variasi` (`KodeProduk`, `TipeVariasi`, `SubVariasi`, `Stok`) VALUES
('C607819193', 'warna', 'hitam', 12),
('C607819193', 'warna', 'putih', 75),
('C607819193', 'warna', 'gold', 2),
('E730876192', 'tipe', 'brightning', 155000),
('E730876192', 'tipe', 'moisturizing', 150000),
('E730876192', 'tipe', 'lactid acid\\', 145000),
('E730876192', 'tipe', 'retinol', 134000),
('E730876192', 'tipe', 'AHA BHA ', 199000),
('J799763949', 'warna', 'putih', 499000),
('J799763949', 'warna', 'hitam', 499000),
('J799763949', 'warna', 'coklat', 499000),
('C633276583', 'warna', 'hitam', 299000),
('C633276583', 'warna', 'putih', 299000),
('C558975381', 'warma', 'hitam', 13),
('C558975381', 'warma', 'putih', 73),
('C558975381', 'warma', 'merah', 36);

INSERT INTO `variasi` (`KodeProduk`, `TipeVariasi`) VALUES
('C607819193', 'warna'),
('E730876192', 'tipe'),
('J799763949', 'warna'),
('C633276583', 'warna'),
('C558975381', 'warma');

INSERT INTO `jasa_kirim`(`EmailPenjual`, `Nama`) VALUES
('keziaagth@gmail.com','Pos Indonesia'),
('keziaagth@gmail.com','Lion Parcel'),
('keziaagth@gmail.com','Anteraja'),
('keziaagth@gmail.com','JNE'),
('keziaagth@gmail.com','siCepat');

INSERT INTO `alamat` (`Email`, `Jenis`, `Provinsi`, `Kabupaten`, `Kecamatan`, `Kelurahan`, `Alamat`, `KodePos`) VALUES
('customer1@gmail.com', 'pembeli', 'Nusa Tenggara Barat', 'Kabupaten Bima', 'Belo', 'Soki', 'Jalan Soki Nomor 53', '12345'),
('customer2@gmail.com','pembeli','Jambi','Kabupaten Tebo','Rimbo Ulu','Wanareja','Jalan Wanareja 4 No. 34',68452),
('customer3@gmail.com','pembeli','Di Yogyakarta','Kabupaten Gunung Kidul','Sapto Sari','Monggol','Jalan Monggol Gang 4 No. 29',46132),
('customer4@gmail.com','pembeli','Sulawesi Utara','Kabupaten Minahasa Selatan','Motoling Barat','Tondei Satu','Jalan Tondei Satu No. 4A',81542),
('feren@gmail.com', 'penjual', 'Dki Jakarta', 'Kota Jakarta Utara', 'Penjaringan', 'Kapuk Muara', 'Mangga Dua', 12345),
('helen@gmail.com', 'penjual', 'Dki Jakarta', 'Kota Jakarta Utara', 'Pademangan', 'Pademangan Timur', 'Pademangan 6', 14410),
('keziaagth@gmail.com', 'penjual', 'Dki Jakarta', 'Kota Jakarta Selatan', 'Setia Budi', 'Setia Budi', 'Jl. Setia Budi No. 19A', 12345);

INSERT INTO `produk_pesanan`(`Email`, `NoPesanan`, `KodeProduk`, `NamaProduk`, `Harga`, `Berat`, `Kategori`, `Kondisi`, `Kuantitas`, `Variasi`, `SubVariasi`) VALUES
('keziaagth@gmail.com',1,'C558975381','Laptop Acer',20000000,3.5,'Elektronik','Baru',1,'warma','hitam'),
('keziaagth@gmail.com',1,'C558975381','Laptop Acer',20000000,3.5,'Elektronik','Baru',1,'warma','putih'),
('keziaagth@gmail.com',1,'C633276583','Logitech Keyboard',299000,1.3,'Elektronik','Baru',1,'warna','hitam'),
('keziaagth@gmail.com',1,'C633276583','Logitech Keyboard',299000,1.3,'Elektronik','Baru',1,'warna','putih');
INSERT INTO `produk_pesanan`(`Email`, `NoPesanan`, `KodeProduk`, `NamaProduk`, `Harga`, `Berat`, `Kategori`, `Kondisi`, `Kuantitas`, `Variasi`, `SubVariasi`) VALUES
('keziaagth@gmail.com',2,'C568225879','Kabel LAN 10 Meter',20000,1,'Elektronik','Baru',10,null,null),
('keziaagth@gmail.com',2,'C633276583','Logitech Keyboard',299000,1.3,'Elektronik','Baru',1,'warna','putih');
INSERT INTO `produk_pesanan`(`Email`, `NoPesanan`, `KodeProduk`, `NamaProduk`, `Harga`, `Berat`, `Kategori`, `Kondisi`, `Kuantitas`, `Variasi`, `SubVariasi`) VALUES
('keziaagth@gmail.com',3,'C558975381','Laptop Acer',20000000,3.5,'Elektronik','Baru',2,'warma','hitam'),
('keziaagth@gmail.com',3,'C607819193','Iphone 13 Pro Max',21300000,2.4,'Elektronik','Baru',2,'warna','hitam');
INSERT INTO `produk_pesanan`(`Email`, `NoPesanan`, `KodeProduk`, `NamaProduk`, `Harga`, `Berat`, `Kategori`, `Kondisi`, `Kuantitas`, `Variasi`, `SubVariasi`) VALUES
('keziaagth@gmail.com',4,'C568225879','Kabel LAN 10 Meter',20000,1,'Elektronik','Baru',50,null,null),
('keziaagth@gmail.com',4,'C607819193','Iphone 13 Pro Max',21300000,2.4,'Elektronik','Baru',4,'warna','putih');

INSERT INTO `pesanan`(`Email`, `EmailPembeli`, `NoTelpPembeli`, `NoPesanan`, `WaktuDibuat`, `WaktuDibayar`, `WaktuDikirim`, `WaktuSelesai`, `SubtotalProduk`, `Ongkir`, `BiayaPenanganan`, `TotalHarga`, `MetodePembayaran`, `Kurir`, `NoResi`, `Status`) VALUES ('keziaagth@gmail.com','customer1@gmail.com','088965213658',null,'2022-07-07 12:25:47',null,null,null,40598000,100000,202990,40900990,'Transfer Bank: BCA','Lion Parcel',null,'Menunggu Pembayaran');
INSERT INTO `pesanan`(`Email`, `EmailPembeli`, `NoTelpPembeli`, `NoPesanan`, `WaktuDibuat`, `WaktuDibayar`, `WaktuDikirim`, `WaktuSelesai`, `SubtotalProduk`, `Ongkir`, `BiayaPenanganan`, `TotalHarga`, `MetodePembayaran`, `Kurir`, `NoResi`, `Status`) VALUES ('keziaagth@gmail.com','customer2@gmail.com','084625136589',2,'2022-07-05 03:45:03','2022-07-05 03:50:43',null,null,499000,240000,2495,741495,'Alfamart','Pos Indonesia',null,'Perlu Dikirim');
INSERT INTO `pesanan`(`Email`, `EmailPembeli`, `NoTelpPembeli`, `NoPesanan`, `WaktuDibuat`, `WaktuDibayar`, `WaktuDikirim`, `WaktuSelesai`, `SubtotalProduk`, `Ongkir`, `BiayaPenanganan`, `TotalHarga`, `MetodePembayaran`, `Kurir`, `NoResi`, `Status`) VALUES ('keziaagth@gmail.com','customer3@gmail.com','084512369574',3,'2022-07-06 23:15:56','2022-07-06 23:16:25','2022-07-07 14:36:45',null,82600000,120000,413000,83133000,'Transfer Bank: BNI','Anteraja','A21456325145849','Dalam Perjalanan');
INSERT INTO `pesanan`(`Email`, `EmailPembeli`, `NoTelpPembeli`, `NoPesanan`, `WaktuDibuat`, `WaktuDibayar`, `WaktuDikirim`, `WaktuSelesai`, `SubtotalProduk`, `Ongkir`, `BiayaPenanganan`, `TotalHarga`, `MetodePembayaran`, `Kurir`, `NoResi`, `Status`) VALUES ('keziaagth@gmail.com','customer4@gmail.com','084625613698',4,'2022-06-29 20:36:25','2022-06-29 21:26:03','2022-06-30 15:26:15','2022-07-05 11:52:14',86200000,1200000,431000,87831000,'Indomaret','siCepat','SC2145621458745','Pesanan Selesai');


-- hanya untuk simulasi
-- courier
DROP DATABASE IF EXISTS courier;
CREATE DATABASE IF NOT EXISTS courier;

USE courier;

-- CREATE TABLE
CREATE TABLE received (
	NoResi VARCHAR(15) NOT NULL,
	EmailPengirim TEXT NOT NULL,
	PRIMARY KEY (NoResi)
);

-- INSERT INTO
INSERT INTO `received`(`NoResi`, `EmailPengirim`) VALUES
('PI2314587954625','keziaagth@gmail.com');

-- 1
-- keziaagth@gmail.com
-- Asdfg12345$