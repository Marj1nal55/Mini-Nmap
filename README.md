<div align="center">

# 🔍 mini-nmap

**Python `socket` modülü ile sıfırdan yazılmış port tarayıcı ve banner grabbing aracı**

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Aktif%20Geliştirme-yellow)

</div>

---

## 📖 Hakkında

`mini-nmap`, Nmap'in temel mantığını (port tarama + servis bilgisi toplama) sıfırdan anlamak amacıyla geliştirilmiş eğitim odaklı bir araçtır. Hiçbir dış kütüphane kullanılmadan, sadece Python'un standart kütüphanesiyle (`socket`, `argparse`, `html`, `os`) yazılmıştır.

## ✨ Özellikler

| Özellik | Açıklama |
|---|---|
| 🔌 Port Tarama | Belirtilen IP aralığında açık portları tespit eder |
| 🏷️ Banner Grabbing | Açık portlarda HTTP sunucu bilgisi ve sayfa başlığı çeker |
| 🔤 HTML Decode | `&#70;` gibi HTML entity kodlarını okunabilir metne çevirir |
| 🛡️ Hata Toleransı | Bağlantı hatalarında çökmez, `try/except` ile korunur |
| 💾 Sonuç Kaydı | Tarama sonuçlarını `tarama_sonucu.txt` dosyasına kaydeder |
| ⌨️ CLI Desteği | `argparse` ile Nmap tarzı komut satırı kullanımı |
| 🌐 Kendi IP Gösterimi | Programı çalıştırdığın anda bulunduğun ağ IP'sini gösterir |
| 🧠 Cihaz Tahmini | Açık port kalıplarına bakarak cihaz türü tahmini yapar (router, Chromecast, Linux/Windows cihazı vb.) |
| 📋 Etkileşimli Menü | Tarama sonrası tekrar detaylı tarama, özet görüntüleme veya çıkış seçeneği sunar |

## 🚀 Kullanım

```bash
python mini_nmap.py <hedef_ip> <baslangic_portu> <bitis_portu>
```

**Örnek:**
```bash
python mini_nmap.py 192.168.1.1 1 500
```

**Yardım ekranı:**
```bash
python mini_nmap.py --help
```

## 📋 Örnek Çıktı

```
========================================
      MINI-NMAP v1.0
   Basit Port Tarayıcı & Banner Graber
   Senin İP adresin: 192.168.1.12
========================================

192.168.1.1 taranıyor...

[AÇIK] Port 53
[AÇIK] Port 80
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

## ⚙️ Nasıl Çalışıyor

1. **Kendi IP Tespiti** — UDP soketiyle sahte bir bağlantı denemesi yapılarak işletim sisteminin kullandığı yerel IP okunur.
2. **Port Tarama** — Her port için `connect_ex()` ile bağlantı denenir. `0` dönerse port açık kabul edilir.
3. **Banner Grabbing** — Açık portlara basit bir `GET / HTTP/1.1` isteği gönderilir, sunucu cevabı döngüyle (parça parça) okunur.
4. **Ayrıştırma (Parsing)** — Cevap metninden `Server:` başlığı ve `<title>` etiketi çıkarılır, HTML entity'ler çözülür.
5. **Cihaz Tahmini** — Bulunan açık portların kümesi, bilinen port kalıplarıyla (`{8008, 8009, 8443}` → Chromecast gibi) karşılaştırılır.
6. **Sonuç Kaydı** — Her adım aynı anda hem ekrana hem `tarama_sonucu.txt` dosyasına yazılır.
7. **Etkileşimli Menü** — Tarama bitince kullanıcı döngü içinde tekrar tarama yapabilir, özet görebilir veya çıkabilir.

## 🗂️ Dosya Yapısı

```
mini-nmap/
├── mini_nmap.py       # Ana araç — tüm özellikler birleşik
├── tarayici.py         # İlk versiyon — sadece port tarama
├── banner.py            # İlk versiyon — sadece banner grabbing
├── nmap_notlar.pdf      # Nmap komut/NSE script referans notları
└── README.md
```

## 🧭 Yol Haritası

- [x] Sonuçları dosyaya kaydetme
- [x] Komut satırı argümanları (`argparse`)
- [x] Basit cihaz tahmini
- [x] Etkileşimli sonuç menüsü
- [ ] SSH, FTP gibi farklı protokoller için özel banner ayrıştırma
- [ ] `threading` ile çoklu port tarama (hız artışı)
- [ ] Sonuçları `.json` formatında da kaydetme
- [ ] Basit bir CVE eşleştirme (versiyon bilgisine göre bilinen açık arama)

## ⚠️ Sorumluluk Reddi

Bu araç yalnızca **kendi sahip olduğun veya tarama izni verilen** ağlar/cihazlar üzerinde kullanılmalıdır. Başkasına ait sistemlerde izinsiz kullanım suçtur.

## 🧰 Gereksinimler

- Python 3.x
- Ek kütüphane gerekmez (sadece standart kütüphane: `socket`, `argparse`, `html`, `os`)

---

<div align="center">

Geliştiren: [Marj1nal55](https://github.com/Marj1nal55) · Öğrenme amaçlı geliştirilmektedir 🌱

</div>

