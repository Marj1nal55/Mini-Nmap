# mini-nmap

Python `socket` modülü kullanılarak sıfırdan yazılmış, basit bir port tarayıcı ve banner grabbing aracı. Nmap'in temel mantığını (port tarama + servis bilgisi toplama) anlamak amacıyla eğitim amaçlı geliştirilmiştir.

## Özellikler

- Belirtilen bir IP aralığında port tarama
- Açık portlarda HTTP banner grabbing (sunucu bilgisi ve sayfa başlığı çekme)
- HTML entity çözme (örn. `&#70;` gibi kodları okunabilir hale getirme)

## Kullanım

```bash
python mini_nmap.py
```

Program sırasıyla şunları soracak:
- Hedef IP adresi
- Başlangıç portu
- Bitiş portu

## Örnek çıktı

```
192.168.1.1 taranıyor...

[AÇIK] Port 53
[AÇIK] Port 80
    Sunucu: Server:
    Başlık: F6600

Tarama tamamlandı.
```

## Nasıl çalışıyor

1. **Port tarama:** Her port için bir socket bağlantısı denenir (`connect_ex`). Bağlantı başarılıysa (`0` dönerse) port açık kabul edilir.
2. **Banner grabbing:** Açık bulunan her port için basit bir HTTP GET isteği gönderilir, sunucudan gelen cevap okunur.
3. **Ayrıştırma (parsing):** Gelen cevap metninden `Server:` başlığı ve `<title>` etiketi aranıp çıkarılır.

## Uyarı

Bu araç yalnızca **kendi sahip olduğun veya tarama izni verilen** ağlar/cihazlar üzerinde kullanılmalıdır. Başkasına ait sistemlerde izinsiz kullanım yasa dışıdır.

## Geliştirme fikirleri (ileride eklenebilir)

- [ ] Farklı protokoller için özel bannerlar (SSH, FTP)
- [ ] Sonuçları dosyaya kaydetme
- [ ] Threading ile hızlandırma
- [ ] Komut satırı argümanları (input() yerine)

## Gereksinimler

- Python 3.x (ek kütüphane gerekmez, sadece standart kütüphane kullanılmıştır)

