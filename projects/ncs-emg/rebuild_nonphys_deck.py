from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path


ROOT = Path(
    sys.argv[1]
    if len(sys.argv) > 1
    else r"C:\Users\uugur\OneDrive\Desktop\Second_Brain\10_Projects\presentations\artifacts_of_ncs_emg"
)
ANIM = ROOT / "animations"
STAGING = Path(
    r"C:\Users\uugur\.codex\visualizations\2026\07\28\019faae7-0429-7922-9e1b-f4bb10c72700"
)


def E(title, sections, rule, source):
    return {"title": title, "sections": sections, "rule": rule, "source": source}


EXPLANATIONS = {
    "impedans-gurultu/index.html": E(
        "Elektriksel gürültü kaçınılmazdır; hedef onu sinyalden ayırmaktır",
        [
            ("Kaynak", "60 Hz interferansı ışık, fan, ısıtıcı ve bilgisayarlardan yayılır; yoğun bakımda ventilatör ve monitörler ek kaynak oluşturur."),
            ("En kırılgan kayıtlar", "Mikrovolt düzeyindeki DSAP'lar ve fibrilasyon potansiyelleri çevresel gürültüden en kolay etkilenen sinyallerdir."),
            ("Hedef", "Gürültü tamamen yok edilemeyebilir; doğru elektrot, empedans, kablo ve yerleşimle kabul edilebilir düzeye indirilir."),
        ],
        "Küçük bir yanıtı yorumlamadan önce gürültü kaynağı ve kayıt kalitesi kontrol edilmelidir.",
        "Preston & Shapiro, Bölüm 8, s. 82-83; Şekil 8.3-8.6",
    ),
    "impedans-gurultu/diferansiyel-amplifikasyon.html": E(
        "Amplifikatör G1'i değil, G1-G2 farkını büyütür",
        [
            ("Diferansiyel kayıt", "NCS ve iğne EMG'de G1 ile G2 arasındaki voltaj farkı yükseltilir ve ekranda gösterilir."),
            ("Ortak mod reddi", "Aynı gürültü iki girişte eşitse birbirinden çıkar; hedef sinyal kalır. Buna ortak mod reddi denir."),
            ("Uyumsuz giriş", "Gürültü girişlerde farklıysa çıkarılamaz, amplifikatörü doyurabilir ve dik çizgiler oluşturabilir. Sensitivite 20 µV/div'den 10 mV/div'e düşürülünce 50/60 Hz sinüs görünür."),
        ],
        "Ortak mod reddi ancak G1 ve G2 benzer gürültüyü gördüğünde etkilidir.",
        "s. 82; Şekil 8.4-8.5",
    ),
    "impedans-gurultu/impedans-uyumsuzlugu.html": E(
        "Aynı çevresel akım, farklı empedansta farklı gürültü voltajı üretir",
        [
            ("Empedans", "DC direncini ve AC için kapasitans/indüktans etkilerini birlikte tanımlar; iki kayıt elektrodunda mümkün olduğunca eşit olmalıdır."),
            ("Ohm yasası", "E = I × R: aynı indüklenen akım, empedanslar farklıysa G1 ve G2'de farklı voltaj oluşturur."),
            ("Kayıt sonucu", "Diferansiyel amplifikatör bu voltaj farkını da büyütür; 50/60 Hz gürültü hedef sinyali örtebilir."),
        ],
        "Yalnız düşük empedans değil, G1-G2 empedans eşleşmesi gereklidir.",
        "s. 82-83; Şekil 8.4-8.5",
    ),
    "impedans-gurultu/60hz-azaltma.html": E(
        "50/60 Hz gürültüsü sistematik bir kayıt kontrolüyle azaltılır",
        [
            ("Elektrot ve kablo", "G1-G2 aynı tip olmalı; bağlantılar sağlam, kablolar yıpranmamış ve mümkünse koaksiyel olmalıdır."),
            ("Deri teması", "Kir ve yağ alkol/asetonla temizlenmeli, iletken jel kullanılmalı ve elektrotlar sıkıca sabitlenmelidir."),
            ("Yerleşim", "Toprak stimülatör ile kayıt elektrotları arasına konmalı; G1-G2 birbirine yaklaştıkça ortak gürültü daha benzer görülür."),
        ],
        "Gürültülü kayıtta cihaz ayarından önce elektrot-kablo-deri zinciri denetlenmelidir.",
        "s. 83; Box 8.3, Şekil 8.6",
    ),
    "filtreler/index.html": E(
        "Filtre gürültüyü azaltırken hedef sinyali de değiştirir",
        [
            ("İki sınır", "Her NCS ve iğne EMG sinyali alçak kesim (high-pass) ve yüksek kesim (low-pass) filtresinden geçer."),
            ("Terminoloji", "Filtrenin adı kestiği değil, geçirdiği frekansları ifade eder: high-pass yüksekleri, low-pass düşükleri geçirir."),
            ("Gürültü", "<10 Hz bileşenler bazal kayma; >10 kHz bileşenler DSAP ve fibrilasyon potansiyellerini örten yüksek frekanslı gürültü oluşturur."),
        ],
        "Filtre ayarı yalnız gürültüyü değil, ölçülen dalga biçimini de belirler.",
        "s. 83-84; Şekil 8.7-8.9",
    ),
    "filtreler/gecirgen-bant.html": E(
        "Motor ve duysal kayıtlar aynı geçirgen bantla değerlendirilmez",
        [
            ("Geçirgen bant", "İki kesim frekansı arasındaki bileşenler korunur; sınırların dışındaki gürültü kademeli olarak zayıflatılır."),
            ("Motor NCS", "Tipik ayar 10 Hz-10 kHz'dir."),
            ("Duysal NCS", "Tipik ayar 20 Hz-2 kHz'dir. DSAP yüksek frekans içeriği taşır; düşük amplitüd nedeniyle yüksek frekanslı gürültüden daha kolay etkilenir."),
        ],
        "Normal değerlerle karşılaştırma aynı çalışma türü ve aynı filtre ayarlarıyla yapılmalıdır.",
        "s. 83-84; Şekil 8.7-8.8",
    ),
    "filtreler/filtre-odunlesimi.html": E(
        "Daha temiz iz, daha doğru iz anlamına gelmeyebilir",
        [
            ("Geçiş kademelidir", "Analog ve dijital filtreler kesim frekansında duvar oluşturmaz; sinyal bileşenleri de kısmen zayıflar."),
            ("Alçak kesim", "Alçak kesim azaltıldığında düşük frekans içeriği artar ve potansiyel süresi uzar."),
            ("Yüksek kesim", "Yüksek kesim 2 kHz'den 0.5 kHz'e düşürüldüğünde yüksek frekans içeriği kaybolur; örnekte DSAP 30 µV'den 16 µV'ye iner."),
        ],
        "Filtre değişikliği sonrası amplitüd ve süre değişimi patoloji olarak yorumlanmamalıdır.",
        "s. 84; Şekil 8.8-8.9",
    ),
    "elektronik-ortalama/index.html": E(
        "Ortalama, tekrarlanabilir yanıtı korur; rastgele gürültüyü söndürür",
        [
            ("Endikasyon", "Filtre ve empedans kontrolüne rağmen mikrovolt düzeyindeki duysal veya mikst yanıtın bazali gürültülü kalabilir."),
            ("Mekanizma", "Ardışık uyarımlar dijitalleştirilir. Rastgele gürültünün pozitif ve negatif fazları birbirini götürür; zamana kilitli yanıt üst üste eklenir."),
            ("Kazanç", "Bazal netleşir; onset latansı ve amplitüd daha güvenilir ölçülür."),
        ],
        "Ortalama, tutarlı artefaktı değil yalnız rastgele gürültüyü azaltır.",
        "s. 84; Şekil 8.10",
    ),
    "stimulus-artefakti/index.html": E(
        "Stimulus artefaktı her kayıtta vardır; sorun DSAP başlangıcını örtmesidir",
        [
            ("Kaynak", "Stimülatör akımı siniri depolarize ederken hacim iletimiyle kayıt elektrotlarına da ulaşır; bu nedenle her sinir ileti çalışmasında stimulus artefaktı oluşur."),
            ("İşlev", "Şok zamanını gösterir ve latans ölçümünün sıfır noktasını belirler."),
            ("Ölçüm hatası", "Kuyruk DSAP onsetiyle çakışırsa amplitüd ve onset latansı yanlış ölçülür. Risk küçük duysal yanıtlar ve kısa uyarı-kayıt mesafelerinde artar."),
        ],
        "Stimulus artefaktının varlığı normaldir; sorun kuyruğunun kaydedilen potansiyeli örtmesidir.",
        "s. 84-85; Şekil 8.11",
    ),
    "stimulus-artefakti/azaltma-yontemleri.html": E(
        "Stimulus artefaktı tek ayarla değil, tüm kayıt geometrisiyle azaltılır",
        [
            ("Toprak ve empedans", "Toprak stimülatör ile kayıt elektrotları arasında olmalı; G1-G2 empedans uyumsuzluğu azaltılmalıdır."),
            ("Kablo", "Koaksiyel kayıt kablosu kullanılmalı; stimülatör ve kayıt kabloları ayrılmalıdır."),
            ("Uyarım ve mesafe", "Stimülatör sinir üzerinde optimize edilerek daha düşük şiddet kullanılmalı; mümkünse uyarı-kayıt mesafesi artırılmalıdır."),
        ],
        "Artefaktı azaltırken gerçek sinir yanıtının supramaksimal uyarıldığından emin olunmalıdır.",
        "s. 85; Box 8.4, Şekil 8.12",
    ),
    "stimulus-artefakti/anot-dondurme.html": E(
        "Katot sabitken anodu döndürmek artefakt geometrisini değiştirir",
        [
            ("Teknik", "Walking the anode sırasında katot yerinde tutulur, anot hafifçe döndürülür; depolarizasyon noktası değişmez."),
            ("Mekanizma", "Katot-anot ekseninin kayıt elektrotlarına göre yönü değişir; hacim iletilen artefaktın polaritesi ve büyüklüğü değişebilir."),
            ("Ölçüm", "Şekil 8.11'de negatif artefakt 29 µV/2.1 ms; nötr 38 µV/2.0 ms; pozitif artefakt 45 µV/1.9 ms ölçtürür."),
        ],
        "Anot döndürme siniri değil, stimulus artefaktının kayıt elektrotlarına projeksiyonunu değiştirir.",
        "s. 85; Şekil 8.11 ve 8.13",
    ),
    "stimulus-artefakti/kablo-ayrimi.html": E(
        "Çakışan kablolar stimulus artefaktını kayıt hattına indükler",
        [
            ("İndüksiyon", "Stimülatör kablosundaki hızlı akım değişimi yakındaki kayıt kablosunda istenmeyen voltaj oluşturabilir."),
            ("Risk", "Paralel veya üst üste uzanan serbest G1-G2 kabloları daha büyük ortak olmayan artefakt toplar."),
            ("Çözüm", "Stimülatör ve kayıt kabloları ayrılmalı; G1-G2 iletkenlerini birbirine yakın tutan koaksiyel kablo tercih edilmelidir."),
        ],
        "Kablo güzergâhı kayıt devresinin bir parçasıdır ve her çalışmada kontrol edilmelidir.",
        "s. 85; Şekil 8.12",
    ),
    "katot-polarite/index.html": E(
        "Depolarizasyon katotta başlar; mesafe ve yön buna göre kurulmalıdır",
        [
            ("Katot kuralı", "Mesafe katot ile G1 arasında ölçülür; katot G1'e bakmalıdır: siyaha siyah."),
            ("Ters polarite", "Katot proksimale dönerse impuls önce 2.5-3.0 cm ek yol alır; distal latans uzar."),
            ("Anodal blok", "Anot altındaki hiperpolarizasyon teorik olarak iletimi engelleyip yanıtı azaltabilir veya yok edebilir; rutin çalışmada nadirdir."),
        ],
        "Her uyarım yerinde katot yönü mesafe ölçümünden önce doğrulanmalıdır.",
        "s. 86-87; Şekil 8.14-8.16",
    ),
    "katot-polarite/latans-hatasi.html": E(
        "Ters polarite distal latansı uzatır; motor segment hızını değiştirmez",
        [
            ("Ek yol", "Katot-anot arası 2.5-3.0 cm nedeniyle distal latans yaklaşık 0.3-0.4 ms uzar."),
            ("Duysal çalışma", "Tüm distal duysal latanslar uzar; kitap yaklaşık 10 m/s yavaşlama bildirir. Şekil 8.16'da 2.2 ms, ters polaritede 2.5 ms'dir."),
            ("Motor çalışma", "Distal motor latans uzar; distal ve proksimal ölçümlerde aynı hata çıkarıldığı için segmental motor İH değişmez."),
        ],
        "Uzamış distal latansla korunmuş motor segment hızı polarite hatasını düşündürmelidir.",
        "s. 86-87; Şekil 8.16",
    ),
    "supramaksimal/index.html": E(
        "NCS ölçümleri tüm aksonların uyarıldığı varsayımına dayanır",
        [
            ("Temel", "Amplitüd, latans ve iletim hızı ancak ilgili sinirin tüm uyarılabilir aksonları depolarize edildiğinde karşılaştırılabilir."),
            ("Eşikler değişir", "Sinir derinliği, anatomi ve bireysel özellikler gerekli akımı değiştirir."),
            ("Örnek", "Median sinirin bilek uyarımı, tibial sinirin popliteal fossa uyarımından çok daha düşük akım gerektirir."),
        ],
        "Yüksek cihaz çıkışı supramaksimal demek değildir; yanıt platosu gösterilmelidir.",
        "s. 87-88; Şekil 8.17",
    ),
    "supramaksimal/nasil-yapilir.html": E(
        "Supramaksimal uyarım, plato gösterilip üzerine %25 çıkılarak kanıtlanır",
        [
            ("Artır", "Akım küçük basamaklarla yükseltilir; her basamakta BKAP/DSAP amplitüdü izlenir."),
            ("Plato", "Amplitüd artık artmadığında tüm uyarılabilir aksonların katıldığı kabul edilir; akım ek %25 artırılır."),
            ("Doğrula", "Amplitüd değişmiyorsa supramaksimal düzey sağlanmıştır. Latans, amplitüd platosuna yaklaşırken bir süre daha kısalabilir."),
        ],
        "Normal aralığa ulaşmak değil, bireyin kendi amplitüd platosunu göstermek gerekir.",
        "s. 87-88; Şekil 8.17",
    ),
    "supramaksimal/yanlis-yorumlar.html": E(
        "Submaksimal uyarım aksonal kayıp veya ileti bloğunu taklit edebilir",
        [
            ("Distal yetersizlik", "Distal yanıt düşükse aksonal kayıp veya anomali innervasyonu yanlış düşünülebilir."),
            ("Proksimal yetersizlik", "Distal supramaksimal, proksimal submaksimalse yapay amplitüd düşüşü ileti bloğu görünümü oluşturur."),
            ("İH varsayımı", "Gerçek segment hızı aynı hızlı liflerin distal ve proksimalde uyarıldığını varsayar; amplitüd normal aralığa girince akımı durdurmak yeterli değildir."),
        ],
        "Her uyarım noktası bağımsız olarak supramaksimal gösterilmelidir.",
        "s. 88; Şekil 8.18",
    ),
    "kostimulasyon/index.html": E(
        "Akım yükseldikçe hedef sinir kadar komşu sinir de uyarılabilir",
        [
            ("Risk", "Patolojik sinir veya kötü temas daha yüksek akım gerektirir; akım alanı komşu sinire yayılır ve yapay büyük yanıt oluşturur."),
            ("Sık bölgeler", "Üst ekstremitede median-ulnar bilek/dirsek/aksilla; alt ekstremitede peroneal-tibial diz çevresi risklidir."),
            ("Proksimal uyarım", "Erb noktası ve C8-T1 kök uyarımında median-ulnar birlikteliği kaçınılmazdır; ayrım için kollizyon çalışmaları gerekir."),
        ],
        "Supramaksimal hedeflenirken ko-stimülasyon eşzamanlı olarak dışlanmalıdır.",
        "s. 88-90; Şekil 8.18-8.20",
    ),
    "kostimulasyon/hata-oruntuleri.html": E(
        "Ko-stimülasyon hem yalancı blok oluşturabilir hem gerçek bloğu gizleyebilir",
        [
            ("Yalancı normal", "Aksonal kayıplı düşük yanıt komşu sinirin katkısıyla normal aralığa çıkabilir."),
            ("Yalancı blok", "Yalnız distalde ko-stimülasyon proksimal yanıtı görece düşük gösterir; yalnız proksimalde ko-stimülasyon anomali innervasyonunu taklit edebilir."),
            ("Gizlenen blok", "Gerçek blok varken proksimal ko-stimülasyon amplitüdü yükseltir ve patolojiyi normal gösterebilir."),
        ],
        "Beklenmedik amplitüd artışında dalga biçimi ve uyarılan kaslar birlikte değerlendirilmelidir.",
        "s. 88-90; Şekil 8.20",
    ),
    "kostimulasyon/onleme-yontemleri.html": E(
        "En düşük akımla en büyük hedef yanıtı veren nokta bulunmalıdır",
        [
            ("Yerleşim araması", "İlk küçük yanıt alınır; akım sabitken stimülatör medial-lateral kaydırılır. En büyük yanıt sinire en yakın konumu gösterir; sonra supramaksimale çıkılır."),
            ("İpuçları", "Ani bifid morfoloji ve kas seğirmesinin değişmesi ko-stimülasyonu düşündürür: median tenar/lumbrikal, ulnar yaygın fleksiyon; peroneal dorsifleksiyon/eversiyon, tibial plantar fleksiyon/inversiyon."),
            ("Eşik ve doğrulama", "0.2 ms uyarıda >50 mA dikkat gerektirir. Şüphede hedef ve komşu kas iki kanaldan eşzamanlı kaydedilir."),
        ],
        "Ko-stimülasyon akımı artırarak değil, önce stimülatör konumunu optimize ederek önlenir.",
        "s. 89-90; Box 8.5, Şekil 8.19-8.20",
    ),
    "motor-elektrot-yerlesimi/index.html": E(
        "Belly-tendon montajında hem G1 hem G2 dalga biçimini belirler",
        [
            ("Standart", "G1 kas karnındaki motor noktaya; G2 distal tendona yerleştirilir."),
            ("Varsayım", "Tendonun elektriksel olarak sessiz olduğu ve kaydın esas olarak G1'i temsil ettiği kabul edilir."),
            ("İki hata yolu", "G1 motor noktadan uzaksa ilk pozitif sapma ve düşük amplitüd; G2 aktif tendon potansiyeli görürse morfoloji ve amplitüd değişir."),
        ],
        "Motor yanıtın teknik doğruluğu yalnız G1'e değil, G1-G2 montajının tamamına bağlıdır.",
        "s. 90-92; Şekil 8.21-8.25",
    ),
    "motor-elektrot-yerlesimi/g1-yerlesimi.html": E(
        "İlk pozitif sapma G1'in motor nokta dışında olduğunu düşündürür",
        [
            ("Mekanizma", "Depolarizasyon motor uç plakta başlar. G1 uzaktaysa hacim iletilen aktivite önce pozitif, depolarizasyon elektrot altına gelince negatif görünür."),
            ("Amplitüd", "BKAP maksimize olmaz; Şekil 8.22'de motor noktada 7.8 mV, dışında 5.6 mV'dir."),
            ("Latans", "İlk pozitif sapma onseti belirsizleştirip latansı yapay uzatabilir; G1, pozitif başlangıç kaybolana kadar taşınmalıdır."),
        ],
        "İlk pozitif sapma anatomik varyanttan önce G1 yerleşim hatası olarak araştırılmalıdır.",
        "s. 90-91; Şekil 8.21-8.23",
    ),
    "motor-elektrot-yerlesimi/g2-yerlesimi.html": E(
        "Tendon G2 özellikle ulnar ve tibial kayıtlarda elektriksel olarak sessiz değildir",
        [
            ("Tendon potansiyeli", "G2 yakın ve proksimal kaslardan hacim iletilen çoğunlukla pozitif bir uzak-alan potansiyeli kaydedebilir."),
            ("Diferansiyel sonuç", "Negatif G1'den pozitif G2 çıkarıldığında BKAP daha büyük negatif görünür; amplitüdün önemli kısmı G2 katkısından gelebilir."),
            ("Tutarlılık", "Şekil 8.25'te G2 konumuna göre 8.3/7.2/5.6 mV ölçülür; sağ-sol farklı G2 yerleşimi yalancı asimetri yaratır."),
        ],
        "Karşılaştırmalı motor çalışmalarda G2 konumu da G1 kadar standartlaştırılmalıdır.",
        "s. 91-92; Şekil 8.24-8.25",
    ),
    "antidromik-ortodromik/index.html": E(
        "Antidromik ve ortodromik iletim hızı aynıdır; amplitüd kayıt mesafesine bağlıdır",
        [
            ("İletim", "Sinir iki yönde eşit iletir; aynı mesafede latans ve İH aynıdır."),
            ("Amplitüd", "Antidromik D2 halka elektrotları dijital sinire yakındır; ortodromik bilek kaydında karpal ligaman ve bağ dokusu araya girer, yanıt küçülür."),
            ("Avantaj", "Yüksek antidromik amplitüd yan karşılaştırma, seri izlem ve küçük patolojik yanıtları bulmada yararlıdır."),
        ],
        "Antidromik-ortodromik amplitüd farkı iletim yönünden değil elektrot-sinir mesafesinden kaynaklanır.",
        "s. 92-93; Şekil 8.26",
    ),
    "antidromik-ortodromik/hacim-iletilen-motor.html": E(
        "Antidromik kayıtta motor potansiyel sahte DSAP oluşturabilir",
        [
            ("Kaynak", "Yalnız duysal lifler kaydedilse de uyarım motor ve duysal lifleri birlikte aktive eder; DSAP'ı hacim iletilen motor yanıt izler."),
            ("Genel durum", "DSAP daha erken olduğu için iki bileşen çoğunlukla ayrılır."),
            ("Tehlike", "DSAP yoksa veya latanslar yakınsa motor yanıtın ilk bileşeni yanlışlıkla duysal yanıt kabul edilebilir."),
        ],
        "Antidromik kayıtta geç motor bileşen tanınmadan küçük bir DSAP varlığı raporlanmamalıdır.",
        "s. 92-93; Şekil 8.26",
    ),
    "elektrot-sinir-mesafesi/index.html": E(
        "Sinirden uzaklaşan elektrot amplitüdü dramatik olarak azaltır",
        [
            ("İlke", "Duysal ve mikst kayıtta araya giren doku, sinyalin özellikle yüksek frekanslı bileşenlerini zayıflatır."),
            ("Şekil 8.27", "Median mikst yanıtta sinir üzerinde 38 µV; 0.5 cm lateralde 31 µV; 1.0 cm lateralde 12 µV ölçülür."),
            ("Bağlantı", "Ortodromik kayıtta sinir çoğu kez daha derindedir; antidromik yanıttan daha küçük amplitüdün temel nedeni budur."),
        ],
        "Düşük duysal amplitüd patoloji kabul edilmeden elektrot-sinir mesafesi doğrulanmalıdır.",
        "s. 93-94; Şekil 8.27",
    ),
    "elektrot-sinir-mesafesi/odem-etkisi.html": E(
        "Ödem siniri elektrottan uzaklaştırır ve duysal yanıtı atenüe eder",
        [
            ("Sık senaryo", "Sural ve süperfisyal peroneal çalışmalarında venöz yetmezlik veya kalp yetmezliğine bağlı ödem sık teknik sınırlamadır."),
            ("Dalga etkisi", "Mesafe artınca amplitüd azalır; süre yayılır, onset hafif kısalabilir ve peak latans uzayabilir. Doku mekânsal yüksek frekans filtresi gibi davranır."),
            ("Yorum", "Belirgin ödemde normal yanıt anlamlıdır; düşük/yok yanıt teknik faktör olarak rapora yansıtılmalıdır."),
        ],
        "Ödemli ekstremitede yok duysal yanıt tek başına nöropati kanıtı değildir.",
        "s. 93-94; Şekil 8.28",
    ),
    "elektrot-sinir-mesafesi/lateral-yerlesim.html": E(
        "Anatomik işaret başlangıç noktasıdır; en büyük yanıt aktif olarak aranmalıdır",
        [
            ("Değişken sinirler", "Palmar mikst, antebrakial, sural, safen ve süperfisyal peroneal sinirlerde ilk elektrot konumu optimal olmayabilir."),
            ("Arama", "Uyarı akımı sabit tutulur; kayıt elektrotları medial ve lateral küçük adımlarla taşınır. En yüksek amplitüd sinire en yakın konumu gösterir."),
            ("İstisna", "Median/ulnar antidromik halka elektrotları dijital sinire yakındır; süperfisyal radial sinir EPL tendonu üzerinde palpe edilebilir."),
        ],
        "Yan karşılaştırmadan önce her tarafta bağımsız elektrot araması yapılmalıdır.",
        "s. 94; Şekil 8.27",
    ),
    "elektrot-sinir-mesafesi/latans-hatasi.html": E(
        "Sinir dışından kayıt onseti kısaltıp iletim hızını yapay yükseltebilir",
        [
            ("Beklenmeyen etki", "Elektrot medial/lateral uzaklaştığında onset latansı sola kayabilir; peak latans görece korunur."),
            ("Hesap hatası", "Kısalmış onset süreyi küçültür; sabit mesafe/süre hesabı yapay hızlı İH verir."),
            ("Birlikte bulgu", "Düşük amplitüd ile beklenmedik hızlı İH aynı kayıtta görülürse elektrot yerleşimi düşünülmelidir."),
        ],
        "Sinire en yakın konum en yüksek amplitüdü ve en güvenilir onseti verir.",
        "s. 94; Şekil 8.29",
    ),
    "aktif-referans-mesafesi/index.html": E(
        "G1-G2 çok yakınsa aynı depolarizasyon iki girişte eşzamanlı görülür",
        [
            ("Sıra", "Depolarize sinir segmenti önce G1, sonra G2 altından geçer; cihaz iki giriş arasındaki farkı kaydeder."),
            ("İptal", "Elektrotlar çok yakınsa G1 ve G2 aynı anda aktif olur; ortak bileşen çıkar ve DSAP amplitüdü düşer."),
            ("Mesafe", "Duysal ve mikst kayıt için 3-4 cm, olağan iletim hızlarında yeterli zamansal ayrım sağlar."),
        ],
        "G1-G2 mesafesi değiştirilirse amplitüd karşılaştırması geçerliliğini kaybeder.",
        "s. 94-96; Şekil 8.30-8.31",
    ),
    "ekstremite-mesafe/index.html": E(
        "Dirsek ekstansiyonu ulnar sinir uzunluğunu olduğundan kısa ölçtürür",
        [
            ("Mekanizma", "Ekstansiyonda ulnar sinir gevşek ve redundanttır; yüzey mesafesi gerçek sinir yolunu eksik temsil eder."),
            ("Hata", "Mesafe küçük, latans farkı aynı kalınca hesaplanan dirsek segment İH yapay yavaşlar."),
            ("Çözüm", "Şekil 8.32'de ekstansiyonda 9 cm, fleksiyonda 10 cm'dir; fleksiyon gerçek uzunluğu daha iyi yansıtır."),
        ],
        "Ulnar dirsek segmenti standart fleksiyon açısında ölçülmeli ve uyarılmalıdır.",
        "s. 95-96; Şekil 8.32",
    ),
    "ekstremite-mesafe/diger-sinirler-caliper.html": E(
        "Düz cetvel, kıvrımlı sinir yolunu sistematik olarak kısaltır",
        [
            ("Riskli segmentler", "Radyal sinirin humerus çevresindeki spirali ve median/ulnar sinirin aksilla-Erb noktası yolu yüzeyde düz değildir."),
            ("Hata", "Düz iki nokta ölçümü gerçek eğrisel sinir uzunluğundan kısa kalır ve İH hesabını bozar."),
            ("Çözüm", "Obstetrik kaliper yüzey konturunu izleyerek alttaki sinir uzunluğunu daha doğru yaklaşıklar."),
        ],
        "Kıvrımlı proksimal segmentlerde ölçüm aracı sinirin anatomik yoluna uymalıdır.",
        "s. 95",
    ),
    "ekstremite-morfoloji/index.html": E(
        "Uyarım noktaları arasında ekstremite pozisyonu değişmemelidir",
        [
            ("Elektrot kayması", "Pozisyon değişince cilt ve elektrotlar alttaki kas/sinire göre yer değiştirebilir."),
            ("Tendon potansiyeli", "Ulnar ve tibial G2 uzak-alan potansiyeli pozisyonla şekil ve latans değiştirebilir."),
            ("Örnek", "Bilek kol düzken, dirsek noktaları fleksiyonda uyarılırsa amplitüd ve İH farkı teknik olarak oluşabilir."),
        ],
        "Aynı sinirin distal ve proksimal uyarımları aynı ekstremite pozisyonunda kaydedilmelidir.",
        "s. 95-97",
    ),
    "sweep-sensitivite/index.html": E(
        "Onset latansı ekran ölçeğine bağlıdır; ayarlar karşılaştırma boyunca sabit kalmalıdır",
        [
            ("Sensitivite", "Sensitivite arttıkça küçük başlangıç sapması daha erken görülür ve onset latansı kısalır."),
            ("Sweep", "Sweep yavaşlayıp ms/div büyüdükçe yatay çözünürlük azalır; onset ölçümü genellikle uzar."),
            ("Karşılaştırma", "Distal-proksimal kayıtlar farklı ayarlardaysa İH hatalıdır. Peak latans ayarlardan daha az etkilenir, ancak peak latansla İH hesaplanamaz."),
        ],
        "Bir sinirin tüm latansları aynı sensitivite ve sweep hızıyla ölçülmelidir.",
        "s. 97; Şekil 8.33-8.34",
    ),
}


