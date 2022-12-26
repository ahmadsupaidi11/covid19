import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import requests

resp_jabar = requests.get('https://data.covid19.go.id/public/api/prov_detail_JAWA_BARAT.json')
resp = requests.get('https://data.covid19.go.id/public/api/update.json')
print(resp.headers)

covid_19 = resp.json()
print('Length of cov_id_raw: %d.' %len(covid_19))
print('komponen  cov_id_raw: %s.' %covid_19.keys())
covid19_update = covid_19['update']

print('tanggal pembaharuan dan penambahan kasus', covid19_update['penambahan']['tanggal'])
print('jumlah penduduk sembuh', covid19_update['penambahan']['jumlah_sembuh'])
print('jumlah pendidik meninggah', covid19_update['penambahan']['jumlah_meninggal'])
print('kasus positif saat ini', covid19_update['total']['jumlah_positif'])
print('jumlah total kasus meninggal', covid19_update['total']['jumlah_meninggal'])

cov_jabar = resp_jabar.json()
print('nama-nama elemen utama \n', cov_jabar.keys())
print('jumlah total kasus covid-19 di jawabarat: %d' %cov_jabar['kasus_total'])
print('persentase data keamtian covid-19 di jawabarat: %f.2%%' %cov_jabar['meninggal_persen'])
print('persentasi tingkat kesembuhan dari covid %f.2%%' %cov_jabar['sembuh_persen'])

cov_jabar = pd.DataFrame(cov_jabar['list_perkembangan'])
print('info covid_19\n', cov_jabar.info())
print(cov_jabar.head())

cov_jabar_tidy = (cov_jabar.drop(columns=[item for item in cov_jabar.columns
                                          if item.startswith('AKUMULASI')
                                          or item.startswith('dirawat')])
                    .rename(columns=str.lower)
                    .rename(columns={'kasus':'kasus_baru'})
                  )
cov_jabar_tidy['tanggal'] = pd.to_datetime(cov_jabar_tidy['tanggal']*1e6, unit='ns')
print(cov_jabar_tidy.head())

plt.clf()
fig, ax = plt.subplots(figsize=(10,5))
ax.bar(data= cov_jabar_tidy, x='tanggal', height='kasus_baru', color='salmon')
fig.suptitle('Kasus Harian Covid-19 di jabar', y=1.00, fontsize=12, fontweight='bold', ha='center')
ax.set_title('terjadi pelonjakan kasus covid 19 di awal bulan juli akiba klaster secada AD bandung', fontsize=10)
ax.set_xlabel('')
ax.set_ylabel('jumlah kasus')
ax.text(1,-0.1, 'sumber data: covid.go.id', color='blue',
        ha='right', transform =ax.transAxes)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.grid(axis='y')
plt.tight_layout()
plt.show()

plt.clf()
fig, ax = plt.subplots(figsize=(10,5))
ax.bar(data= cov_jabar_tidy, x='tanggal', height='kasus_baru', color='salmon')
fig.suptitle('Kasus Harian Covid-19 di jabar', y=1.00, fontsize=12, fontweight='bold', ha='center')
ax.set_title('terjadi pelonjakan kasus covid 19 di awal bulan juli akiba klaster secada AD bandung', fontsize=10)
ax.set_xlabel('')
ax.set_ylabel('jumlah kasus')
ax.text(1,-0.1, 'Sumber data: covid.go.id', color='blue', ha='right', transform=ax.transAxes)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.grid(axis='y')
plt.tight_layout()
plt.show()

plt.clf()
fig, ax = plt.subplots(figsize=(10,5))
ax.bar(data= cov_jabar_tidy, x='tanggal', height='sembuh', color= 'olivedrab')
ax.set_title('Kasus Harian sembuh dari covid-19 di jabar', fontsize=12)
ax.set_xlabel('')
ax.set_ylabel('Jumlah Kasus')
ax.text(1,-0.1, 'Sumber data: covid.go.id', color='blue', ha='right', transform=ax.transAxes)
ax.xaxis.set_minor_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.grid(axis='y')
plt.tight_layout()
plt.show()

