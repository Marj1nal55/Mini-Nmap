import socket
import html
import argparse
import os
import ssl
import requests

acik_portlar = []

parser = argparse.ArgumentParser()
parser.add_argument("ip", help="Hedef IP adresi")
parser.add_argument("--all", action="store_true", help="Tüm portları tara (1-65535)")
parser.add_argument("--top", action="store_true", help="Sadece popüler portları tara")
parser.add_argument("--baslangic", type=int, help="Başlangıç portu (özel aralık için)")
parser.add_argument("--bitis", type=int, help="Bitiş portu (özel aralık için)")
args = parser.parse_args()

POPULER_PORTLAR = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080]

if args.all:
    portlar = range(1, 65536)
elif args.top:
    portlar = POPULER_PORTLAR
elif args.baslangic and args.bitis:
    portlar = range(args.baslangic, args.bitis + 1)
else:
    print("Lütfen --all, --top ya da --baslangic/--bitis belirt")
    exit()


def cve_ara(servis_bilgisi):
    if not servis_bilgisi or servis_bilgisi.strip() == "":
        return []

    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    parametreler = {"keywordSearch": servis_bilgisi, "resultsPerPage": 3}

    try:
        cevap = requests.get(url, params=parametreler, timeout=5)
        veri = cevap.json()

        sonuclar = []
        for zafiyet in veri.get("vulnerabilities", []):
            cve_id = zafiyet["cve"]["id"]
            aciklama = zafiyet["cve"]["descriptions"][0]["value"]
            sonuclar.append((cve_id, aciklama[:150]))
        return sonuclar
    except Exception:
        return []


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


CAMGOBEGI = "\033[96m"
YESIL = "\033[92m"
SIFIRLA = "\033[0m"


def baslangic_ekrani():
    os.system("clear")
    print(CAMGOBEGI + "╔" + "=" * 48 + "╗")
    print("║" + "MINI-NMAP v1.0".center(48) + "║")
    print("║" + "Basit Port Tarayıcı & Banner Grabber".center(48) + "║")
    print("╠" + "=" * 48 + "╣")
    print("║" + f"IP: {kendi_ip_bul()}".center(48) + "║")
    print("╚" + "=" * 48 + "╝" + SIFIRLA)


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
        if port == 443:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            s = context.wrap_socket(s, server_hostname=hedef_ip)
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
dosya = open("tarama_sonucu.txt", "w")
print(f"\n{hedef_ip} taranıyor...\n")

for port in portlar:
    if port_tara(hedef_ip, port):
        print(f"[AÇIK] Port {port}")
        dosya.write(f"[AÇIK] Port {port}\n")
        acik_portlar.append(port)

        banner_yazi = banner_al(hedef_ip, port)
        if banner_yazi:
            for satir in banner_yazi.split("\n"):
                if "Server:" in satir:
                    servis_bilgisi = satir.replace("Server:", "").strip()
                    print(f"    Sunucu: {satir.strip()}")
                    dosya.write(f"    Sunucu: {satir.strip()}\n")

                    if servis_bilgisi:
                        cve_sonuclari = cve_ara(servis_bilgisi)
                        if cve_sonuclari:
                            print(f"    ⚠️  Bilinen {len(cve_sonuclari)} zafiyet bulundu:")
                            for cve_id, aciklama in cve_sonuclari:
                                print(f"       {cve_id}: {aciklama}...")
                                dosya.write(f"    {cve_id}: {aciklama}...\n")

            if "<title>" in banner_yazi:
                baslangic = banner_yazi.find("<title>") + len("<title>")
                bitis = banner_yazi.find("</title>")
                baslik = html.unescape(banner_yazi[baslangic:bitis])
                print(f"    Başlık: {baslik}")
                dosya.write(f"    Başlık: {baslik}\n")

if acik_portlar:
    tahmin = cihaz_tahmin_et(acik_portlar)
    print(f"\nCihaz tahmini: {tahmin}")
    dosya.write(f"\nCihaz tahmini: {tahmin}\n")

print("\nTarama tamamlandı.")

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

dosya.close()
