-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 13 Apr 2026 pada 05.09
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_kepuasan`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `admin`
--

CREATE TABLE `admin` (
  `id_admin` int(11) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `admin`
--

INSERT INTO `admin` (`id_admin`, `nama`, `username`, `password`, `created_at`) VALUES
(1, 'ADMIN', 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', '2026-04-09 22:01:54');

-- --------------------------------------------------------

--
-- Struktur dari tabel `dataset_testing`
--

CREATE TABLE `dataset_testing` (
  `id_testing` int(11) NOT NULL,
  `komentar` text DEFAULT NULL,
  `label` varchar(20) DEFAULT NULL,
  `tanggal_upload` datetime DEFAULT current_timestamp(),
  `tanggal` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `dataset_testing`
--

INSERT INTO `dataset_testing` (`id_testing`, `komentar`, `label`, `tanggal_upload`, `tanggal`) VALUES
(1, 'makanannya enak porsi sedikit kurang hangat', NULL, '2026-04-09 21:13:06', '2026-04-09 14:53:40'),
(2, 'makanannya enak', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(3, 'porsi cukup banyak', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(4, 'rasanya lumayan', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(5, 'kurang hangat', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(6, 'makanan biasa saja', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(7, 'sangat enak', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(8, 'tidak enak', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(9, 'porsi kecil', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(10, 'rasanya standar', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(11, 'cukup memuaskan', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(12, 'tidak terlalu enak', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(13, 'makanan lezat', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(14, 'pelayanan baik', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(15, 'kurang memuaskan', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(16, 'menu enak', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(17, 'makanan dingin', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(18, 'rasanya aneh', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(19, 'cukup bagus', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(20, 'biasa saja', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40'),
(21, 'kurang cocok', NULL, '2026-04-09 21:29:34', '2026-04-09 14:53:40');

-- --------------------------------------------------------

--
-- Struktur dari tabel `dataset_training`
--

CREATE TABLE `dataset_training` (
  `id_training` int(11) NOT NULL,
  `komentar` text DEFAULT NULL,
  `label` enum('PUAS','NETRAL','TIDAK PUAS') DEFAULT NULL,
  `sumber` varchar(100) DEFAULT NULL,
  `tanggal_upload` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `dataset_training`
--

INSERT INTO `dataset_training` (`id_training`, `komentar`, `label`, `sumber`, `tanggal_upload`) VALUES
(1, 'makanan enak', 'PUAS', NULL, '2026-04-09 21:09:39'),
(2, 'rasanya enak', 'PUAS', NULL, '2026-04-09 21:22:29'),
(3, 'porsi banyak', 'PUAS', NULL, '2026-04-09 21:22:38'),
(4, 'kurang hangat', 'NETRAL', NULL, '2026-04-09 21:23:05'),
(5, 'biasa saja', 'NETRAL', NULL, '2026-04-09 21:23:16'),
(6, 'lumayan', 'NETRAL', NULL, '2026-04-09 21:23:30'),
(7, 'tidak enak', 'TIDAK PUAS', NULL, '2026-04-09 21:23:46'),
(8, 'porsi sedikit', 'TIDAK PUAS', NULL, '2026-04-09 21:23:55'),
(9, 'terlalu asin', 'TIDAK PUAS', NULL, '2026-04-09 21:24:04'),
(10, 'rasanya enak sekali', 'PUAS', NULL, '2026-04-09 21:29:01'),
(11, 'porsi cukup besar', 'PUAS', NULL, '2026-04-09 21:29:01'),
(12, 'makanan hangat', 'PUAS', NULL, '2026-04-09 21:29:01'),
(13, 'pelayanan ramah', 'PUAS', NULL, '2026-04-09 21:29:01'),
(14, 'menu sangat lezat', 'PUAS', NULL, '2026-04-09 21:29:01'),
(15, 'makanan berkualitas', 'PUAS', NULL, '2026-04-09 21:29:01'),
(16, 'rasa sangat nikmat', 'PUAS', NULL, '2026-04-09 21:29:01'),
(17, 'menu memuaskan', 'PUAS', NULL, '2026-04-09 21:29:01'),
(18, 'pelayanan cepat', 'PUAS', NULL, '2026-04-09 21:29:01'),
(19, 'makanan cukup enak', 'PUAS', NULL, '2026-04-09 21:29:01'),
(20, 'lumayan enak', 'NETRAL', NULL, '2026-04-09 21:29:01'),
(21, 'rasanya biasa', 'NETRAL', NULL, '2026-04-09 21:29:01'),
(22, 'porsi standar', 'NETRAL', NULL, '2026-04-09 21:29:01'),
(23, 'cukup baik', 'NETRAL', NULL, '2026-04-09 21:29:01'),
(24, 'makanan tidak istimewa', 'NETRAL', NULL, '2026-04-09 21:29:01'),
(25, 'rasa cukup', 'NETRAL', NULL, '2026-04-09 21:29:01'),
(26, 'lumayan saja', 'NETRAL', NULL, '2026-04-09 21:29:01'),
(27, 'standar saja', 'NETRAL', NULL, '2026-04-09 21:29:01'),
(28, 'cukup memadai', 'NETRAL', NULL, '2026-04-09 21:29:01'),
(29, 'tidak terlalu spesial', 'NETRAL', NULL, '2026-04-09 21:29:01'),
(30, 'tidak enak', 'TIDAK PUAS', NULL, '2026-04-09 21:29:01'),
(31, 'rasanya buruk', 'TIDAK PUAS', NULL, '2026-04-09 21:29:01'),
(32, 'porsi sedikit', 'TIDAK PUAS', NULL, '2026-04-09 21:29:01'),
(33, 'makanan dingin', 'TIDAK PUAS', NULL, '2026-04-09 21:29:01'),
(34, 'kurang enak', 'TIDAK PUAS', NULL, '2026-04-09 21:29:01'),
(35, 'rasa aneh', 'TIDAK PUAS', NULL, '2026-04-09 21:29:01'),
(36, 'makanan hambar', 'TIDAK PUAS', NULL, '2026-04-09 21:29:01'),
(37, 'pelayanan lambat', 'TIDAK PUAS', NULL, '2026-04-09 21:29:01'),
(38, 'tidak memuaskan', 'TIDAK PUAS', NULL, '2026-04-09 21:29:01'),
(39, 'menu tidak enak', 'TIDAK PUAS', NULL, '2026-04-09 21:29:01');

-- --------------------------------------------------------

--
-- Struktur dari tabel `hasil_prediksi`
--

CREATE TABLE `hasil_prediksi` (
  `id_prediksi` int(11) NOT NULL,
  `komentar` text DEFAULT NULL,
  `hasil` enum('PUAS','NETRAL','TIDAK PUAS') DEFAULT NULL,
  `confidence` decimal(5,2) DEFAULT NULL,
  `tanggal` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `hasil_prediksi`
--

INSERT INTO `hasil_prediksi` (`id_prediksi`, `komentar`, `hasil`, `confidence`, `tanggal`) VALUES
(22, 'kurang cocok', 'TIDAK PUAS', NULL, '2026-04-12 10:05:33'),
(23, 'biasa saja', 'NETRAL', NULL, '2026-04-12 10:05:33'),
(24, 'cukup bagus', 'NETRAL', NULL, '2026-04-12 10:05:33'),
(25, 'rasanya aneh', 'TIDAK PUAS', NULL, '2026-04-12 10:05:33'),
(26, 'makanan dingin', 'TIDAK PUAS', NULL, '2026-04-12 10:05:33'),
(27, 'menu enak', 'PUAS', NULL, '2026-04-12 10:05:33'),
(28, 'kurang memuaskan', 'PUAS', NULL, '2026-04-12 10:05:33'),
(29, 'pelayanan baik', 'PUAS', NULL, '2026-04-12 10:05:33'),
(30, 'makanan lezat', 'PUAS', NULL, '2026-04-12 10:05:33'),
(31, 'tidak terlalu enak', 'TIDAK PUAS', NULL, '2026-04-12 10:05:33'),
(32, 'cukup memuaskan', 'PUAS', NULL, '2026-04-12 10:05:33'),
(33, 'rasanya standar', 'NETRAL', NULL, '2026-04-12 10:05:33'),
(34, 'porsi kecil', 'TIDAK PUAS', NULL, '2026-04-12 10:05:33'),
(35, 'tidak enak', 'TIDAK PUAS', NULL, '2026-04-12 10:05:33'),
(36, 'sangat enak', 'PUAS', NULL, '2026-04-12 10:05:33'),
(37, 'makanan biasa saja', 'NETRAL', NULL, '2026-04-12 10:05:33'),
(38, 'kurang hangat', 'NETRAL', NULL, '2026-04-12 10:05:33'),
(39, 'rasanya lumayan', 'NETRAL', NULL, '2026-04-12 10:05:33'),
(40, 'porsi cukup banyak', 'NETRAL', NULL, '2026-04-12 10:05:33'),
(41, 'makanannya enak', 'PUAS', NULL, '2026-04-12 10:05:33'),
(42, 'makanannya enak porsi sedikit kurang hangat', 'TIDAK PUAS', NULL, '2026-04-12 10:05:33');

-- --------------------------------------------------------

--
-- Struktur dari tabel `hasil_sentimen`
--

CREATE TABLE `hasil_sentimen` (
  `id_hasil` int(11) NOT NULL,
  `id_komentar` int(11) DEFAULT NULL,
  `hasil` varchar(20) DEFAULT NULL,
  `confidence` float DEFAULT NULL,
  `tanggal` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `hasil_sentimen`
--

INSERT INTO `hasil_sentimen` (`id_hasil`, `id_komentar`, `hasil`, `confidence`, `tanggal`) VALUES
(4, 1, 'PUAS', 2.23547, '2026-04-11 15:00:37'),
(10, 2, 'NETRAL', 2.22221, '2026-04-11 15:57:37'),
(16, 3, 'TIDAK PUAS', 2.14445, '2026-04-12 03:07:47');

-- --------------------------------------------------------

--
-- Struktur dari tabel `komentar`
--

CREATE TABLE `komentar` (
  `id_komentar` int(11) NOT NULL,
  `id_responden` int(11) DEFAULT NULL,
  `isi_komentar` text DEFAULT NULL,
  `tanggal` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `komentar`
--

INSERT INTO `komentar` (`id_komentar`, `id_responden`, `isi_komentar`, `tanggal`) VALUES
(1, 1, 'Layanan MBG sudah sangat membantu, responnya cepat dan hasilnya memuaskan.', '2026-04-11 20:45:02'),
(2, 2, 'Layanan sudah cukup baik, tapi masih bisa ditingkatkan lagi.', '2026-04-11 22:57:11'),
(3, 3, 'Pelayanan kurang responsif terhadap keluhan.', '2026-04-12 10:07:17');

-- --------------------------------------------------------

--
-- Struktur dari tabel `log_training`
--

CREATE TABLE `log_training` (
  `id_log` int(11) NOT NULL,
  `jumlah_data` int(11) DEFAULT NULL,
  `akurasi` decimal(5,2) DEFAULT NULL,
  `precision_score` decimal(5,2) DEFAULT NULL,
  `recall_score` decimal(5,2) DEFAULT NULL,
  `tanggal` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `log_training`
--

INSERT INTO `log_training` (`id_log`, `jumlah_data`, `akurasi`, `precision_score`, `recall_score`, `tanggal`) VALUES
(1, NULL, 0.63, NULL, NULL, '2026-04-11 22:47:57'),
(2, 39, 0.63, 0.72, 0.61, '2026-04-11 22:53:26'),
(3, 39, 0.63, 0.72, 0.61, '2026-04-12 10:05:08');

-- --------------------------------------------------------

--
-- Struktur dari tabel `responden`
--

CREATE TABLE `responden` (
  `id_responden` int(11) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `sekolah` varchar(100) DEFAULT NULL,
  `kelas` varchar(50) DEFAULT NULL,
  `tanggal` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `responden`
--

INSERT INTO `responden` (`id_responden`, `nama`, `sekolah`, `kelas`, `tanggal`) VALUES
(1, 'Dimas', 'Sekolah 1', 'X', '2026-04-11 20:45:02'),
(2, 'Andini', 'Sekolah 1', 'Xl', '2026-04-11 22:57:11'),
(3, 'Candra', 'Sekolah 1', 'Xll', '2026-04-12 10:07:17');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`);

