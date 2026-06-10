#!/usr/bin/env python3
"""
Madara terminal - a Kali-like simple terminal emulator in Python.
Usage: python3 madara.py

Features:
- Interactive prompt with basic builtins: ls, cd, pwd, cat, echo, clear, help, history, whoami, uname
- Unknown commands are executed via the system shell (safe-guarded)
- Writes history to ~/.madara_history
- Minimal dependencies (stdlib only)

This is a simulation — it is not a full shell. Dangerous commands are blocked by default.
"""

import cmd
import os
import shlex
import subprocess
import sys
import readline
from pathlib import Path

HISTFILE = Path.home() / '.madara_history'
BLOCKED_PATTERNS = [
    'rm -rf', 'rm -r', 'mkfs', 'dd', 'shutdown', 'reboot', 'poweroff', 'passwd', 'passwd -',
    'chown', 'chmod 0', 'chmod -R 777', '>: /dev/sda', 'fdisk', 'parted'
]

CSI = '\x1b['
GREEN = CSI + '32m'
BLUE = CSI + '34m'
YELLOW = CSI + '33m'
RESET = CSI + '0m'

BANNER = r'''
  __  __           _                _
 |  \/  | __ _ ___| | ___  _   _ __| | ___ _ __
 | |\/| |/ _` / __| |/ _ \| | | / _` |/ _ \ '__|
 | |  | | (_| \__ \ | (_) | |_| | (_| |  __/ |
 |_|  |_|\__,_|___/_|\___/ \__,_|\__,_|\___|_|

 Madara terminal (simulated Kali-like)
 Type 'help' for commands. Use 'exit' or Ctrl-D to quit.
'''


