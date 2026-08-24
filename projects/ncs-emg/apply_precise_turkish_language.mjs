import fs from "node:fs";
import path from "node:path";

const roots = [
  path.resolve("animations"),
  path.resolve("C:/Users/uugur/OneDrive/Desktop/EMG_NCS_Nonfizyolojik_Faktorler_Sunumu_FIXED_2026-07-31"),
];

// Ordered from context-specific phrases to safe, general verb replacements.
const replacements = [
  ["Konu (tıklanabilir)", "Konu (tıklayın)"],
  ["yüzey mesafesi güvenilir olmayabilir", "yüzey mesafesi güvenilir değildir"],
  ["<b>kabul edilebilir düzeye</b> indirilebilir", "<b>kabul sınırına</b> indirilir"],
  ["<b>kontrol edilebilir</b>", "<b>kontrol altına alınır</b>"],
  ["<b>geçersiz</b> olabilir", "<b>geçersizdir</b>"],
  ["<b>tendon potansiyelinden</b> gelebilir .", "<b>tendon potansiyelinden</b> gelir."],
  ["Soruları hem bu ekranda hem telefonunuzda görebilirsiniz ama sadece telefon ekranından cevaplayabilirsiniz.", "Sorular bu ekranda ve telefonda görünür; yanıt yalnız telefondan verilir."],
  ["<b>bifid</b> olabilir", "<b>bifid</b> biçime dönüşür"],
  ["sinirin gerçek uzunluğu daha doğru yaklaşık olarak ölçülür", "sinir yolu yüzey mezurasına göre daha doğru ölçülür"],
  ["BKAP’lar karşılaştırmaya uygundur", "BKAP’lar doğrudan karşılaştırılır"],
  ["Hedef APB yanıtları karşılaştırmaya uygundur", "Hedef APB yanıtları doğrudan karşılaştırılır"],
  ["Teknik olarak karşılaştırmaya uygundur:", "Teknik karşılaştırma geçerlidir:"],
  ["Ulnar ve tibial çalışmalarda tendon G2 elektriksel aktivite kaydeder.", "Ulnar ve tibial kayıtlarda tendon G2 çoğu kez elektriksel aktivite kaydeder."],
  ["; <b>ulnar ve tibial</b> sinirde G2 elektriksel aktivite kaydeder.", "; özellikle <b>ulnar ve tibial</b> sinirde G2 sıklıkla elektriksel aktivite kaydeder."],
  ["Yalnızca <b>normal bir yanıtın varlığı</b> bu durumda güvenle yorumlanır.", "Bu durumda yalnız <b>normal bir yanıt</b> güvenilir bulgu sayılır."],
  ["görülebilen başlangıcı", "görünen başlangıcı"],
  ["Hedefi örtebilen elektriksel gürültü", "Hedefi örten elektriksel gürültü"],
  ["GERÇEK KONUM ANATOMİK İŞARETTEN SAPABİLİR", "GERÇEK KONUM ANATOMİK İŞARETTEN SAPAR"],
  ["YANIT ÖLÇÜLEBİLİR", "YANIT ÖLÇÜLÜR"],
  ["GERÇEK BLOK GİZLENEBİLİR", "GERÇEK BLOK GİZLENİR"],
  ["TEKNİK OLARAK YORUMLANABİLİR KAYIT", "TEKNİK OLARAK GEÇERLİ KAYIT"],
  ["farklı ayarlar hatalı İH hesaplanmasına yol açabilir", "farklı ayarlar hatalı İH hesabına yol açar"],
  ["median kubbe, ulnar katılınca bifid olabilir", "median kubbe, ulnar katılınca bifid biçime dönüşür"],
  ["iki yorumu karşılaştırabilirsiniz", "iki yorumu yan yana karşılaştırın"],
  ["yanlışlıkla <b>demiyelinizan nöropati</b> olarak yorumlanabilir", "yanlışlıkla <b>demiyelinizan nöropati</b> olarak yorumlanır"],
  ["Öngörülebilir Latans Hatası", "Beklenen Latans Hatası"],
  ["maksimize edilmemiş olabilir", "maksimize edilmemiştir"],
  ["her iki varsayım da bozulabilir", "her iki varsayım da bozulur"],
  ["elde etmek güç olabilir", "elde etmek güçleşir"],
  ["~%${snap.toFixed(0)}'e düşmüş olabilir", "bu modelde ~%${snap.toFixed(0)}'e düşer"],
  ["Bunlar soğuk ekstremiteden de olabilir.", "Soğuk ekstremite de aynı bulguları üretir."],
  ["G2'nin etkisi karşıt fazlıysa negatif tepe daha küçük gelebilir .", "G2'nin etkisi karşıt fazlıysa negatif tepe küçülür."],
  ["G2’nin etkisi karşıt fazlıysa negatif tepe daha küçük gelebilir .", "G2’nin etkisi karşıt fazlıysa negatif tepe küçülür."],
  ["Soğukta ölçülen hız “normal” görünse bile düzeltme sonrası sınır içine girebilir", "Soğukta ölçülen hız “normal” görünse bile düzeltme sonrası sınır içine girer"],
  ["G1 anatomik motor noktaya yakın değilse başlangıç latansı uzamış görünebilir", "G1 anatomik motor noktaya yakın değilse başlangıç latansı yapay olarak uzar"],
  ["20–40 dakika</span> sürebilir", "20–40 dakika</span> sürer"],
  ["hastalıklı sinire birebir uymayabilir", "hastalıklı sinire doğrudan uygulanmaz"],
  ["G2 elektriksel olarak aktif olabilir", "G2 elektriksel aktivite kaydeder"],
  ["tendon G2 elektriksel olarak aktif olabilir", "tendon G2 sıklıkla elektriksel aktivite kaydeder"],
  ["aynı anda <b>ikisi de</b> elektriksel olarak aktif olabilir", "aynı anda <b>ikisi de</b> elektriksel aktivite kaydeder"],
  ["kabul edilebilir düzeye indirilebilir", "kabul sınırına indirilir"],
  ["teknikle kontrol edilebilir", "teknikle kontrol altına alınır"],
  ["BKAP’lar karşılaştırılabilir", "BKAP’lar karşılaştırmaya uygundur"],
  ["doğrusal ve öngörülebilir şekilde", "doğrusal bir ilişkiyle"],
  ["Genelde Ayırt Edilebilir", "Genelde Ayrım Nettir"],
  ["Birden fazla doğru seçenek olabilir.", "Bazı sorularda birden fazla doğru seçenek vardır."],
  ["Soruları bu ekranda da görebilirsiniz ama sadece telefon ekranından cevaplayabilirsiniz.", "Sorular bu ekranda ve telefonda görünür; yanıt yalnız telefondan verilir."],
  ["yanlışlıkla demiyelinizasyon düşünebilir", "yanlışlıkla demiyelinizasyon diye yorumlar"],
  ["birden çok teknik veya anatomik nedeni olabileceğini", "birden çok teknik veya anatomik nedeni olduğunu"],
  ["Konum uygun olabilir, fakat", "Konum geometrisi uygun; ancak"],
  ["yanıt hâlâ büyüyebilir", "yanıt henüz platoda değildir"],
  ["ödem kaynaklı teknik faktör olabileceği belirtilmeli", "ödeme bağlı teknik faktör olduğu belirtilmeli"],
  ["Onset seçilebilirliği", "Onset görünürlüğü"],
  ["ilk konum optimal olmayabilir", "ilk konum çoğu zaman optimal değildir"],
  ["palpe edilebilir, doğrudan üzerine yerleştirilebilir", "palpasyonla bulunur; elektrot doğrudan üzerine yerleştirilir"],
  ["doğru ölçülebilir hâle gelir", "doğru ölçüm için görünür hâle gelir"],
  ["güvenle yorumlanabilir", "güvenle yorumlanır"],
  ["G2 katkısı olabilir", "G2 katkısı vardır"],
  ["DSAP seçilebilir", "DSAP görünür"],
  ["ko-stimüle olabilir", "ko-stimüle olur"],
  ["geçersiz olabilir", "geçersizdir"],
  ["kaynaklı olabilir", "kaynaklıdır"],
  ["olabileceği belirtilmeli", "olduğu belirtilmeli"],
  ["olabileceğini vurgular", "olduğunu vurgular"],
  ["olabileceğini", "olduğunu"],
  ["olabileceği", "olduğu"],
  ["olabileceği", "olduğu"],
  ["sanılabilir", "sanılır"],
  ["yayılabilir", "yayılır"],
  ["bindirebilir", "bindirir"],
  ["girebilir", "girer"],
  ["götürebilir", "götürür"],
  ["ortaya çıkabilir", "ortaya çıkar"],
  ["yaratabilir", "yaratır"],
  ["gizleyebilir", "gizler"],
  ["gizlenebilir", "gizlenir"],
  ["taklit edebilir", "taklit eder"],
  ["gizlemiş olabilir", "gizlemiştir"],
  ["hatalı ölçülebilir", "hatalı ölçülür"],
  ["engelleyebilir", "engeller"],
  ["azalabilir", "azalır"],
  ["kaybolabilir", "kaybolur"],
  ["artabilir", "artar"],
  ["sürebilir", "sürer"],
  ["uymayabilir", "doğrudan uygulanmaz"],
  ["düşürülebilir", "düşürülür"],
  ["artırılabilir", "artırılır"],
  ["farklılaşabilir", "farklılaşır"],
  ["kayabilir", "kayar"],
  ["bifidleşebilir", "bifidleşir"],
  ["oluşabilir", "oluşur"],
  ["düşünülebilir", "düşünülür"],
  ["görünebilir", "görünür"],
  ["görülebilir", "görülür"],
  ["bloke edebilir", "bloke eder"],
  ["kuplaj bırakabilir", "kuplaj bırakır"],
  ["kalabilir", "kalır"],
  ["gerekebilir", "gerekir"],
  ["azaltabilir", "azaltır"],
  ["kısalabilir", "kısalır"],
  ["uzayabilir", "uzar"],
  ["bozabilir", "bozar"],
  ["yerleşebilir", "yerleşir"],
  ["korunabilir", "korunur"],
  ["doğrulayabilir", "doğrular"],
  ["yorumlanabilir", "yorumlanır"],
  ["hatalı seçilebilir", "hatalı seçilir"],
  ["değiştirebilir", "değiştirir"],
  ["gösterebilir", "gösterir"],
  ["kısaltabilir", "kısaltır"],
  ["uzatabilir", "uzatır"],
  ["yansıtmayabilir", "yansıtmaz"],
  ["iptal edebilir", "iptal eder"],
  ["işaretlenebilir", "işaretlenir"],
  ["kafa karıştırabilir", "kafa karıştırır"],
  ["açıklanabilir", "açıklanır"],
  ["karşılaştırılabilir", "karşılaştırmaya uygundur"],
  ["ölçülebilir", "ölçülür"],
  ["değişebilir", "değişir"],
  ["tıklanabilir", "tıklayın"],
];