PAIRS = [
    ("impedans-gurultu/index.html", ["impedans-gurultu/animasyon-0-gurultu-haritasi.html"]),
    ("impedans-gurultu/diferansiyel-amplifikasyon.html", ["impedans-gurultu/animasyon-1-diferansiyel-amp.html"]),
    ("impedans-gurultu/impedans-uyumsuzlugu.html", ["impedans-gurultu/animasyon-3-ohm-empedans.html"]),
    ("impedans-gurultu/60hz-azaltma.html", ["impedans-gurultu/animasyon-2-gurultu-azaltma.html"]),
    ("filtreler/index.html", ["filtreler/animasyon-0-filtre-spektrumu.html"]),
    ("filtreler/gecirgen-bant.html", ["filtreler/animasyon-1-gecirgen-bant.html"]),
    ("filtreler/filtre-odunlesimi.html", ["filtreler/animasyon-2-filtre-odunlesimi.html"]),
    ("elektronik-ortalama/index.html", ["elektronik-ortalama/animasyon-1-ortalama.html"]),
    ("stimulus-artefakti/index.html", ["stimulus-artefakti/animasyon-0-mekanizma.html"]),
    ("stimulus-artefakti/azaltma-yontemleri.html", ["stimulus-artefakti/animasyon-2-artefakt-azaltma.html"]),
    ("stimulus-artefakti/anot-dondurme.html", ["stimulus-artefakti/animasyon-1-anot-rotasyon.html"]),
    ("stimulus-artefakti/kablo-ayrimi.html", ["stimulus-artefakti/animasyon-3-kablo-induksiyonu.html"]),
    ("katot-polarite/index.html", ["katot-polarite/animasyon-0-depolarizasyon-anodal-blok.html"]),
    ("katot-polarite/latans-hatasi.html", ["katot-polarite/animasyon-1-polarite-tersligi.html"]),
    ("supramaksimal/index.html", ["supramaksimal/animasyon-0-akson-rekrutmani.html"]),
    ("supramaksimal/nasil-yapilir.html", ["supramaksimal/animasyon-1-uyari-egrisi.html"]),
    ("supramaksimal/yanlis-yorumlar.html", ["supramaksimal/animasyon-2-amplitud-farki.html"]),
    ("kostimulasyon/index.html", ["kostimulasyon/animasyon-0-akim-yayilimi.html"]),
    ("kostimulasyon/hata-oruntuleri.html", ["kostimulasyon/animasyon-1-tanisal-hatalar.html"]),
    ("kostimulasyon/onleme-yontemleri.html", ["kostimulasyon/animasyon-2-optimal-yerlesim.html"]),
    ("motor-elektrot-yerlesimi/index.html", ["motor-elektrot-yerlesimi/animasyon-0-belly-tendon-montaj.html"]),
    ("motor-elektrot-yerlesimi/g1-yerlesimi.html", ["motor-elektrot-yerlesimi/animasyon-1-g1-konumu.html"]),
    ("motor-elektrot-yerlesimi/g2-yerlesimi.html", ["motor-elektrot-yerlesimi/animasyon-2-g2-tendon-potansiyeli.html"]),
    ("antidromik-ortodromik/index.html", ["antidromik-ortodromik/animasyon-1-antidromik-vs-ortodromik.html"]),
    ("antidromik-ortodromik/hacim-iletilen-motor.html", ["antidromik-ortodromik/animasyon-2-sahte-dsap.html"]),
    ("elektrot-sinir-mesafesi/index.html", ["elektrot-sinir-mesafesi/animasyon-0-derinlik-filtresi.html"]),
    ("elektrot-sinir-mesafesi/odem-etkisi.html", ["elektrot-sinir-mesafesi/animasyon-1-mesafe-amplitud-latans.html"]),
    ("elektrot-sinir-mesafesi/lateral-yerlesim.html", ["elektrot-sinir-mesafesi/animasyon-2-elektrot-arama.html"]),
    ("elektrot-sinir-mesafesi/latans-hatasi.html", ["elektrot-sinir-mesafesi/animasyon-3-yanlis-hiz.html"]),
    ("aktif-referans-mesafesi/index.html", ["aktif-referans-mesafesi/animasyon-1-g1-g2-mesafesi.html"]),
    ("ekstremite-mesafe/index.html", ["ekstremite-mesafe/animasyon-1-dirsek-pozisyonu.html"]),
    ("ekstremite-mesafe/diger-sinirler-caliper.html", ["ekstremite-mesafe/animasyon-2-kaliper.html"]),
    ("ekstremite-morfoloji/index.html", ["ekstremite-morfoloji/animasyon-1-pozisyon-tutarliligi.html"]),
    ("sweep-sensitivite/index.html", ["sweep-sensitivite/animasyon-1-sensitivite.html", "sweep-sensitivite/animasyon-2-sweep-hizi.html"]),
]


