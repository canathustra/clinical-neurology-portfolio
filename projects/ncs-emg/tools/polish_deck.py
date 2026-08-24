from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parents[1] / "animations"


def topic(n, file, slug, title, accent, ref, subtitle, facts, items, clinical, rule, skip=False):
    return {
        "n": n,
        "file": file,
        "slug": slug,
        "title": title,
        "accent": accent,
        "ref": ref,
        "subtitle": subtitle,
        "facts": facts,
        "items": items,
        "clinical": clinical,
        "rule": rule,
        "skip": skip,
    }


TOPICS = [
    topic("01", "01_iki_kapi.html", "iki_kapi", "EDX Doğruluğunun İki Aşaması", "#126f86", "Chapter 8 giriş; Box 8.1",
          "Güvenilir EDX iki ayrı basamağa dayanır: veriyi doğru toplamak ve doğru yorumlamak.",
          [("Toplama", "Kayıt teknik olarak hatalıysa yorum doğru olamaz."), ("Yorumlama", "Doğru veri klinik soru ve paternle birlikte değerlendirilir."), ("Risk", "Tanı hatası gereksiz tetkik ve tedaviye yol açabilir.")],
          [("Temel mesaj", "EDX çalışmasının değeri doğru veri toplama ve doğru yorumlama süreçlerine bağlıdır."), ("Teknik doğruluk", "Toplanan veri teknik olarak doğru değilse aynı anda ya da daha sonra doğru yorum yapılamaz."), ("Faktörler", "Sıcaklık, yaş, elektrot impedansı, elektriksel gürültü ve filtre ayarları sonucu değiştirebilir."), ("Hata tipi", "Teknik faktör fark edilmezse normal kişiye anormal tanı konabilir ya da gerçek anormallik atlanabilir.")],
          "Her anormal bulguda önce teknik güvenilirliği sorgula; sonra patofizyolojik yoruma geç.", "Kötü veri iyi yorumla düzelmez."),
    topic("02", "02_kucuk_sinyal.html", "kucuk_sinyal", "Düşük Amplitüdlü Sinyal ve Gürültü", "#2f6fbd", "Chapter 8 giriş; Box 8.1",
          "NCS/EMG mikrovolt ve milivolt düzeyindeki sinyalleri büyütür; bu yüzden gürültü de büyür.",
          [("Sinyal", "SNAP ve spontan aktivite çok düşük amplitüdlü olabilir."), ("Amplifikasyon", "Amplifikatör biyolojik sinyali de teknik gürültüyü de yükseltir."), ("Sonuç", "Küçük teknik farklar ekranda büyük artefakt gibi görünür.")],
          [("Bioelektrik sinyal", "EDX çok küçük bioelektrik sinyalleri edinir ve amplifiye eder."), ("Teknik zorluk", "Bu işlem hassastır; fizyolojik ve nonfizyolojik faktörler verinin doğruluğunu bozabilir."), ("Gürültü", "Elektriksel gürültü küçük amplitüdlü potansiyelleri örtebilir."), ("Yaklaşım", "Sinyali yorumlamadan önce baseline, impedans, filtre ve stimülasyon koşullarını kontrol et.")],
          "SNAP küçüldüğünde ilk refleks hastalık demek değil; sinyal-gürültü oranını düşün.", "Amplifikatör seçmez; sinyal ile gürültüyü birlikte büyütür."),
    topic("03", "03_tip1_tip2.html", "tip1_tip2", "Tip I ve Tip II Hata", "#b43b47", "Chapter 8 giriş",
          "Teknik hata fark edilmezse ya olmayan hastalık tanısı konur ya da gerçek hastalık kaçırılır.",
          [("Tip I", "Normal kişiye anormal EDX sonucu verme riskidir."), ("Tip II", "Gerçek anormalliği atlama riskidir."), ("Ağırlık", "Teknik kaynaklı yalancı pozitif sonuçlar klinikte özellikle zararlıdır.")],
          [("Tip I hata", "Anormallik yokken anormal tanı koymaktır."), ("Tip II hata", "Anormallik varken bunu fark edememektir."), ("Teknik köken", "Sıcaklık, elektrot, filtre, uyarı ve ölçüm hataları iki hata tipini de yaratabilir."), ("Klinik sonuç", "Yanlış EDX tanısı gereksiz ileri tetkik, yanlış tedavi ve hasta kaygısı doğurabilir.")],
          "Şüpheli paternlerde önce teknik tekrar yapılır; rapora ancak güvenilir veri girer.", "Teknik hatayı tanımak tanı koymanın parçasıdır."),
    topic("04", "04_sicaklik_mekanizma.html", "sicaklik_mekanizma", "Sıcaklık: Sodyum Kanal İnaktivasyonu", "#126f86", "Temperature; Box 8.2",
          "Soğukta sodyum kanalı daha uzun açık kalır; depolarizasyon büyür ve uzar.",
          [("İnaktivasyon", "Soğuk inaktivasyonu geciktirir."), ("Depolarizasyon", "Daha uzun açık kanal daha fazla sodyum girişi demektir."), ("Trase", "Yanıt yavaşlar, genişler ve amplitüd artabilir.")],
          [("Mekanizma", "Sıcaklık düştüğünde sodyum kanalının inaktivasyonu yavaşlar."), ("Tek lif etkisi", "Kanal daha uzun açık kaldığı için depolarizasyon süresi uzar."), ("Bileşik potansiyel", "Liflerin daha uzun aktivitesi SNAP/CMAP morfolojisine genişlik ve amplitüd olarak yansıyabilir."), ("Yorum", "Soğuma yalnızca yavaşlatan değil, dalga formunu büyüten bir etkidir.")],
          "Yavaşlama ile birlikte amplitüd artışı görürsen sıcaklık etkisini öne al.", "Soğukta yanıt yavaşlar; aynı zamanda genişleyip büyüyebilir."),
    topic("05", "05_sicaklik_dalga_formu.html", "sicaklik_dalga_formu", "Sıcaklık: Dalga Formu", "#2f6fbd", "Fig. 8.1; Box 8.2",
          "Fig. 8.1 aynı hastada sıcaklığın dalga formunu nasıl değiştirdiğini gösterir.",
          [], [], "", "", True),
    topic("06", "06_sicaklik_faz_iptali.html", "sicaklik_faz_iptali", "Sıcaklık: Faz İptali", "#5a5fcf", "Temperature; Box 8.2",
          "Duysal yanıtlar soğumayla motordan daha belirgin büyüyebilir; temel neden faz iptalinin azalmasıdır.",
          [("SNAP", "Çok sayıda lifin zamanlamasına duyarlıdır."), ("Soğuma", "İletim yavaşlar ve potansiyel süresi uzar."), ("Sonuç", "Faz iptali azalınca duysal amplitüd belirgin artabilir.")],
          [("Bileşik yanıt", "SNAP farklı liflerden gelen potansiyellerin toplamıdır."), ("Zamanlama", "Lifler birbirine göre kaydığında pozitif ve negatif fazlar kısmen birbirini söndürür."), ("Soğuk etkisi", "Soğukta dalga formu genişler; bazı durumlarda faz iptali azalır ve amplitüd artar."), ("Motor-duysal fark", "Bu amplitüd artışı duysal yanıtlarda CMAP’a göre daha belirgin olabilir.")],
          "Soğuk ekstremitede büyük SNAP hastalığı dışlamaz; önce sıcaklığı normalize et.", "Soğukta duysal amplitüd artışı fizyolojik bir sıcaklık etkisi olabilir."),
    topic("07", "07_sicaklik_tuzak.html", "sicaklik_tuzak", "Sıcaklık: Soğuma Tuzağı", "#b56a20", "Temperature; Fig. 8.1; Box 8.2",
          "Soğuk ekstremite yavaş iletim üretebilir; yanlış yorum demiyelinizan hastalık izlenimi verebilir.",
          [("Yavaş", "CV düşer ve DL uzar."), ("Büyük", "Amplitüd ve süre artabilir."), ("Tuzak", "Yavaşlama tek başına patoloji değildir.")],
          [("Beklenen kombinasyon", "Soğuma ile hız düşer, distal latans uzar, amplitüd ve süre artabilir."), ("Yanlış alarm", "Sadece yavaş CV’ye bakmak demiyelinizasyon varmış gibi düşündürebilir."), ("Ayırıcı nokta", "Yavaş ama büyük/geniş yanıt sıcaklık etkisi lehinedir."), ("Kontrol", "Ekstremite sıcaklığını ölçmeden sınırda yavaşlamayı patolojik kabul etme.")],
          "Raporlamadan önce ekstremite sıcaklığı ve gerekirse ısıtma sonrası tekrar kayıt belirtilir.", "Yavaş + büyük yanıt önce soğumayı düşündürür."),
    topic("08", "08_sicaklik_isinma.html", "sicaklik_isinma", "Sıcaklık: Isınma Gecikmesi", "#c56f1c", "Fig. 8.2",
          "Deri sıcaklığının yükselmesi sinir sıcaklığının hemen normale döndüğü anlamına gelmez.",
          [("Deri", "Hızlı ısınabilir."), ("Sinir", "Daha yavaş ısınır."), ("Zaman", "Soğuk ekstremitede 15-20 dakika gerekebilir.")],
          [("Figür mesajı", "Isıtma sonrası sinir iletim hızının limit değere ulaşması zaman alır."), ("Klinik anlam", "Deri termometresi normale dönse bile sinir hâlâ soğuk olabilir."), ("Tibial/sural", "Derin ve yüzeyel sinirlerde ısınma süresi farklılık gösterebilir."), ("Uygulama", "Ölçüm güvenilir değilse yeterli ısıtma süresi sonrası kaydı tekrarla.")],
          "Özellikle ayak ve bacak çalışmalarında hızlı yüzey ısıtmasıyla yetinme.", "Deri ısındı diye sinirin ısındığını varsayma."),
    topic("09", "09_yas.html", "yas", "Yaş ve Normal Değerler", "#2f7653", "Age",
          "Yaş, normal değerleri değiştirir; aynı sayı farklı yaşta farklı anlam taşır.",
          [("Yenidoğan", "CV erişkinden belirgin yavaştır."), ("Olgunlaşma", "Miyelinizasyonla hız artar."), ("Yaşlılık", "Amplitüdler ve hızlar yaşla azalabilir.")],
          [("Çocukluk", "Sinir iletim hızları doğumda düşüktür ve miyelinizasyonla artar."), ("Erişkinlik", "Normal aralık yaş grubuna göre değerlendirilmelidir."), ("Yaşlılık", "Duyusal amplitüdlerde azalma yaşla daha sık görülür."), ("Referans", "Çalışmayı yaşa uygun laboratuvar referanslarıyla yorumla.")],
          "Aynı SNAP amplitüdü genç erişkinde patolojik, ileri yaşta kabul edilebilir olabilir.", "Normal değer yaşsız yorumlanmaz."),
    topic("10", "10_boy.html", "boy", "Boy ve Sinir İletim Hızı", "#3f7d8a", "Height",
          "Uzun ekstremitede sinir segmenti daha uzun ve çoğu zaman iletim hızı daha düşüktür.",
          [("Boy", "Özellikle alt ekstremite iletimini etkiler."), ("Mesafe", "Uzun sinirde distal segment etkisi artar."), ("Yorum", "Uzun boy sınırda yavaş CV yaratabilir.")],
          [("Temel ilişki", "Boy arttıkça özellikle alt ekstremite sinir iletim hızları düşme eğilimindedir."), ("Fizyolojik neden", "Daha uzun ekstremite ve distal segment özellikleri ölçülen hızı etkiler."), ("Klinik risk", "Uzun hastada sınırda yavaş hız yanlışlıkla patoloji sanılabilir."), ("Referans", "Boy etkisini dikkate alan normal değerler tercih edilmelidir.")],
          "Peroneal, tibial ve sural çalışmalarda uzun boyu yorumun içine kat.", "Boy arttıkça özellikle bacak sinirlerinde hız daha düşük olabilir."),
    topic("11", "11_proksimal_distal.html", "proksimal_distal", "Proksimal ve Distal Segmentler", "#6a5acd", "Physiologic factors",
          "Aynı sinirde distal ve proksimal segmentlerin iletim özellikleri aynı olmayabilir.",
          [("Distal", "Sıcaklık ve teknik ölçüm hatasına daha duyarlı olabilir."), ("Proksimal", "Segment uzunluğu ve anatomi farklıdır."), ("Tuzak", "Segment farkı tek başına fokal lezyon değildir.")],
          [("Segment farkı", "Sinir boyunca ölçülen hız tüm segmentlerde aynı olmak zorunda değildir."), ("Distal etki", "Distal segmentler sıcaklık ve teknik ölçüm hatalarından daha fazla etkilenebilir."), ("Karşılaştırma", "Fokal yavaşlama kararı segmentin normal beklentisiyle karşılaştırılarak verilir."), ("Ölçüm", "Mesafe, sıcaklık ve elektrot pozisyonu segment karşılaştırmasında sabit tutulmalıdır.")],
          "Bir segment yavaşsa önce ölçüm koşullarını ve beklenen segment farkını kontrol et.", "Aynı sinirde segmentler arası hız farkı fizyolojik olabilir."),
    topic("12", "12_impedans_60hz.html", "impedans_60hz", "Elektrot İmpedansı ve 60 Hz Gürültü", "#126f86", "Fig. 8.3-8.5; Box 8.3",
          "Diferansiyel amplifikasyon ancak G1 ve G2 aynı gürültüyü gördüğünde gürültüyü bastırır.",
          [("G1-G2", "Amplifikatör iki giriş arasındaki farkı büyütür."), ("İmpedans", "Eşitsizlik ortak mod reddini bozar."), ("60 Hz", "Sinüzoidal gürültü küçük potansiyelleri örtebilir.")],
          [("Diferansiyel kayıt", "G2’deki sinyal G1’den çıkarılır ve fark amplifiye edilir."), ("Ortak mod reddi", "Aynı gürültü iki elektrotta da eşitse çıkarma işlemi gürültüyü azaltır."), ("Uyumsuzluk", "Elektrot impedansı farklıysa aynı çevresel gürültü iki girişte farklı voltaj oluşturur."), ("Düzeltme", "Cildi hazırla, jel kullan, aynı tip elektrot kullan ve kabloları sağlam tut.")],
          "Fibrilasyon ya da küçük SNAP ararken 60 Hz gürültü önce temizlenmelidir.", "İki elektrot aynı gürültüyü görmüyorsa amplifikatör gürültüyü de büyütür."),
    topic("13", "13_filtreler.html", "filtreler", "Filtreler ve Passband", "#2f6fbd", "Fig. 8.7-8.9",
          "Filtreler istenmeyen frekansları azaltır; yanlış ayar sinyalin kendisini de değiştirir.",
          [("Passband", "Sinyalin geçmesine izin verilen frekans aralığıdır."), ("High cut", "Azaltılırsa yüksek frekans içeriği kaybolur."), ("Low cut", "Artırılırsa yavaş bileşenler bastırılır.")],
          [("Spektrum", "EDX dalga formları tek frekans değil, frekans spektrumundan oluşur."), ("Filtreleme", "Passband dışındaki frekanslar azaltılır."), ("SNAP etkisi", "High-frequency filtre çok düşürülürse SNAP amplitüdü ve şekli değişebilir."), ("Standartlaştırma", "Karşılaştırılan çalışmalar aynı filtre ayarlarıyla yapılmalıdır.")],
          "Filtreyle gürültüyü azaltırken ölçtüğün amplitüdü de değiştirdiğini unutma.", "Filtre gürültüyü azaltabilir; ama sinyali de yeniden şekillendirir."),
    topic("14", "14_elektronik_ortalama.html", "elektronik_ortalama", "Elektronik Ortalama ve Sinyal-Gürültü Oranı", "#2f7653", "Fig. 8.10",
          "Tekrarlanan sabit yanıtlar ortalamada korunur; rastgele gürültü azalır.",
          [("Sinyal", "Uyarıya zaman kilitlidir."), ("Gürültü", "Rastgele fazdadır."), ("Ortalama", "Sinyal-gürültü oranını artırır.")],
          [("Tek uyarı", "Küçük SNAP baseline gürültüsü içinde zor seçilebilir."), ("Tekrar", "Aynı uyarı ile sinyal aynı zamanda gelir."), ("Ortalama", "Rastgele gürültü birbirini azaltırken zaman kilitli potansiyel belirginleşir."), ("Sınır", "Ortalama teknik hatayı düzeltmez; sadece rastgele gürültüyü azaltır.")],
          "Düşük amplitüdlü duysal yanıtta ortalama kullan; ancak sistematik artefaktı ortalama ile maskeleme.", "Ortalama rastgele gürültüyü azaltır, sistematik hatayı düzeltmez."),
    topic("15", "15_stimulus_artefakti.html", "stimulus_artefakti", "Stimulus Artefaktı ve Anot Pozisyonu", "#b56a20", "Fig. 8.11-8.13; Box 8.4",
          "Stimulus artefaktı başlangıç latansı ve amplitüd ölçümünü bozabilir; anodu küçük açılarla çevirmek baseline’ı düzeltebilir.",
          [("Artefakt", "Yanıtın başlangıcını örtebilir."), ("Anot", "Katot sabitken anot yönü değiştirilebilir."), ("Baseline", "Daha temiz baseline ölçümü güvenilir yapar.")],
          [("Ölçüm hatası", "Büyük negatif stimulus artefaktı amplitüdü düşük, onset latansı uzun gösterebilir."), ("Anodu yürütme", "Katot yerinde tutulurken anot hafifçe çevrilerek artefakt azaltılabilir."), ("Topraklama", "Toprak elektrot stimülatör ve kayıt elektrotları arasına yerleştirilir."), ("Kablolar", "Koaksiyel kablo ve yakın kayıt uçları stimulus artefaktını azaltabilir.")],
          "Artefakt dalganın başlangıcına karışıyorsa ölçümden önce baseline’ı düzelt.", "Katot siniri uyarır; anodu artefaktı azaltmak için yürüt."),
    topic("16", "16_kutup_tersligi.html", "kutup_tersligi", "Stimülatör Polaritesi: Katot-Anot Tersliği", "#b43b47", "Fig. 8.14-8.16",
          "Stimülatör katodu G1’e bakmalıdır; terslik anodal blok ve yapay yavaşlama yaratabilir.",
          [("Katot", "Depolarizasyon önce katot altında başlar."), ("Anot", "Altındaki segment hiperpolarize olabilir."), ("Terslik", "Yanıt gecikir veya bloklanabilir.")],
          [("Doğru yön", "İletim hızı hesabında mesafe G1 ile katot arasında ölçülür."), ("Ters bağlantı", "Katot G1’den uzağa bakarsa etkin uyarı noktası değişir."), ("Anodal blok", "Anot altındaki hiperpolarizasyon impulsun ilerlemesini engelleyebilir."), ("Sonuç", "Latans uzar ve iletim hızı olduğundan yavaş hesaplanabilir.")],
          "Beklenmedik yavaşlama varsa stimülatör polaritesini ve katodun yönünü kontrol et.", "Siyah katot G1’e bakar; ters yön yapay yavaşlama yaratır."),
    topic("17", "17_supramaksimal.html", "supramaksimal", "Supramaksimal Uyarım ve Amplitüd Platosu", "#2f7653", "Fig. 8.17",
          "Tüm aksonların uyarıldığından emin olmak için akım amplitüd platosunun üstüne çıkarılır.",
          [("Eşik", "Aksonlar farklı akımda aktive olur."), ("Plato", "CMAP artık artmıyorsa maksimuma yaklaşılmıştır."), ("Supramaksimal", "Platonun biraz üstünde güvenli uyarımdır.")],
          [("Artan akım", "Akım artırıldıkça daha fazla akson uyarılır ve CMAP büyür."), ("Maksimum yanıt", "Tüm lifler uyarıldığında amplitüd plato yapar."), ("Gereklilik", "NCS’de güvenilir amplitüd için supramaksimal uyarım gerekir."), ("Hata", "Yetersiz uyarı yalancı düşük amplitüd veya yalancı blok izlenimi yaratır.")],
          "Düşük amplitüd ya da iletim bloğu yorumundan önce uyarım platosu doğrulanmalıdır.", "Supramaksimal uyarım, maksimum yanıtın üstünde güvenlik payıdır."),
    topic("18", "18_kostimulasyon.html", "kostimulasyon", "Komşu Sinir Ko-stimülasyonu", "#6a5acd", "Fig. 8.18-8.20; Box 8.5",
          "Fazla akım veya yanlış stimülatör pozisyonu komşu siniri de uyarabilir.",
          [("Komşu sinir", "Aynı akım alanına girebilir."), ("Morfoloji", "Dalga şekli ani değişebilir."), ("Blok taklidi", "Proksimal-distal amplitüd farkını bozabilir.")],
          [("Mekanizma", "Uyarı doğrudan hedef sinir üzerinde değilse ya da akım çok yayılırsa komşu sinir aktive olur."), ("Tanı tuzağı", "Yanlış amplitüd karşılaştırması ile iletim bloğu varmış gibi görünebilir."), ("İpuçları", "Dalga morfolojisinde ani değişiklik ve beklenmeyen kas seğirmesi ko-stimülasyon düşündürür."), ("Önleme", "Stimülatör hedef sinir üzerine optimize edilir ve akım gereksiz artırılmaz.")],
          "Amplitüd bir bölgede beklenmedik yüksekse “daha iyi kayıt” değil ko-stimülasyon olabilir.", "Ko-stimülasyon iletim bloğunu hem taklit eder hem maskeleyebilir."),
    topic("19", "19_motor_elektrot.html", "motor_elektrot", "Motor Elektrot Yerleşimi", "#c56f1c", "Fig. 8.21-8.23",
          "G1 motor noktanın üzerinde olmalıdır; uzak yerleşim başlangıç pozitifliği ve düşük amplitüd üretir.",
          [("Motor nokta", "Depolarizasyon ilk burada başlar."), ("G1", "Aktif elektrot motor noktayı görmelidir."), ("Hata", "G1 uzakta ise CMAP şekli bozulur.")],
          [("Normal yerleşim", "G1 motor nokta üzerine, G2 distal tendon üzerine yerleştirilir."), ("Başlangıç negatifliği", "G1 doğru yerdeyse CMAP başlangıcı negatif sapma ile başlar."), ("Yanlış yer", "G1 motor noktadan uzaksa başlangıç pozitifliği görülür ve amplitüd azalabilir."), ("Düzeltme", "G1 kas üzerinde motor noktaya doğru küçük hareketlerle kaydırılır.")],
          "Motor çalışmada başlangıç pozitifliği görürsen ilk düzeltilecek şey G1 pozisyonudur.", "G1 motor noktadan uzaksa CMAP hem küçülür hem şekil değiştirir."),
    topic("20", "20_referans_elektrot.html", "referans_elektrot", "Referans Elektrot ve Tendon Potansiyeli", "#126f86", "Fig. 8.24-8.25",
          "G2 sessiz kabul edilir; ancak tendon ve çevre dokular elektriksel aktivite taşıyabilir.",
          [("Belly-tendon", "Motor kayıtta standart montajdır."), ("G2", "Referans elektrot tamamen pasif olmayabilir."), ("Morfoloji", "Tendon potansiyeli bifid CMAP oluşturabilir.")],
          [("Montaj", "Motor çalışmalarda G1 kas karnına, G2 distal tendona yerleştirilir."), ("Referans etkisi", "G2 altındaki tendon ve yakın yapılar volüm iletimiyle potansiyel alabilir."), ("Ulnar/tibial", "Bazı sinirlerde tendon potansiyeli CMAP morfolojisini belirgin etkiler."), ("Amplitüd", "Referans elektrot pozisyonu ölçülen amplitüdü değiştirebilir.")],
          "Bifid morfolojide patoloji yorumundan önce G2 ve tendon potansiyeli değerlendirilmelidir.", "Referans elektrot sessiz olmak zorunda değildir."),
    topic("21", "21_antidromik_ortodromik.html", "antidromik_ortodromik", "Antidromik ve Ortodromik Duysal Kayıt", "#2f6fbd", "Fig. 8.26",
          "Mesafe aynıysa latans ve CV aynı kalır; amplitüd kayıt yönüne göre değişir.",
          [("Antidromik", "Duyusal yanıt distalde kaydedilir."), ("Ortodromik", "Yanıt proksimalde kaydedilir."), ("Fark", "Antidromik amplitüd genellikle daha büyüktür.")],
          [("Aynı mesafe", "Antidromik ve ortodromik median duysal çalışmada mesafe aynıysa latans ve CV aynıdır."), ("Amplitüd", "Antidromik yöntem, kayıt elektrotlarının sinire yakınlığı nedeniyle daha yüksek amplitüd sağlar."), ("Klinik kullanım", "Düşük amplitüdlü potansiyellerde antidromik kayıt daha avantajlı olabilir."), ("Yorum", "Yöntem değişirse amplitüd karşılaştırması doğrudan yapılamaz.")],
          "Takip çalışmalarında aynı yöntemi kullan; antidromik/ortodromik amplitüdleri karıştırma.", "Yön değişirse amplitüd değişir; aynı mesafede latans ve CV değişmez."),
    topic("22", "22_elektrot_sinir_mesafesi.html", "elektrot_sinir_mesafesi", "Elektrot-Sinir Mesafesi ve Ödem", "#b56a20", "Fig. 8.27-8.29",
          "Kayıt elektrotu sinirden uzaklaştıkça amplitüd azalır; ödem bu mesafeyi artırır.",
          [("Mesafe", "Volüm iletimi mesafeye duyarlıdır."), ("Ödem", "Sinir-elektrot aralığını artırır."), ("Latans", "Elektrot lateral kayarsa onset de kayabilir.")],
          [("Varsayım", "Duysal ve mikst çalışmalarda sinirin cilde yakın olduğu varsayılır."), ("Uzaklaşma", "Kayıt elektrotları sinirden uzaklaştıkça amplitüd düşer."), ("Ödem", "Ödem sinir ile elektrot arasındaki mesafeyi artırarak düşük amplitüd yaratabilir."), ("Onset", "Elektrot sinirin üzerinden laterale kayarsa onset latansı da değişebilir.")],
          "Düşük SNAP amplitüdünde ödem, obezite ve elektrotun sinire uzaklığını mutlaka düşün.", "Amplitüd yalnızca akson sayısı değil, elektrot-sinir mesafesidir."),
    topic("23", "23_g1_g2_mesafesi.html", "g1_g2_mesafesi", "G1-G2 Mesafesi ve Faz İptali", "#5a5fcf", "Fig. 8.30-8.31",
          "Aktif ve referans elektrot arasındaki mesafe SNAP morfolojisini ve amplitüdünü belirler.",
          [("Fark sinyali", "SNAP G1 ve G2 arasındaki aktivite farkıdır."), ("Çok yakın", "İki elektrot aynı anda aktif olabilir."), ("Sonuç", "Amplitüd düşer, morfoloji değişir.")],
          [("Temel prensip", "Kayıt edilen duysal potansiyel G1 ve G2 arasındaki elektriksel farktır."), ("Normal mesafe", "Depolarizasyon önce G1, sonra G2 altından geçer ve net fark oluşur."), ("Kısa mesafe", "G1-G2 çok yakınsa iki elektrot kısa süre aynı anda aktif olur."), ("Faz iptali", "Eşzamanlı aktivite farkı azaltır; SNAP amplitüdü düşer ve şekil değişir.")],
          "Ring elektrot mesafesi değişirse amplitüd karşılaştırmasını güvenilir sayma.", "G1-G2 çok yakınsa sinyal kendi içinde iptal olur."),
    topic("24", "24_ekstremite_mesafe.html", "ekstremite_mesafe", "Ekstremite Pozisyonu ve Mesafe Ölçümü", "#2f7653", "Fig. 8.32",
          "Dirsek pozisyonu ulnar sinirin gerçek uzunluğunu değiştirir; cilt mesafesi sinir yolunu yanlış temsil edebilir.",
          [("Ekstansiyon", "Ulnar sinir gevşek ve kıvrımlı olabilir."), ("Fleksiyon", "Ölçülen yüzey mesafesi gerçek sinir uzunluğuna yaklaşır."), ("CV", "Yanlış mesafe yanlış hız üretir.")],
          [("Ulnar sinir", "Dirsek ekstansiyondayken ulnar sinir gevşek ve redundant olabilir."), ("Yüzey ölçümü", "Bu pozisyonda cilt üzerinden ölçülen mesafe gerçek sinir uzunluğunu olduğundan kısa gösterebilir."), ("Fleksiyon", "Dirsek fleksiyonu sinir yolunu gerer ve mesafe ölçümünü daha doğru yapar."), ("Sonuç", "Mesafe kısa ölçülürse CV hatalı hesaplanır.")],
          "Dirsek segmenti ölçümünde pozisyonu standartlaştır; özellikle ulnar çalışmada.", "Cildi ölçersin, ama hız sinirin gerçek yolundan hesaplanır."),
    topic("25", "25_ekstremite_morfoloji.html", "ekstremite_morfoloji", "Ekstremite Pozisyonu ve Dalga Morfolojisi", "#3f7d8a", "Limb position",
          "Ekstremite pozisyonu sadece mesafeyi değil, kayıt geometrisini ve dalga formunu da değiştirebilir.",
          [("Pozisyon", "Sinir ve elektrot ilişkisi değişir."), ("Morfoloji", "Dalga formu şekli kayabilir."), ("Standart", "Tekrar çalışmalarda aynı pozisyon gerekir.")],
          [("Geometri", "Eklem pozisyonu sinirin yüzeye ve elektrotlara göre konumunu değiştirir."), ("Kayıt etkisi", "Elektrot-sinir mesafesi ve iletim yolu değişince dalga morfolojisi de değişebilir."), ("Karşılaştırma", "Pozisyon farkı gerçek patoloji gibi görünen morfoloji farkı oluşturabilir."), ("Tekrar", "Seri çalışmalar aynı pozisyon ve aynı mesafe ölçüm yöntemiyle yapılmalıdır.")],
          "Önceki çalışma ile karşılaştırırken ekstremite pozisyonunun aynı olduğundan emin ol.", "Pozisyon değişirse sadece mesafe değil, dalga formu da değişebilir."),
    topic("26", "26_sweep_sensitivite.html", "sweep_sensitivite", "Sweep Hızı, Sensitivite ve Latans Ölçümü", "#b43b47", "Fig. 8.33-8.34",
          "Ekran ayarları siniri değiştirmez; fakat latans ölçüm noktasını değiştirebilir.",
          [("Sensitivite", "Artınca başlangıç daha erken görülür."), ("Sweep", "Yavaşlayınca başlangıç daha geç görünebilir."), ("Standart", "Aynı ayarlar kullanılmalıdır.")],
          [("Sensitivite", "Duyarlılık arttığında dalga baseline’dan daha erken ayrılıyor gibi görünür; ölçülen latans kısalabilir."), ("Sweep hızı", "Sweep hızı düştüğünde latans ölçümü uzayabilir."), ("Sabit ayar", "Latans ölçümleri aynı sensitivite ve aynı sweep hızıyla yapılmalıdır."), ("Tepe latansı", "Tepe latansı daha az etkilenebilir; ancak CV hesabı onset latansına dayanır.")],
          "Farklı ayarla ölçülen latansları doğrudan karşılaştırma.", "Ayar değişirse ölçüm değişir; sinir değişmiş olmak zorunda değildir."),
]


