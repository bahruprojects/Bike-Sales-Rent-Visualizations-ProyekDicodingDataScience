import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Membaca dataset 
df = pd.read_csv(r'C:\Users\OPTION\Documents\Proyek Akhir\Dataset\day.csv')

# Mengonversi kolom 'dteday' menjadi format datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# Title untuk dashboard
st.title("Dashboard Peminjaman Sepeda Tahun 2011 - 2012")
st.sidebar.header("Masukkan Tanggal")
st.write("Nama : Alfin Bahru Rahmika Umar")
st.write("Email : Rahmikalfin@gmail.com")
st.write("ID Dicoding : Alfinbahru")

st.write(
    """
    # Pertanyaan Bisnis
    Pertanyaan 1 : Bagaimana performa peminjaman sepeda (rental) terhadap faktor jenis hari?.
    Pertanyaan 2 : Bagaimana performa peminjaman sepeda (rental) terhadap faktor cuaca dan musim?.
    Pertanyaan 3 : Berapa besarnya rental (Peminjaman Sepeda) dalam tahun 2011?.
    Pertanyaan 4 : Berapa besarnya rental (Peminjaman Sepeda) dalam tahun 2012?.
    """
)

# Sidebar

tahun = st.sidebar.selectbox("Pilih Tahun", [2011, 2012])

# Filter data berdasarkan tahun yang dipilih
filtered_data = df[df['dteday'].dt.year == tahun]

# ---- Bar Plot: Hubungan Jumlah Rental dengan Jenis Hari (Weekday) ----
st.subheader("Hubungan Jumlah Rental Dengan Jenis Hari")
weekday_rentals = df.groupby('weekday')['cnt'].sum()
weekdays = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
plt.figure(figsize=(10, 5))
plt.bar(weekdays, weekday_rentals, color='skyblue')
plt.xlabel('Jenis Hari')
plt.ylabel('Jumlah Rental')
plt.title('Hubungan Jumlah Rental Dengan Jenis Hari')
st.pyplot(plt)

st.write(
    """
    # Insight:
Berdasarkan hasil visualisasi data yang telah dilakukan cleaning,
 terungkap bahwa rental sepeda terbesar jatuh pada hari Jum'at (hari ke-5)
   disusul oleh hari Kamis dan hari Sabtu. Data Time Series dari tahun 2011 sampai 2012 menujukkan,
     bahwa total peminjaman sepeda hampir mencapai 500000 peminjaman selama 1 tahun.
    """
)





