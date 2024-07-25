import re
import sys

def parse_diff(diff):
    lines = diff.split('\n')
    start_line = None
    current_line = None
    start_side = 'RIGHT'
    side = 'RIGHT'
    changes = []
    
    # Regular expression to match the chunk header
    chunk_header_re = re.compile(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@')

    for i, diff_line in enumerate(lines):
        chunk_header_match = chunk_header_re.match(diff_line)
        if chunk_header_match:
            if start_line is None:
                start_line = int(chunk_header_match.group(1))
            current_line = int(chunk_header_match.group(1))
            continue
        
        if diff_line.startswith('+') and not diff_line.startswith('+++'):
            if start_line is not None:
                changes.append(current_line)
        if diff_line.startswith('-') and not diff_line.startswith('---'):
            if start_line is not None:
                changes.append(current_line)
        current_line += 1

    if changes:
        start_line = changes[0]
        line = changes[-1]
    else:
        start_line = line = 1

    return start_line, line, start_side, side

if __name__ == "__main__":
    diff = sys.stdin.read()
    start_line, line, start_side, side = parse_diff(diff)
    print(f"{start_line} {line} {start_side} {side}")