FIGURES = {
    "08": {"file": "08f_sicaklik_isinma_figure.html", "title": "Sıcaklık: Isınma Süresi", "ref": "Fig. 8.2", "images": ["source/p03_img01_xref35_650x681.png"], "caption": "Isıtma sonrası sinir iletim hızının limit değere yaklaşması zaman alır. Deri sıcaklığı normale dönse bile sinir daha geç ısınabilir.", "points": ["Deri sıcaklığı tek başına yeterli güvence değildir.", "Soğuk ekstremitede 15-20 dakikalık gecikme klinik olarak anlamlı olabilir.", "Isıtma sonrası kayıt için yeterli süre beklenmelidir."]},
    "13": {"file": "13f_filtreler_figure.html", "title": "Filtreler: Gerçek Trase Örnekleri", "ref": "Fig. 8.8-8.9", "images": ["source/p07_img01_xref55_681x1090.png", "source/p07_img02_xref57_1000x875.png"], "caption": "High-frequency filtre azaltıldıkça gürültü azalabilir; ancak SNAP morfolojisi ve amplitüdü de değişebilir.", "points": ["Filtre ayarı ölçümü doğrudan etkiler.", "Aynı hasta/aynı sinir farklı filtreyle farklı görünür.", "Karşılaştırma aynı filtre ayarıyla yapılmalıdır."]},
    "14": {"file": "14f_elektronik_ortalama_figure.html", "title": "Elektronik Ortalama: Gerçek Kayıt", "ref": "Fig. 8.10", "images": ["source/p07_img03_xref58_1001x860.png"], "caption": "Tek uyarıda belirgin baseline gürültüsü varken, çoklu uyarının ortalaması sinyal-gürültü oranını artırır.", "points": ["Sinyal uyarıya zaman kilitlidir.", "Rastgele gürültü ortalamada azalır.", "Ortalama sistematik teknik hatayı düzeltmez."]},
    "15": {"file": "15f_stimulus_artefakti_figure.html", "title": "Stimulus Artefaktı: Gerçek Trase", "ref": "Fig. 8.11-8.13", "images": ["source/p08_img01_xref63_370x203.jpeg", "source/p08_img02_xref64_370x203.jpeg", "source/p08_img03_xref65_370x202.jpeg", "source/p09_img01_xref87_501x376.jpeg"], "caption": "Stimulus artefaktı onset latansı ve amplitüd ölçümüne karışabilir. Anodun yönü değiştirilerek baseline düzeltilebilir.", "points": ["Katot sabit tutulur.", "Anot küçük açılarla çevrilir.", "Amaç artefaktı değil, ölçüm baseline'ını düzeltmektir."]},
    "16": {"file": "16f_kutup_tersligi_figure.html", "title": "Katot-Anot Tersliği: Gerçek Kayıt", "ref": "Fig. 8.14-8.16", "images": ["source/p09_img02_xref88_288x376.png", "source/p10_img02_xref96_450x536.png"], "caption": "Stimülatör polaritesi ters olduğunda etkin uyarı noktası ve yanıt latansı değişebilir.", "points": ["Katot G1'e bakmalıdır.", "Ters polarite yapay yavaşlama yaratabilir.", "Beklenmedik latans uzamasında stimülatör yönü kontrol edilir."]},
    "17": {"file": "17f_supramaksimal_figure.html", "title": "Supramaksimal Uyarım: Akım-Yanıt", "ref": "Fig. 8.17", "images": ["source/p10_img01_xref95_485x601.png"], "caption": "Akım artırıldıkça CMAP büyür; tüm aksonlar uyarıldığında yanıt plato yapar.", "points": ["Plato görülmeden maksimum yanıt varsayılmaz.", "Yetersiz uyarı düşük amplitüd taklidi yapabilir.", "Supramaksimal uyarım plato üstü güvenlik payıdır."]},
    "18": {"file": "18f_kostimulasyon_figure.html", "title": "Ko-stimülasyon: Gerçek Kayıt", "ref": "Fig. 8.18-8.20", "images": ["source/p11_img01_xref101_550x1051.png", "source/p11_img02_xref104_1000x475.png", "source/p12_img01_xref109_593x451.jpeg"], "caption": "Komşu sinirin uyarılması amplitüd karşılaştırmasını bozar ve iletim bloğu yorumunu yanıltabilir.", "points": ["Ani morfoloji değişikliği uyarıcıdır.", "Beklenmeyen kas seğirmesi izlenmelidir.", "Stimülatör hedef sinir üzerine yeniden konumlandırılır."]},
    "19": {"file": "19f_motor_elektrot_figure.html", "title": "Motor Elektrot Yerleşimi: Gerçek Kayıt", "ref": "Fig. 8.21-8.23", "images": ["source/p13_img01_xref117_1075x981.png", "source/p14_img01_xref121_291x226.jpeg"], "caption": "G1 motor noktadan uzaklaştığında CMAP başlangıcı pozitifleşebilir ve amplitüd düşebilir.", "points": ["Doğru G1 yerleşimi başlangıç negatifliği verir.", "Başlangıç pozitifliği G1 pozisyonunu sorgulatır.", "Elektrot küçük hareketlerle motor noktaya alınır."]},
    "20": {"file": "20f_referans_elektrot_figure.html", "title": "Referans Elektrot: Tendon Potansiyeli", "ref": "Fig. 8.24-8.25", "images": ["source/p15_img01_xref140_1140x1180.png"], "caption": "G2 tamamen sessiz olmayabilir. Tendon potansiyeli CMAP konfigürasyonunu ve amplitüdünü değiştirebilir.", "points": ["Belly-tendon montajında G2 aktif katkı alabilir.", "Bifid morfoloji teknik/montaj etkisi olabilir.", "Referans elektrot pozisyonu standart tutulmalıdır."]},
    "21": {"file": "21f_antidromik_ortodromik_figure.html", "title": "Antidromik-Ortodromik: Gerçek Kayıt", "ref": "Fig. 8.26", "images": ["source/p15_img02_xref141_680x851.png"], "caption": "Aynı mesafede latans ve iletim hızı aynıdır; antidromik yöntemde amplitüd genellikle daha büyüktür.", "points": ["Yön amplitüdü değiştirir.", "Mesafe aynıysa latans ve CV aynı kalır.", "Takipte aynı yöntem kullanılmalıdır."]},
    "22": {"file": "22f_elektrot_sinir_mesafesi_figure.html", "title": "Elektrot-Sinir Mesafesi: Gerçek Kayıt", "ref": "Fig. 8.27-8.29", "images": ["source/p16_img99_xref147_701x876.png", "source/p17_img01_xref401_620x791.png"], "caption": "Kayıt elektrotu sinirden uzaklaştıkça amplitüd azalır; elektrot lateral kayarsa onset latansı da değişebilir.", "points": ["Düşük amplitüd her zaman akson kaybı değildir.", "Ödem elektrot-sinir mesafesini artırır.", "Elektrot sinirin tam üzerine yerleştirilmelidir."]},
    "23": {"file": "23f_g1_g2_mesafesi_figure.html", "title": "G1-G2 Mesafesi: Gerçek Kayıt", "ref": "Fig. 8.30-8.31", "images": ["source/p19_img01_xref410_726x885.png"], "caption": "G1-G2 mesafesi azaldığında iki elektrot aynı anda aktif olabilir; SNAP amplitüdü ve morfolojisi değişir.", "points": ["SNAP G1-G2 fark sinyalidir.", "Çok kısa mesafe faz iptali yaratabilir.", "Ring elektrot aralığı standart tutulmalıdır."]},
    "24": {"file": "24f_ekstremite_mesafe_figure.html", "title": "Ekstremite Pozisyonu: Gerçek Fotoğraf", "ref": "Fig. 8.32", "images": ["source/p19_img59_xref457_501x376.jpeg", "source/p19_img60_xref458_501x376.jpeg"], "caption": "Dirsek pozisyonu ulnar sinirin gerçek uzunluğunu ve yüzeyden ölçülen mesafeyi değiştirir.", "points": ["Ekstansiyonda sinir gevşek kalabilir.", "Fleksiyonda mesafe gerçek sinir yoluna yaklaşır.", "CV hesabında pozisyon standart olmalıdır."]},
    "26": {"file": "26f_sweep_sensitivite_figure.html", "title": "Sweep ve Sensitivite: Gerçek Kayıt", "ref": "Fig. 8.33-8.34", "images": ["source/p20_img01_xref489_656x1486.png", "source/p20_img02_xref491_340x215.jpeg", "source/p20_img03_xref492_340x215.jpeg"], "caption": "Sensitivite ve sweep ayarı değiştiğinde ölçülen onset latansı değişebilir.", "points": ["Aynı sinir farklı ayarla farklı ölçülür.", "Latans ölçümleri aynı ekran ayarıyla yapılmalıdır.", "Tepe latansı CV hesabının yerine geçmez."]},
}