function collectHtmlFiles(root) {
  if (!fs.existsSync(root)) return [];
  const files = [];
  const stack = [root];
  while (stack.length) {
    const current = stack.pop();
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) stack.push(full);
      else if (entry.isFile() && entry.name.toLowerCase().endsWith(".html")) files.push(full);
    }
  }
  return files;
}

const counts = new Map(replacements.map(([from]) => [from, 0]));
const changedFiles = [];

for (const root of roots) {
  for (const file of collectHtmlFiles(root)) {
    const original = fs.readFileSync(file, "utf8");
    let updated = original;
    let fileCount = 0;
    for (const [from, to] of replacements) {
      if (!updated.includes(from)) continue;
      const hits = updated.split(from).length - 1;
      updated = updated.split(from).join(to);
      counts.set(from, counts.get(from) + hits);
      fileCount += hits;
    }
    if (updated !== original) {
      fs.writeFileSync(file, updated, "utf8");
      changedFiles.push({ file, replacements: fileCount });
    }
  }
}

const unmatched = [...counts.entries()].filter(([, count]) => count === 0).map(([text]) => text);
const totalReplacements = [...counts.values()].reduce((sum, count) => sum + count, 0);

console.log(JSON.stringify({
  roots,
  changedFileCount: changedFiles.length,
  totalReplacements,
  changedFiles,
  unmatched,
}, null, 2));
