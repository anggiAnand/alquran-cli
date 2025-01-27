import click
import re
import requests
import shutil

API_BASE_URL = "https://equran.id/api/v2"
API_HADITH_URL = "https://api.hadith.gading.dev"
RANGE_PATTERN = r"\d+-\d+"

def get_surah_list():
    """Mengambil daftar surah dari API."""
    response = requests.get(f"{API_BASE_URL}/surat")
    return response.json()["data"]

def get_surah_details(nomor):
    """Mengambil detail surah dari API berdasarkan nomor surah."""
    response = requests.get(f"{API_BASE_URL}/surat/{nomor}")
    return response.json()["data"]

def get_tafsir_details(nomor):
    """Mengambil detail tafsir dari API berdasarkan nomor surah."""
    response = requests.get(f"{API_BASE_URL}/tafsir/{nomor}")
    return response.json()["data"]

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

@click.group()
def cli():
    """CLI Al-Quran."""
    pass

@cli.group()
def surah():
    """Kategori : Surah - Surah Al-Qur'an"""
    pass

@cli.group()
def hadits():
    """Kategori : Riwayat - Riwayat Hadits"""
    pass

@hadits.command()
def daftar_hadits():
    """Menampilkan daftar riwayat-riwayat hadits"""
    hadits = get_hadits_list()
    data = hadits["data"]
    if hadits["code"] != 200 or hadits["error"] == True:
        click.echo(hadits["message"])
        return
    for idx, riwayat in enumerate(data, start=1):
        click.echo(f"{idx}. {riwayat['name']} | 1 - {riwayat['available']} ({riwayat['id']})")

@hadits.command()
@click.argument("id_hadits")
@click.argument("nomor_hadits", required=False, type=int)
@click.option(
    "--range",
    default=None,
    help="Range dari beberapa hadits tertentu, contoh --range 1-3"
)
def lihat_hadits(id_hadits, nomor_hadits, range):
    """Memberikan isi dari sebuah hadits berdasarkan spesifikasi"""
    if range:
        range = re.findall(RANGE_PATTERN, range)
        if len(range) == 0:
            click.echo("Invalid range pattern")
            return

        hadits = get_hadits_range(id_hadits, range[0])
        if hadits["code"] == 400 and hadits["error"] == True:
            click.echo("Tidak bisa >300 range (Masalah performa)")
            return
        data = hadits["data"]
        click.echo("-" * shutil.get_terminal_size().columns+"\n")    
        for hadith in data["hadiths"]:
            click.echo(f"“{hadith['arab']}”\n")
            click.echo(f" “{hadith['id']}” - {data['name']} ({hadith['number']})\n")
            click.echo("-" * shutil.get_terminal_size().columns+"\n")
    else:
        if not nomor_hadits:
            click.echo("Nomor hadits tidak boleh kosong kecuali range diberikan")
            return
        hadits = get_hadits(id_hadits, nomor_hadits)
        if hadits["code"] == 404 and hadits["error"] == True:
            click.echo(hadits["message"])
            return
        data = hadits["data"]
        click.echo("-" * shutil.get_terminal_size().columns+"\n")
        click.echo(f"“{data['contents']['arab']}”\n")
        click.echo(f" “{data['contents']['id']}” - {data['name']} ({data['contents']['number']})")
        click.echo("\n" + "-" * shutil.get_terminal_size().columns)

@surah.command()
def daftar_surah():
    """Menampilkan daftar surah dalam Al-Quran."""
    surahs = get_surah_list()
    for surah in surahs:
        click.echo(f"{surah['nomor']}. {surah['nama']} ({surah['namaLatin']}) - {surah['jumlahAyat']} Ayat")

@surah.command()
@click.argument("nomor_surah", type=int)
def detail_surah(nomor_surah):
    """Menampilkan detail surah berdasarkan nomor surah."""
    if nomor_surah > 114:
      click.echo("Al-Quran hanya berisi sebanyak 114 surah")
      return
    surah = get_surah_details(nomor_surah)
    click.echo(f"Surah: {surah['nama']} ({surah['namaLatin']})")
    click.echo(f"Jumlah Ayat: {surah['jumlahAyat']}")
    click.echo(f"Tempat Turun: {surah['tempatTurun']}")
    click.echo(f"Arti: {surah['arti']}")
    click.echo(f"Deskripsi: {surah['deskripsi'].replace('<i>', '').replace('</i>', '').replace('<br>', '').replace('</br>', '')}")
    # click.echo("\nAudio:")
    # for key, audio in surah['audioFull'].items():
    #     click.echo(f"  Reciter {key}: {audio}")

@surah.command()
@click.argument("nomor_surah", type=int)
@click.option(
    "--ayat",
    default=None,
    help="Filter ayat tertentu sesuai rentang, contoh --ayat 5 / --ayat 2-5",
)
def isi_surah(nomor_surah, ayat):
    """Memberikan isi bacaan ayat ayat berdasarkan nomor surah"""
    if nomor_surah > 114:
      click.echo("Al-Quran hanya berisi sebanyak 114 surah")
      return
    surah = get_surah_details(nomor_surah)
    ayat_ayat = surah["ayat"]

    # Jika ada opsi ayat, filter ayat yang sesuai
    if ayat != None:
        ayat_filter = []
        for bagian in ayat.split(","):
            if "-" in bagian:
                start, end = bagian.split("-")
                ayat_filter.extend(
                    range(int(start), int(end) + 1)
                )
            else:
                ayat_filter.append(int(bagian))
        ayat_ayat = [
            ayat for ayat in ayat_ayat if int(ayat["nomorAyat"]) in ayat_filter
        ]
    if not ayat_ayat:
      click.echo("Ayat tidak tersedia seperti filter")
      return
    click.echo(f"{surah['namaLatin']} {surah['nomor']}:1-{surah['jumlahAyat']} ({surah['nama']})\n")
    for ayah in ayat_ayat:
      click.echo(f" “{ayah['teksArab']}”")
      click.echo(f"{ayah['teksLatin']} ({ayah['nomorAyat']})\n")
    click.echo("Terjemahan : ")
    for ayah in ayat_ayat:
      click.echo(f"{ayah['nomorAyat']}. {ayah['teksIndonesia']}")
      click.echo("-" * shutil.get_terminal_size().columns)

@surah.command()
@click.argument("nomor_surah", type=int)
def tafsir_surah(nomor_surah):
    """Menampilkan tafsir untuk surah berdasarkan nomor surah."""
    if nomor_surah > 114:
      click.echo("Al-Quran hanya berisi sebanyak 114 surah")
      return
    tafsir_data = get_tafsir_details(nomor_surah)
    click.echo(f"Tafsir untuk Surah {tafsir_data['nama']} ({tafsir_data['namaLatin']}):")
    for tafsir in tafsir_data['tafsir']:
        click.echo(f"Ayat {tafsir['ayat']} - {tafsir['teks']}")

if __name__ == "__main__":
    cli()
