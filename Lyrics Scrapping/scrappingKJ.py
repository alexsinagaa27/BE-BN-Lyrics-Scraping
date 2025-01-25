import requests # untuk send request dan recieve respons dari website tertentu
from bs4 import BeautifulSoup # untuk parsing HTML agar dapat mengekstrak elemen tertentu
import json # format umum untuk menyimpan data dalam bentuk semi-structured

# List untuk menyimpan hasil
data_lagu = []

# Loop dari 1 sampai 478
for nomorKJ in range(1, 479):
    # Membuat URL dinamis dengan nomorKJ
    url = f"https://alkitab.app/KJ/{nomorKJ}"
    
    # Mengirim permintaan untuk mendapatkan halaman
    response = requests.get(url)
    
    # Memeriksa apakah permintaan berhasil
    if response.status_code == 200:
        # Parsing konten HTML
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Mengambil judul
        judul_div = soup.find("div", class_="judul")
        judul = judul_div.get_text().strip() if judul_div else "Judul tidak ditemukan"
        
        # Mengambil nada dasar
        nadaDasar_div = soup.find("div", class_="nadaDasar")
        nadaDasar = nadaDasar_div.get_text().strip() if nadaDasar_div else "Nada Dasar tidak ditemukan"

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
            "nomorKJ": nomorKJ,
            "judul": judul,
            "baits": bait_list
        }
        
        # Tambahkan data lagu ke dalam list
        data_lagu.append(lagu)
        
        # Print informasi lagu untuk setiap iterasi (opsional)
        print(f"{nomorKJ} - Judul: {judul}")
        
        # Simpan data setiap 25 iterasi
        if nomorKJ % 25 == 0:
            try:
                # Membaca data dari file sebelumnya jika ada
                with open("data_laguKJ.json", "r", encoding="utf-8") as f:
                    all_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                all_data = []  # Jika file belum ada atau kosong

            # Tambahkan data baru ke data yang sudah ada
            all_data.extend(data_lagu)
            
            # Tulis kembali semua data ke file JSON
            with open("data_laguKJ.json", "w", encoding="utf-8") as f:
                json.dump(all_data, f, ensure_ascii=False, indent=4)
            print(f"Progress tersimpan pada iterasi {nomorKJ}")
            
            # Kosongkan data_lagu untuk iterasi selanjutnya
            data_lagu = []

# Simpan data yang tersisa (jika ada) di akhir
if data_lagu:
    try:
        with open("data_laguKJ.json", "r", encoding="utf-8") as f:
            all_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_data = []
    
    all_data.extend(data_lagu)
    
    with open("data_laguKJ.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    print("Data tersisa disimpan ke file data_laguKJ.json")
