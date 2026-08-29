import socket
import html
import argparse
import os


acik_portlar = []

parser = argparse.ArgumentParser()
parser.add_argument("ip",  help="Taranacak hedef IP adresi")
parser.add_argument("baslangic", type=int, help="Taranmanın başlayacağı port numarası")
parser.add_argument("bitis", type=int, help="Taramanın biteceği port numarası")
args = parser.parse_args()

def cihaz_tahmin_et(portlar):
    portlar_seti = set(portlar)

    if {8008, 8009, 8443}.issubset(portlar_seti):
        return "Muhtemelen bir Chromecast/Google Cast cihazı"
    if {135, 445, 3389}.issubset(portlar_seti):
        return "Muhtemelen bir Windows cihazı"
    if {22} <= portlar_seti and 80 in portlar_seti:
        return "Muhtemelen bir Linux sunucu/cihaz"
    if 53 in portlar_seti and 80 in portlar_seti:
        return "Muhtemelen bir router/modem"

    return "Cihaz türü tahmin edilemedi"


def kendi_ip_bul():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "Bulunamadı"
    finally:
        s.close()
    return ip


def baslangic_ekrani():
    os.system("clear")
    print("=" * 40)
    print("            MINI-NMAP v1.0")
    print("   Basit Port Tarayici & Banner Graber")
    print(f"     Senin İP adresin {kendi_ip_bul()}")
    print("=" * 40)
def port_tara(hedef_ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    sonuc = s.connect_ex((hedef_ip, port))
    s.close()
    return sonuc == 0


def banner_al(hedef_ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((hedef_ip, port))

        istek = f"GET / HTTP/1.1\r\nHost: {hedef_ip}\r\n\r\n"
        s.send(istek.encode())

        banner = b""
        while True:
            try:
                parca = s.recv(4096)
                if not parca:
                    break
                banner += parca
            except socket.timeout:
                break

        s.close()
        return banner.decode(errors="ignore")
    except Exception:
        return None

baslangic_ekrani()
hedef_ip = args.ip
baslangic_port = args.baslangic
bitis_port = args.bitis
dosya = open("tarama_sonucu.txt", "w")
print(f"\n{hedef_ip} taranıyor...\n")

for port in range(baslangic_port, bitis_port + 1):
    if port_tara(hedef_ip, port):
        print(f"[AÇIK] Port {port}")
        dosya.write(f"[AÇIK] Port {port}\n")
        acik_portlar.append(port)
        banner_yazi = banner_al(hedef_ip, port)
        if banner_yazi:
            for satir in banner_yazi.split("\n"):
                if "Server:" in satir:
                    print(f"    Sunucu: {satir.strip()}")
                    dosya.write(f"   Sunucu: {satir.strip()}\n")
            if "<title>" in banner_yazi:
                baslangic = banner_yazi.find("<title>") + len("<title>")
                bitis = banner_yazi.find("</title>")
                baslik = html.unescape(banner_yazi[baslangic:bitis])
                print(f"    Başlık: {baslik}")
                dosya.write(f"   Başlık: {baslik}\n")
if acik_portlar:
    tahmin = cihaz_tahmin_et(acik_portlar)
    print(f"\nCihaz tahmini: {tahmin}")
    dosya.write(f"\nCihaz tahmini: {tahmin}\n")

while True:
    print("\nNe yapmak istersin?")
    print("1) Belirli bir portu tekrar detaylı tara")
    print("2) Sonuçları tekrar göster")
    print("3) Çıkış")
 
    secim = input("Seçimin (1/2/3): ")

    if secim == "1":
        secilen_port = int(input("Hangi portu detaylı taramak istersin? "))
        banner_yazi = banner_al(hedef_ip, secilen_port)
        if banner_yazi:
            print(banner_yazi)
        else:
            print("Bu porttan banner alınamadı.")

    elif secim == "2":
        print("\nAçık portlar:", acik_portlar)
        print("Cihaz tahmini:", cihaz_tahmin_et(acik_portlar))

    elif secim == "3":
        print("Çıkılıyor...")
        break

    else:
        print("Geçersiz seçim, tekrar dene.")

print("\nTarama tamamlandı.")
dosya.close()
