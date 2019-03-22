import os
import sys

# This exists because msvcrt.getwch does not exist
# on operating systems other than windows.
# We need to keep compatability with macos as one of our
# team members has a macbook, and we dont know what our
# beloved instructor has.
# The readkey_unix function is from:
# https://docs.python.org/2/faq/library.html#how-do-i-get-a-single-keypress-at-a-time

# Translate key codes in unix to windows
KEYMAP = {
    10: 13,
    127: 8,
    10051: 10083,
    10065: 10072,
    10066: 10080,
    10067: 10077,
    10068: 10075
}


def readkey() -> int:
    if os.name == 'nt':
        from msvcrt import getwch
        key = ord(getwch())
        if key == 224:
            key = ord(getwch()) + 10000
        return key
    else:
        return readkey_unix()


def readkey_unix():
    import termios
    import fcntl
    fd = sys.stdin.fileno()
    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)
    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
    try:
        while 1:
            try:
                c = ord(sys.stdin.read(1))
                if c == 27:
                    sys.stdin.read(1)
                    c = ord(sys.stdin.read(1)) + 10000
                break
            except (IOError, TypeError):
                pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    return KEYMAP.get(c, c)

if __name__ == "__main__":  # demo
    key = readkey()
    print(key)
