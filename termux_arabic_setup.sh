#!/usr/bin/env bash
# Termux Arabic support setup
# Creates a small Arabic reshaper filter and shell helpers to display Arabic better in terminals
# Usage: bash termux_arabic_setup.sh

set -e
DIR="$HOME/.termux_arabic"
mkdir -p "$DIR"

cat > "$DIR/arabic_filter.py" <<'PY'
#!/usr/bin/env python3
import sys
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
except Exception:
    sys.stderr.write("Missing dependencies. Install with: pip install arabic-reshaper python-bidi\n")
    sys.exit(1)

# read all stdin and reshape Arabic text for display
for line in sys.stdin:
    line = line.rstrip('\n')
    try:
        reshaped = arabic_reshaper.reshape(line)
        bidi = get_display(reshaped)
        print(bidi)
    except Exception:
        print(line)
PY

chmod +x "$DIR/arabic_filter.py"

# Append helpers to ~/.bashrc if not already present
RC="$HOME/.bashrc"
MARK="# TERMUX_ARABIC_HELPERS"
if ! grep -q "$MARK" "$RC" 2>/dev/null; then
  cat >> "$RC" <<'BASH'
# TERMUX_ARABIC_HELPERS
# enable_arabic: set environment and alias to shape Arabic output
enable_arabic() {
  export LANG=ar_SA.UTF-8
  export LC_ALL=ar_SA.UTF-8
  alias arabiccat="python3 $HOME/.termux_arabic/arabic_filter.py"
  echo "Arabic helpers enabled. Use: cat file | arabiccat or somecmd | arabiccat"
}

# disable_arabic: remove aliases
disable_arabic() {
  unset LANG
  unset LC_ALL
  unalias arabiccat 2>/dev/null || true
  echo "Arabic helpers disabled."
}
BASH
  echo "Added Arabic helpers to $RC"
else
  echo "Helpers already in $RC"
fi

cat <<EOF
Setup complete.
Next steps (run in Termux):
1) Install Python if needed: pkg install python
2) Install dependencies: pip install --user arabic-reshaper python-bidi
3) Reload shell: source ~/.bashrc
4) Enable helpers: enable_arabic
5) Use: cat file.txt | arabiccat

Limitations:
- This reshapes Arabic for left-to-right terminals by applying Arabic reshaping and bidi algorithms before printing.
- It does not change terminal rendering engine; some glyph shaping may still appear imperfect.
EOF
