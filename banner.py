import socket
import html 

def banner_al(hedef_ip, hedef_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect((hedef_ip, hedef_port))

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

    banner_yazi = banner.decode(errors="ignore")

    for satir in banner_yazi.split("\n"):
        if "Server:" in satir:
            print("Sunucu bilgisi:", satir)

    if "<title>" in banner_yazi:
        baslangic = banner_yazi.find("<title>") + len("<title>")
        bitis = banner_yazi.find("</title>")
        baslik = banner_yazi[baslangic:bitis]
        baslik_temiz = html.unescape(baslik)
        print("Sayfa başlığı:", baslik_temiz)
    else:
        print("Title bulunamadı (veri eksik gelmiş olabilir)")

hedef_ip = input("IP adresini gir: ")
hedef_port = int(input("Port numarasını gir: "))
banner_al(hedef_ip, hedef_port)
