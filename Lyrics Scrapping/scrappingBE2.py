import requests
from bs4 import BeautifulSoup
import json

# Daftar nomor lagu yang ingin diambil
nomor_lagu = [568, 597, 603, 637, 738, 796]
versi_lagu = ['A', 'B']  # Versi yang akan dicari

# List untuk menyimpan hasil
data_lagu = []

# Fungsi untuk melakukan scraping satu lagu
def scraping_lagu(nomorBE, versi):
    url = f"https://alkitab.app/BE/{nomorBE}{versi}"  # URL lagu
    response = requests.get(url)  # Mengirim permintaan untuk mendapatkan halaman
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Mengambil judul
        judul_div = soup.find("div", class_="judul")
        judul = judul_div.get_text().strip() if judul_div else "Judul tidak ditemukan"
        
        # Mengambil lirik per bait
        bait_list = []
        bait_divs = soup.find_all("div", class_="bait")
        for bait in bait_divs:
            # Ambil nomor bait
            bait_no_div = bait.find("div", class_="bait-no")
            bait_no = bait_no_div.get_text().strip() if bait_no_div else "Tidak ada nomor bait"
            
            # Ambil semua baris dalam bait
            baris_lirik = [baris.get_text().strip() for baris in bait.find_all("div", class_="baris")]
            
            # Gabungkan nomor bait dan liriknya
            bait_list.append({
                "nomor_bait": bait_no,
                "lirik": baris_lirik
            })
        
        # Menyimpan data dalam dictionary
        lagu = {
            "nomorBE": nomorBE,
            "versi": versi,
            "judul": judul,
            "baits": bait_list
        }
        
        return lagu  # Mengembalikan data lagu
    else:
        print(f"Gagal mengakses {url}: {response.status_code}")
        return None

# Mengambil data untuk setiap nomor dan versi
for nomorBE in nomor_lagu:
    lagu_found = False  # Flag untuk menandai apakah lagu ditemukan
    for versi in versi_lagu:
        lagu = scraping_lagu(nomorBE, versi)
        if lagu:
            data_lagu.append(lagu)
            print(f"{nomorBE}{versi} - Judul: {lagu['judul']}")
            lagu_found = True  # Tandai bahwa lagu ditemukan
        else:
            print(f"Tidak ditemukan lagu untuk nomor {nomorBE}{versi}.")
    
    if not lagu_found:
        print(f"Tidak ditemukan lagu untuk nomor {nomorBE} versi A dan B.")

# Menyimpan data ke dalam file JSON
with open("data_laguBE2.json", "w", encoding="utf-8") as f:
    json.dump(data_lagu, f, ensure_ascii=False, indent=4)

print("Data lagu berhasil disimpan dalam 'data_laguBE2.json'.")

# Menampilkan data yang diambil
for lagu in data_lagu:
    print(f"{lagu['nomorBE']}{lagu['versi']}")
    print(f"Judul: {lagu['judul']}")
    print("Lirik:")
    for bait in lagu['baits']:
        print(f"{bait['nomor_bait']}:")
        for baris in bait['lirik']:
            print(baris)
    print("\n" + "-" * 40 + "\n")  # Pemisah antar lagu