# ---- Pie Chart: Hubungan Jumlah Rental Dengan Jenis Hari Kerja ----
# ---- Agregasi Data ----
agg_df = df.groupby(by="workingday").agg({
    "cnt": ["sum", "count"]
}) 
# Mengambil kolom 'sum' dari hasil agregasi
sum_values = agg_df['cnt', 'sum']
# Membuat mapping dari workingday (0-1) ke nama hari dalam bahasa Indonesia
workingday_map = {
    0: "Hari Kerja",
    1: "Hari Libur",
}
# Mengganti nilai index 'workingday' dengan nama hari menggunakan .map()
sum_values.index = sum_values.index.map(workingday_map)
# ---- Membuat Pie Chart ----
st.subheader('Persentase Rental Pada Hari Kerja dan Hari Libur')
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(sum_values, labels=sum_values.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
ax.set_title('Persentase Rental Pada Hari Kerja (0) Dan Hari Libur (1)', fontsize=15)
# Menampilkan pie chart di Streamlit
st.pyplot(fig)

st.write(
    """
    # Insight:
Berdasarkan hasil visualisasi data yang telah dilakukan cleaning,
terungkap bahwa rental sepeda terbesar jatuh pada hari Jum'at (hari ke-5)
disusul oleh hari Kamis dan hari Sabtu. Data Time Series dari tahun 2011 sampai 2012 menujukkan,
bahwa total peminjaman sepeda hampir mencapai 500000 peminjaman selama 1 tahun.
    """
)




# ---- Bar Plot: Hubungan Jumlah Rental Dengan Faktor Cuaca (Weathersit) ----
# Melakukan agregasi data berdasarkan cuaca
agg_df = df.groupby(by="weathersit").agg({
    "cnt": ["max", "min", "sum", "count"]
})

# Mengambil kolom 'sum' dari hasil agregasi
sum_values_weather = agg_df['cnt', 'sum']

# Membuat mapping dari weather (1-4)
weather_map = {
    1: "Clear Weather",
    2: "Mist/Cloudy",
    3: "Light Snow/Rain",
    4: "Heavy Rain/Thunderstorm",
}

# Mengganti nilai index 'weathersit' dengan deskripsi cuaca menggunakan .map()
sum_values_weather.index = sum_values_weather.index.map(weather_map)

# ---- Membuat Bar Plot ----
st.subheader('Hubungan Cuaca Dengan Jumlah Rental')
plt.figure(figsize=(8, 6))
plt.bar(sum_values_weather.index, sum_values_weather, color='green')

# Menambahkan label dan judul
plt.xlabel('Jenis Cuaca (Weathersit)', fontsize=12)
plt.ylabel('Jumlah Rental Sepeda', fontsize=12)
plt.title('Hubungan Cuaca Dengan Jumlah Rental', fontsize=15)

# Menampilkan plot di Streamlit
st.pyplot(plt)

st.write(
    """
    # Insight: 
    Weathersit dapat dianalogikan sebagai skala cuaca, 
    berdasarkan keterangan pada sumber dataset (Kaggle), berikut adalah informasinya:
    weathersit :
    1: Clear, Few clouds, Partly cloudy, Partly cloudy.
    2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist.
    3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds.
    4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog.
    Insight: Pada Bar Chart, terlihat bahwa orang-orang jarang melakukan peminjaman sepeda 
    apabila nilai Weathersit adalah 3, karena faktor salju, hujan gerimis, 
    petir dan cuaca yang kurang bersahabat. 
    Peminjaman sepeda paling sering terjadi pada skala Weathersit 1, 
    dimana cuaca bersih, tanpa hujan dan salju.
    """
)




# ---- Horizontal Bar Plot: Hubungan Jumlah Rental Dengan Musim ----
# ---- Agregasi Data ----
agg_df = df.groupby(by="season").agg({
    "cnt": ["sum", "count"]
})
# Mengambil kolom 'sum' dari hasil agregasi
sum_values = agg_df['cnt', 'sum']
# ---- Membuat mapping dari season (1-4) ----
season_map = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter",
}
# Mengganti nilai index 'season' dengan nama musim menggunakan .map()
sum_values.index = sum_values.index.map(season_map)
# ---- Membuat Horizontal Bar Plot ----
st.subheader('Korelasi Rental Sepeda Dengan Musim')
plt.figure(figsize=(6, 6))
plt.barh(sum_values.index, sum_values, color='red')
# Menambahkan label dan judul
plt.xlabel('Jumlah Rental', fontsize=12)
plt.ylabel('Jenis Musim', fontsize=12)
plt.title('Korelasi Rental Sepeda Dengan Musim', fontsize=15)
# Menampilkan plot di Streamlit
st.pyplot(plt)

st.write(
    """
    # Insight: 
    Berdasarkan informasi diatas, 
    peminjaman sepeda (rental) lebih sering terjadi pada musim panas (summer)
    dan musim gugur (fall), masing-masing nilai hampir mencapai 9 x 10^6 dan lebih dari 10^6 
    peminjaman total selama tahun 2011 - 2012
    """
)




