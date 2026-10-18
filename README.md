# Uğurcan Uğur — Clinical Neurology Portfolio

> **Ekim 2026:** Bu portföy ana siteyle birleşti. Tek adres: <https://www.ucugur.workers.dev>. Bu depodaki sayfalar eski bağlantılar çalışmaya devam etsin diye korunuyor; eski katalog sayfası `arsiv.html`.

Bu depo, Uğurcan Uğur'un halka açık nöroloji eğitim materyallerinin kalıcı ve sürümlü arşividir. Etkileşimli HTML sunumları, medikal animasyonları, gerekli görselleri ve videoları içerir.

## Canlı adresler

- Kişisel site ve aranabilir kütüphane: <https://www.ucugur.workers.dev/library>
- GitHub Pages arşivi: <https://canathustra.github.io/clinical-neurology-portfolio/>
- Neurophysiology Lab: <https://www.ucugur.workers.dev/lab>

GitHub bu projenin kaynak ve yedek katmanıdır. `www.ucugur.workers.dev` ise ziyaretçiler için düzenlenmiş ana giriş ve katalogdur.

## Yayındaki koleksiyonlar

| Koleksiyon | Kapsam | Giriş |
|---|---|---|
| NCS teknik faktörler | 19 konu girişi; artefaktlar, kayıt ve ölçüm | [Aç](projects/ncs-emg/animations/index.html) |
| GBS / AIDP | Klinik, BOS, elektrodiagnostik ve prognoz | [Aç](projects/gbs-aidp/index.html) |
| MUAP görsel atlası | 121 slaytlık interaktif sunum | [Aç](projects/muap-ready-slides/index.html) |
| MUAP analizi | Şekil ve videolarla interaktif bölüm | [Aç](projects/muap-analysis/index.html) |
| Kuantal deplesyon | Nöromüsküler bileşke animasyonu | [Aç](projects/ach-animation/nmj-deplesyon.html) |
| Blink refleksi | Mekanizma videosu | [Aç](projects/yeni-video/ugurcan-animasyon.mp4) |

## Yayın ilkeleri

- Hasta bilgisi, klinik kayıt veya kimliği belirlenebilir veri yayımlanmaz.
- Kaynak kitapların PDF kopyaları depoya eklenmez; yalnızca bibliyografik atıf tutulur.
- Yalnızca paylaşım hakkı bulunan görseller ve videolar halka açık sürüme eklenir.
- Taslak, QA ve üretim dosyaları ziyaretçi kataloğunda gösterilmez.
- Yeni bir materyal eklenince hem bu arşivdeki giriş yolu hem de kişisel sitedeki `/library` kataloğu güncellenir.

## Yerel kullanım

Depoyu indirdikten sonra kökteki `index.html` dosyasını açabilir veya basit bir statik HTTP sunucusu kullanabilirsin:

```sh
git clone https://github.com/canathustra/clinical-neurology-portfolio.git
cd clinical-neurology-portfolio
python -m http.server 8000
```

Ardından [http://localhost:8000](http://localhost:8000) adresini aç. Materyaller GitHub Pages üzerinde doğrudan HTML, CSS ve JavaScript olarak çalışacak biçimde paketlenmiştir.

Bu içerikler yalnızca eğitim amaçlıdır; klinik değerlendirme, tanı veya tedavi kararının yerine geçmez.

## Depo düzeni

- [index.html](index.html): ziyaretçi kataloğu ve koleksiyon girişleri.
- [projects/](projects/): HTML sunumlar, animasyonlar ve gerekli medya.
- [assets/](assets/), [styles.css](styles.css), [script.js](script.js): ortak görünüm ve gezinme.
- [scripts/](scripts/): yayın ve doğrulama araçları.

## İlgili projeler

- [Neurophysiology Lab](https://github.com/canathustra/neuroedx-lab): sentetik sinyallerle EMG/NCS eğitim simülatörü ve bağımsız MUAP sunumu.
- [AFV Benchmark](https://github.com/canathustra/afv-benchmark): keşif amaçlı EEG alfa frekansı araştırma yazılımı.
- [Clinical Neurology Animations](https://github.com/canathustra/clinical-neurology-animations): henüz uygulama içermeyen başlangıç deposu; yayımlanmış animasyonlar bu portföyde bulunur.

## İçerik hakları

Bu depoda genel bir açık kaynak lisansı tanımlanmamıştır. Her materyalin kaynak ve kullanım koşullarını kontrol et; üçüncü taraf görsel ve videolar için özgün hak sahiplerinin koşulları geçerlidir.
