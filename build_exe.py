import subprocess
import os
import shutil
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent
    
    print("== 1. C# Analyzer Derleniyor (win-x64) ==")
    csproj_path = root / "csharp-analyzer" / "src" / "TcfAnalyzer" / "TcfAnalyzer.csproj"
    out_path = root / "artifacts" / "analyzer" / "win-x64"
    
    # dotnet publish komutu
    dotnet_cmd = [
        "dotnet", "publish", str(csproj_path),
        "-c", "Release",
        "-r", "win-x64",
        "--self-contained", "true",
        "-p:PublishSingleFile=true",
        "-p:IncludeNativeLibrariesForSelfExtract=true",
        "-p:DebugType=None",
        "-p:DebugSymbols=false",
        "-o", str(out_path)
    ]
    
    # shell=False (varsayılan) bırakıyoruz ki sistem kesinlikle CMD'yi (cmd.exe) açmaya çalışmasın.
    # Windows'ta siyah CMD penceresinin anlık bile olsa parlamasını engellemek için:
    if os.name == 'nt':
        creationflags = subprocess.CREATE_NO_WINDOW
    else:
        creationflags = 0
        
    subprocess.run(dotnet_cmd, check=True, creationflags=creationflags)
    
    print("\n== 2. analyzer.exe _bundled klasörüne taşınıyor ==")
    dest_dir = root / "src" / "codeanalyzer" / "_bundled"
    
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    src_exe = out_path / "analyzer.exe"
    dest_exe = dest_dir / "analyzer.exe"
    shutil.copy2(src_exe, dest_exe)
    print(f"Kopyalandı: {dest_exe}")
    
    print("\n== 3. PyInstaller ile Python uygulaması EXE'ye dönüştürülüyor ==")
    venv_python = root / ".venv" / "Scripts" / "python.exe"
    
    if venv_python.exists():
        python_exe = str(venv_python)
        print("✅ Sanal ortam (.venv) bulundu, kullanılıyor...")
    else:
        import sys
        python_exe = sys.executable
        # IDLE genelde pythonw.exe kullanır, biz arka plan işlemleri için python.exe'ye çevirelim
        if python_exe.lower().endswith("pythonw.exe"):
            python_exe = python_exe[:-11] + "python.exe"
            
        print(f"⚠️ Sanal ortam (.venv) bulunamadı. Sistem Python'u kullanılıyor: {python_exe}")
        
        # PyInstaller'ın yüklü olup olmadığını kontrol et
        try:
            subprocess.run([python_exe, "-m", "PyInstaller", "--version"], check=True, capture_output=True, creationflags=creationflags)
        except Exception:
            print("\n⏳ PyInstaller bulunamadı, otomatik olarak kuruluyor... Lütfen bekleyin.")
            try:
                subprocess.run([python_exe, "-m", "pip", "install", "pyinstaller"], check=True, creationflags=creationflags)
                print("✅ PyInstaller başarıyla kuruldu! İşleme devam ediliyor...\n")
            except Exception as e:
                print(f"\nHATA: PyInstaller otomatik kurulamadı: {e}")
                print(f"Lütfen komut satırını açıp şu komutu çalıştırın:\n{python_exe} -m pip install pyinstaller\n")
                return

        # Proje gereksinimlerini (Flask vb.) kontrol et ve kur
        req_path = root / "requirements.txt"
        if req_path.exists():
            print("\n⏳ Proje gereksinimleri (Flask vb.) kontrol ediliyor/kuruluyor... Lütfen bekleyin.")
            try:
                subprocess.run([python_exe, "-m", "pip", "install", "-r", str(req_path)], check=True, creationflags=creationflags)
                print("✅ Gereksinimler başarıyla kuruldu! İşleme devam ediliyor...\n")
            except Exception as e:
                print(f"\nHATA: Gereksinimler otomatik kurulamadı: {e}")
                return

    spec_path = root / "packaging" / "codeanalyzer.spec"
    dist_path = Path.home() / "Desktop"
    build_path = root / "build"
    
    pyinstaller_cmd = [
        python_exe, "-m", "PyInstaller",
        "--clean", "--noconfirm",
        "--distpath", str(dist_path),
        "--workpath", str(build_path),
        str(spec_path)
    ]
    
    # Yine shell=True OLMADAN doğrudan python.exe'yi çalıştırıyoruz. CMD kullanılmaz.
    subprocess.run(pyinstaller_cmd, check=True, creationflags=creationflags)
    
    print("\n=======================================================")
    print("BAŞARILI! Uygulama paketlendi.")
    print(f"Sonuç klasörü: {dist_path / 'codeanalyzer'}")
    print("Bu klasörü alıp (ziplayıp) istediğiniz ofis bilgisayarında çalıştırabilirsiniz!")
    print("Çıkmak için Enter'a basın...")
    input()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        input("Çıkmak için Enter'a basın...")