NEW_SIMS = {
    "impedans-gurultu/animasyon-0-gurultu-haritasi.html": {
        "kind": "noise_map", "title": "Gürültü kaynağından diferansiyel çıkışa",
        "subtitle": "Çevre → G1/G2 → ortak mod reddi → kayıt",
        "rule": "Küçük sinyalde önce gürültünün iki girişte eşit görülüp görülmediği değerlendirilir.",
        "controls": [
            ["mismatch", "G1-G2 empedans farkı", 0, 100, 1, 0, "%"],
            ["noise", "Çevresel gürültü", 0, 100, 1, 60, "%"],
        ],
        "presets": [["Eşleşmiş", [0, 60]], ["YBÜ", [35, 95]], ["Doygunluk", [100, 100]]],
        "steps": ["Aynı 50/60 Hz iki girişte iptal olur.", "Empedans farkı ortak gürültüyü diferansiyel sinyale çevirir.", "Büyük fark amplifikatörü doyurup küçük DSAP'ı örter."],
    },
    "impedans-gurultu/animasyon-3-ohm-empedans.html": {
        "kind": "ohm", "title": "Empedans uyumsuzluğu: E = I × R",
        "subtitle": "Aynı indüklenen akım, farklı giriş voltajı",
        "rule": "Düşük empedans kadar G1-G2 empedans eşleşmesi de gereklidir.",
        "controls": [
            ["r1", "G1 empedansı", 1, 20, 1, 5, "kΩ"],
            ["r2", "G2 empedansı", 1, 20, 1, 5, "kΩ"],
        ],
        "presets": [["Eşit 5/5", [5, 5]], ["Hafif fark", [5, 9]], ["Belirgin fark", [4, 18]]],
        "steps": ["R1 = R2 iken indüklenen voltajlar eşittir.", "Aynı akım R2 yüksek olduğunda daha büyük voltaj üretir.", "Amplifikatör V1-V2 farkını büyütür ve hedef sinyali örter."],
    },
    "filtreler/animasyon-0-filtre-spektrumu.html": {
        "kind": "filter_band", "title": "Geçirgen bant: hangi frekanslar kayda kalır?",
        "subtitle": "Bazal kayma · hedef sinyal · yüksek frekanslı gürültü",
        "rule": "Filtre ayarı sinyalin hangi bileşenlerinin ölçüme katılacağını belirler.",
        "controls": [
            ["low", "Alçak kesim", 1, 100, 1, 10, "Hz"],
            ["high", "Yüksek kesim", 500, 20000, 100, 10000, "Hz"],
        ],
        "presets": [["Motor", [10, 10000]], ["Duysal", [20, 2000]], ["Aşırı dar", [100, 500]]],
        "steps": ["Motor bant 10 Hz-10 kHz aralığını korur.", "Duysal kayıtta yüksek kesim 2 kHz'e indirilir.", "Aşırı dar bant gürültüyle birlikte hedef sinyali de keser."],
    },
    "filtreler/animasyon-2-filtre-odunlesimi.html": {
        "kind": "filter_tradeoff", "title": "Filtre ödünleşimi: süre ve amplitüd",
        "subtitle": "Aynı DSAP · farklı filtre · farklı ölçüm",
        "rule": "Filtre değişikliği sonrası dalga biçimi değişikliği patoloji olarak yorumlanmamalıdır.",
        "controls": [
            ["low", "Alçak kesim", 1, 100, 1, 20, "Hz"],
            ["high", "Yüksek kesim", 500, 5000, 100, 2000, "Hz"],
        ],
        "presets": [["Standart", [20, 2000]], ["Uzun süre", [2, 2000]], ["Düşük amplitüd", [20, 500]]],
        "steps": ["Standart duysal filtre dalga biçimini korur.", "Alçak kesim azaltılınca düşük frekans geçer ve süre uzar.", "Yüksek kesim 0.5 kHz'e düşünce amplitüd 30'dan yaklaşık 16 µV'ye iner."],
    },
    "stimulus-artefakti/animasyon-3-kablo-induksiyonu.html": {
        "kind": "cable", "title": "Kablo geometrisi ve indüksiyon",
        "subtitle": "Stimülatör kablosu → kayıt kablosu → stimulus artefaktı",
        "rule": "Stimülatör ve kayıt kabloları ayrılmalı; koaksiyel kayıt kablosu tercih edilmelidir.",
        "controls": [
            ["separation", "Kablolar arası mesafe", 0, 30, 1, 4, "cm"],
            ["coax", "Koaksiyel koruma", 0, 100, 1, 0, "%"],
        ],
        "presets": [["Çakışan", [0, 0]], ["Ayrı", [25, 0]], ["Koaksiyel", [5, 100]]],
        "steps": ["Çakışan kablolar büyük indüklenen artefakt üretir.", "Fiziksel ayrım indüksiyonu hızla azaltır.", "Koaksiyel yapı G1-G2 iletkenlerini aynı dış alana maruz bırakır."],
    },
    "katot-polarite/animasyon-0-depolarizasyon-anodal-blok.html": {
        "kind": "polarity", "title": "Katot yönü, ek iletim yolu ve anodal blok",
        "subtitle": "Doğru polarite · ters polarite · teorik blok",
        "rule": "Katot G1'e bakmalı ve mesafe katottan ölçülmelidir.",
        "controls": [
            ["reverse", "Polarite", 0, 1, 1, 0, ""],
            ["block", "Anodal blok gücü", 0, 100, 1, 0, "%"],
        ],
        "presets": [["Doğru", [0, 0]], ["Ters", [1, 0]], ["Ters + blok", [1, 100]]],
        "steps": ["Doğru polaritede depolarizasyon G1'e yakın katotta başlar.", "Ters polarite impulsa 2.5-3.0 cm ek yol ekler.", "Anot hiperpolarizasyonu teorik olarak yanıtı azaltabilir veya engelleyebilir."],
    },
    "supramaksimal/animasyon-0-akson-rekrutmani.html": {
        "kind": "recruitment", "title": "Akson eşikleri ve BKAP rekrutmanı",
        "subtitle": "Akım arttıkça daha fazla akson, daha büyük BKAP",
        "rule": "Supramaksimal düzey cihaz çıkışıyla değil amplitüd platosuyla kanıtlanır.",
        "controls": [
            ["current", "Uyarı akımı", 0, 120, 1, 20, "mA"],
            ["depth", "Sinir derinliği", 0, 100, 1, 25, "%"],
        ],
        "presets": [["Submaksimal", [25, 25]], ["Plato", [75, 25]], ["Derin sinir", [100, 85]]],
        "steps": ["Düşük eşikli aksonlar önce katılır.", "Akım arttıkça BKAP büyür ve plato oluşur.", "Derin sinirde aynı plato için daha yüksek akım gerekir."],
    },
    "kostimulasyon/animasyon-0-akim-yayilimi.html": {
        "kind": "costim", "title": "Akım alanı hedef sinirden komşu sinire taşabilir",
        "subtitle": "Median hedef · ulnar komşu · iki kas yanıtı",
        "rule": "Akım arttıkça yalnız amplitüd değil, dalga biçimi ve kas seğirmesi de izlenmelidir.",
        "controls": [
            ["current", "Uyarı akımı", 0, 100, 1, 25, "mA"],
            ["offset", "Stimülatör hedefe uzaklığı", 0, 30, 1, 0, "mm"],
        ],
        "presets": [["Hedefte", [35, 0]], ["Yüksek akım", [85, 0]], ["Kötü yerleşim", [85, 25]]],
        "steps": ["Optimal yerleşimde düşük akım yalnız hedef siniri uyarır.", "Akım alanı büyüdüğünde komşu sinir katkısı başlar.", "Kötü yerleşim daha yüksek akım ve daha erken ko-stimülasyon gerektirir."],
    },
    "motor-elektrot-yerlesimi/animasyon-0-belly-tendon-montaj.html": {
        "kind": "montage", "title": "Belly-tendon montajında kayıt G1-G2 farkıdır",
        "subtitle": "Motor nokta · tendon potansiyeli · BKAP",
        "rule": "G1 ve G2 konumu birlikte standartlaştırılmadan amplitüd karşılaştırılamaz.",
        "controls": [
            ["g1", "G1 motor noktadan uzaklık", 0, 30, 1, 0, "mm"],
            ["g2", "G2 tendon aktivitesi", 0, 100, 1, 20, "%"],
        ],
        "presets": [["Standart", [0, 20]], ["G1 uzakta", [30, 20]], ["Aktif G2", [0, 100]]],
        "steps": ["G1 motor noktada, G2 distal tendonda standart BKAP oluşur.", "G1 uzaklaşınca ilk pozitif sapma ve amplitüd kaybı görülür.", "Pozitif tendon potansiyeli G1-G2 sonucunu büyütüp morfolojiyi değiştirir."],
    },
    "antidromik-ortodromik/animasyon-2-sahte-dsap.html": {
        "kind": "false_snap", "title": "Hacim iletilen motor potansiyel sahte DSAP olabilir",
        "subtitle": "Gerçek DSAP · geç motor yanıt · duysal yanıt yokluğu",
        "rule": "Antidromik kayıtta geç motor bileşen tanınmadan küçük DSAP raporlanmamalıdır.",
        "controls": [
            ["snap", "Gerçek DSAP amplitüdü", 0, 30, 1, 20, "µV"],
            ["motor", "Motor uzak-alan amplitüdü", 0, 100, 1, 60, "%"],
        ],
        "presets": [["İkisi var", [20, 60]], ["DSAP küçük", [5, 80]], ["DSAP yok", [0, 100]]],
        "steps": ["DSAP önce, motor uzak-alan yanıtı sonra gelir.", "Küçük DSAP büyük motor bileşen önünde gözden kaçabilir.", "DSAP yokken motor bileşenin ilk fazı sahte duysal yanıt oluşturabilir."],
    },
    "elektrot-sinir-mesafesi/animasyon-0-derinlik-filtresi.html": {
        "kind": "depth", "title": "Doku mesafesi mekânsal yüksek frekans filtresi gibi davranır",
        "subtitle": "Derinlik · amplitüd · dispersiyon · onset/peak",
        "rule": "Düşük duysal amplitüd yorumundan önce elektrot-sinir mesafesi değerlendirilmelidir.",
        "controls": [
            ["depth", "Elektrot-sinir mesafesi", 0, 20, 1, 2, "mm"],
            ["edema", "Ödem", 0, 100, 1, 0, "%"],
        ],
        "presets": [["Yüzeyel", [2, 0]], ["Derin", [15, 0]], ["Ödemli", [12, 100]]],
        "steps": ["Yüzeyel sinirde yüksek frekanslı DSAP korunur.", "Mesafe amplitüdü azaltıp dalgayı genişletir.", "Ödem onseti hafif sola, peak'i sağa kaydırabilir."],
    },
    "elektrot-sinir-mesafesi/animasyon-2-elektrot-arama.html": {
        "kind": "search", "title": "Medial-lateral elektrot araması",
        "subtitle": "Akım sabit · elektrot hareketli · en büyük yanıt hedef",
        "rule": "Her tarafta en yüksek amplitüd bağımsız olarak bulunmadan yan karşılaştırma yapılmamalıdır.",
        "controls": [
            ["offset", "Elektrotun sinire göre konumu", -15, 15, 1, 0, "mm"],
            ["current", "Uyarı akımı", 20, 100, 1, 50, "%"],
        ],
        "presets": [["Sinir üstü", [0, 50]], ["5 mm lateral", [5, 50]], ["10 mm lateral", [10, 50]]],
        "steps": ["Sinir üzerinde amplitüd maksimum ve onset güvenilirdir.", "Küçük lateral hareket amplitüdü belirgin azaltır.", "Uyarı akımı sabitken arama yapılması konum etkisini izole eder."],
    },
    "elektrot-sinir-mesafesi/animasyon-3-yanlis-hiz.html": {
        "kind": "false_speed", "title": "Onset kısalması yapay hızlı iletim hızı üretir",
        "subtitle": "Sabit mesafe ÷ ölçülen süre",
        "rule": "Düşük amplitüd ve beklenmedik hızlı İH birlikteyse elektrot yerleşimi kontrol edilmelidir.",
        "controls": [
            ["offset", "Elektrot lateral uzaklığı", 0, 10, 1, 0, "mm"],
            ["distance", "Uyarı-kayıt mesafesi", 8, 20, 1, 14, "cm"],
        ],
        "presets": [["Doğru", [0, 14]], ["5 mm lateral", [5, 14]], ["10 mm lateral", [10, 14]]],
        "steps": ["Doğru konum gerçek onset ve İH verir.", "Lateral kayıt onseti sola kaydırır ve amplitüdü düşürür.", "Aynı mesafe daha kısa süreye bölündüğünde İH yapay yükselir."],
    },
    "ekstremite-mesafe/animasyon-2-kaliper.html": {
        "kind": "caliper", "title": "Düz cetvel ve eğrisel sinir yolu",
        "subtitle": "Radyal spiral · aksilla-Erb segmenti · obstetrik kaliper",
        "rule": "Kıvrımlı proksimal segmentlerde ölçüm aracı anatomik yüzey konturunu izlemelidir.",
        "controls": [
            ["curve", "Sinir yolu kıvrımı", 0, 100, 1, 70, "%"],
            ["segment", "Segment uzunluğu", 10, 30, 1, 20, "cm"],
        ],
        "presets": [["Düz segment", [0, 20]], ["Radyal spiral", [70, 20]], ["Erb-aksilla", [100, 25]]],
        "steps": ["Düz segmentte cetvel ve sinir yolu eşleşir.", "Kıvrım arttıkça iki nokta cetveli gerçek yolu kısaltır.", "Kaliper yüzey konturunu izleyerek gerçek uzunluğa yaklaşır."],
    },
}


