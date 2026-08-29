import socket
import html

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


hedef_ip = input("Hedef IP adresini gir: ")
baslangic_port = int(input("Başlangıç portu: "))
bitis_port = int(input("Bitiş portu: "))
dosya = open("tarama_sonucu.txt", "w")
print(f"\n{hedef_ip} taranıyor...\n")

for port in range(baslangic_port, bitis_port + 1):
    if port_tara(hedef_ip, port):
        print(f"[AÇIK] Port {port}")
        dosya.write(f"[AÇIK] Port {port}\n")

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
print("\nTarama tamamlandı.")
dosya.close()
