import time
from datetime import datetime, timedelta

jadwal = {}

# Warna ANSI
BIRU = "\033[94m"
HIJAU = "\033[92m"
KUNING = "\033[93m"
MERAH = "\033[91m"
PUTIH = "\033[97m"
BOLD = "\033[1m"
BLINK = "\033[5m"
RESET = "\033[0m"

def bersihkan_layar():
    print("\033[H\033[2J", end="")

def tampilkan_jam_realtime():
    return datetime.now().strftime("%H:%M:%S")

def menu():
    bersihkan_layar()
    print(f"{BIRU}{BOLD}════════════════════════════════════════════════════{RESET}")
    print(f"{PUTIH}{BOLD}       🕒 PENGINGAT JADWAL HARIAN ZIFBY DEVS 🕒         {RESET}")
    print(f"{BIRU}{BOLD}════════════════════════════════════════════════════{RESET}")
    print(f"{KUNING}Waktu sekarang: {BOLD}{tampilkan_jam_realtime()}{RESET}   📅 {datetime.now().strftime('%d %B %Y')}")
    print()
    print(f"{HIJAU}1. ➕ Tambah Jadwal")
    print(f"2. 📋 Lihat Jadwal")
    print(f"3. 🗑  Hapus Jadwal")
    print(f"4. 🚨 Mulai Pengingat (Real-time + Notif 5 menit sebelum)")
    print(f"5. 🚪 Keluar{RESET}")
    print(f"{BIRU}{BOLD}════════════════════════════════════════════════════{RESET}")
    return input(f"{PUTIH}Pilih menu (1-5): {RESET}")

def tambah_jadwal():
    while True:
        bersihkan_layar()
        print(f"{HIJAU}{BOLD}➕ TAMBAH JADWAL BARU{RESET}\n")
        jam = input("Masukkan jam (HH:MM, contoh 07:30): ").strip()
        if len(jam) != 5 or jam[2] != ':' or not jam.replace(':', '').isdigit():
            print(f"{MERAH}Format salah! Gunakan HH:MM{RESET}")
            time.sleep(1.5)
            continue
        if int(jam[:2]) > 23 or int(jam[3:]) > 59:
            print(f"{MERAH}Jam atau menit tidak valid!{RESET}")
            time.sleep(1.5)
            continue
        break

    kegiatan = input("Masukkan kegiatan: ").strip()
    jadwal[jam] = kegiatan
    print(f"\n{HIJAU}✅ Jadwal '{BOLD}{kegiatan}{RESET}{HIJAU}' pada pukul {BOLD}{jam}{RESET}{HIJAU} berhasil ditambahkan!{RESET}")
    time.sleep(2)

def lihat_jadwal():
    bersihkan_layar()
    print(f"{HIJAU}{BOLD}📋 DAFTAR JADWAL HARI INI{RESET}\n")
    if not jadwal:
        print(f"{KUNING}Belum ada jadwal. Silakan tambah dulu!{RESET}")
    else:
        for i, (jam, keg) in enumerate(sorted(jadwal.items()), 1):
            print(f"{PUTIH}{i:2}. {BOLD}{jam}{RESET} → {keg}")
    print(f"\n{KUNING}Tekan Enter untuk kembali...{RESET}")
    input()

def hapus_jadwal():
    bersihkan_layar()
    print(f"{MERAH}{BOLD}🗑 HAPUS JADWAL{RESET}\n")
    if not jadwal:
        print(f"{KUNING}Tidak ada jadwal untuk dihapus.{RESET}")
        time.sleep(2)
        return
    lihat_jadwal()
    jam = input(f"\n{MERAH}Ketik jam yang ingin dihapus (HH:MM): {RESET}").strip()
    if jam in jadwal:
        hapus = jadwal.pop(jam)
        print(f"\n{MERAH}🗑 Jadwal '{BOLD}{hapus}{RESET}{MERAH}' pada {jam} telah dihapus!{RESET}")
    else:
        print(f"{MERAH}❌ Jadwal pada {jam} tidak ditemukan!{RESET}")
    time.sleep(2)

def beep():
    print('\a', end='')

def mulai_pengingat():
    bersihkan_layar()
    print(f"{HIJAU}{BOLD}🚨 PENGINGAT SEDANG BERJALAN 🚨{RESET}")
    print(f"{KUNING}Tekan CTRL + C untuk berhenti kapan saja.\n{RESET}")

    sudah_diingatkan = set()

    try:
        while True:
            sekarang = datetime.now()

            print(f"\r{KUNING}⏰ Waktu sekarang: {BOLD}{sekarang.strftime('%H:%M:%S')}{RESET}  |  Tekan CTRL+C untuk keluar", end="")

            for jam_jadwal, kegiatan in jadwal.items():
                try:
                    waktu_jadwal = datetime.strptime(jam_jadwal, "%H:%M")
                    waktu_jadwal = sekarang.replace(
                        hour=waktu_jadwal.time().hour,
                        minute=waktu_jadwal.time().minute,
                        second=0,
                        microsecond=0
                    )
                except:
                    continue

                if waktu_jadwal - timedelta(minutes=5) <= sekarang < waktu_jadwal:
                    key = f"5menit_{jam_jadwal}"
                    if key not in sudah_diingatkan:
                        bersihkan_layar()
                        print(f"{BLINK}{KUNING}{BOLD}⚠  5 MENIT LAGI! ⚠{RESET}")
                        print(f"{KUNING}Pukul {jam_jadwal} → {BOLD}{kegiatan}{RESET}")
                        for _ in range(6):
                            beep()
                            time.sleep(0.5)
                        sudah_diingatkan.add(key)

                if abs((sekarang - waktu_jadwal).total_seconds()) < 60:
                    key = f"tepat_{jam_jadwal}"
                    if key not in sudah_diingatkan:
                        bersihkan_layar()
                        print(f"{BLINK}{MERAH}{BOLD}🔔 WAKTUNYA SEKARANG! 🔔{RESET}")
                        print(f"{MERAH}{BOLD}⏰ {jam_jadwal} → {kegiatan.upper()}{RESET}")
                        for _ in range(10):
                            beep()
                            time.sleep(0.3)
                        sudah_diingatkan.add(key)

            time.sleep(0.5)

    except KeyboardInterrupt:
        bersihkan_layar()
        print(f"{HIJAU}✅ Pengingat dihentikan. Kembali ke menu...{RESET}")
        time.sleep(2)

# ========== MAIN LOOP ==========
if __name__ == "__main__":
    while True:
        pilihan = menu()
        if pilihan == "1":
            tambah_jadwal()
        elif pilihan == "2":
            lihat_jadwal()
        elif pilihan == "3":
            hapus_jadwal()
        elif pilihan == "4":
            if not jadwal:
                bersihkan_layar()
                print(f"{KUNING}⚠  Belum ada jadwal! Tambah dulu ya.{RESET}")
                time.sleep(2)
            else:
                mulai_pengingat()
        elif pilihan == "5":
            bersihkan_layar()
            print(f"{HIJAU}{BOLD}Sampai jumpa lagi, Razif! Semangat hari ini! 🌟{RESET}")
            time.sleep(2)
            break
        else:
            print(f"{MERAH}Pilihan tidak valid!{RESET}")
            time.sleep(1.5)