EXISTING_ANIMS = {
    "impedans-gurultu/animasyon-1-diferansiyel-amp.html": [
        ["Eşleşmiş girişlerde 50/60 Hz ortak mod olarak iptal olur.", {"selector": "#mismatchSlider", "value": 0}],
        ["Empedans farkı arttığında ortak gürültü çıkışa sızar.", {"selector": "#mismatchSlider", "value": 100}],
        ["Düşük sensitivitede doygunluğun altında sinüs görünür.", {"text": "10 mV/div"}],
    ],
    "impedans-gurultu/animasyon-2-gurultu-azaltma.html": [
        ["Başlangıçta kontrol zincirinin hiçbir basamağı doğrulanmamıştır.", {"checkboxes": 0}],
        ["Elektrot, deri, jel ve sabitleme düzeltilir.", {"checkboxes": 4}],
        ["Kablo, toprak ve yerleşimle sekiz kontrol tamamlanır.", {"checkboxes": 8}],
    ],
    "filtreler/animasyon-1-gecirgen-bant.html": [
        ["Motor kayıt 10 Hz-10 kHz geçirgen bantla başlar.", {"text": "Motor"}],
        ["Duysal kayıt yüksek frekans gürültüsünü azaltmak için 20 Hz-2 kHz kullanır.", {"text": "Duysal"}],
        ["Yüksek kesim aşırı düşerse DSAP amplitüdü de azalır.", {"selector": "#hffSlider", "value": 48}],
    ],
    "elektronik-ortalama/animasyon-1-ortalama.html": [
        ["Tek uyarıda DSAP vardır fakat bazal gürültülüdür.", {"selector": "#nSlider", "value": 1}],
        ["On uyarı ortalaması Şekil 8.10'daki bazal netleşmesini gösterir.", {"selector": "#nSlider", "value": 10}],
        ["Daha çok ortalama rastgele gürültüyü azaltır; zamana kilitli yanıt kalır.", {"selector": "#nSlider", "value": 32}],
    ],
    "stimulus-artefakti/animasyon-2-artefakt-azaltma.html": [
        ["Başlangıçta Box 8.4 kontrolleri uygulanmamıştır.", {"checkboxes": 0}],
        ["Toprak, empedans, koaksiyel kablo ve yerleşim düzeltilir.", {"checkboxes": 4}],
        ["Şiddet, anot, mesafe ve kablo ayrımı tamamlanır.", {"checkboxes": 8}],
    ],
    "stimulus-artefakti/animasyon-1-anot-rotasyon.html": [
        ["Negatif artefakt amplitüdü düşük, onseti uzun ölçtürür.", {"selector": "#rotSlider", "value": -100}],
        ["Nötr geometride gerçek 38 µV ve 2.0 ms değerleri görülür.", {"selector": "#rotSlider", "value": 0}],
        ["Pozitif artefakt amplitüdü yüksek, onseti kısa ölçtürür.", {"selector": "#rotSlider", "value": 100}],
    ],
    "katot-polarite/animasyon-1-polarite-tersligi.html": [
        ["Katot G1'e bakarken mesafe ve latans doğru ölçülür.", {"text": "Doğru"}],
        ["Ters polarite 2.5-3.0 cm ek yol ve 0.3-0.4 ms gecikme oluşturur.", {"text": "Ters Çevrilmiş"}],
        ["Anodal blok seçeneği teorik amplitüd kaybını gösterir.", {"selector": "#anodalChk", "checked": True}],
    ],
    "supramaksimal/animasyon-1-uyari-egrisi.html": [
        ["Düşük akımda yalnız düşük eşikli aksonlar katılır.", {"selector": "#curSlider", "value": 60}],
        ["Akım arttıkça amplitüd büyür ve latans kısalır.", {"selector": "#curSlider", "value": 140}],
        ["Plato sonrası ek %25 artış supramaksimal düzeyi doğrular.", {"selector": "#curSlider", "value": 210}],
    ],
    "supramaksimal/animasyon-2-amplitud-farki.html": [
        ["Distal submaksimal yanıt aksonal kaybı taklit eder.", {"text": "Örnek A"}],
        ["Proksimal submaksimal yanıt ileti bloğunu taklit eder.", {"text": "Örnek B"}],
        ["Her iki noktada plato sağlandığında gerçek karşılaştırma yapılır.", {"text": "Normal"}],
    ],
    "kostimulasyon/animasyon-1-tanisal-hatalar.html": [
        ["Aksonal kayıpta ko-stimülasyon düşük yanıtı yapay normalleştirebilir.", {"text": "Aksonal Kayıp"}],
        ["Yalnız distalde ko-stimülasyon yalancı ileti bloğu oluşturabilir.", {"text": "Sadece Distalde"}],
        ["Yalnız proksimalde ko-stimülasyon gerçek bloğu gizleyebilir.", {"text": "Sadece Proksimalde"}],
    ],
    "kostimulasyon/animasyon-2-optimal-yerlesim.html": [
        ["Stimülatör hedef sinir üzerindeyken gereken akım en düşüktür.", {"selector": "#posSlider", "value": 0}],
        ["Lateral sapma eşik akımını ve ko-stimülasyon riskini artırır.", {"selector": "#posSlider", "value": 20}],
        ["Medial sapma aynı sorunu karşı yönde üretir.", {"selector": "#posSlider", "value": -20}],
    ],
    "motor-elektrot-yerlesimi/animasyon-1-g1-konumu.html": [
        ["G1 motor noktada iken BKAP maksimum ve başlangıç negatiftir.", {"selector": "#posSlider", "value": 0}],
        ["G1 uzaklaşınca ilk pozitif sapma ve düşük amplitüd oluşur.", {"selector": "#posSlider", "value": 15}],
        ["Karşı yöndeki sapma aynı teknik hatayı yeniden üretir.", {"selector": "#posSlider", "value": -15}],
    ],
    "motor-elektrot-yerlesimi/animasyon-2-g2-tendon-potansiyeli.html": [
        ["Standart G2 konumu beklenen BKAP morfolojisini verir.", {"selector": "#g2Slider", "value": 0}],
        ["G2 tendon potansiyeli arttıkça G1-G2 sonucu büyür.", {"selector": "#g2Slider", "value": 100}],
        ["Sağ-sol farklı G2 konumu yalancı amplitüd asimetrisi yaratır.", {"text": "Farklı Konum"}],
    ],
    "antidromik-ortodromik/animasyon-1-antidromik-vs-ortodromik.html": [
        ["Antidromik kayıt sinire yakın olduğu için yüksek amplitüdlüdür.", {"text": "Antidromik"}],
        ["Ortodromik kayıt daha derinden ve düşük amplitüdle alınır.", {"text": "Ortodromik"}],
        ["Yön değişse de aynı mesafede latans ve İH değişmez.", {"text": "Antidromik"}],
    ],
    "elektrot-sinir-mesafesi/animasyon-1-mesafe-amplitud-latans.html": [
        ["Yüzeyel sinirde amplitüd yüksek, süre dardır.", {"text": "Ödem Yok"}],
        ["Ödem amplitüdü azaltır, dalgayı genişletir.", {"text": "Ödem Var"}],
        ["Uzak kayıt onseti hafif kısaltıp peak'i uzatabilir.", {"selector": "#latSlider", "value": 30}],
    ],
    "aktif-referans-mesafesi/animasyon-1-g1-g2-mesafesi.html": [
        ["1 cm yakınlıkta G1 ve G2 eşzamanlı aktif olur ve iptal artar.", {"selector": "#distSlider", "value": 10}],
        ["2.5 cm'de zamansal ayrım ve amplitüd artar.", {"selector": "#distSlider", "value": 25}],
        ["3-4 cm olağan duysal İH için tercih edilen aralıktır.", {"selector": "#distSlider", "value": 40}],
    ],
    "ekstremite-mesafe/animasyon-1-dirsek-pozisyonu.html": [
        ["Ekstansiyonda yüzey mesafesi ulnar sinir yolunu kısa ölçer.", {"selector": "#flexSlider", "value": 0}],
        ["Fleksiyon mesafeyi gerçek sinir uzunluğuna yaklaştırır.", {"selector": "#flexSlider", "value": 100}],
        ["Aynı latans farkında 9 yerine 10 cm kullanmak yapay yavaşlamayı düzeltir.", {"selector": "#flexSlider", "value": 100}],
    ],
    "ekstremite-morfoloji/animasyon-1-pozisyon-tutarliligi.html": [
        ["Tüm uyarım noktalarında aynı pozisyon karşılaştırılabilir yanıt verir.", {"text": "Tutarlı"}],
        ["Pozisyon değişikliği cilt-elektrot ve tendon potansiyelini değiştirir.", {"text": "Tutarsız"}],
        ["Morfoloji farkı sinir segmenti yerine kayıt geometrisinden kaynaklanabilir.", {"text": "Tutarsız"}],
    ],
    "sweep-sensitivite/animasyon-1-sensitivite.html": [
        ["Düşük sensitivitede küçük onset sapması geç görünür.", {"selector": "#sensSlider", "value": 0}],
        ["Sensitivite arttıkça onset imleci gerçek başlangıca yaklaşır.", {"selector": "#sensSlider", "value": 4}],
        ["Karşılaştırma boyunca aynı µV/div veya mV/div kullanılmalıdır.", {"selector": "#sensSlider", "value": 2}],
    ],
    "sweep-sensitivite/animasyon-2-sweep-hizi.html": [
        ["Hızlı sweep yatay çözünürlüğü artırır.", {"selector": "#sweepSlider", "value": 0}],
        ["Yavaş sweep imleç yerleşimini kabalaştırıp onseti uzatabilir.", {"selector": "#sweepSlider", "value": 4}],
        ["Peak latans daha stabildir; ancak peak ile İH hesaplanamaz.", {"selector": "#sweepSlider", "value": 2}],
    ],
}


