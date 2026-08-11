import os
import sys
import shutil
import subprocess
from pathlib import Path

def build_project_for_office():
    print("🚀 Ofis bilgisayarı için güvenli Build işlemi başlatılıyor...")
    print("🛡️ Güvenlik Kalkanı: CMD veya PowerShell KULLANILMAYACAKTIR (shell=False).")

    # Proje ve Masaüstü yollarının tespiti
    project_dir = Path(__file__).parent.absolute()
    desktop_dir = Path(os.path.expanduser("~")) / "Desktop"
    release_dir = desktop_dir / "CodeAnalyzer_Office_Release"
    
    cs_project = project_dir / "csharp-analyzer" / "src" / "TcfAnalyzer" / "TcfAnalyzer.csproj"
    bundled_dir = project_dir / "src" / "codeanalyzer" / "_bundled"
    
    # ---------------------------------------------------------
    # AŞAMA 1: C# Projesini Derleme (.NET CLI doğrudan çağrılır)
    # ---------------------------------------------------------
    print("\n[1/3] C# Analizörü derleniyor...")
    
    # CMD kullanmamak için dotnet.exe'nin tam yolunu buluyoruz
    dotnet_exe = shutil.which("dotnet")
    if not dotnet_exe:
        print("HATA: Bilgisayarda 'dotnet' bulunamadı!")
        return

    # shell=False hayat kurtarır, CMD.exe'yi by-pass eder
    subprocess.run([
        dotnet_exe, "publish", str(cs_project),
        "-c", "Release",
        "-r", "win-x64",
        "--self-contained", "true",
        "-p:PublishSingleFile=true"
    ], shell=False, check=True)

    # ---------------------------------------------------------
    # AŞAMA 2: C# EXE'sini Python _bundled klasörüne taşıma
    # ---------------------------------------------------------
    print("\n[2/3] C# EXE dosyası taşıma işlemi...")
    bundled_dir.mkdir(parents=True, exist_ok=True)
    
    # .NET 8 derleme çıktısının bulunduğu standart yol
    compiled_exe = project_dir / "csharp-analyzer" / "src" / "TcfAnalyzer" / "bin" / "Release" / "net8.0" / "win-x64" / "publish" / "TcfAnalyzer.exe"
    
    if compiled_exe.exists():
        shutil.copy2(compiled_exe, bundled_dir / "analyzer.exe")
        print("Kopyalama başarılı.")
    else:
        print("HATA: C# EXE dosyası belirtilen konumda bulunamadı!")
        return

    # ---------------------------------------------------------
    # AŞAMA 3: PyInstaller ile Python Uygulamasını Masaüstüne Paketleme
    # ---------------------------------------------------------
    print("\n[3/3] PyInstaller ile nihai proje oluşturuluyor...")
    
    # CMD kullanmamak için sys.executable (mevcut python.exe) kullanıyoruz
    pyinstaller_args = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",           # Tek klasör formatı (antivirüs dostu)
        "--windowed",         # Arkada siyah konsol ekranı açılmasını engeller
        "--name", "CodeAnalyzer",
        "--add-data", f"{project_dir / 'src' / 'codeanalyzer' / 'web' / 'templates'};codeanalyzer/web/templates",
        "--add-data", f"{project_dir / 'src' / 'codeanalyzer' / 'web' / 'static'};codeanalyzer/web/static",
        "--add-data", f"{bundled_dir};codeanalyzer/_bundled",
        "--distpath", str(release_dir),          # Çıktı klasörü doğrudan MASAÜSTÜ
        "--workpath", str(project_dir / "build"), # Geçici dosyalar
        str(project_dir / "start_app.py")
    ]

    subprocess.run(pyinstaller_args, shell=False, check=True)

    # ---------------------------------------------------------
    # SONUÇ
    # ---------------------------------------------------------
    print(f"\n✅ BAŞARILI! Tüm proje masaüstüne derlendi.")
    print(f"📁 Konum: {release_dir}")
    print("Ofis bilgisayarında hiçbir kurulum veya terminale ihtiyaç duymadan 'CodeAnalyzer.exe'ye tıklayarak çalıştırabilirsiniz.")

if __name__ == "__main__":
    try:
        build_project_for_office()
    except Exception as e:
        print(f"\n❌ Beklenmeyen bir hata oluştu: {e}")
    finally:
        input("\nÇıkmak için Enter'a basın...")
