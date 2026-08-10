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