EXPLANATION_CSS = r"""
:root{--bg:#071118;--ink:#eef6f8;--muted:#9db1b8;--line:#29434c;--cyan:#48d7e8;--green:#69dfa0;--amber:#ffc05c;--red:#ff6876}
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#03080b;color:var(--ink);font-family:Inter,"Segoe UI",Arial,sans-serif}
body{display:grid;place-items:center;padding:12px}.slide{position:relative;width:min(calc(100vw - 24px),1600px);aspect-ratio:16/9;max-height:calc(100vh - 24px);overflow:hidden;border:1px solid #29434c;background:radial-gradient(circle at 82% 16%,rgba(72,215,232,.10),transparent 34%),linear-gradient(135deg,#0b1921,#061016 72%);box-shadow:0 25px 72px rgba(0,0,0,.5)}
.topline{height:5px;background:linear-gradient(90deg,var(--cyan),var(--green),var(--amber))}.head{display:flex;justify-content:space-between;align-items:center;padding:24px 48px 0}.eyebrow{font-size:15px;font-weight:750;letter-spacing:.13em;color:var(--cyan);text-transform:uppercase}.count{font-size:13px;color:var(--muted);letter-spacing:.07em}
h1{margin:22px 48px 0;max-width:1320px;font-size:clamp(34px,3.15vw,56px);line-height:1.06;letter-spacing:-.035em;font-weight:660}.facts{margin:34px 48px 0;max-width:1320px;border-top:1px solid var(--line)}
.fact{display:grid;grid-template-columns:190px 1fr;gap:26px;padding:19px 0;border-bottom:1px solid var(--line);align-items:start}.fact b{font-size:18px;color:var(--cyan);letter-spacing:.015em}.fact:nth-child(2) b{color:var(--green)}.fact:nth-child(3) b{color:var(--red)}.fact:nth-child(4) b{color:var(--amber)}.fact p{margin:0;font-size:clamp(19px,1.42vw,25px);line-height:1.37;color:#dce9ec}
.rule{position:absolute;left:48px;right:48px;bottom:66px;display:grid;grid-template-columns:105px 1fr;gap:18px;align-items:center;padding-top:16px;border-top:2px solid var(--amber)}.rule strong{color:var(--amber);font-size:18px;letter-spacing:.08em}.rule span{font-size:clamp(18px,1.35vw,24px);line-height:1.3}
nav{position:absolute;left:48px;right:48px;bottom:16px;display:flex;align-items:center;justify-content:space-between;gap:12px;font-size:13px;color:var(--muted)}.nav-links{display:flex;gap:8px}.nav-links a{color:var(--ink);text-decoration:none;border:1px solid #3b5c67;background:#10232c;padding:8px 13px}.nav-links a:hover,.nav-links a:focus-visible{border-color:var(--cyan);outline:none}
@media(max-width:900px){.head{padding:18px 28px 0}h1{margin:18px 28px 0}.facts{margin:24px 28px 0}.fact{grid-template-columns:135px 1fr;padding:13px 0}.rule,nav{left:28px;right:28px}}
"""


SIM_CSS = r"""
:root{--bg:#050b10;--ink:#eef6f8;--muted:#9db1b8;--line:#27434d;--cyan:#48d7e8;--green:#69dfa0;--amber:#ffc05c;--red:#ff6876;--blue:#71baff}
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#03070a;color:var(--ink);font-family:Inter,"Segoe UI",Arial,sans-serif}body{display:grid;place-items:center;padding:10px}
.app{position:relative;width:min(calc(100vw - 20px),1600px);aspect-ratio:16/9;max-height:calc(100vh - 20px);overflow:hidden;border:1px solid #294752;background:#071219;box-shadow:0 28px 80px rgba(0,0,0,.55);display:grid;grid-template-rows:66px minmax(0,1fr) 104px 44px}
header{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:0 24px;border-bottom:1px solid var(--line);background:linear-gradient(180deg,#10212a,#09151c)}.titles{min-width:0}.titles h1{margin:0;font-size:27px;letter-spacing:-.025em;white-space:nowrap}.titles p{margin:4px 0 0;color:var(--muted);font-size:13px}.actions{display:flex;align-items:center;gap:7px}.btn{border:1px solid #3b5b66;background:#10242d;color:var(--ink);padding:8px 11px;cursor:pointer;text-decoration:none;white-space:nowrap}.btn.primary{background:#d9fbff;color:#071014;border-color:#d9fbff;font-weight:750}.btn:hover,.btn:focus-visible{border-color:var(--cyan);outline:none}.btn[disabled]{opacity:.4;cursor:not-allowed}
.stage{position:relative;min-height:0;background:#061017}.stage canvas{position:absolute;inset:0;width:100%;height:100%}.message{position:absolute;left:22px;top:16px;max-width:720px;background:rgba(5,14,19,.88);border-left:3px solid var(--cyan);padding:9px 12px;font-size:16px}.message strong{color:var(--cyan)}.readout{position:absolute;right:22px;top:16px;text-align:right;background:rgba(5,14,19,.86);border-right:3px solid var(--amber);padding:9px 12px}.readout b{display:block;font-size:19px}.readout span{color:var(--muted);font-size:12px}
.controls{display:grid;grid-template-columns:1fr 1fr 1.35fr;gap:22px;align-items:center;padding:10px 22px;background:#0a1820;border-top:1px solid var(--line)}.control label{display:flex;justify-content:space-between;gap:12px;color:var(--muted);font-size:13px;margin-bottom:6px}.control output{color:var(--ink);font-weight:750}.control input{width:100%;accent-color:var(--cyan)}.presets{display:flex;gap:7px;flex-wrap:wrap}.preset{border:1px solid #3a5863;background:#0e2028;color:#dbe8ea;padding:7px 9px;cursor:pointer;font-size:12px}.preset.active,.preset:hover,.preset:focus-visible{border-color:var(--amber);outline:none}
footer{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:0 20px;border-top:1px solid var(--line);background:#081319;color:var(--muted);font-size:12px}.rule{color:#d9e7e9}.rule b{color:var(--amber)}.footer-nav{display:flex;gap:6px}.footer-nav a{color:var(--ink);text-decoration:none;border:1px solid #36545e;padding:6px 9px}
@media(max-width:980px){.app{grid-template-rows:60px minmax(0,1fr) 150px 44px}.controls{grid-template-columns:1fr 1fr}.presets{grid-column:1/-1}.titles h1{font-size:21px}.titles p{display:none}}
"""


def href_from(src_rel: str, dst_rel: str) -> str:
    src = Path(src_rel).parent
    rel = Path(__import__("os").path.relpath(Path(dst_rel), src))
    return rel.as_posix()


def explanation_html(rel: str, data: dict, prev_rel: str, next_rel: str, number: int) -> str:
    import html
    topic = Path(rel).parent.name.replace("-", " ")
    facts = "\n".join(
        f'<article class="fact"><b>{html.escape(label)}</b><p>{html.escape(text)}</p></article>'
        for label, text in data["sections"]
    )
    return f"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(data['title'])}</title><style>{EXPLANATION_CSS}</style></head>
