import requests
from bs4 import BeautifulSoup
import json

# List untuk menyimpan hasil
data_lagu = []

# Loop dari 1 sampai 865
for nomorBN in range(1, 866):
    # Membuat URL dinamis dengan nomorBN
    url = f"https://alkitab.app/BN/{nomorBN}"
    
    # Mengirim permintaan untuk mendapatkan halaman
    response = requests.get(url)
    
    # Memeriksa apakah permintaan berhasil
    if response.status_code == 200:
        # Parsing konten HTML
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Mengambil judul
        judul_div = soup.find("div", class_="judul")
        judul = judul_div.get_text().strip() if judul_div else "Judul tidak ditemukan"
        
        # Mengambil judul asli
        judul_asli_div = soup.find("div", class_="judul_asli")
        judul_asli = judul_asli_div.get_text().strip() if judul_asli_div else "Judul asli tidak ditemukan"
        
        # Mengambil nada dasar
        nada_dasar_div = soup.find("div", class_="nadaDasar")
        nada_dasar = nada_dasar_div.get_text().strip() if nada_dasar_div else "Nada dasar tidak ditemukan"
        
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
            "nomorBN": nomorBN,
            "judul": judul,
            "judul_asli": judul_asli,
            "nada_dasar": nada_dasar,
            "baits": bait_list
        }
        
        # Tambahkan data lagu ke dalam list
        data_lagu.append(lagu)
        
        # Print informasi lagu untuk setiap iterasi (opsional)
        print(f"Lagu BN {nomorBN} - Judul: {judul}")
        
        # Simpan data setiap 20 iterasi
        if nomorBN % 20 == 0:
            try:
                # Membaca data dari file sebelumnya jika ada
                with open("data_lagu.json", "r", encoding="utf-8") as f:
                    all_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                all_data = []  # Jika file belum ada atau kosong

            # Tambahkan data baru ke data yang sudah ada
            all_data.extend(data_lagu)
            
            # Tulis kembali semua data ke file JSON
            with open("data_lagu.json", "w", encoding="utf-8") as f:
                json.dump(all_data, f, ensure_ascii=False, indent=4)
            print(f"Progress tersimpan pada iterasi {nomorBN}")
            
            # Kosongkan data_lagu untuk iterasi selanjutnya
            data_lagu = []

# Simpan data yang tersisa (jika ada) di akhir
if data_lagu:
    try:
        with open("data_lagu.json", "r", encoding="utf-8") as f:
            all_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_data = []
    
    all_data.extend(data_lagu)
    
    with open("data_lagu.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    print("Data tersisa disimpan ke file data_lagu.json")