def sequence():
    seq = []
    for t in TOPICS:
        seq.append(t["file"])
        if t["skip"]:
            seq.extend(["05b_sicaklik_simulasyon.html", "05c_sicaklik_ozet.html"])
        else:
            if t["n"] in FIGURES:
                seq.append(FIGURES[t["n"]]["file"])
            seq.append(f"{t['n']}b_{t['slug']}_ozet.html")
    return seq


SEQ = sequence()
BY_FILE = {t["file"]: t for t in TOPICS}
TOPIC_BY_N = {t["n"]: t for t in TOPICS}
SUMMARY = {f"{t['n']}b_{t['slug']}_ozet.html": t for t in TOPICS if not t["skip"]}
FIGURES_BY_FILE = {v["file"]: (k, v) for k, v in FIGURES.items()}


def nav(prev_file, label, sub, next_file):
    prev = f'<a class="navbtn" href="{prev_file}" aria-label="Önceki">&#8249;</a>' if prev_file else '<span class="navbtn disabled">&#8249;</span>'
    nxt = f'<a class="navbtn" href="{next_file}" aria-label="Sonraki">&#8250;</a>' if next_file else '<span class="navbtn disabled">&#8250;</span>'
    return f'<div class="modnav">{prev}<a class="navnum" href="index.html">{label}<span>{sub}</span></a>{nxt}</div>'