<body><main class="slide" aria-labelledby="slide-title"><div class="topline"></div>
<div class="head"><div class="eyebrow">Nonfizyolojik faktörler · {html.escape(topic)}</div><div class="count">Açıklama {number:02d} / 34</div></div>
<h1 id="slide-title">{html.escape(data['title'])}</h1><section class="facts">{facts}</section>
<div class="rule"><strong>KURAL</strong><span>{html.escape(data['rule'])}</span></div>
<nav><span>Kaynak: {html.escape(data['source'])}</span><div class="nav-links">
<a href="{href_from(rel, prev_rel)}">F1 · Önceki</a><a href="../index.html">F2 · İçindekiler</a><a href="{href_from(rel, next_rel)}">F3 · Animasyon →</a>
</div></nav></main></body></html>"""


SIM_SCRIPT = r"""
const spec=SPEC_DATA;
const canvas=document.getElementById("simCanvas"),ctx=canvas.getContext("2d");
const controls=[...document.querySelectorAll(".control input")];
const outputs=[...document.querySelectorAll(".control output")];
const presets=[...document.querySelectorAll(".preset")];
const msg=document.getElementById("message"),summary=document.getElementById("summary");
const play=document.getElementById("play"),pause=document.getElementById("pause"),free=document.getElementById("free");
let tour=false,paused=false,step=0,timer=null,last=performance.now(),pulse=0;
function resize(){const r=canvas.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);canvas.width=r.width*d;canvas.height=r.height*d;ctx.setTransform(d,0,0,d,0,0)}
addEventListener("resize",resize);resize();
function value(id){return Number(document.getElementById(id).value)}
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function bell(x,m,s){const z=(x-m)/s;return Math.exp(-.5*z*z)}
function fmt(n,d=0){return Number(n).toFixed(d)}
function updateOutputs(){controls.forEach((el,i)=>{const c=spec.controls[i],unit=c[6];outputs[i].textContent=`${Number(el.value).toFixed(c[4]<1?1:0)} ${unit}`.trim()})}
function grid(x,y,w,h){ctx.fillStyle="#03110c";ctx.fillRect(x,y,w,h);ctx.strokeStyle="#12342a";ctx.lineWidth=1;for(let i=0;i<=12;i++){const xx=x+w*i/12;ctx.beginPath();ctx.moveTo(xx,y);ctx.lineTo(xx,y+h);ctx.stroke()}for(let i=0;i<=6;i++){const yy=y+h*i/6;ctx.beginPath();ctx.moveTo(x,yy);ctx.lineTo(x+w,yy);ctx.stroke()}ctx.strokeStyle="#2b6852";ctx.beginPath();ctx.moveTo(x,y+h/2);ctx.lineTo(x+w,y+h/2);ctx.stroke()}
function line(points,color="#69dfa0",width=2,dash=[]){ctx.strokeStyle=color;ctx.lineWidth=width;ctx.setLineDash(dash);ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.stroke();ctx.setLineDash([])}
function text(t,x,y,color="#dce9ec",size=15,align="left",weight=500){ctx.fillStyle=color;ctx.font=`${weight} ${size}px Segoe UI`;ctx.textAlign=align;ctx.fillText(t,x,y);ctx.textAlign="left"}
function scopeTrace(x,y,w,h,fn,color="#69dfa0",dash=[]){grid(x,y,w,h);const pts=[];for(let i=0;i<=500;i++){const t=i/500;pts.push([x+w*t,y+h/2+fn(t)*h*.38])}line(pts,color,2.4,dash)}
function drawNoise(W,H,v){const mis=v[0]/100,noise=v[1]/100;const top=55;ctx.fillStyle="#0b1b23";ctx.fillRect(34,top,W-68,H*.38);text("ÇEVRESEL 50/60 Hz",60,top+35,"#48d7e8",15);for(let i=0;i<4;i++){const x=78+i*68;ctx.strokeStyle="#48d7e8";ctx.beginPath();ctx.arc(x,top+100,18+i*4,0,Math.PI*2);ctx.stroke()}const ax=W*.55,ay=top+105;text("G1",ax-150,ay-38,"#ffc05c",16);text("G2",ax-150,ay+52,"#71baff",16);line([[ax-115,ay-43],[ax-25,ay-20]],"#ffc05c",3);line([[ax-115,ay+45],[ax-25,ay+20]],"#71baff",3);ctx.strokeStyle="#dce9ec";ctx.beginPath();ctx.moveTo(ax-25,ay-60);ctx.lineTo(ax-25,ay+60);ctx.lineTo(ax+70,ay);ctx.closePath();ctx.stroke();text("G1-G2",ax+5,ay+5,"#dce9ec",14,"center");const residual=noise*mis;text(`Ortak gürültü: ${Math.round(noise*100)}%`,W-310,top+68,"#9db1b8",14);text(`Diferansiyel kalan: ${Math.round(residual*100)}%`,W-310,top+98,residual>.35?"#ff6876":"#69dfa0",18);const sx=34,sy=H*.51,sw=W-68,sh=H*.39;scopeTrace(sx,sy,sw,sh,t=>.12*Math.sin(t*15)+residual*1.7*Math.sin(t*2*Math.PI*10));summary.textContent=residual>.55?"Amplifikatör doygunluğu: küçük DSAP seçilemiyor.":residual>.12?"Gürültü hedef sinyale ekleniyor.":"Ortak mod reddi hedef sinyali koruyor."}
function drawOhm(W,H,v){const r1=v[0],r2=v[1],I=2;const V1=r1*I,V2=r2*I,d=Math.abs(V1-V2);text("Aynı indüklenen akım: I = 2 birim",45,80,"#48d7e8",18);const x1=W*.23,x2=W*.48,y=165;[ [x1,r1,V1,"G1","#ffc05c"],[x2,r2,V2,"G2","#71baff"]].forEach(([x,r,V,n,c])=>{text(n,x,y-70,c,20,"center",700);ctx.strokeStyle=c;ctx.lineWidth=4;ctx.strokeRect(x-55,y-42,110,84);text(`R = ${r} kΩ`,x,y,c,16,"center");text(`E = ${V}`,x,y+28,"#dce9ec",15,"center")});text("V1 - V2",W*.72,y-22,"#9db1b8",16,"center");text(`${fmt(d)} birim`,W*.72,y+18,d>12?"#ff6876":"#69dfa0",28,"center",700);text("E = I × R",W*.87,y,"#ffc05c",26,"center",700);const amp=clamp(d/50,0,1.5);scopeTrace(35,H*.5,W-70,H*.4,t=>amp*Math.sin(t*2*Math.PI*8)+.08*Math.sin(t*20));summary.textContent=d<2?"G1 ve G2 voltajları eşit: gürültü iptal.":`Giriş farkı ${fmt(d)} birim: 50/60 Hz çıkışta büyütülüyor.`}
function drawFilterBand(W,H,v){const lo=v[0],hi=v[1];const x=55,y=75,w=W-110,h=205;ctx.fillStyle="#0b1b23";ctx.fillRect(x,y,w,h);const f2x=f=>x+w*(Math.log10(f)-0)/(5);const lx=f2x(lo),hx=f2x(hi);ctx.fillStyle="rgba(105,223,160,.18)";ctx.fillRect(lx,y,hx-lx,h);ctx.strokeStyle="#69dfa0";ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x,y+h);ctx.bezierCurveTo(lx-40,y+h,lx-20,y+22,lx+20,y+22);ctx.lineTo(hx-20,y+22);ctx.bezierCurveTo(hx+20,y+22,hx+40,y+h,x+w,y+h);ctx.stroke();[1,10,100,1000,10000,100000].forEach(f=>{const xx=f2x(f);ctx.strokeStyle="#27434d";ctx.beginPath();ctx.moveTo(xx,y);ctx.lineTo(xx,y+h);ctx.stroke();text(f>=1000?`${f/1000}k`:`${f}`,xx,y+h+22,"#9db1b8",12,"center")});text("<10 Hz bazal kayma",x+90,y+55,"#ffc05c",14,"center");text("HEDEF SİNYAL",x+w*.52,y+70,"#69dfa0",17,"center",700);text(">10 kHz gürültü",x+w-110,y+55,"#ff6876",14,"center");const narrow=clamp((Math.log10(hi/lo)-1)/4,0,1);scopeTrace(35,H*.55,W-70,H*.34,t=>(.7*narrow)*(-bell(t,.36,.035)+.62*bell(t,.43,.05)-.18*bell(t,.52,.07))+.15*(hi>10000?1:0)*Math.sin(t*120));summary.textContent=`Geçirgen bant ${lo} Hz-${hi>=1000?fmt(hi/1000,1)+" kHz":hi+" Hz"}; sınır dışı bileşenler kademeli zayıflıyor.`}
function drawFilterTradeoff(W,H,v){const lo=v[0],hi=v[1];const dur=clamp(1+Math.log10(20/lo)*.22,.75,1.65),amp=clamp(hi/2000,.35,1.3);text(`Süre katsayısı ×${dur.toFixed(2)}`,55,76,"#ffc05c",20);text(`Amplitüd ≈ ${Math.round(30*amp)} µV`,W-260,76,"#69dfa0",20);const fn0=t=>-.85*bell(t,.38,.035)+.58*bell(t,.46,.055)-.14*bell(t,.57,.08);const fn=t=>amp*(-.85*bell(t,.38,.035*dur)+.58*bell(t,.46,.055*dur)-.14*bell(t,.57,.08*dur));scopeTrace(35,100,W-70,H*.72,fn0,"#ffc05c",[7,5]);const x=35,y=100,w=W-70,h=H*.72;const pts=[];for(let i=0;i<=500;i++){const t=i/500;pts.push([x+w*t,y+h/2+fn(t)*h*.38])}line(pts,"#69dfa0",2.7);text("kesikli: standart 20 Hz-2 kHz",60,y+h-22,"#ffc05c",13);text("yeşil: seçilen filtre",290,y+h-22,"#69dfa0",13);summary.textContent=hi<=600?"Yüksek kesim aşırı düşük: DSAP amplitüdü yaklaşık 30 → 16 µV.":lo<=3?"Alçak kesim düşük: potansiyel süresi uzuyor.":"Standart duysal filtre: ölçüm referansına yakın."}
function drawCable(W,H,v){const sep=v[0],coax=v[1]/100,ind=clamp((1-sep/30)*(1-.88*coax),0,1);text("Stimülatör kablosu",60,70,"#ff6876",17);text("G1 / G2 kayıt kablosu",60,108,"#48d7e8",17);const y1=165,y2=165+sep*4;line([[50,y1],[W-60,y1]],"#ff6876",7);line([[50,y2],[W-60,y2]],"#48d7e8",coax?10:4);if(coax){line([[50,y2],[W-60,y2]],"#dbe7ea",2,[6,5]);text("koaksiyel dış kalkan",W*.5,y2+34,"#9db1b8",14,"center")}for(let i=0;i<5;i++){ctx.strokeStyle=`rgba(255,104,118,${ind*(.65-i*.09)})`;ctx.beginPath();ctx.arc(W*.5,y1,32+i*19,0,Math.PI*2);ctx.stroke()}text(`İndüklenen artefakt: ${Math.round(ind*100)}%`,W-330,78,ind>.55?"#ff6876":"#69dfa0",19);scopeTrace(35,H*.52,W-70,H*.36,t=>ind*(1.5*Math.exp(-t*16)-.75*Math.exp(-t*5))+.12*(-bell(t,.55,.03)+.5*bell(t,.62,.05)));summary.textContent=ind>.55?"Kablolar çakışıyor: stimulus artefaktı kayıt hattına indükleniyor.":coax>.7?"Koaksiyel kalkan ve yakın G1-G2 iletkenleri ortak gürültüyü azaltıyor.":"Fiziksel ayrım indüksiyonu azaltıyor."}
function drawPolarity(W,H,v){const rev=v[0]>.5,block=v[1]/100;const y=170,x1=160,x2=W-180;line([[x1,y],[x2,y]],"#ffc05c",6);const cath=rev?W*.38:W*.58,an=rev?W*.58:W*.38;ctx.fillStyle="#161d21";ctx.beginPath();ctx.arc(cath,y-35,22,0,Math.PI*2);ctx.fill();ctx.strokeStyle="#fff";ctx.stroke();ctx.fillStyle="#b33e49";ctx.beginPath();ctx.arc(an,y-35,22,0,Math.PI*2);ctx.fill();ctx.stroke();text("Katot",cath,y-70,"#dce9ec",15,"center");text("Anot",an,y-70,"#ff9aa3",15,"center");text("G1",x2,y-35,"#48d7e8",18,"center",700);if(block>0){ctx.fillStyle=`rgba(255,104,118,${.2+.5*block})`;ctx.fillRect(an-14,y-20,28,40);text("hiperpolarizasyon",an,y+48,"#ff6876",13,"center")}const latency=2+(rev?.35:0),amp=38*(1-.85*block);scopeTrace(35,H*.48,W-70,H*.4,t=>amp/38*(-bell(t,.25+latency/20,.035)+.55*bell(t,.32+latency/20,.05)));summary.textContent=block>.7?`Anodal blok modeli: yanıt ${Math.round(amp)} µV'ye düşüyor.`:rev?`Ters polarite: yaklaşık ${latency.toFixed(2)} ms; ek 2.5-3.0 cm yol.`:"Doğru polarite: depolarizasyon G1'e yakın katotta başlıyor."}
function drawRecruitment(W,H,v){const cur=v[0],depth=v[1]/100;const effective=cur*(1-.55*depth),n=Math.round(clamp(effective/70,0,1)*28);text(`Katılan akson: ${n}/28`,55,70,n===28?"#69dfa0":"#ffc05c",21);for(let i=0;i<28;i++){const x=70+(i%14)*(W-140)/13,y=115+Math.floor(i/14)*62;ctx.fillStyle=i<n?"#69dfa0":"#29434d";ctx.beginPath();ctx.arc(x,y,12,0,Math.PI*2);ctx.fill();text(`${22+i*2}`,x,y+4,i<n?"#04100c":"#9db1b8",10,"center",700)}const amp=8*n/28;scopeTrace(35,H*.48,W-70,H*.4,t=>amp/8*(-bell(t,.36,.035)+.58*bell(t,.44,.055)-.15*bell(t,.55,.08)));summary.textContent=n<28?`Submaksimal: ${28-n} akson henüz uyarılmadı; BKAP ${amp.toFixed(1)} mV.`:`Plato: tüm aksonlar katıldı; BKAP ${amp.toFixed(1)} mV. Ek %25 ile doğrulayın.`}
function drawCostim(W,H,v){const cur=v[0],off=v[1],radius=45+cur*1.7,center=W*.38+off*4;const y1=150,y2=245;line([[80,y1],[W-100,y1]],"#ffc05c",6);line([[80,y2],[W-100,y2]],"#71baff",6);text("Hedef median",90,y1-18,"#ffc05c",16);text("Komşu ulnar",90,y2-18,"#71baff",16);ctx.strokeStyle="rgba(72,215,232,.65)";ctx.lineWidth=4;ctx.beginPath();ctx.arc(center,y1,radius,0,Math.PI*2);ctx.stroke();const target=clamp((cur-18+Math.max(0,15-off))/35,0,1),adj=clamp((radius-(y2-y1))/110,0,1);text(`Hedef yanıt ${Math.round(target*100)}%`,W-340,y1+8,"#69dfa0",18);text(`Komşu katkı ${Math.round(adj*100)}%`,W-340,y2+8,adj>.15?"#ff6876":"#9db1b8",18);scopeTrace(35,H*.58,W-70,H*.3,t=>target*(-bell(t,.28,.035)+.6*bell(t,.36,.06))+adj*(-.7*bell(t,.34,.035)+.45*bell(t,.46,.06)));summary.textContent=adj>.35?"Ko-stimülasyon: amplitüd ve morfoloji artık iki sinirin toplamı.":target<.8?"Hedef sinir submaksimal; stimülatör konumu optimize edilmeli.":"Hedef sinir seçici ve yeterli uyarılıyor."}
function drawMontage(W,H,v){const g1=v[0],g2=v[1]/100;const x=80,y=115,w=W-160,h=155;ctx.fillStyle="#8f5148";ctx.beginPath();ctx.ellipse(W*.5,y+70,w*.42,62,0,0,Math.PI*2);ctx.fill();ctx.fillStyle="#d8b28d";ctx.fillRect(W*.77,y+38,w*.14,64);const g1x=W*.5+g1*8,g2x=W*.82;ctx.fillStyle="#20282d";ctx.beginPath();ctx.arc(g1x,y+16,18,0,Math.PI*2);ctx.fill();ctx.fillStyle="#b84a55";ctx.beginPath();ctx.arc(g2x,y+16,18,0,Math.PI*2);ctx.fill();text("G1",g1x,y-12,"#dce9ec",15,"center");text("G2",g2x,y-12,"#ff9aa3",15,"center");text("motor nokta",W*.5,y+80,"#ffc05c",14,"center");const off=clamp(g1/30,0,1),amp=(7.8-2.2*off)*(1+.18*g2),pos=.28*off;scopeTrace(35,H*.52,W-70,H*.36,t=>pos*bell(t,.30,.025)-amp/7.8*bell(t,.36,.04)+.55*amp/7.8*bell(t,.44,.06));summary.textContent=off>.5?"G1 motor nokta dışında: ilk pozitif sapma ve düşük BKAP.":g2>.75?"Aktif G2 tendon potansiyeli BKAP'ı büyütüyor ve morfolojiyi değiştiriyor.":"Standart belly-tendon montajı."}
function drawFalseSnap(W,H,v){const snap=v[0]/20,motor=v[1]/100;text("Duysal volley",65,85,"#ffc05c",17);line([[65,110],[W*.58,110]],"#ffc05c",5);text("Motor volley",65,165,"#71baff",17);line([[65,190],[W*.78,190]],"#71baff",5);const fn=t=>snap*(-bell(t,.32,.025)+.5*bell(t,.37,.035))+motor*(-.65*bell(t,.52,.045)+.48*bell(t,.61,.07));scopeTrace(35,H*.43,W-70,H*.46,fn);ctx.strokeStyle="#ffc05c";ctx.setLineDash([5,4]);ctx.beginPath();ctx.moveTo(35+(W-70)*.32,H*.43);ctx.lineTo(35+(W-70)*.32,H*.89);ctx.stroke();ctx.setLineDash([]);summary.textContent=snap<.05&&motor>.5?"Gerçek DSAP yok: motor yanıtın ilk fazı sahte DSAP olarak seçilebilir.":snap<.4?"Küçük DSAP büyük motor uzak-alan potansiyeli önünde zor seçiliyor.":"DSAP ve geç motor bileşen zaman içinde ayrılıyor."}
function drawDepth(W,H,v){const depth=v[0]+v[1]/15;const att=Math.exp(-depth/14),wide=1+depth/25;ctx.fillStyle="#c98f72";ctx.fillRect(60,70,W-120,75);ctx.fillStyle="#d5b99d";ctx.fillRect(60,145,W-120,depth*5+25);line([[80,190+depth*5],[W-100,190+depth*5]],"#ffc05c",7);ctx.fillStyle="#20282d";ctx.beginPath();ctx.arc(W*.5,48,18,0,Math.PI*2);ctx.fill();line([[W*.5,65],[W*.5,180+depth*5]],"#48d7e8",2,[5,5]);text(`${Math.round(depth)} mm`,W*.5+12,120+depth*2,"#48d7e8",16);const fn=t=>att*(-bell(t,.36,.035*wide)+.58*bell(t,.44,.055*wide)-.15*bell(t,.55,.08*wide));scopeTrace(35,H*.56,W-70,H*.32,fn);summary.textContent=`Amplitüd ≈ ${Math.round(38*att)} µV; doku mesafesi dalgayı atenüe ediyor ve genişletiyor.`}
function drawSearch(W,H,v){const off=v[0],cur=v[1]/100,amp=38*Math.exp(-Math.pow(off/7.5,2))*cur/.5;const cx=W*.5,cy=190;ctx.fillStyle="#c98f72";ctx.fillRect(50,65,W-100,220);ctx.fillStyle="#ffc05c";ctx.beginPath();ctx.arc(cx,cy,28,0,Math.PI*2);ctx.fill();const ex=cx+off*18;ctx.fillStyle="#20282d";ctx.beginPath();ctx.arc(ex,85,19,0,Math.PI*2);ctx.fill();line([[ex,105],[ex,cy-32]],"#48d7e8",2,[5,5]);text(`offset ${off} mm`,ex,55,"#48d7e8",15,"center");scopeTrace(35,H*.54,W-70,H*.34,t=>amp/38*(-bell(t,.36-Math.abs(off)*.004,.035)+.55*bell(t,.44,.055)));summary.textContent=`Amplitüd ${Math.max(1,amp).toFixed(0)} µV; ${Math.abs(off)<2?"elektrot sinir üzerinde.":"küçük lateral hareket yanıtı belirgin azaltıyor."}`}
function drawFalseSpeed(W,H,v){const off=v[0],dist=v[1],trueLat=dist/7,meas=trueLat-off*.035,trueCV=dist/trueLat*10,measCV=dist/meas*10;text(`Mesafe = ${dist} cm`,55,75,"#48d7e8",19);text(`Gerçek onset ${trueLat.toFixed(2)} ms`,55,112,"#ffc05c",18);text(`Ölçülen onset ${meas.toFixed(2)} ms`,55,145,"#69dfa0",18);text("İH = mesafe / süre",W*.58,92,"#9db1b8",18);text(`${trueCV.toFixed(0)} → ${measCV.toFixed(0)} m/s`,W*.78,125,measCV>trueCV+5?"#ff6876":"#69dfa0",30,"center",700);scopeTrace(35,H*.42,W-70,H*.46,t=>-.8*bell(t,.30-off*.004,.035)+.5*bell(t,.38-off*.004,.055));summary.textContent=off>3?`Onset ${Math.abs(trueLat-meas).toFixed(2)} ms erken seçildi: İH yapay ${measCV.toFixed(0)} m/s.`:"Elektrot sinir üzerinde: onset ve İH güvenilir."}
function drawCaliper(W,H,v){const curve=v[0]/100,seg=v[1],x1=100,x2=W-100,y=210;line([[x1,y],[x2,y]],"#9db1b8",2,[7,5]);const pts=[];let length=0,prev=null;for(let i=0;i<=220;i++){const t=i/220,x=x1+(x2-x1)*t,yy=y-curve*120*Math.sin(Math.PI*t)-curve*35*Math.sin(3*Math.PI*t);pts.push([x,yy]);if(prev)length+=Math.hypot(x-prev[0],yy-prev[1]);prev=[x,yy]}line(pts,"#ffc05c",7);const chord=x2-x1,ratio=length/chord;ctx.strokeStyle="#48d7e8";ctx.lineWidth=4;ctx.beginPath();ctx.arc(W*.5,y-curve*120,120+curve*30,Math.PI*.15,Math.PI*.85);ctx.stroke();text(`Düz cetvel: ${seg.toFixed(0)} cm`,W*.28,78,"#9db1b8",20,"center");text(`Kontur/kaliper: ${(seg*ratio).toFixed(1)} cm`,W*.72,78,"#69dfa0",20,"center");text("yüzey konturunu izleyen kaliper",W*.5,y+65,"#48d7e8",16,"center");summary.textContent=curve>.3?`Düz ölçüm gerçek eğrisel yolu ${(seg*(ratio-1)).toFixed(1)} cm kısa gösteriyor.`:"Düz segmentte cetvel ve sinir yolu eşleşiyor."}
function draw(now){const r=canvas.getBoundingClientRect(),W=r.width,H=r.height,v=controls.map(x=>Number(x.value));ctx.clearRect(0,0,W,H);ctx.fillStyle="#061017";ctx.fillRect(0,0,W,H);switch(spec.kind){case"noise_map":drawNoise(W,H,v);break;case"ohm":drawOhm(W,H,v);break;case"filter_band":drawFilterBand(W,H,v);break;case"filter_tradeoff":drawFilterTradeoff(W,H,v);break;case"cable":drawCable(W,H,v);break;case"polarity":drawPolarity(W,H,v);break;case"recruitment":drawRecruitment(W,H,v);break;case"costim":drawCostim(W,H,v);break;case"montage":drawMontage(W,H,v);break;case"false_snap":drawFalseSnap(W,H,v);break;case"depth":drawDepth(W,H,v);break;case"search":drawSearch(W,H,v);break;case"false_speed":drawFalseSpeed(W,H,v);break;case"caliper":drawCaliper(W,H,v);break}last=now;requestAnimationFrame(draw)}
function applyPreset(i,user=false){const vals=spec.presets[i][1];controls.forEach((el,j)=>{el.value=vals[j];el.dispatchEvent(new Event("input",{bubbles:true}))});presets.forEach((b,j)=>b.classList.toggle("active",j===i));if(user){msg.innerHTML=`<strong>Laboratuvar:</strong> ${spec.presets[i][0]} koşulu.`}}
function lock(flag){controls.forEach(x=>x.disabled=flag);presets.forEach(x=>x.disabled=flag)}
function runStep(){clearTimeout(timer);if(step>=Math.min(3,spec.presets.length)){tour=false;paused=false;lock(false);play.textContent="Gösterimi yinele";play.disabled=false;pause.disabled=true;msg.innerHTML="<strong>Serbest laboratuvar:</strong> değişkenleri ayarlayın ve ölçüm sonucunu izleyin.";return}applyPreset(step);msg.innerHTML=`<strong>${step+1}. aşama:</strong> ${spec.steps[step]}`;step++;timer=setTimeout(runStep,2400)}
function start(){step=0;tour=true;paused=false;lock(true);play.disabled=true;pause.disabled=false;pause.textContent="Duraklat";runStep()}
play.addEventListener("click",start);pause.addEventListener("click",()=>{if(!tour)return;paused=!paused;pause.textContent=paused?"Sürdür":"Duraklat";if(paused)clearTimeout(timer);else runStep()});free.addEventListener("click",()=>{clearTimeout(timer);tour=false;lock(false);play.disabled=false;pause.disabled=true;msg.innerHTML="<strong>Serbest laboratuvar:</strong> değişkenleri ayarlayın ve ölçüm sonucunu izleyin."});
controls.forEach(x=>x.addEventListener("input",()=>{updateOutputs();presets.forEach(b=>b.classList.remove("active"))}));presets.forEach((b,i)=>b.addEventListener("click",()=>applyPreset(i,true)));
updateOutputs();applyPreset(0);lock(true);requestAnimationFrame(draw);
"""


def new_sim_html(rel: str, spec: dict, prev_rel: str, next_rel: str) -> str:
    import html
    controls = "\n".join(
        f"""<div class="control"><label for="{c[0]}"><span>{html.escape(c[1])}</span><output></output></label>
