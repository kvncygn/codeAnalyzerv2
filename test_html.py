from pathlib import Path
from src.codeanalyzer.html_analyzer import analyze_html_reports

test_dir = Path("test_html_analyzer")
test_dir.mkdir(exist_ok=True)
(test_dir / "index.html").write_text("<th>NR TOTAL TEST CASES</th><td><b>10</b></td>")
(test_dir / "TC_WINDOWS_SCA_TCF_Test1_RC1_v1.html").write_text("<th>Number of Total Steps</th><td><b>5</b></td>")
(test_dir / "TC_MANUAL_TCF_Test1_RC1_v2.html").write_text("<th>Number of Total Steps</th><td><b>3</b></td>")
(test_dir / "TC_SCA_MANUAL_TCF_Test2_RC1.html").write_text("<th>Number of Total Steps</th><td><b>7</b></td>")
(test_dir / "TC_SCA_WINDOWS_TCF_Test2_RC1.html").write_text("<th>Number of Total Steps</th><td><b>2</b></td>")
(test_dir / "RandomFile.html").write_text("<th>Number of Total Steps</th><td><b>2</b></td>")

res = analyze_html_reports(test_dir)
print("Index Report:", res.index_report is not None)
print("Virtual Folders:")
for vf in res.virtual_folders:
    print(f"  - {vf.name}")
    for sub in vf.subfolders:
        print(f"      [{sub.name}] - {len(sub.reports)} reports")
        for r in sub.reports:
            print(f"          - {r.file_name}")



import os
import subprocess
from datetime import datetime

# ==================== BU ALANLARI KENDİNE GÖRE DÜZENLE ====================
# İçinde birden fazla SVN projesi olan EN ÜST klasör yolu:
PARENT_DIR = r"C:\Tüm_Projelerim"

# Log dosyalarının kaydedileceği klasör yolu:
LOG_DIR = r"C:\SVN_Loglari"
# =========================================================================

def svn_komutu_calistir(komut, klasor):
    """SVN komutunu çalıştırır ve çıktısını döndürür."""
    try:
        sonuc = subprocess.run(
            komut, 
            cwd=klasor, 
            capture_output=True, 
            text=True, 
            encoding="utf-8",
            errors="replace",
            check=True
        )
        return sonuc.stdout.strip()
    except Exception as e:
        return f"Hata oluştu: {str(e)}"

def svn_projelerini_bul(ana_klasor):
    """os.walk ile ana klasör altındaki tüm SVN projelerini (.svn) recursive bulur."""
    svn_klasorleri = []
    for kok_dizin, alt_dizinler, dosya_listesi in os.walk(ana_klasor):
        if ".svn" in alt_dizinler:
            svn_klasorleri.append(kok_dizin)
            # Bu klasör bir SVN kökü ise, altındaki .svn klasörlerini tekrar taramasın
            alt_dizinler.remove(".svn")
    return svn_klasorleri

def main():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    zaman_damgasi = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dosya_yolu = os.path.join(LOG_DIR, f"toplu_svn_log_{zaman_damgasi}.txt")

    bulunan_proje_listesi = svn_projelerini_bul(PARENT_DIR)

    if not bulunan_proje_listesi:
        print(f"UYARI: '{PARENT_DIR}' içinde hiç SVN projesi bulunamadı.")
        return

    rapor = []
    rapor.append("=" * 60)
    rapor.append(f"TOPLU SVN ANALİZ RAPORU - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    rapor.append(f"Taranan Ana Klasör: {PARENT_DIR}")
    rapor.append(f"Bulunan SVN Proje Sayısı: {len(bulunan_proje_listesi)}")
    rapor.append("=" * 60 + "\n")

    for idx, proje_yolu in enumerate(bulunan_proje_listesi, start=1):
        proje_adi = os.path.basename(proje_yolu)
        
        rapor.append(f"##################################################")
        rapor.append(f"PROJE [{idx}/{len(bulunan_proje_listesi)}]: {proje_adi}")
        rapor.append(f"Konum: {proje_yolu}")
        rapor.append(f"##################################################\n")

        commit_loglari = svn_komutu_calistir(["svn", "log", "-r", "BASE:HEAD"], proje_yolu)
        rapor.append("--- [COMMIT LOGLARI] ---")
        rapor.append(commit_loglari if commit_loglari else "Yeni commit yok veya sunucuya erişilemedi.")
        rapor.append("")

        kod_farklari = svn_komutu_calistir(["svn", "diff", "-r", "BASE:HEAD"], proje_yolu)
        rapor.append("--- [KOD FARKILILIKLARI (DIFF)] ---")
        rapor.append(kod_farklari if kod_farklari else "Değişiklik yok (Güncel).")
        rapor.append("\n" + "-"*50 + "\n")

    with open(log_dosya_yolu, "w", encoding="utf-8") as f:
        f.write("\n".join(rapor))

    print(f"İşlem bitti! {len(bulunan_proje_listesi)} proje analiz edildi.")

if __name__ == "__main__":
    main()
