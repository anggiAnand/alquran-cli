# Alquran CLI
CLI Sederhana untuk mengambil isi-isi surah al-Quran dan tafsirnya serta riwayat-riwayat hadits.

## Instalasi
Cara 1 :
```bash
pip install alquran-cli
```
Cara 2 :
```bash
git clone https://github.com/anggiAnand/alquran-cli.git

cd alquran-cli

pip install .
```
Cara 3 :
```bash
pip install git+https://github.com/anggiAnand/alquran-cli
```

## General Usage
Untuk menggunakan command bisa dapat dengan.
```python
>>> import alquran.core as alquran

>>> # Cari hadith
>>> alquran.lihat_hadith("tirmidzi", 1) # Memberikan raw response
{'name': 'HR. Tirmidzi', 'id': 'tirmidzi', ...}
>>>
>>> # Atau dengan range
>>> alquran.lihat_hadith("tirmidzi", 1, "1-2")
{'name': 'HR. Tirmidzi', 'id': 'tirmidzi', 'available': 3625, 'requested': 2, 'hadiths': [{'number': 1, ...}, {'number': 2, ...}]}
>>>
>>> # Isi Surah
>>> alquran.isi_surah(1) # Memberikan tuple dimana index 0 adalah detail surah dan index 1 adalah isi surah yang terfilter (Jika memberikan argument ayat)
({'nomor': 1, 'nama': 'الفاتحة', 'namaLatin': 'Al-Fatihah', 'jumlahAyat': 7, 'tempatTurun': 'Mekah', 'arti': 'Pembukaan' ...}, [{'nomorAyat': 1, 'teksArab': 'بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ', 'teksLatin': 'bismillāhir-raḥmānir-raḥīm(i).', 'teksIndonesia': 'Dengan nama Allah Yang Maha Pengasih, Maha Penyayang.', ...}])
```

## CLI Usage
Jika sudah install dari pip
```bash
alquran --help
```
Jika tidak
```bash
pip install requirements.txt

python3 alquran/alquran.py --help
```
