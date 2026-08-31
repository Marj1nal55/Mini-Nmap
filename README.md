<div align="center">

# 🔍 mini-nmap

**Python `socket` modülü ile sıfırdan yazılmış port tarayıcı, banner grabbing ve zafiyet tarama aracı**

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Aktif%20Geliştirme-yellow)

</div>

---

## 📖 Hakkında

`mini-nmap`, Nmap'in temel mantığını (port tarama, servis tespiti, zafiyet araştırması) sıfırdan anlamak amacıyla geliştirilmiş, eğitim odaklı bir siber güvenlik aracıdır. Sadece Python'un standart kütüphanesi (`socket`, `ssl`, `argparse`, `html`, `os`) ve tek bir dış kütüphane (`requests`) kullanılarak yazılmıştır.

Bu proje gerçek Nmap'in yerini tutmaz — amacı, port tarama araçlarının **arka planda nasıl çalıştığını** satır satır öğrenmektir.

## ✨ Özellikler

| Özellik | Açıklama |
|---|---|
| 🔌 Port Tarama | Belirtilen aralıkta açık portları tespit eder |
| 🏷️ Banner Grabbing | Açık portlarda HTTP sunucu bilgisi ve sayfa başlığı çeker |
| 🔒 SSL/HTTPS Desteği | 443 portunda şifreli bağlantı kurup gerçek banner alır |
| 🔤 HTML Decode | `&#70;` gibi HTML entity kodlarını okunabilir metne çevirir |
| 🛡️ Hata Toleransı | Bağlantı hatalarında çökmez, `try/except` ile korunur |
| 💾 Sonuç Kaydı | Tarama sonuçlarını `tarama_sonucu.txt` dosyasına kaydeder |
| ⌨️ CLI Desteği | `argparse` ile Nmap tarzı komut satırı kullanımı (`--all`, `--top`, özel aralık) |
| 🌐 Kendi IP Gösterimi | Programı çalıştırdığın anda bulunduğun ağ IP'sini gösterir |
| 🧠 Cihaz Tahmini | Açık port kalıplarına bakarak cihaz türü tahmini yapar |
| 🔎 CVE Sorgusu | Bulunan servis bilgisini NVD (National Vulnerability Database) üzerinden gerçek zamanlı sorgular |
| 📋 Etkileşimli Menü | Tarama sonrası tekrar detaylı tarama, özet görüntüleme veya çıkış seçeneği sunar |
| 🎨 Terminal Arayüzü | Kutu çizgileri ve renkli çıktı ile okunabilir, "araç" hissi veren ekran |

## 🚀 Kurulum

```bash
pip install requests
git clone https://github.com/Marj1nal55/mini-nmap.git
cd mini-nmap
```

## 🚀 Kullanım

```bash
# Popüler portları tara
python mini_nmap.py <hedef_ip> --top

# Tüm portları tara (1-65535, uzun sürebilir)
python mini_nmap.py <hedef_ip> --all

# Özel port aralığı
python mini_nmap.py <hedef_ip> --baslangic 1 --bitis 500
```

**Örnek:**
```bash
python mini_nmap.py 192.168.1.1 --top
```

**Yardım ekranı:**
```bash
python mini_nmap.py --help
```

## 📋 Örnek Çıktı

```
╔================================================╗
║                 MINI-NMAP v1.0                 ║
║      Basit Port Tarayıcı & Banner Grabber       ║
╠================================================╣
║               IP: 192.168.1.12                  ║
╚================================================╝

192.168.1.1 taranıyor...

[AÇIK] Port 53
[AÇIK] Port 80
    Sunucu: Server:
    Başlık: F6600
[AÇIK] Port 443
    Sunucu: Server:
    Başlık: F6600

Cihaz tahmini: Muhtemelen bir router/modem

Tarama tamamlandı.

Ne yapmak istersin?
1) Belirli bir portu tekrar detaylı tara
2) Sonuçları tekrar göster
3) Çıkış
Seçimin (1/2/3):
```