cov_jabar_pekanan = (cov_jabar_tidy.set_index('tanggal')['kasus_baru']
.resample('W')
.sum()
.reset_index()
.rename(columns={'kasus_baru': 'jumlah'})
)

cov_jabar_pekanan['tahun'] = cov_jabar_pekanan['tanggal'].apply(lambda x: x.year)
cov_jabar_pekanan['pekan_ke'] = cov_jabar_pekanan['tanggal'].apply(lambda x: x.weekofyear)
cov_jabar_pekanan = cov_jabar_pekanan[['tahun','pekan_ke','jumlah']]

print('info cov_jabar_pekanan')
print(cov_jabar_pekanan.info())
print('lima data teratas cov_jabar_pekanan:', cov_jabar_pekanan.head())

cov_jabar_pekanan['jumlah_pekanlalu'] = cov_jabar_pekanan['jumlah'].shift().replace(np.nan, 0 ).astype(np.int)
cov_jabar_pekanan['lebih_baik'] = cov_jabar_pekanan['jumlah'] < cov_jabar_pekanan['jumlah_pekanlalu']
print(cov_jabar_pekanan.head(10))

plt.clf()

fig,ax = plt.subplots(figsize=(10,5))
ax.bar(data=cov_jabar_pekanan, x='pekan_ke', height='jumlah', color=['mediumseagreen' if x is True else 'salmon' for x in cov_jabar_pekanan['lebih_baik']])
fig.suptitle('kasus pekanan positif COVID-19 di jabar', y=1.00, fontsize=12, fontweight='bold', ha='center')
ax.set_title('kolom hijau menunjukkan penambahan kasus baru lebih sedikit dibandingkan satu pekan sebelumnya', fontsize=12)
ax.set_xlabel('')
ax.set_ylabel('Jumlah Kasus')
ax.text (1,-0.1, 'sumber data : covid.19.go.id', color='blue', ha='right', transform=ax.transAxes)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

cov_jabar_akumulasi = cov_jabar_tidy[['tanggal']].copy()
cov_jabar_akumulasi['akumulasi_aktif'] = (cov_jabar_tidy['kasus_baru']- cov_jabar_tidy['sembuh'] - cov_jabar_tidy['meninggal']).cumsum()
cov_jabar_akumulasi['sembuh'] = cov_jabar_tidy['sembuh'].cumsum()
cov_jabar_akumulasi['meninggal'] = cov_jabar_tidy['meninggal'].cumsum()
cov_jabar_akumulasi.tail()

plt.clf()
fig, ax = plt.subplots(figsize=(10,5))
ax.plot('tanggal', 'akumulasi_aktif', data=cov_jabar_akumulasi, lw=2)
ax.set_title('Akumulasi aktif covid-19 di jabar', fontsize=22)
ax.set_xlabel('')
ax.set_ylabel('Akumulasi Aktif')
ax.text(1,-0.1, ' sumber Data: covid.19.go.id', color='blue', ha='right', transform=ax.transAxes)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.grid(axis='y')
plt.tight_layout()
plt.show()

plt.clf()
fig, ax = plt.subplots(figsize=(10,5))
cov_jabar_akumulasi.plot(x='tanggal', kind='line', ax=ax, lw=3,
color=['salmon', 'slategrey', 'olivedrab'])

ax.set_title('Dinamika Kasus COVID-19 di Jawa Barat',
fontsize=22)
ax.set_xlabel('')
ax.set_ylabel('Akumulasi aktif')
ax.text(1, -0.1, 'Sumber data: covid.19.go.id', color='blue',
ha='right', transform=ax.transAxes)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.grid()
plt.tight_layout()
plt.show()