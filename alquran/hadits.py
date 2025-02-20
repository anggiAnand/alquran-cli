import requests
import re
from alquran.config import API_HADITH_URL, RANGE_PATTERN


def get_hadits_list():
    """Mengambil daftar buku hadits dari API"""
    response = requests.get(f"{API_HADITH_URL}/books")
    return response.json()


def get_hadits(id_hadits, nomor_hadits):
    """Mengambil riwayat hadits sesuai dengan id nya (tirmidzi, muslim, dsb)"""
    response = requests.get(f"{API_HADITH_URL}/books/{id_hadits}/{nomor_hadits}")
    return response.json()


def get_hadits_range(id_hadits, range_nomor):
    """Mengambil riwayat hadits sesuai dengan id dan berdasarkan range nya"""
    response = requests.get(f"{API_HADITH_URL}/books/{id_hadits}?range={range_nomor}")
    return response.json()


def daftar_hadith():
    """Menampilkan daftar riwayat-riwayat hadits"""
    hadits = get_hadits_list()
    data = hadits["data"]
    if hadits["code"] != 200 or hadits["error"] is True:
        print(hadits["message"])
        return False
    return data


def lihat_hadith(id_hadits, nomor_hadits, range=None):
    """Memberikan isi dari sebuah hadits berdasarkan spesifikasi"""
    if range:
        range = re.findall(RANGE_PATTERN, range)
        if len(range) == 0:
            print("Invalid range pattern")
            return False

        hadits = get_hadits_range(id_hadits, range[0])
        if hadits["code"] == 400 and hadits["error"] is True:
            print("Tidak bisa >300 range (Masalah performa)")
            return False
        if hadits["code"] == 404 and hadits["error"] is True:
            print(hadits["message"])
            return False
        data = hadits["data"]
        return data
    else:
        if not nomor_hadits:
            print("Nomor hadits tidak boleh kosong kecuali range diberikan")
            return False
        hadits = get_hadits(id_hadits, nomor_hadits)
        if hadits["code"] == 404 and hadits["error"] is True:
            print(hadits["message"])
            return False
        data = hadits["data"]
        return data