# ---- Line Chart: Jumlah Peminjaman Sepeda Sepanjang Tahun 2011 ----
# ---- Memfilter data hanya untuk tahun 2011 ----
df_2011 = df[df['dteday'].dt.year == 2011]
# ---- Melakukan agregasi ----
agg_2011 = df_2011.groupby(by="dteday").agg({
    "cnt": ["min", "max", "mean", "std", "sum", "count"]
})
# Mengambil kolom 'sum' dari hasil agregasi
sum_values_2011 = agg_2011['cnt', 'sum']
# ---- Membuat plot time series ----
st.subheader('Time Series Rental Sepeda Per Hari Selama Tahun 2012')
plt.figure(figsize=(12, 8))
plt.plot(sum_values_2011.index, sum_values_2011, color='purple', marker='o', linestyle='-', label='Total Rental')
# Menambahkan label dan judul
plt.xlabel('Rentang Tanggal Tahun 2011', fontsize=12)
plt.ylabel('Jumlah Peminjaman Per Hari', fontsize=12)
plt.title('Time Series Rental Sepeda Per Hari Selama Tahun 2011', fontsize=15)
# Format sumbu X agar lebih rapi (menampilkan tanggal dengan format bulanan)
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b-%Y'))
plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator())
# Memutar label tanggal agar lebih mudah dibaca
plt.xticks(rotation=90)
# Menambahkan grid
plt.grid(True)
# Menampilkan plot di Streamlit
st.pyplot(plt)

# ---- Tanggal Dengan Jumlah Rental Terbanyak Dan Paling Sedikit Tahun 2011 ----
# ---- Melakukan agregasi ----
agg_2012 = df_2011.groupby(by="dteday").agg({
    "cnt": ["min", "max", "mean", "std", "sum", "count"]
})
# Mengambil kolom 'sum' dari hasil agregasi
sum_values_2011 = agg_2011['cnt', 'sum']
# ---- Mengambil nilai SUM maksimal ----
max_sum_value_2011 = sum_values_2011.max()
# Mendapatkan tanggal di mana SUM maksimal terjadi
max_sum_date_2011 = sum_values_2011.idxmax()
# ---- Menghitung total nilai SUM pada tahun 2012 ----
total_sum_2011 = sum_values_2011.sum()
# ---- Mengambil nilai SUM minimal ----
min_sum_value_2011 = sum_values_2011.min()
# Mendapatkan tanggal di mana SUM minimal terjadi
min_sum_date_2011 = sum_values_2011.idxmin()
# ---- Menampilkan hasil di Streamlit ----
st.subheader("Hasil Analisis Rental Sepeda Tahun 2011")
st.write(f"Total Nilai Rental Tahun 2011: {total_sum_2011} Peminjaman")
st.write(f"Total Nilai Rental Terbesar: {max_sum_value_2011} pada tanggal: {max_sum_date_2011.date()}")
st.write(f"Total Nilai Rental Terkecil: {min_sum_value_2011} pada tanggal: {min_sum_date_2011.date()}")

st.write(
    """
    # Insight:
Berdasarkan Grafik TIME SERIES selama tahun 2011 disimpulkan hal berikut:
Total Nilai Rental Selama Tahun 2011: 1243103 Peminjaman.
Total Nilai Rental Terbesar: 6043, terjadi pada tanggal: 2011-07-04.
Total Nilai Rental Terkecil: 431, terjadi pada tanggal: 2011-01-27.
    """
)




# ---- Line Chart: Jumlah Peminjaman Sepeda Sepanjang Tahun 2012 ----
# ---- Memfilter data hanya untuk tahun 2012 ----
df_2012 = df[df['dteday'].dt.year == 2012]
# ---- Melakukan agregasi ----
agg_2012 = df_2012.groupby(by="dteday").agg({
    "cnt": ["min", "max", "mean", "std", "sum", "count"]
})
# Mengambil kolom 'sum' dari hasil agregasi
sum_values_2012 = agg_2012['cnt', 'sum']
# ---- Membuat plot time series ----
st.subheader('Time Series Rental Sepeda Per Hari Selama Tahun 2012')
plt.figure(figsize=(12, 8))
plt.plot(sum_values_2012.index, sum_values_2012, color='orange', marker='o', linestyle='-', label='Total Rental')
# Menambahkan label dan judul
plt.xlabel('Rentang Tanggal Tahun 2012', fontsize=12)
plt.ylabel('Jumlah Peminjaman Per Hari', fontsize=12)
plt.title('Time Series Rental Sepeda Per Hari Selama Tahun 2012', fontsize=15)
# Format sumbu X agar lebih rapi (menampilkan tanggal dengan format bulanan)
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b-%Y'))
plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator())
# Memutar label tanggal agar lebih mudah dibaca
plt.xticks(rotation=90)
# Menambahkan grid
plt.grid(True)
# Menampilkan plot di Streamlit
st.pyplot(plt)

