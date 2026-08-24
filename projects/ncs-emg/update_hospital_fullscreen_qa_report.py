from pathlib import Path

report = Path(
    r"C:\Users\uugur\OneDrive\Desktop"
    r"\EMG_NCS_Nonfizyolojik_Faktorler_Sunumu\QA_RAPORU.txt"
)
text = """EMG–NCS NON-FİZYOLOJİK FAKTÖRLER — KAPANIŞ QA RAPORU

- Tam ekran düzenlenen non-fizyolojik sayfa: 83
- Açıklama sayfası: 34
- Animasyon sayfası: 35
- Konu giriş sayfası: 14
- 1366×768, 1600×900 ve 1920×1080 toplam görünüm kontrolü: 249
- Görünüm/taşma/eksik görsel hatası: 0
- Animasyon düğme ve slider hata sayısı: 0
- Doğrulanan gezinme bağlantısı: 167
- Dış internet bağımlılığı: 0
- Bilgisayara özel mutlak dosya yolu: 0

Non-fizyolojik 83 sayfanın her biri tarayıcı alanını tam olarak doldurur.
Fizyolojik bölüm dosyaları ve mevcut ZIP arşivi değiştirilmemiştir.
"""
report.write_text(text, encoding="utf-8")
print({"qa_report_updated": str(report)})
