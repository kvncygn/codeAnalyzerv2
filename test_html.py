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
# Bilgisayarındaki SVN projesinin klasör yolu:
WORKING_COPY_PATH = r"C:\Projelerim\SvnProjem"

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
    except subprocess.CalledProcessError as e:
        return f"SVN Hata verdi: {e.stderr}"
    except FileNotFoundError:
        return "HATA: 'svn' komutu bulunamadı. TortoiseSVN kurarken 'Command Line Tools' seçeneğini açtığından emin ol."

def main():
    # Log klasörü yoksa otomatik oluştur
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Bugünün tarihi ve saati ile log dosyası adı belirle
    zaman_damgasi = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dosya_yolu = os.path.join(LOG_DIR, f"svn_fark_log_{zaman_damgasi}.txt")

    # 1. Bilgisayardaki mevcut commit ile Sunucudaki son commit arasındaki LOGLARI al
    commit_loglari = svn_komutu_calistir(["svn", "log", "-r", "BASE:HEAD"], WORKING_COPY_PATH)

    # 2. İki sürüm arasındaki KOD FARKINI (Diff) al
    kod_farklari = svn_komutu_calistir(["svn", "diff", "-r", "BASE:HEAD"], WORKING_COPY_PATH)

    # Raporu oluştur
    rapor = []
    rapor.append(f"==================================================")
    rapor.append(f"SVN ANALİZ RAPORU - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    rapor.append(f"Proje Klasörü: {WORKING_COPY_PATH}")
    rapor.append(f"==================================================\n")
    
    rapor.append("--- [1] SUNUCUDAKİ YENİ COMMIT'LER VE MESAJLARI ---")
    rapor.append(commit_loglari if commit_loglari else "Yeni commit yok veya sunucuya erişilemedi.")
    rapor.append("\n" + "="*50 + "\n")
    
    rapor.append("--- [2] DETAYLI KOD FARKILILIKLARI (DIFF) ---")
    rapor.append(kod_farklari if kod_farklari else "Kodlarda herhangi bir değişiklik yok (Yerel kopya güncel).")

    # Dosyaya yaz
    with open(log_dosya_yolu, "w", encoding="utf-8") as f:
        f.write("\n".join(rapor))

    print(f"İşlem tamamlandı. Log dosyası: {log_dosya_yolu}")

if __name__ == "__main__":
    main()
