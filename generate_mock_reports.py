import os
from pathlib import Path

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test Automation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .header {{ background: #333; color: #fff; padding: 10px; }}
        .random-table {{ margin: 20px 0; border-collapse: collapse; }}
        .random-table td {{ border: 1px solid #ccc; padding: 5px; }}
    </style>
</head>
<body>

    <div class="header">
        <h1>Automated Test Execution Results</h1>
        <p>Execution Date: 2026-07-30 15:45:00</p>
        <p>Environment: Staging (Windows Server 2022)</p>
    </div>

    <div>
        <h2>System Health Check</h2>
        <table class="random-table">
            <tr><td>CPU Usage</td><td>45%</td></tr>
            <tr><td>Memory</td><td>8 GB Free</td></tr>
            <tr><td>Network</td><td>Stable</td></tr>
        </table>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam at porttitor sem.</p>
    </div>

    <!-- The actual targeted table (embedded deeply with random spacing/newlines) -->
    <div id="test-summary" style="margin-top: 50px;">
        <h3>Execution Summary</h3>
        <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
            
            <tr>
                <th>
                    Number of Total Steps
                </th>
                <td>
                    <b>
                        {total}
                    </b>
                </td>
            </tr>

            <tr>
                <th>  Number of Passed Steps  </th>
                <td> <b> {passed} </b> </td>
            </tr>
            <tr>
                <th>
Number of Failed Steps
</th>
<td><b>{failed}</b></td>
            </tr>
            <tr>
                <th>Number of N/A Steps</th> <td>   <b> {na} </b>   </td>
            </tr>
        </table>
    </div>

    <div class="footer">
        <p>Report generated automatically by CI/CD pipeline.</p>
        <p>Contact DevOps team for any anomalies in the log structure.</p>
    </div>
</body>
</html>
"""

def create_mock_reports():
    base_dir = Path("examples/SunumDemosu/html_reports")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    reports = [
        # Group 1 (Virtual Folder: TCF_Login_Valid_RC1)
        ("TCF_Login_Valid_RC1_v1.html", 10, 10, 0, 0),
        ("TCF_Login_Valid_RC1_v2.html", 12, 11, 1, 0),
        
        # Group 2 (Virtual Folder: TCF_Payment_Fail_RC1)
        ("TCF_Payment_Fail_RC1_testA.html", 5, 2, 3, 0),
        ("TCF_Payment_Fail_RC1_testB.html", 5, 5, 0, 0),
        ("TCF_Payment_Fail_RC1_testC.html", 5, 4, 0, 1),
        
        # Single files (No virtual folder, just root)
        ("TCF_Register_Success_RC1_only.html", 20, 20, 0, 0),
        ("TCF_Dashboard_Load_v2.html", 8, 8, 0, 0), # No RC1 in name, so won't be grouped
        ("Random_Report.html", 2, 1, 1, 0) # Not starting with TCF, won't be grouped
    ]
    
    for filename, total, passed, failed, na in reports:
        filepath = base_dir / filename
        content = html_template.format(total=total, passed=passed, failed=failed, na=na)
        filepath.write_text(content, encoding="utf-8")
        
    print(f"Mock reports created in: {base_dir.absolute()}")

if __name__ == "__main__":
    create_mock_reports()
