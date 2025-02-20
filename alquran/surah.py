import requests
from alquran.config import API_SURAH_URL


def get_surah_list():
    """Mengambil daftar surah dari API."""
    response = requests.get(f"{API_SURAH_URL}/surat")
    return response.json()["data"]


def get_surah_details(nomor):
    """Mengambil detail surah dari API berdasarkan nomor surah."""
    response = requests.get(f"{API_SURAH_URL}/surat/{nomor}")
    return response.json()["data"]


def get_tafsir_details(nomor):
    """Mengambil detail tafsir dari API berdasarkan nomor surah."""
    response = requests.get(f"{API_SURAH_URL}/tafsir/{nomor}")
    return response.json()["data"]


def daftar_surat():
    """Menampilkan daftar surah dalam Al-Quran."""
    surahs = get_surah_list()
    return surahs


def detail_surat(nomor_surah):
    """Menampilkan detail surah berdasarkan nomor surah."""
    if nomor_surah > 114:
        print("Al-Quran hanya berisi sebanyak 114 surah")
        return False
    surah = get_surah_details(nomor_surah)
    return surah


def isi_surat(nomor_surah, ayat=None):
    """Memberikan isi bacaan ayat ayat berdasarkan nomor surah"""
    if nomor_surah > 114:
        print("Al-Quran hanya berisi sebanyak 114 surah")
        return False
    surah = get_surah_details(nomor_surah)
    ayat_ayat = surah["ayat"]

    # Jika ada opsi ayat, filter ayat yang sesuai
    if ayat is not None:
        ayat_filter = []
        for bagian in ayat.split(","):
            if "-" in bagian:
                start, end = bagian.split("-")
                ayat_filter.extend(range(int(start), int(end) + 1))
            else:
                ayat_filter.append(int(bagian))
        ayat_ayat = [
            ayat for ayat in ayat_ayat if int(ayat["nomorAyat"]) in ayat_filter
        ]
    if not ayat_ayat:
        print("Ayat tidak tersedia seperti filter")
        return False
    return (surah, ayat_ayat)


def tafsir_surat(nomor_surah):
    """Menampilkan tafsir untuk surah berdasarkan nomor surah."""
    if nomor_surah > 114:
        print("Al-Quran hanya berisi sebanyak 114 surah")
        return False
    tafsir_data = get_tafsir_details(nomor_surah)
    return tafsir_data
