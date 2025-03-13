# Air Quality Dataset: Analisis Data Kualitas Udara di Kota Aotizhongxin

## Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis kualitas udara di kota Aotizhongxin menggunakan dataset kualitas udara. Analisis mencakup perbandingan kadar PM₂.₅ pada hari kerja (weekday) dan akhir pekan (weekend), serta pengaruh faktor lingkungan lainnya terhadap tingkat polusi udara.

## Dataset
Dataset yang digunakan diambil dari:
[PRSA Data Aotizhongxin](https://raw.githubusercontent.com/lailarizzah/Air-Quality-Dataset/refs/heads/main/data/PRSA_Data_Aotizhongxin.csv)

### Fitur-Fitur Utama dalam Dataset:
- `year`, `month`, `day`: Informasi tanggal pencatatan kualitas udara.
- `PM2.5`: Konsentrasi PM₂.₅ dalam udara.
- `DEWP`, `TEMP`, `PRES`: Faktor cuaca seperti titik embun, suhu, dan tekanan udara.
- `Iws`: Kecepatan angin.
- `precipitation`: Curah hujan.
- `weekday`: Hari dalam seminggu (0 = Senin, 6 = Minggu).

## Cara Menjalankan Dashboard
Proyek ini menggunakan Streamlit untuk membuat dashboard interaktif.

### 1. Instalasi Dependensi
Pastikan Anda telah menginstal pustaka yang diperlukan dengan perintah berikut:
```bash
pip install -r requirements.txt
```

### 2. Jalankan Dashboard
Gunakan perintah berikut untuk menjalankan Streamlit:
```bash
streamlit run dashboard.py
```

## Fitur Dashboard
- **Tampilkan Data** → Menampilkan beberapa data awal dari dataset.
- **Filter Data** → Memilih data berdasarkan tahun dan bulan.
- **Perbandingan PM₂.₅** → Visualisasi kadar PM₂.₅ pada hari kerja vs akhir pekan.
- **Analisis Korelasi** → Menampilkan hubungan antara variabel lingkungan dan PM₂.₅.

## Library yang Digunakan
- Python
- Pandas & NumPy
- Matplotlib & Seaborn
- Streamlit

## Struktur Direktori Proyek
'''
/ 
submission
├───dashboard       
| ├───main_data.csv
| └───dashboard.py
├───data
| ├───data_1.csv
| └───data_2.csv
├───notebook.ipynb
├───README.md
└───requirements.txt
└───url.txt
'''