<input id="{c[0]}" type="range" min="{c[2]}" max="{c[3]}" step="{c[4]}" value="{c[5]}"></div>"""
        for c in spec["controls"]
    )
    presets = "\n".join(
        f'<button class="preset{" active" if i == 0 else ""}" type="button">{html.escape(p[0])}</button>'
        for i, p in enumerate(spec["presets"])
    )
    data = json.dumps(spec, ensure_ascii=False).replace("</", "<\\/")
    script = SIM_SCRIPT.replace("SPEC_DATA", data)
    return f"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(spec['title'])}</title><style>{SIM_CSS}</style></head>
<body><main class="app" aria-labelledby="sim-title"><header><div class="titles"><h1 id="sim-title">{html.escape(spec['title'])}</h1><p>{html.escape(spec['subtitle'])}</p></div>
<div class="actions"><button class="btn primary" id="play">Gösterimi başlat</button><button class="btn" id="pause" disabled>Duraklat</button><button class="btn" id="free">Serbest laboratuvar</button></div></header>
<section class="stage"><canvas id="simCanvas" aria-label="{html.escape(spec['title'])} interaktif simülasyonu"></canvas>
<div class="message" id="message"><strong>Önce gösterim:</strong> üç aşamadan sonra kontroller açılacak.</div>
<div class="readout"><b id="summary">Model hazırlanıyor</b><span>Kitap mekanizmasına dayalı göreceli simülasyon</span></div></section>
<section class="controls">{controls}<div class="control"><label><span>Klinik koşul</span><output>Preset</output></label><div class="presets">{presets}</div></div></section>
<footer><div class="rule"><b>Kural:</b> {html.escape(spec['rule'])}</div><div class="footer-nav"><a href="{href_from(rel, prev_rel)}">F1</a><a href="../index.html">F2</a><a href="{href_from(rel, next_rel)}">F3</a></div></footer>
</main><script>{script}</script></body></html>"""


GUIDED_STYLE = r"""
/* guided-tour-v2 */
.guided-tour-v2{position:absolute;z-index:80;top:58px;right:18px;width:min(620px,calc(100% - 36px));display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px;align-items:center;padding:10px 12px;background:rgba(5,17,23,.96);border:1px solid #4a6a75;border-left:4px solid #48d7e8;box-shadow:0 10px 32px rgba(0,0,0,.30);color:#eef6f8;font-family:Inter,"Segoe UI",Arial,sans-serif}
.guided-tour-v2 .gt-copy{min-width:0}.guided-tour-v2 .gt-kicker{display:block;color:#48d7e8;font-size:11px;font-weight:800;letter-spacing:.10em;text-transform:uppercase;margin-bottom:3px}.guided-tour-v2 .gt-text{display:block;font-size:13px;line-height:1.28}.guided-tour-v2 .gt-actions{display:flex;gap:6px;align-items:center}
.guided-tour-v2 button{border:1px solid #4a6a75;background:#10242d;color:#eef6f8;padding:7px 9px;cursor:pointer;font-size:12px;white-space:nowrap}.guided-tour-v2 button.gt-primary{background:#d9fbff;color:#071014;border-color:#d9fbff;font-weight:800}.guided-tour-v2 button:disabled{opacity:.42;cursor:not-allowed}
.guided-tour-v2 .gt-progress{position:absolute;left:0;right:0;bottom:-3px;height:3px;background:#18333d}.guided-tour-v2 .gt-progress i{display:block;height:100%;width:0;background:linear-gradient(90deg,#48d7e8,#69dfa0);transition:width .25s}
@media(max-width:900px){.guided-tour-v2{top:52px;left:12px;right:12px;width:auto;grid-template-columns:1fr}.guided-tour-v2 .gt-actions{justify-content:flex-end}.guided-tour-v2 .gt-text{font-size:12px}}
"""