def css(accent):
    return f""":root{{--ink:#14212b;--muted:#5c6973;--paper:#f7f9f5;--line:#d7dfd9;--teal:#126f86;--blue:#2f6fbd;--amber:#b56a20;--red:#b43b47;--green:#2f7653;--purple:#5a5fcf;--accent:{accent};--accent2:#c56f1c;--shadow:0 20px 54px rgba(18,32,42,.16);}}
*{{box-sizing:border-box;}}html,body{{width:100%;height:100%;margin:0;background:#e5ebe7;color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}}body{{display:grid;place-items:center;padding:18px;}}.slide{{width:min(100vw - 36px,1360px);aspect-ratio:16/9;max-height:calc(100vh - 36px);background:var(--paper);border:1px solid var(--line);border-radius:8px;box-shadow:var(--shadow);display:grid;grid-template-rows:auto 1fr auto;overflow:hidden;}}header{{display:grid;grid-template-columns:1fr auto;gap:18px;align-items:end;padding:18px 30px 12px;background:linear-gradient(90deg,#ffffff 0%,#f4fbfd 48%,#fff7ed 100%);border-top:6px solid var(--accent);border-bottom:1px solid var(--line);}}h1{{margin:0;font-size:clamp(22px,2.55vw,34px);line-height:1.06;font-weight:850;letter-spacing:0;}}.subtitle{{margin-top:5px;color:var(--muted);font-size:clamp(12px,1.08vw,14.5px);line-height:1.36;max-width:880px;}}.modnav{{display:flex;align-items:center;gap:8px;}}.navbtn{{display:grid;place-items:center;width:32px;height:32px;border-radius:6px;border:1px solid var(--line);background:#fff;color:var(--accent);font-size:18px;text-decoration:none;}}.navbtn.disabled{{opacity:.32;pointer-events:none;}}.navnum{{display:grid;justify-items:center;color:var(--accent);font-weight:850;font-size:18px;text-decoration:none;line-height:1.1;min-width:70px;}}.navnum span{{color:var(--muted);font-size:9.5px;font-weight:750;text-transform:uppercase;letter-spacing:.05em;}}main{{min-height:0;padding:14px 30px;display:grid;grid-template-rows:auto 1fr auto;gap:12px;}}.topline{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;}}.fact{{border:1px solid var(--line);background:#fff;padding:12px 14px;border-left:5px solid var(--accent);min-height:82px;}}.fact b{{display:block;color:var(--accent);font-size:12px;text-transform:uppercase;letter-spacing:.06em;margin-bottom:5px;}}.fact span{{font-size:15px;line-height:1.32;font-weight:720;}}.logic{{min-height:0;display:grid;grid-template-columns:1.05fr .95fr;gap:12px;}}.panel{{min-width:0;min-height:0;border:1px solid var(--line);background:#fff;display:flex;flex-direction:column;overflow:hidden;}}.panel-head{{flex:none;padding:9px 14px;border-bottom:1px solid var(--line);background:linear-gradient(90deg,rgba(18,111,134,.08),rgba(197,111,28,.08));color:var(--muted);font-size:10.5px;font-weight:850;text-transform:uppercase;letter-spacing:.07em;}}.bullets{{flex:1;min-height:0;padding:15px 18px;display:grid;align-content:start;gap:11px;}}.item{{display:grid;grid-template-columns:112px 1fr;gap:12px;align-items:start;}}.item strong{{color:var(--accent);font-size:13px;line-height:1.2;}}.item p{{margin:0;font-size:15px;line-height:1.35;font-weight:660;}}.sourcebox{{padding:15px 18px;display:grid;align-content:start;gap:10px;}}.sourcebox h2{{margin:0;color:var(--accent);font-size:13px;text-transform:uppercase;letter-spacing:.06em;}}.sourcebox p{{margin:0;font-size:14.5px;line-height:1.36;font-weight:680;}}.clinical{{display:grid;grid-template-columns:1fr 1fr;gap:12px;}}.clinical div{{border:1px solid var(--line);background:#fbfcf8;padding:12px 14px;border-top:4px solid var(--accent2);}}.clinical b{{display:block;color:var(--accent);font-size:12px;text-transform:uppercase;letter-spacing:.06em;margin-bottom:5px;}}.clinical span{{font-size:14.5px;line-height:1.32;font-weight:700;}}footer{{padding:11px 30px 15px;border-top:1px solid var(--line);background:#fbfcf8;font-size:clamp(12.5px,1.12vw,14.5px);line-height:1.35;font-weight:760;}}footer b{{color:var(--accent);}}@media(max-width:980px){{html,body{{overflow-x:hidden;}}body{{display:block;padding:0;}}.slide{{width:100%;max-width:100%;min-height:100vh;max-height:none;aspect-ratio:auto;border-radius:0;}}header{{grid-template-columns:minmax(0,1fr);align-items:start;}}header>div{{min-width:0;}}h1{{font-size:22px;overflow-wrap:anywhere;}}.modnav{{justify-self:start;}}header,main,footer{{padding-left:16px;padding-right:16px;}}.topline,.logic,.clinical{{grid-template-columns:minmax(0,1fr);}}.item{{grid-template-columns:1fr;}}.panel,.fact,.clinical div{{min-width:0;max-width:100%;}}}}"""