# ---- Tanggal Dengan Jumlah Rental Terbanyak Dan Paling Sedikit Tahun 2012 ----
# ---- Melakukan agregasi ----
agg_2012 = df_2012.groupby(by="dteday").agg({
    "cnt": ["min", "max", "mean", "std", "sum", "count"]
})
# Mengambil kolom 'sum' dari hasil agregasi
sum_values_2012 = agg_2012['cnt', 'sum']
# ---- Mengambil nilai SUM maksimal ----
max_sum_value_2012 = sum_values_2012.max()
# Mendapatkan tanggal di mana SUM maksimal terjadi
max_sum_date_2012 = sum_values_2012.idxmax()
# ---- Menghitung total nilai SUM pada tahun 2012 ----
total_sum_2012 = sum_values_2012.sum()
# ---- Mengambil nilai SUM minimal ----
min_sum_value_2012 = sum_values_2012.min()
# Mendapatkan tanggal di mana SUM minimal terjadi
min_sum_date_2012 = sum_values_2012.idxmin()
# ---- Menampilkan hasil di Streamlit ----
st.subheader("Hasil Analisis Rental Sepeda Tahun 2012")
st.write(f"Total Nilai Rental Tahun 2012: {total_sum_2012} Peminjaman")
st.write(f"Total Nilai Rental Terbesar: {max_sum_value_2012} pada tanggal: {max_sum_date_2012.date()}")
st.write(f"Total Nilai Rental Terkecil: {min_sum_value_2012} pada tanggal: {min_sum_date_2012.date()}")

st.write(
    """
    # Insight:
Berdasarkan Grafik TIME SERIES selama tahun 2012 disimpulkan hal berikut:
Total Nilai Rental Tahun 2012: 2049576 Peminjaman. 
Total Nilai Rental Terbesar: 8714, terjadi pada tanggal: 2012-09-15. 
Total Nilai Rental Terkecil: 22, terjadi pada tanggal: 2012-10-29.
    """
)


st.write(
    """
    # Kesimpulan: 
    Rental sepeda terbesar umumnya jatuh pada hari Jum'at (hari ke-5) disusul oleh hari Kamis dan hari Sabtu,
     terutama menjelang Weekend. Data Time Series dari tahun 2011 sampai 2012 menujukkan, 
     bahwa total peminjaman sepeda mencapai hampir 500000 peminjaman selama 1 tahun, 
     terlihat bahwa orang-orang cenderung melakukan peminjaman sepeda (rental sepeda) pada hari libur (weekend)
      seperti hari sabtu dan minggu, dibandingkan dengan hari-hari kerja (weekdays). 
      Persentase peminjaman pada hari libur dan hari kerja adalah 69,6% banding 30,4%. 
      Orang-orang jarang melakukan peminjaman sepeda apabila nilai Weathersit adalah 3, karena faktor salju, 
      hujan gerimis, petir dan cuaca yang kurang bersahabat. Peminjaman sepeda paling sering terjadi pada skala Weathersit 1, 
      dimana cuaca bersih, tanpa hujan dan salju. Peminjaman sepeda (rental) lebih sering terjadi pada musim panas (summer) dan musim gugur (fall), 
      masing-masing nilai hampir mencapai 9 x 10^6 dan lebih dari 10^6 peminjaman total selama tahun 2011 - 2012. 
      Tahun 2011, rincian exploratory data adalah sebagai berikut : Total Nilai Rental Selama Tahun 2011: 1243103 Peminjaman. 
      Total Nilai Rental Terbesar: 6043, terjadi pada tanggal: 2011-07-04. 
      Total Nilai Rental Terkecil: 431, terjadi pada tanggal: 2011-01-27. Sedangkan pada tahun 2012, 
      rinciannya adalah sebagai berikut: Total Nilai Rental Tahun 2012: 2049576 Peminjaman. 
      Total Nilai Rental Terbesar: 8714, terjadi pada tanggal: 2012-09-15. 
      Total Nilai Rental Terkecil: 22, terjadi pada tanggal: 2012-10-29.
    """
)