**Bilinen bir zafiyeti olan bir servis bulunursa:**
```
[AÇIK] Port 80
    Sunucu: Server: Apache/2.4.49
    ⚠️  Bilinen 2 zafiyet bulundu:
       CVE-2021-41773: A flaw was found in a change made to path normalization...
       CVE-2021-42013: It was found that the fix for CVE-2021-41773...
```

## ⚙️ Nasıl Çalışıyor

1. **Kendi IP Tespiti** — UDP soketiyle sahte bir bağlantı denemesi yapılarak işletim sisteminin kullandığı yerel IP okunur.
2. **Port Tarama** — Her port için `connect_ex()` ile bağlantı denenir. `0` dönerse port açık kabul edilir.
3. **SSL El Sıkışması** — Port 443 ise, önce `ssl.wrap_socket()` ile şifreli bir katman kurulur, sonra istek gönderilir.
4. **Banner Grabbing** — Açık portlara `GET / HTTP/1.1` isteği gönderilir, sunucu cevabı döngüyle (parça parça) okunur.
5. **Ayrıştırma (Parsing)** — Cevap metninden `Server:` başlığı ve `<title>` etiketi çıkarılır, HTML entity'ler çözülür.
6. **CVE Sorgusu** — `Server:` başlığından elde edilen servis bilgisi, NVD'nin REST API'sine gönderilir; dönen sonuçlar listelenir.
7. **Cihaz Tahmini** — Bulunan açık portların kümesi, bilinen port kalıplarıyla (örn. `{8008, 8009, 8443}` → Chromecast) karşılaştırılır.
8. **Sonuç Kaydı** — Her adım aynı anda hem ekrana hem `tarama_sonucu.txt` dosyasına yazılır.
9. **Etkileşimli Menü** — Tarama bitince kullanıcı döngü içinde tekrar tarama yapabilir, özet görebilir veya çıkabilir.

## 🗂️ Dosya Yapısı

```
mini-nmap/
├── mini_nmap.py       # Ana araç — tüm özellikler birleşik
├── tarayici.py         # İlk versiyon — sadece port tarama
├── banner.py            # İlk versiyon — sadece banner grabbing
├── nmap_notlar.pdf      # Nmap komut/NSE script referans notları
├── requirements.txt      # Gerekli dış kütüphaneler
└── README.md
```

## 🧭 Yol Haritası

- [x] Sonuçları dosyaya kaydetme
- [x] Komut satırı argümanları (`argparse`)
- [x] Basit cihaz tahmini
- [x] Etkileşimli sonuç menüsü
- [x] SSL/HTTPS desteği
- [x] CVE/zafiyet sorgusu (NVD API entegrasyonu)
- [x] Görsel terminal arayüzü
- [ ] SSH, FTP gibi farklı protokoller için özel banner ayrıştırma
- [ ] `threading` ile çoklu port tarama (hız artışı)
- [ ] UDP port tarama desteği
- [ ] Sonuçları `.json` formatında da kaydetme

## ⚠️ Sorumluluk Reddi

Bu araç yalnızca **kendi sahip olduğun veya tarama izni verilen** ağlar/cihazlar üzerinde kullanılmalıdır. Başkasına ait sistemlerde izinsiz kullanım suçtur. CVE sorgusu özelliği yalnızca bilgilendirme amaçlıdır; bulunan zafiyetleri istismar etmek (exploit) bu aracın kapsamı ve amacı dışındadır.

## 🧰 Gereksinimler

- Python 3.x
- `requests` kütüphanesi (`pip install requests`)
- İnternet bağlantısı (CVE sorgusu için)

---

<div align="center">

Geliştiren: [Marj1nal55](https://github.com/Marj1nal55) · Öğrenme amaçlı geliştirilmektedir 🌱

</div>