--
-- Indeks untuk tabel `dataset_testing`
--
ALTER TABLE `dataset_testing`
  ADD PRIMARY KEY (`id_testing`);

--
-- Indeks untuk tabel `dataset_training`
--
ALTER TABLE `dataset_training`
  ADD PRIMARY KEY (`id_training`);

--
-- Indeks untuk tabel `hasil_prediksi`
--
ALTER TABLE `hasil_prediksi`
  ADD PRIMARY KEY (`id_prediksi`);

--
-- Indeks untuk tabel `hasil_sentimen`
--
ALTER TABLE `hasil_sentimen`
  ADD PRIMARY KEY (`id_hasil`),
  ADD UNIQUE KEY `id_komentar` (`id_komentar`);

--
-- Indeks untuk tabel `komentar`
--
ALTER TABLE `komentar`
  ADD PRIMARY KEY (`id_komentar`),
  ADD KEY `id_responden` (`id_responden`);

--
-- Indeks untuk tabel `log_training`
--
ALTER TABLE `log_training`
  ADD PRIMARY KEY (`id_log`);

--
-- Indeks untuk tabel `responden`
--
ALTER TABLE `responden`
  ADD PRIMARY KEY (`id_responden`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `dataset_testing`
--
ALTER TABLE `dataset_testing`
  MODIFY `id_testing` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT untuk tabel `dataset_training`
--
ALTER TABLE `dataset_training`
  MODIFY `id_training` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT untuk tabel `hasil_prediksi`
--
ALTER TABLE `hasil_prediksi`
  MODIFY `id_prediksi` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT untuk tabel `hasil_sentimen`
--
ALTER TABLE `hasil_sentimen`
  MODIFY `id_hasil` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT untuk tabel `komentar`
--
ALTER TABLE `komentar`
  MODIFY `id_komentar` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `log_training`
--
ALTER TABLE `log_training`
  MODIFY `id_log` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `responden`
--
ALTER TABLE `responden`
  MODIFY `id_responden` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `hasil_sentimen`
--
ALTER TABLE `hasil_sentimen`
  ADD CONSTRAINT `hasil_sentimen_ibfk_1` FOREIGN KEY (`id_komentar`) REFERENCES `komentar` (`id_komentar`);

--
-- Ketidakleluasaan untuk tabel `komentar`
--
ALTER TABLE `komentar`
  ADD CONSTRAINT `komentar_ibfk_1` FOREIGN KEY (`id_responden`) REFERENCES `responden` (`id_responden`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
