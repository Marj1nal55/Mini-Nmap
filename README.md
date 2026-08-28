<div align="center">

# 🔍 mini-nmap

**Python `socket` modülü ile sıfırdan yazılmış port tarayıcı ve banner grabbing aracı**

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Aktif%20Geliştirme-yellow)

</div>

---

## 📖 Hakkında

`mini-nmap`, Nmap'in temel mantığını (port tarama + servis bilgisi toplama) sıfırdan anlamak amacıyla geliştirilmiş eğitim odaklı bir araçtır. Hiçbir dış kütüphane kullanılmadan, sadece Python'un standart `socket` modülüyle yazılmıştır.

## ✨ Özellikler

| Özellik | Açıklama |
|---|---|
| 🔌 Port Tarama | Belirtilen IP aralığında açık portları tespit eder |
| 🏷️ Banner Grabbing | Açık portlarda HTTP sunucu bilgisi ve sayfa başlığı çeker |
| 🔤 HTML Decode | `&#70;` gibi HTML entity kodlarını okunabilir metne çevirir |
| 🛡️ Hata Toleransı | Bağlantı hatalarında çökmez, `try/except` ile korunur |

## 🚀 Kullanım

```bash
python mini_nmap.py
```

Program sırasıyla şunları soracak:

```
Hedef IP adresini gir: 192.168.1.1
Başlangıç portu: 1
Bitiş portu: 500
```

## 📋 Örnek Çıktı

```
192.168.1.1 taranıyor...

[AÇIK] Port 53
[AÇIK] Port 80
    Sunucu: Server:
    Başlık: F6600

Tarama tamamlandı.
```

## ⚙️ Nasıl Çalışıyor

1. **Port Tarama** — Her port için `connect_ex()` ile bağlantı denenir. `0` dönerse port açık kabul edilir.
2. **Banner Grabbing** — Açık portlara basit bir `GET / HTTP/1.1` isteği gönderilir, sunucu cevabı okunur.
3. **Ayrıştırma (Parsing)** — Cevap metninden `Server:` başlığı ve `<title>` etiketi çıkarılır.

## 🗂️ Dosya Yapısı

```
mini-nmap/
├── mini_nmap.py      # Ana araç — port tarama + banner grabbing birleşik
├── tarayici.py        # İlk versiyon — sadece port tarama
├── banner.py           # İlk versiyon — sadece banner grabbing
├── nmap_notlar.pdf     # Nmap komut/NSE script referans notları
└── README.md
```

## 🧭 Yol Haritası

- [ ] SSH, FTP gibi farklı protokoller için özel banner ayrıştırma
- [ ] Sonuçları `.txt` / `.json` dosyasına kaydetme
- [ ] `threading` ile çoklu port tarama (hız artışı)
- [ ] Komut satırı argümanları desteği (`argparse` ile `input()` yerine)
- [ ] Basit bir CVE eşleştirme (versiyon bilgisine göre bilinen açık arama)

## ⚠️ Sorumluluk Reddi

Bu araç yalnızca **kendi sahip olduğun veya tarama izni verilen** ağlar/cihazlar üzerinde kullanılmalıdır. Başkasına ait sistemlerde izinsiz kullanım suçtur.

## 🧰 Gereksinimler

- Python 3.x
- Ek kütüphane gerekmez (sadece standart kütüphane)

---

<div align="center">

Geliştiren: [Marj1nal55](https://github.com/Marj1nal55) · Öğrenme amaçlı geliştirilmektedir 🌱

</div>
