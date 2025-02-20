from alquran.hadits import get_hadits, get_hadits_list, get_hadits_range, daftar_hadith, lihat_hadith
from alquran.surah import get_surah_details, get_surah_list, get_tafsir_details, daftar_surat, isi_surat, detail_surat, tafsir_surat
from alquran.config import API_HADITH_URL, API_SURAH_URL, RANGE_PATTERN
from alquran.utils.version import check_package_update

check_package_update("alquran-cli")
