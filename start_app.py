import subprocess
from pathlib import Path
import sys
import time

def main():
    root = Path(__file__).resolve().parent
    exe_path = root / "dist" / "codeanalyzer" / "codeanalyzer.exe"
    
    if not exe_path.exists():
        print(f"HATA: {exe_path} bulunamadı!")
        print("Lütfen önce 'build_exe.py' çalıştırıp uygulamayı paketlediğinizden emin olun.")
        input("Çıkmak için Enter'a basın...")
        return
        
    print("codeAnalyzer başlatılıyor...")
    print("Lütfen IDLE'ı veya bu pencereyi KAPATMAYIN (uygulama kapanır).")
    print("----------------------------------------------------------------")
    
    try:
        # shell=False ile doğrudan EXE'yi başlatıyoruz, CMD'ye takılmayacak
        # subprocess.PIPE kullanarak uygulamanın gizli linkini bu ekrana (IDLE'a) yazdıracağız.
        process = subprocess.Popen(
            [str(exe_path)],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Uygulamanın verdiği token linkini ekrana satır satır bas
        for line in process.stdout:
            print(line, end="")
            
        process.wait()
    except KeyboardInterrupt:
        print("\nUygulama durduruldu.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        input("Çıkmak için Enter'a basın...")

if __name__ == "__main__":
    main()
