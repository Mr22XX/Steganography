import numpy as np
from PIL import Image

def EmbeddingPesan(cover, pesan, stego):
    # Baca citra cover
    citra = Image.open(cover)
    if citra.mode != 'RGB':
        print("ERROR: Citra harus dalam format RGB")
        return
    
    larik_pixel = np.array(citra)
    tinggi, lebar, _ = larik_pixel.shape

    # Tambahkan delimiter untuk menandai akhir pesan
    pesan += "stego"

    # Ubah pesan ke dalam biner
    pesan_biner = ''.join([format(ord(i), "08b") for i in pesan])
    jumlah_pixel_embed = len(pesan_biner)

    # Periksa apakah ukuran cukup untuk menampung pesan
    total_kapasitas = tinggi * lebar * 3  # Karena ada 3 channel (RGB)
    if jumlah_pixel_embed > total_kapasitas:
        print("ERROR: Ukuran citra tidak cukup untuk menyisipkan pesan")
        return

    # Penyisipan bit pada LSB setiap byte pixel
    index = 0
    for i in range(tinggi):
        for j in range(lebar):
            for k in range(3):  # R, G, B
                if index < jumlah_pixel_embed:
                    # Ganti LSB dengan bit pesan
                    larik_pixel[i, j, k] = (larik_pixel[i, j, k] & 0b11111110) | int(pesan_biner[index])
                    index += 1

    # Simpan gambar stego
    stego_image = Image.fromarray(larik_pixel.astype('uint8'))
    stego_image.save(stego)
    print("Penyisipan pesan ke dalam citra berhasil!")

def EkstraksiPesan(stego):
    # Baca citra stego
    citra = Image.open(stego)
    if citra.mode != 'RGB':
        print("ERROR: Citra harus dalam format RGB")
        return

    larik_pixel = np.array(citra)
    tinggi, lebar, _ = larik_pixel.shape
    bit_pesan = ""

    # Ekstraksi bit LSB dari setiap pixel
    for i in range(tinggi):
        for j in range(lebar):
            for k in range(3):  # R, G, B
                bit_pesan += str(larik_pixel[i, j, k] & 1)  # Ambil bit terakhir

    # Konversi bit ke karakter ASCII
    bit_pesan = [bit_pesan[i:i+8] for i in range(0, len(bit_pesan), 8)]
    
    try:
        pesan = ''.join([chr(int(b, 2)) for b in bit_pesan])
    except ValueError:
        print("ERROR: Data tidak dapat dikonversi menjadi teks!")
        return

    # Ambil hanya hingga delimiter "stego"
    if "stego" in pesan:
        pesan = pesan.split("stego")[0]
        print("Pesan yang diekstrak:", pesan)
    else:
        print("ERROR: Pesan tidak ditemukan atau rusak!")

def ProgramSteganografi():
    print("-- Steganografi pada Citra Digital --")
    print("1: Penyisipan pesan")
    print("2: Ekstraksi pesan")
    
    pilih = input("Pilih opsi: ")
    if pilih == '1':
        cover = input("Masukkan nama citra cover (termasuk ekstensi, contoh: gambar.jpg): ")
        pesan = input("Ketikkan pesan yang akan disisipkan: ")
        stego = input("Masukkan nama citra output (stego image, contoh: stego.png): ")
        print("Penyisipan pesan...")
        EmbeddingPesan(cover, pesan, stego)

    elif pilih == '2':
        stego = input("Masukkan nama citra stego (contoh: stego.png): ")
        print("Ekstraksi pesan...")
        EkstraksiPesan(stego)

    else:
        print("Pilihan salah")

# Jalankan program
ProgramSteganografi()