def summary_page(t, filename):
    idx = SEQ.index(filename)
    facts = "\n".join(f'<div class="fact"><b>{html.escape(k)}</b><span>{html.escape(v)}</span></div>' for k, v in t["facts"])
    items = "\n".join(f'<div class="item"><strong>{html.escape(k)}</strong><p>{html.escape(v)}</p></div>' for k, v in t["items"])
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['n']}b - {html.escape(t['title'])}: Kaynak Özeti</title>
<style>{css(t['accent'])}</style>
</head>
<body>
<section class="slide" aria-label="{html.escape(t['title'])} kaynak metin özeti">
<header>
<div>
<h1>{html.escape(t['title'])}: Kaynak Metin Özeti</h1>
<div class="subtitle">{html.escape(t['subtitle'])}</div>
</div>
{nav(SEQ[idx-1] if idx else None, t['n'] + 'b', 'özet', SEQ[idx+1] if idx < len(SEQ)-1 else None)}
</header>
<main>
<section class="topline" aria-label="Ana noktalar">{facts}</section>
<section class="logic">
<div class="panel"><div class="panel-head">Doğrudan ders mesajı</div><div class="bullets">{items}</div></div>
<div class="panel"><div class="panel-head">Kaynak ve klinik çeviri</div><div class="sourcebox">
<h2>{html.escape(t['ref'])}</h2>
<p>Bu sayfa ilgili başlığın ders sırasında okunacak kısa Türkçe karşılığıdır. Cümleler doğrudan klinik uygulamaya yöneliktir; teknik terimler EMG/NCS kullanımına göre korunmuştur.</p>
<p>{html.escape(t['clinical'])}</p>
</div></div>
</section>
<section class="clinical"><div><b>Sunumda vurgula</b><span>{html.escape(t['clinical'])}</span></div><div><b>Kontrol sorusu</b><span>Bu bulgu gerçek patoloji mi, yoksa ölçüm koşulunun beklenen sonucu mu?</span></div></section>
</main>
<footer><b>Kural:</b> {html.escape(t['rule'])}</footer>
</section>
</body>
</html>
"""


def figure_page(topic_n, fig):
    t = TOPIC_BY_N[topic_n]
    filename = fig["file"]
    idx = SEQ.index(filename)
    imgs = "\n".join(
        f'<div class="figure-frame"><img src="figures/{html.escape(src)}" alt="{html.escape(fig["ref"])} kaynak şekli"></div>'
        for src in fig["images"]
    )
    points = "\n".join(f"<li>{html.escape(point)}</li>" for point in fig["points"])
    figure_css = css(t["accent"]) + """
