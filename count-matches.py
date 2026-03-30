#!./tensorflow/bin/python

import sys
import re

# Regex to capture:
# 1) text inside quotes
# 2) text after the word "identified"
pattern = re.compile(r'"([^"]+)"\s+identified\s+(.+)$')

matches = 0
non_matches = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    m = pattern.match(line)
    if not m:
        # Skip malformed lines (or you could count them as non-matches)
        continue

    quoted_text = m.group(1).strip()
    identified_text = m.group(2).strip()

    if quoted_text == identified_text:
        matches += 1
    else:
        non_matches += 1

total = matches + non_matches

if total == 0:
    print("No valid lines processed.")
else:
    ratio = matches / total
    print(f"Matches: {matches}")
    print(f"Non-matches: {non_matches}")
    print(f"Match ratio: {ratio:.6f}")
