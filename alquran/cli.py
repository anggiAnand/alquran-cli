import click
from alquran.hadits import lihat_hadith, daftar_hadith
from alquran.surah import isi_surat, detail_surat, tafsir_surat, daftar_surat

@click.group()
def cli():
  """CLI Al-Quran."""
  pass

@cli.group()
def hadits():
  """Kategori : Surah - Surah Al-Qur'an"""
  pass

@cli.group()
def surah():
  """Kategori : Riwayat - Riwayat Hadits"""
  pass

@hadits.command()
def daftar_hadits():
  """Menampilkan daftar riwayat-riwayat hadits"""
  data = daftar_hadits()
  if data is False:
    return
  for idx, riwayat in enumerate(data, start=1):
    click.echo(f"{idx}. {riwayat['name']} | 1 - {riwayat['available']} ({riwayat['id']})")

@hadits.command()
@click.argument("id_hadits")
@click.argument("nomor_hadits", type=int)
@click.option(
    "--range",
    default=None,
    help="Range dari beberapa hadits tertentu, contoh --range 1-3",
)
def lihat_hadits(id_hadits, nomor_hadits, range):
  """Memberikan isi dari sebuah hadits berdasarkan spesifikasi"""
  data = lihat_hadith(id_hadits, nomor_hadits, range)
  if data is False:
    return
  if range:
    click.echo("-" * shutil.get_terminal_size().columns+"\n")
    for hadith in data["hadiths"]:
      click.echo(f"“{hadith['arab']}”\n")
      click.echo(f" “{hadith['id']}” - {data['name']} ({hadith['number']})\n")
      click.echo("-" * shutil.get_terminal_size().columns+"\n")
  else:
    click.echo("-" * shutil.get_terminal_size().columns+"\n")
    click.echo(f"“{data['contents']['arab']}”\n")
    click.echo(f" “{data['contents']['id']}” - {data['name']} ({data['contents']['number']})")
    click.echo("\n" + "-" * shutil.get_terminal_size().columns)

@surah.command()
def daftar_surah():
  """Menampilkan daftar surah dalam Al-Quran"""
  surahs = daftar_surat()
  if surahs is False:
    return
  for surah in surahs:
        print(f"{surah['nomor']}. {surah['nama']} ({surah['namaLatin']}) - {surah['jumlahAyat']} Ayat")

@surah.command()
@click.argument("nomor_surah", type=int)
def detail_surah(nomor_surah):
  """Menampilkan detail surah berdasarkan nomor surah"""
  surah = detail_surat(nomor_surah)
  if surah is False:
    return
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
  res = isi_surat(nomor_surah, ayat)
  if res is False:
    return
  surah = res[0]
  ayat_ayat = res[1]
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
  """Menampilkan tafsir untuk surah berdasarkan nomor surah"""
  tafsir_data = tafsir_surat(nomor_surah)
  if tafsir_data is False:
    return
  click.echo(f"Tafsir untuk Surah {tafsir_data['nama']} ({tafsir_data['namaLatin']}):")
  for tafsir in tafsir_data['tafsir']:
    click.echo(f"Ayat {tafsir['ayat']} - {tafsir['teks']}")