.figure-main{min-height:0;padding:14px 30px;display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:14px;}
.figure-panel,.read-panel{min-width:0;min-height:0;border:1px solid var(--line);background:#fff;display:flex;flex-direction:column;overflow:hidden;}
.figure-grid{flex:1;min-height:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;padding:12px;background:#fff;}
.figure-frame{min-width:0;min-height:0;display:grid;place-items:center;background:#07100f;border:1px solid #253936;box-shadow:inset 0 0 0 1px rgba(255,255,255,.04);overflow:hidden;}
.figure-frame img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;display:block;}
.figure-caption{flex:none;border-top:1px solid var(--line);background:#fbfcf8;padding:10px 14px;font-size:14px;line-height:1.35;font-weight:700;}
.read-body{padding:16px;display:grid;align-content:start;gap:13px;}
.ref{color:var(--accent);font-size:13px;font-weight:850;text-transform:uppercase;letter-spacing:.06em;}
.read-body p{margin:0;font-size:14.5px;line-height:1.36;font-weight:680;}
.read-body ul{margin:0;padding:0;list-style:none;display:grid;gap:10px;}
.read-body li{border-left:4px solid var(--accent);background:#fbfcf8;border:1px solid var(--line);padding:9px 10px 9px 12px;font-size:14px;line-height:1.3;font-weight:700;}
@media(max-width:980px){.figure-main{grid-template-columns:minmax(0,1fr);padding-left:16px;padding-right:16px;}.figure-grid{grid-template-columns:minmax(0,1fr);}.figure-frame{min-height:260px;}}
"""
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{topic_n}f - {html.escape(fig['title'])}</title>
<style>{figure_css}</style>
</head>
<body>
<section class="slide" aria-label="{html.escape(fig['title'])} gerçek şekil sayfası">
<header>
<div>
<h1>{html.escape(fig['title'])}</h1>
<div class="subtitle">Kaynak şekil sayfası: gerçek ders figürü önce gösterilir, sonra model/özet yorumu yapılır.</div>
</div>
{nav(SEQ[idx-1] if idx else None, topic_n + 'f', 'şekil', SEQ[idx+1] if idx < len(SEQ)-1 else None)}
</header>
<main class="figure-main">
<section class="figure-panel">
<div class="panel-head">{html.escape(fig['ref'])} - gerçek kaynak figürü</div>
<div class="figure-grid">{imgs}</div>
<div class="figure-caption">{html.escape(fig['caption'])}</div>
</section>
<aside class="read-panel">
<div class="panel-head">Klinik okuma</div>
<div class="read-body">
<div class="ref">{html.escape(t['title'])}</div>
<p>{html.escape(t['subtitle'])}</p>
<ul>{points}</ul>
</div>
</aside>
</main>
<footer><b>Kural:</b> {html.escape(t['rule'])}</footer>
</section>
</body>
</html>
"""


def cluster_for(filename):
    idx = SEQ.index(filename)
    prev_file = SEQ[idx - 1] if idx > 0 else None
    next_file = SEQ[idx + 1] if idx < len(SEQ) - 1 else None
    if filename in SUMMARY:
        t = SUMMARY[filename]
        return nav(prev_file, t["n"] + "b", "özet", next_file)
    if filename in FIGURES_BY_FILE:
        topic_n, _ = FIGURES_BY_FILE[filename]
        return nav(prev_file, topic_n + "f", "şekil", next_file)
    if filename == "05b_sicaklik_simulasyon.html":
        return nav(prev_file, "05b", "model", next_file)
    if filename == "05c_sicaklik_ozet.html":
        return nav(prev_file, "05c", "özet", next_file)
    t = BY_FILE[filename]
    return nav(prev_file, t["n"], "konsept", next_file)


def generate_summaries():
    for filename, t in SUMMARY.items():
        (ROOT / filename).write_text(summary_page(t, filename), encoding="utf-8")


def generate_figures():
    for topic_n, fig in FIGURES.items():
        (ROOT / fig["file"]).write_text(figure_page(topic_n, fig), encoding="utf-8")


def update_nav():
    for filename in SEQ:
        path = ROOT / filename
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new_text, count = re.subn(r'<div class="modnav">.*?</div>\s*</header>', cluster_for(filename) + "\n</header>", text, count=1, flags=re.S)
        if count:
            path.write_text(new_text, encoding="utf-8")


def polish_existing_pages():
    root_pattern = re.compile(r":root\{[^}]+\}")
    for t in TOPICS:
        path = ROOT / t["file"]
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new_root = f":root{{--ink:#14212b;--muted:#5c6973;--paper:#f7f9f5;--line:#d7dfd9;--teal:#126f86;--amber:#b56a20;--red:#b43b47;--green:#2f7653;--blue:#2f6fbd;--purple:#5a5fcf;--accent:{t['accent']};--accent2:#c56f1c;--shadow:0 20px 54px rgba(18,32,42,.16);}}"
        text = root_pattern.sub(new_root, text, count=1)
        text = text.replace("background:#fbfcf8;border-bottom:1px solid var(--line);", "background:linear-gradient(90deg,#ffffff 0%,#f4fbfd 48%,#fff7ed 100%);border-top:6px solid var(--accent);border-bottom:1px solid var(--line);", 1)
        text = text.replace("color:var(--teal);font-size", "color:var(--accent);font-size")
        text = text.replace("color:var(--teal);font-weight", "color:var(--accent);font-weight")
        text = text.replace("border-radius:10px;", "border-radius:8px;")
        text = text.replace("color:var(--muted);font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.07em;", "background:linear-gradient(90deg,rgba(18,111,134,.08),rgba(197,111,28,.08));color:var(--muted);font-size:11px;font-weight:850;text-transform:uppercase;letter-spacing:.07em;")
        path.write_text(text, encoding="utf-8")


def rebuild_index():
    groups = [("Giriş", TOPICS[:3]), ("Fizyolojik Faktörler", TOPICS[3:11]), ("Nonfizyolojik Faktörler", TOPICS[11:])]
    index_css = """:root{--ink:#14212b;--muted:#5c6973;--paper:#f7f9f5;--line:#d7dfd9;--teal:#126f86;--blue:#2f6fbd;--amber:#b56a20;--red:#b43b47;--green:#2f7653;--shadow:0 18px 48px rgba(18,32,42,.14);}*{box-sizing:border-box;}body{margin:0;background:#e5ebe7;color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;padding:28px;}main{max-width:1220px;margin:0 auto;background:var(--paper);border:1px solid var(--line);border-radius:8px;box-shadow:var(--shadow);overflow:hidden;}header{padding:28px 32px 20px;background:linear-gradient(90deg,#ffffff 0%,#f4fbfd 48%,#fff7ed 100%);border-top:7px solid var(--teal);border-bottom:1px solid var(--line);}h1{margin:0;font-size:clamp(26px,3.6vw,42px);line-height:1.05;font-weight:850;}.subtitle{margin-top:10px;color:var(--muted);font-size:16px;line-height:1.45;max-width:900px;}.pills{display:flex;flex-wrap:wrap;gap:8px;padding:16px 32px 0;}.pill{display:inline-flex;align-items:center;min-height:26px;padding:3px 10px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--muted);font-size:12.5px;font-weight:750;}.pill.done{color:var(--green);border-color:#cbe5d3;background:#eef7f1;}section.group{padding:22px 32px 6px;}section.group h2{margin:0 0 12px;font-size:14px;font-weight:850;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(245px,1fr));gap:10px;padding-bottom:18px;}a.card{display:grid;gap:6px;min-height:102px;padding:14px 16px;border:1px solid var(--line);border-left:5px solid var(--accent,var(--teal));border-radius:6px;background:#fff;color:inherit;text-decoration:none;}a.card.summary{background:#fbfcf8;border-left-color:#c56f1c;}a.card:hover,a.card:focus-visible{border-color:var(--teal);outline:3px solid rgba(18,111,134,.14);}.num{color:var(--accent,var(--teal));font-size:12px;font-weight:850;text-transform:uppercase;letter-spacing:.06em;}h3{margin:0;font-size:16px;line-height:1.2;}p{margin:0;color:var(--muted);line-height:1.3;font-size:12.5px;}footer.foot{padding:10px 32px 26px;color:var(--muted);font-size:12.5px;}"""
    parts = [f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Artifacts and Technical Factors - İçindekiler</title><style>{index_css}</style></head><body><main><header><h1>Artifacts and Technical Factors</h1><div class="subtitle">Chapter 8 için Türkçe interaktif sunum dizisi. Her konu artık en az iki adımda ilerler: önce konsept/animasyon, sonra kaynak metin özeti ve klinik kural.</div></header><div class="pills"><span class="pill done">26 konu</span><span class="pill done">{len(SEQ)} sayfa</span><span class="pill done">kaynak özetleri eklendi</span><span class="pill">Poll: Mentimeter ayrı sekme</span></div>']
    for name, items in groups:
        parts.append(f'<section class="group"><h2>{name}</h2><div class="grid">')
        for t in items:
            parts.append(f'<a class="card" style="--accent:{t["accent"]}" href="{t["file"]}"><div class="num">{t["n"]} konsept</div><h3>{html.escape(t["title"])}</h3><p>{html.escape(t["subtitle"])}</p></a>')
            if t["n"] in FIGURES:
                fig = FIGURES[t["n"]]
                parts.append(f'<a class="card summary" style="--accent:{t["accent"]}" href="{fig["file"]}"><div class="num">{t["n"]}f şekil</div><h3>{html.escape(fig["title"])}</h3><p>{html.escape(fig["ref"])}: gerçek kaynak figürü.</p></a>')
            if t["skip"]:
                parts.append(f'<a class="card summary" style="--accent:{t["accent"]}" href="05c_sicaklik_ozet.html"><div class="num">05c özet</div><h3>Sıcaklık: Kaynak Özeti</h3><p>Fig. 8.1 ve Box 8.2 için klinik okuma.</p></a>')
            else:
                sfile = f'{t["n"]}b_{t["slug"]}_ozet.html'
                parts.append(f'<a class="card summary" style="--accent:{t["accent"]}" href="{sfile}"><div class="num">{t["n"]}b özet</div><h3>Kaynak Metin Özeti</h3><p>{html.escape(t["ref"])} başlığının doğrudan klinik çevirisi.</p></a>')
        parts.append("</div></section>")
    parts.append('<footer class="foot">Sunum sırasında Mentimeter ayrı sekmede kalır. Bu HTML dizisi mekanizma, gerçek kayıt, model ve kaynak özetleri için kullanılır.</footer></main></body></html>')
    (ROOT / "index.html").write_text("\n".join(parts), encoding="utf-8")


if __name__ == "__main__":
    generate_summaries()
    generate_figures()
    update_nav()
    polish_existing_pages()
    rebuild_index()
    print(f"generated {len(SUMMARY)} summary pages")
    print(f"generated {len(FIGURES)} figure pages")
    print(f"wired {len(SEQ)} sequence pages")