class MadaraShell(cmd.Cmd):
    # support both English and Arabic prompts/commands
    ARABIC_BANNER = r'''
    مرحبًا بكم في محطة مدارا (محاكاة)
    اكتب 'مساعدة' أو 'help' للحصول على الأوامر. استخدم 'خروج' أو Ctrl-D للخروج.
    '''

    intro = BANNER + "\n" + ARABIC_BANNER
    # Arabic prompt by default
    prompt = f"{GREEN}مدارا{RESET}@{BLUE}كالي{RESET}:~$ "

    # map Arabic command words to English builtin names
    AR_COMMANDS = {
        'قائمة': 'ls', 'عرض': 'ls', 'ls': 'ls', 'dir': 'ls',
        'اذهب': 'cd', 'انتقل': 'cd', 'cd': 'cd',
        'المسار': 'pwd', 'pwd': 'pwd',
        'اقرأ': 'cat', 'قراءة': 'cat', 'cat': 'cat',
        'مسح': 'clear', 'واضح': 'clear', 'clear': 'clear',
        'مساعدة': 'help', 'معلومات': 'help', 'help': 'help',
        'خروج': 'exit', 'انهاء': 'exit', 'exit': 'exit',
        'تاريخ': 'history', 'history': 'history',
        'من_انا': 'whoami', 'whoami': 'whoami', 'uname': 'uname', 'من': 'whoami'
    }

    def __init__(self):
        super().__init__()
        self.cwd = os.getcwd()
        self._load_history()

    # ------- history persistence
    def _load_history(self):
        try:
            readline.read_history_file(str(HISTFILE))
        except FileNotFoundError:
            HISTFILE.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    def _save_history(self):
        try:
            readline.write_history_file(str(HISTFILE))
        except Exception:
            pass

    def preloop(self):
        pass

    def postloop(self):
        self._save_history()

    # Translate Arabic command tokens to English builtins before execution
    def precmd(self, line):
        if not line:
            return line
        parts = shlex.split(line)
        if not parts:
            return line
        key = parts[0].strip()
        # normalize Arabic punctuation/variants
        key_norm = key.replace('ـ', '').replace('\u200f', '')
        mapped = self.AR_COMMANDS.get(key_norm)
        if mapped and mapped != key:
            parts[0] = mapped
            new_line = ' '.join(shlex.quote(p) for p in parts)
            return new_line
        return line

    # ------- builtins
    def do_exit(self, arg):
        """Exit the terminal"""
        print('مع السلامة — bye')
        return True

    def do_EOF(self, arg):
        print()
        return True

    def do_clear(self, arg):
        """Clear the screen"""
        os.system('clear')

    def do_pwd(self, arg):
        """Print working directory"""
        print(os.getcwd())

    def do_cd(self, arg):
        """Change directory: cd <path>"""
        target = arg.strip() or os.path.expanduser('~')
        try:
            os.chdir(os.path.expanduser(target))
        except Exception as e:
            # show message in Arabic
            print(f"cd: {e}")

    def do_ls(self, arg):
        """List files in the directory: ls [path]"""
        target = arg.strip() or '.'
        try:
            for name in sorted(os.listdir(target)):
                path = os.path.join(target, name)
                if os.path.isdir(path):
                    print(f"{BLUE}{name}{RESET}/")
                else:
                    print(name)
        except Exception as e:
            print(f"ls: {e}")

    def do_cat(self, arg):
        """Print file contents: cat <file>"""
        if not arg:
            print('Usage: cat <file>')
            return
        try:
            with open(os.path.expanduser(arg), 'r', errors='replace') as f:
                print(f.read(), end='')
        except Exception as e:
            print(f"cat: {e}")

    def do_echo(self, arg):
        """Echo text"""
        print(arg)

    def do_whoami(self, arg):
        try:
            print(os.getlogin())
        except Exception:
            print(os.environ.get('USER') or os.environ.get('LOGNAME') or 'madara')

    def do_uname(self, arg):
        try:
            out = subprocess.check_output(['uname', '-a'], stderr=subprocess.DEVNULL, text=True)
            print(out.strip())
        except Exception:
            print('Linux madara 1.0')

    def do_history(self, arg):
        h = [readline.get_history_item(i + 1) for i in range(readline.get_current_history_length())]
        for i, line in enumerate(h, start=1):
            print(f"{i}  {line}")

    def do_help(self, arg):
        """List available commands (English and Arabic)"""
        cmds = [
            ('ls', 'قائمة/عرض'), ('cd', 'اذهب/انتقل'), ('pwd', 'المسار'), ('cat', 'اقرأ/قراءة'),
            ('echo', 'echo'), ('clear', 'مسح'), ('history', 'تاريخ'), ('whoami', 'من_انا'),
            ('uname', 'uname'), ('help', 'مساعدة'), ('exit', 'خروج')
        ]
        print('Available builtins / الأوامر المتاحة:')
        for en, ar in cmds:
            print(f"  {en:6}  —  {ar}")
        print("Unknown commands are executed via system shell.\nالأوامر غير المعروفة تُنفّذ عبر شل النظام. الأوامر الخطرة محجوبة افتراضيًا.")

    # ------- execution of external commands
    def default(self, line):
        line = line.strip()
        if not line:
            return
        # safety check
        lowered = line.lower()
        for p in BLOCKED_PATTERNS:
            if p in lowered:
                print(f"Blocked potentially dangerous command containing: '{p}'")
                return
        # allow user to prefix with '!' to force execution if blocked
        if line.startswith('!'):
            line = line[1:]
            print(f"Running (forced): {line}")
        try:
            # use sh -c to interpret pipes etc.
            proc = subprocess.run(line, shell=True)
            if proc.returncode != 0:
                # non-zero; show rc
                pass
        except KeyboardInterrupt:
            print('^C')
        except Exception as e:
            print(f"Error executing command: {e}")

    # ------- completion helpers
    def complete_cd(self, text, line, begidx, endidx):
        return self._complete_path(text)

    def complete_cat(self, text, line, begidx, endidx):
        return self._complete_path(text)

    def complete_ls(self, text, line, begidx, endidx):
        return self._complete_path(text)

    def _complete_path(self, text):
        if not text:
            text = '.'
        dirname = os.path.dirname(text)
        dirname = dirname if dirname else '.'
        prefix = os.path.basename(text)
        try:
            candidates = os.listdir(os.path.expanduser(dirname))
        except Exception:
            return []
        results = [os.path.join(dirname, c) for c in candidates if c.startswith(prefix)]
        return results


def main():
    shell = MadaraShell()
    try:
        shell.cmdloop()
    except KeyboardInterrupt:
        print('\nInterrupted')
    finally:
        shell._save_history()


if __name__ == '__main__':
    main()
