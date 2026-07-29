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
        "--self-contained", "false",
        "-p:PublishSingleFile=true",
        "-p:IncludeNativeLibrariesForSelfExtract=true",
        "-p:DebugType=None",
        "-p:DebugSymbols=false",
        "-o", str(out_path)
    ]
    
    # shell=False (varsayılan) bırakıyoruz ki sistem kesinlikle CMD'yi (cmd.exe) açmaya çalışmasın.
    # Doğrudan dotnet.exe'ye bağlanır.
    subprocess.run(dotnet_cmd, check=True)
    
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
    
    if not venv_python.exists():
        print(f"HATA: Sanal ortam bulunamadı! {venv_python}")
        print("Lütfen önce sanal ortamı (venv) kurun.")
        return

    spec_path = root / "packaging" / "codeanalyzer.spec"
    dist_path = root / "dist"
    build_path = root / "build"
    
    pyinstaller_cmd = [
        str(venv_python), "-m", "PyInstaller",
        "--clean", "--noconfirm",
        "--distpath", str(dist_path),
        "--workpath", str(build_path),
        str(spec_path)
    ]
    
    # Yine shell=True OLMADAN doğrudan python.exe'yi çalıştırıyoruz. CMD kullanılmaz.
    subprocess.run(pyinstaller_cmd, check=True)
    
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
