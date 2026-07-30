import re
from pathlib import Path
from typing import Any

def calculate_complexities(body_lines, start_line):
    cc = 1
    max_tc = 0
    current_tc = 0
    tc_line = start_line
    
    cc_pattern = re.compile(r'\b(if|for|while|case|catch)\b|&&|\|\||\?')
    loop_start_pattern = re.compile(r'\b(for|while|do)\b')
    
    brace_depth = 0
    loop_depths = []
    
    for i, line in enumerate(body_lines):
        line_num = start_line + i
        clean_line = line.split('//')[0].split('/*')[0]
        
        matches = cc_pattern.findall(clean_line)
        cc += len(matches)
        
        open_braces = clean_line.count('{')
        close_braces = clean_line.count('}')
        
        is_do_while_end = re.search(r'\}\s*while\b', clean_line)
        
        if loop_start_pattern.search(clean_line) and not is_do_while_end:
            loop_depths.append(brace_depth)
            current_tc = len(loop_depths)
            if current_tc > max_tc:
                max_tc = current_tc
                tc_line = line_num
                
        brace_depth += open_braces
        brace_depth -= close_braces
        
        while loop_depths and brace_depth <= loop_depths[-1]:
            loop_depths.pop()
            
    tc_str = "O(1)"
    if max_tc == 1:
        tc_str = "O(N)"
    elif max_tc == 2:
        tc_str = "O(N^2)"
    elif max_tc == 3:
        tc_str = "O(N^3)"
    elif max_tc > 3:
        tc_str = f"O(N^{max_tc})"
        
    return cc, tc_str, tc_line

def analyze_c_file(filepath: Path) -> dict[str, Any]:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception:
        return {"path": str(filepath.absolute()), "methods": []}
        
    methods = []
    # Match return type, spaces, function name, parens. 
    # Example: int main() { or void test_func(int a)
    func_sig_regex = re.compile(r'^\s*(?:[a-zA-Z_]\w*\s*\*?\s+)+([a-zA-Z_]\w*)\s*\([^)]*\)\s*\{?')
    
    in_function = False
    brace_count = 0
    current_func_name = ""
    current_start_line = 0
    body_lines = []
    
    for i, line in enumerate(lines):
        line_num = i + 1
        clean_line = line.split('//')[0]
        
        if not in_function:
            match = func_sig_regex.match(clean_line)
            # Avoid matching function declarations ending with ';'
            if match and not clean_line.strip().endswith(';'):
                current_func_name = match.group(1)
                current_start_line = line_num
                in_function = True
                brace_count = clean_line.count('{') - clean_line.count('}')
                body_lines = [clean_line]
                
                # If { is on the next line
                if brace_count == 0 and not '{' in clean_line:
                    # We will wait for the { on the next lines
                    pass
        else:
            body_lines.append(clean_line)
            brace_count += clean_line.count('{')
            brace_count -= clean_line.count('}')
            
            if brace_count <= 0 and '{' in ''.join(body_lines):
                cc, tc, tc_line = calculate_complexities(body_lines, current_start_line)
                methods.append({
                    "name": current_func_name,
                    "startLine": current_start_line - 1, # 0-indexed
                    "endLine": line_num - 1,             # 0-indexed
                    "cyclomaticComplexity": cc,
                    "timeComplexity": tc,
                    "timeComplexityLine": tc_line
                })
                in_function = False
                
    return {
        "path": str(filepath.absolute()),
        "methods": methods
    }

def analyze_c_files(files) -> dict[str, Any]:
    response_files = []
    for f in files:
        response_files.append(analyze_c_file(f.path))
    return {"files": response_files}