def guided_script(steps: list) -> str:
    payload = json.dumps(steps, ensure_ascii=False).replace("</", "<\\/")
    return r"""
<script>
(() => {
  const GT_STEPS = __GT_STEPS__;
  const panel = document.getElementById("guidedTourV2");
  const text = document.getElementById("gtText");
  const start = document.getElementById("gtStart");
  const pause = document.getElementById("gtPause");
  const free = document.getElementById("gtFree");
  const fill = document.getElementById("gtFill");
  if (!panel || !GT_STEPS.length) return;
  let index = 0, timer = null, paused = false, running = false;
  const candidates = [...document.querySelectorAll("input, select, textarea, button")]
    .filter(el => !el.closest("#guidedTourV2"));
  function lock(on) {
    candidates.forEach(el => {
      el.style.pointerEvents = on ? "none" : "";
      el.style.filter = on ? "saturate(.45)" : "";
      el.setAttribute("aria-disabled", on ? "true" : "false");
    });
  }
  function fire(el) {
    ["input","change"].forEach(name => el.dispatchEvent(new Event(name,{bubbles:true})));
  }
  function clickByText(needle) {
    const el = [...document.querySelectorAll("button,[role=button],label,a")]
      .find(node => !node.closest("#guidedTourV2") &&
        (node.textContent || "").trim().toLocaleLowerCase("tr").includes(needle.toLocaleLowerCase("tr")));
    if (el) el.click();
  }
  function apply(action) {
    if (!action) return;
    if (Object.prototype.hasOwnProperty.call(action,"checkboxes")) {
      const boxes = [...document.querySelectorAll('input[type="checkbox"]')];
      boxes.forEach((box,i) => { box.checked = i < action.checkboxes; fire(box); });
      return;
    }
    if (action.text) { clickByText(action.text); return; }
    const el = action.selector ? document.querySelector(action.selector) : null;
    if (!el) return;
    if (Object.prototype.hasOwnProperty.call(action,"checked")) el.checked = action.checked;
    if (Object.prototype.hasOwnProperty.call(action,"value")) el.value = action.value;
    fire(el);
  }
  function finish() {
    clearTimeout(timer); running = false; paused = false; lock(false);
    start.disabled = false; pause.disabled = true; pause.textContent = "Duraklat";
    start.textContent = "Gösterimi yinele"; fill.style.width = "100%";
    text.innerHTML = "<b>Serbest laboratuvar:</b> aynı değişkenleri kendiniz ayarlayın; teknik hatayı yeniden üretin.";
  }
  function advance() {
    clearTimeout(timer);
    if (index >= GT_STEPS.length) { finish(); return; }
    const [copy,action] = GT_STEPS[index];
    apply(action);
    text.innerHTML = `<b>${index+1}. aşama:</b> ${copy}`;
    fill.style.width = `${((index+1)/GT_STEPS.length)*100}%`;
    index += 1;
    timer = setTimeout(advance,2500);
  }
  function begin() {
    index = 0; paused = false; running = true; lock(true);
    start.disabled = true; pause.disabled = false; pause.textContent = "Duraklat";
    advance();
  }
  start.addEventListener("click",begin);
  pause.addEventListener("click",() => {
    if (!running) return;
    paused = !paused; pause.textContent = paused ? "Sürdür" : "Duraklat";
    if (paused) clearTimeout(timer); else advance();
  });
  free.addEventListener("click",finish);
  lock(true);
})();
</script>
""".replace("__GT_STEPS__", payload)


def inject_guided_tour(text: str, steps: list) -> str:
    if "guided-tour-v2" in text:
        text = re.sub(
            r"\s*<!-- guided-tour-v2 -->.*?<!-- /guided-tour-v2 -->\s*",
            "\n",
            text,
            flags=re.S,
        )
        text = re.sub(r"\s*/\* guided-tour-v2 \*/.*?</style>", "</style>", text, count=1, flags=re.S)
    panel = """<!-- guided-tour-v2 -->
<aside class="guided-tour-v2" id="guidedTourV2" aria-label="Rehberli gösterim">
  <div class="gt-copy"><span class="gt-kicker">Önce rehberli gösterim</span><span class="gt-text" id="gtText">Üç klinik durumu sırayla izleyin; sonra kontroller açılacak.</span></div>
  <div class="gt-actions"><button class="gt-primary" id="gtStart" type="button">Gösterimi başlat</button><button id="gtPause" type="button" disabled>Duraklat</button><button id="gtFree" type="button">Serbest laboratuvar</button></div>
  <div class="gt-progress"><i id="gtFill"></i></div>
</aside>
""" + guided_script(steps) + "\n<!-- /guided-tour-v2 -->"
    if "</style>" in text:
        text = text.replace("</style>", GUIDED_STYLE + "\n</style>", 1)
    else:
        text = text.replace("</head>", f"<style>{GUIDED_STYLE}</style></head>", 1)
    text = text.replace("</body>", panel + "\n</body>", 1)
    return text


def patch_nav(text: str, src_rel: str, prev_rel: str, next_rel: str) -> str:
    destinations = {
        "F1": href_from(src_rel, prev_rel),
        "F2": href_from(src_rel, "index.html"),
        "F3": href_from(src_rel, next_rel),
    }
    for key, href in destinations.items():
        pattern = re.compile(
            rf'(<a\b[^>]*\bhref=)(["\'])[^"\']*\2([^>]*>\s*{key}\b)',
            flags=re.I | re.S,
        )
        text, count = pattern.subn(rf'\1"{href}"\3', text, count=1)
        if count == 0:
            pattern = re.compile(
                rf'(<a\b[^>]*)(>.*?\b{key}\b.*?</a>)',
                flags=re.I | re.S,
            )
            text, _ = pattern.subn(rf'\1 href="{href}"\2', text, count=1)
    return text


def deploy_stimulus_prototype(rel: str, prev_rel: str, next_rel: str) -> None:
    src_html = STAGING / "stimulus-artefakti-simulator-prototip.html"
    src_img = STAGING / "stimulus-artifact-forearm.png"
    if not src_html.exists() or not src_img.exists():
        raise FileNotFoundError("Approved stimulus prototype or anatomy image is missing.")
    dst = ANIM / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = src_html.read_text(encoding="utf-8")
    nav = f"""<nav class="prototype-nav" aria-label="Sunum gezinme">
<a class="btn" title="Önceki sayfa" aria-label="Önceki sayfa" href="{href_from(rel, prev_rel)}">F1</a>
<a class="btn" title="İçindekiler" aria-label="İçindekiler" href="{href_from(rel, 'index.html')}">F2</a>
<a class="btn" title="Sonraki sayfa" aria-label="Sonraki sayfa" href="{href_from(rel, next_rel)}">F3</a>
</nav>"""
    if "prototype-nav" not in text:
        text = text.replace(
            "</style>",
            ".app>*{min-width:0}header{min-width:0;overflow:hidden}.title-wrap{overflow:hidden}"
            ".prototype-nav{display:flex;gap:5px;flex:none;margin-left:auto;margin-right:8px}"
            ".prototype-nav a{text-decoration:none;padding:8px 10px}"
            "@media(max-width:1650px){.sub{display:none}}"
            "@media(max-width:1150px){.prototype-nav{position:absolute;right:18px;bottom:10px;z-index:12}}\n</style>",
            1,
        )
        text = text.replace('<div class="header-actions">', nav + '<div class="header-actions">', 1)
    text = patch_nav(text, rel, prev_rel, next_rel)
    dst.write_text(text, encoding="utf-8")
    shutil.copy2(src_img, dst.parent / src_img.name)


def build_chain() -> list[str]:
    chain: list[str] = []
    for explanation, animations in PAIRS:
        chain.append(explanation)
        chain.extend(animations)
    return chain


def update_index(chain: list[str]) -> None:
    index_path = ANIM / "index.html"
    text = index_path.read_text(encoding="utf-8")
    text = re.sub(
        r"\s*<!-- nonphys-status-v2 -->.*?<!-- /nonphys-status-v2 -->\s*",
        "\n",
        text,
        flags=re.S,
    )
    banner = """<!-- nonphys-status-v2 -->
<aside style="position:fixed;right:18px;bottom:18px;z-index:999;max-width:510px;padding:12px 15px;background:#071820;color:#eef6f8;border:1px solid #3f6672;border-left:4px solid #48d7e8;box-shadow:0 10px 28px rgba(0,0,0,.28);font:600 13px/1.35 'Segoe UI',Arial,sans-serif">
Nonfizyolojik faktörler tamamlandı: <b style="color:#69dfa0">34 açıklama + 35 interaktif animasyon</b>. Her açıklama doğrudan kendi animasyonuyla devam eder.
</aside>
<!-- /nonphys-status-v2 -->"""
    text = text.replace("</body>", banner + "\n</body>", 1)
    index_path.write_text(text, encoding="utf-8")
    manifest = {
        "section": "Nonfizyolojik faktörler",
        "explanations": len(EXPLANATIONS),
        "animations": len(chain) - len(EXPLANATIONS),
        "total_pages": len(chain),
        "sequence": [
            {
                "number": i + 1,
                "type": "explanation" if rel in EXPLANATIONS else "animation",
                "file": rel,
            }
            for i, rel in enumerate(chain)
        ],
    }
    (ANIM / "nonfizyolojik_69_sayfa_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def validate_structure(chain: list[str]) -> dict:
    missing = [rel for rel in chain if not (ANIM / rel).exists()]
    consecutive_explanations = [
        [chain[i], chain[i + 1]]
        for i in range(len(chain) - 1)
        if chain[i] in EXPLANATIONS and chain[i + 1] in EXPLANATIONS
    ]
    local_missing: list[dict] = []
    for rel in chain + ["index.html"]:
        path = ANIM / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for href in re.findall(r'href=["\']([^"\']+)["\']', text, flags=re.I):
            if href.startswith(("#", "http:", "https:", "mailto:", "javascript:")):
                continue
            clean = href.split("#", 1)[0].split("?", 1)[0]
            if not clean:
                continue
            target = (path.parent / clean).resolve()
            if not target.exists():
                local_missing.append({"file": rel, "href": href})
    guided_missing = [rel for rel in EXISTING_ANIMS if "guided-tour-v2" not in (ANIM / rel).read_text(encoding="utf-8")]
    return {
        "pages": len(chain),
        "explanations": sum(rel in EXPLANATIONS for rel in chain),
        "animations": sum(rel not in EXPLANATIONS for rel in chain),
        "missing_pages": missing,
        "consecutive_explanations": consecutive_explanations,
        "broken_local_links": local_missing,
        "existing_animations_without_guided_tour": guided_missing,
    }


def main() -> None:
    if not ANIM.exists():
        raise FileNotFoundError(f"Animations directory not found: {ANIM}")
    chain = build_chain()
    if len(EXPLANATIONS) != 34 or len(chain) != 69:
        raise RuntimeError(
            f"Content contract changed: {len(EXPLANATIONS)} explanations, {len(chain)} total pages."
        )
    previous_before_section = "proksimal-distal/animasyon-1-segment-hizi.html"
    for i, rel in enumerate(chain):
        prev_rel = previous_before_section if i == 0 else chain[i - 1]
        next_rel = "index.html" if i == len(chain) - 1 else chain[i + 1]
        path = ANIM / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if rel in EXPLANATIONS:
            number = list(EXPLANATIONS).index(rel) + 1
            path.write_text(
                explanation_html(rel, EXPLANATIONS[rel], prev_rel, next_rel, number),
                encoding="utf-8",
            )
        elif rel == "stimulus-artefakti/animasyon-0-mekanizma.html":
            deploy_stimulus_prototype(rel, prev_rel, next_rel)
        elif rel in NEW_SIMS:
            path.write_text(new_sim_html(rel, NEW_SIMS[rel], prev_rel, next_rel), encoding="utf-8")
        elif rel in EXISTING_ANIMS:
            text = path.read_text(encoding="utf-8")
            text = inject_guided_tour(text, EXISTING_ANIMS[rel])
            text = patch_nav(text, rel, prev_rel, next_rel)
            path.write_text(text, encoding="utf-8")
        else:
            raise KeyError(f"No authoring rule for {rel}")
    predecessor = ANIM / previous_before_section
    if predecessor.exists():
        pred_text = predecessor.read_text(encoding="utf-8")
        pred_text = patch_nav(pred_text, previous_before_section, "proksimal-distal/index.html", chain[0])
        predecessor.write_text(pred_text, encoding="utf-8")
    update_index(chain)
    report = validate_structure(chain)
    report_path = ANIM / "nonfizyolojik_yapisal_qa.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if any(
        report[key]
        for key in (
            "missing_pages",
            "consecutive_explanations",
            "broken_local_links",
            "existing_animations_without_guided_tour",
        )
    ):
        raise RuntimeError(f"Structural validation failed; see {report_path}")


if __name__ == "__main__":
    main()
