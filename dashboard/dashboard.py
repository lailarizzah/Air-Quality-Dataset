import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# URL dataset
DATA_URL = "https://raw.githubusercontent.com/lailarizzah/Air-Quality-Dataset/refs/heads/main/data/PRSA_Data_Aotizhongxin.csv"

# Fungsi untuk memuat data dengan penanganan error
def load_data():
    try:
        df = pd.read_csv(DATA_URL, sep=";", engine="python", on_bad_lines="skip", encoding="utf-8")
        return df
    except Exception as e:
        print(f"Terjadi error saat membaca dataset: {e}")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong jika terjadi error

# Load data
data = load_data()

# Sidebar untuk filter tahun dan bulan (hanya satu kali)
st.sidebar.header("Filter Data")
year_filter = st.sidebar.selectbox("Pilih Tahun", data["year"].unique(), key="year_select")
month_filter = st.sidebar.selectbox("Pilih Bulan", data["month"].unique(), key="month_select")

# Pastikan dataset telah difilter setelah pemilihan filter
data_filtered = data[(data["year"] == year_filter) & (data["month"] == month_filter)]

# Jika dataset kosong, tampilkan error
if data_filtered.empty:
    st.error("Data tidak ditemukan! Coba pilih tahun dan bulan lain.")
    st.stop()

# Konversi format tanggal dengan benar
data_filtered.loc[:, "weekday"] = pd.to_datetime(data_filtered[["year", "month", "day"]]).dt.weekday
data_filtered.loc[:, "weekend"] = data_filtered["weekday"].apply(lambda x: "Weekend" if x >= 5 else "Weekday")

# Bersihkan format angka (hapus pemisah ribuan)
data = data.replace({",": "", ".": ""}, regex=True)
data = data.apply(pd.to_numeric, errors="coerce")

# Konversi tanggal ke format datetime
data_filtered.loc[:, "weekday"] = pd.to_datetime(data_filtered[["year", "month", "day"]]).dt.weekday
data_filtered.loc[:, "weekend"] = data_filtered["weekday"].apply(lambda x: "Weekend" if x >= 5 else "Weekday")

# Cek apakah data berhasil dimuat
if data.empty:
    print("Gagal memuat dataset. Periksa kembali format file atau URL.")
else:
    print("Dataset berhasil dimuat!")

# Pastikan nama kolom tidak case-sensitive
data.columns = data.columns.str.lower()

if data.empty:
    st.error("Gagal memuat dataset. Periksa kembali URL atau format data.")
    st.stop()

if st.sidebar.checkbox("Tampilkan kolom dataset"):
    st.write("Kolom yang tersedia dalam dataset:", data.columns.tolist())
    
# Pastikan nama kolom tidak case-sensitive
data.columns = data.columns.str.lower()

if "year" not in data.columns:
    st.error("Kolom 'year' tidak ditemukan dalam dataset!")
    st.stop()

if "year" not in data.columns:
    st.error("Kolom 'year' tidak ditemukan dalam dataset!")
    st.stop()

# Judul Dashboard
st.title("Dashboard Kualitas Udara - Kota Aotizhongxin")

# Menampilkan dataset
st.subheader("Data PM₂.₅")
st.dataframe(data_filtered)  # Bisa discroll dan difilter langsung

# Visualisasi PM2.5 berdasarkan weekday vs weekend
data_filtered["weekday"] = pd.to_datetime(data_filtered[["year", "month", "day"]]).dt.weekday

data_filtered["weekend"] = data_filtered["weekday"].apply(lambda x: "Weekend" if x >= 5 else "Weekday")

st.subheader("Perbandingan PM₂.₅ Weekday vs Weekend")
fig, ax = plt.subplots()
sns.boxplot(x="weekend", y="PM2.5", data=data_filtered, ax=ax)
st.pyplot(fig)

# Hitung statistik PM2.5 untuk Weekday dan Weekend
pm25_weekday = data_filtered[data_filtered["weekend"] == "Weekday"]["PM2.5"].median()
pm25_weekend = data_filtered[data_filtered["weekend"] == "Weekend"]["PM2.5"].median()

# Hitung rata-rata faktor cuaca pada Weekday dan Weekend
weather_factors = ["TEMP", "PRES", "WSPM", "RAIN"]
weather_mean_weekday = data_filtered[data_filtered["weekend"] == "Weekday"][weather_factors].mean()
weather_mean_weekend = data_filtered[data_filtered["weekend"] == "Weekend"][weather_factors].mean()

# Tentukan faktor yang paling berbeda antara Weekday dan Weekend
diff_factors = (weather_mean_weekday - weather_mean_weekend).abs()
most_diff_factor = diff_factors.idxmax()
most_diff_value = diff_factors.max()

# Interpretasi
interpretation_boxplot = (
    f"Median PM2.5 pada hari kerja (Weekday) adalah {pm25_weekday:.2f}, "
    f"sedangkan pada akhir pekan (Weekend) adalah {pm25_weekend:.2f}. "
)

interpretation_boxplot += (
    f"Faktor cuaca yang paling berbeda antara Weekday dan Weekend adalah {most_diff_factor} "
    f"dengan selisih {most_diff_value:.2f}. Ini menunjukkan bahwa perubahan {most_diff_factor} "
    "mungkin memiliki pengaruh terhadap kadar polusi udara."
)

st.write("**Interpretasi**")
st.write(interpretation_boxplot)

# Visualisasi Korelasi PM₂.₅ dengan Faktor Cuaca
st.subheader("Korelasi PM₂.₅ dengan Faktor Cuaca")

# Bersihkan format angka dengan benar
data_filtered = data_filtered.apply(pd.to_numeric, errors="coerce")

# Pilih hanya kolom faktor cuaca
weather_factors = ["PM2.5", "TEMP", "PRES", "WSPM", "RAIN"]
data_weather = data_filtered[weather_factors]

# Hitung korelasi hanya untuk faktor cuaca
correlation = data_weather.corr()["PM2.5"].sort_values(ascending=False)

# Visualisasi korelasi dengan heatmap
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(data_weather.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)

# Tampilkan heatmap di Streamlit
st.pyplot(fig)

# Ambil korelasi PM2.5 dengan faktor cuaca lainnya, kecuali dirinya sendiri
correlation_pm25 = correlation.drop("PM2.5")

# Cari faktor cuaca dengan korelasi tertinggi dan terendah
highest_corr = correlation_pm25.idxmax()
highest_value = correlation_pm25.max()
lowest_corr = correlation_pm25.idxmin()
lowest_value = correlation_pm25.min()

# Menentukan Interpretasi
interpretation_corr = (
    f"Korelasi tertinggi antara PM2.5 dan {highest_corr} (r={highest_value:.2f}) "
    f"menunjukkan bahwa faktor ini memiliki dampak paling besar terhadap polusi udara."
)
interpretation_corr += (
    f" Sementara itu, korelasi terendah adalah dengan {lowest_corr} (r={lowest_value:.2f}), "
    "menunjukkan bahwa faktor ini memiliki pengaruh yang kecil terhadap tingkat PM2.5."
)

st.write("**Interpretasi**")
st.write(interpretation_corr)

