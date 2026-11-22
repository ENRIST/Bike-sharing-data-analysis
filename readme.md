# Bike Sharing Analytics Dashboard (2011–2012)

Proyek analisis data eksploratif dan dashboard interaktif menggunakan **Bike Sharing Dataset** dari sistem Capital Bikeshare, Washington D.C., Amerika Serikat periode Januari 2011–Desember 2012.

**Penulis:** Steven Krisna Putra

---

## Ringkasan Analisis & Temuan Utama

* **Pengaruh Musim, Suhu, dan Cuaca:** Musim **Fall** mencatat rata-rata penyewaan harian tertinggi (`5.644` sepeda/hari) dan **Spring** terendah (`2.604` sepeda/hari). Hari bersuhu **Warm (>25°C)** menghasilkan permintaan hampir dua kali lipat (`5.632` sepeda/hari) dibandingkan hari bersuhu **Cool (<15°C)** (`2.833` sepeda/hari). Cuaca buruk **Light Snow/Rain** menurunkan penyewaan harian sebesar **63,02%** (`1.803` vs `4.877` sepeda/hari pada cuaca cerah).
* **Pola Jam Operasional & Segmen Pengguna:** Pada **Working Day**, permintaan membentuk dua puncak komuter pada klaster **Morning Rush (06–09)** (puncak pukul `08.00` = `477`/jam) dan **Evening Rush (16–19)** (puncak pukul `17.00` = `525`/jam) yang didominasi pengguna `registered` (`81,17%` dari total `3.292.679` penyewaan). Sebaliknya, pada **Weekend/Holiday**, penyewaan memuncak di klaster **Midday (10–15)** (puncak pukul `13.00` = `373`/jam) dengan rata-rata pengguna `casual` melonjak **2,25 kali lipat**.

---

## Struktur Direktori

```text
.
├── dashboard/
│   ├── dashboard.py      # Kode utama aplikasi Streamlit
│   └── main_data.csv     # Dataset bersih hasil wrangling & analisis lanjutan
├── data/
│   ├── day.csv           # Data penyewaan agregasi harian (731 baris)
│   ├── hour.csv          # Data penyewaan per jam (17.379 baris)
│   └── Readme.txt        # Dokumentasi resmi dataset
├── notebook.ipynb        # Notebook lengkap (Wrangling, EDA, Visualisasi, & Clustering)
├── requirements.txt      # Daftar pustaka Python yang dibutuhkan
├── url.txt               # Tautan dashboard publik (Streamlit Community Cloud)
└── README.md             # Dokumentasi proyek
```

---

## Setup Environment & Instalasi

Pastikan Python 3.9+ sudah terpasang pada sistem, lalu jalankan perintah berikut di direktori utama proyek:

```bash
pip install -r requirements.txt
```

*(Jika menggunakan Windows dan perintah `pip` belum terdaftar di PATH, gunakan:)*

```bash
py -m pip install -r requirements.txt
```

---

## Menjalankan Dashboard Secara Lokal

Jalankan aplikasi Streamlit dengan perintah berikut dari direktori utama proyek:

```bash
streamlit run dashboard/dashboard.py
```

*(Alternatif untuk Windows jika perintah `streamlit` tidak dikenali:)*

```bash
py -m streamlit run dashboard/dashboard.py
```

Setelah dijalankan, dashboard dapat diakses melalui peramban web pada alamat `http://localhost:8501`.