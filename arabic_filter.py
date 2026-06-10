#!/usr/bin/env python3
"""
Simple Arabic reshaping filter for terminals.
Usage: somecommand | python3 arabic_filter.py
Requires: pip install arabic-reshaper python-bidi
"""
import sys
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
except Exception:
    sys.stderr.write("Missing dependencies. Install with: pip install arabic-reshaper python-bidi\n")
    sys.exit(1)

for line in sys.stdin:
    line = line.rstrip('\n')
    try:
        reshaped = arabic_reshaper.reshape(line)
        bidi = get_display(reshaped)
        print(bidi)
    except Exception:
        print(line)