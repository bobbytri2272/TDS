import requests, re,time,sys,pyfiglet,itertools
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

colors = [
    '\033[91m',  # Đỏ sáng
    '\033[92m',  # Xanh lá cây sáng
    '\033[93m',  # Vàng sáng
    '\033[94m',  # Xanh dương sáng
    '\033[95m',  # Tím sáng
    '\033[96m',  # Xanh lam sáng
    '\033[97m',  # Trắng sáng
    '\033[0m'    # Reset màu
]

def gettime():
    now = datetime.now()
    date_string = now.strftime("%d/%m/%Y")
    time_string = now.strftime("%H:%M:%S")
    return f"{Fore.YELLOW}[{date_string}|{time_string}]"
def logo():
    os.system("cls")
    now = datetime.now()
    date_string = now.strftime("%d/%m/%Y")
    time_string = now.strftime("%H:%M:%S")
    currenttime = f"{date_string}|{time_string}"
    ascii_art = pyfiglet.figlet_format("LE MINH TRI", font="big")

    print("--------------------------------------------------------------------")
    typewriter(ascii_art, 0.001)
    print("--------------------------------------------------------------------")
    coloreffect(f"[{currenttime}]:Tool được làm bởi Lê Minh Trí", 0.01,0.5)
    coloreffect(f"[{currenttime}]:Phiên Bản: 1.0.0",0.01,1)
    
def coloreffect(text, color_delay=0.5, duration=5):
    start_time = time.time()
    while time.time() - start_time < duration:
        for color in itertools.cycle(colors[:-1]):  
            sys.stdout.write('\r' + ' ' * (len(text) + 1))
            sys.stdout.write('\r')
            sys.stdout.write(f'{color}{text}\033[0m')
            sys.stdout.flush()
            time.sleep(color_delay)
            if time.time() - start_time >= duration:
                break
    print("")

def typewriter(text, delay=0.001):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def save_token(tds_token, filename='tds.txt'):
    with open(filename, 'w') as file:
        file.write(tds_token)

def load_token(filename='tds.txt'):
    if not os.path.exists(filename):
        open(filename, 'w').close()
    with open(filename, 'r') as file:
        return file.read().strip()
        
class TDS:
    def __init__(self, token, cookie) -> None:
        self.Token = token
        self.cookie = cookie

    def get_account_info(self):
        url = f"https://traodoisub.com/api/?fields=profile&access_token={self.Token}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data.get("success") == 200:
                user_info = data.get("data", {})
                user = user_info.get("user", "N/A")
                xu = user_info.get("xu", "N/A")
                xudie = user_info.get("xudie", "N/A")
                typewriter(f"Người dùng: {user} | Số xu: {xu}")
                return {
                    "user": user,
                    "xu": xu,
                    "xudie": xudie,
                    "token": self.Token
                }
            else:
                return {"error": "Token invalid or API error"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    def setnickfb(self,id):
        url = f"https://traodoisub.com/api/?fields=run&id={id}&access_token={self.Token}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data.get("success") == 200:
                notfi = data.get("data",{})
                ID = notfi.get("id","N/A")
                state = notfi.get("msg","N/A")
                return {
                    "id":ID,
                    "state":state
                }
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    def getcoin(self, type:str,id:str):
        url = f"https://traodoisub.com/api/coin/?type={type.upper()}&id={id}&access_token={self.Token}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return {str(e)}

    def get_quest(self, type:str,):
        url = f"https://traodoisub.com/api/?fields={type.lower()}&access_token={self.Token}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            quests = []
            if "countdown" in data:
                return "Countdown"
            else:
                for i in data:
                    quests.append(i)
                return quests
        except requests.exceptions.RequestException as e:
            return

class FB:
    def __init__(self, Cookie) -> None:
        cookie = Cookie.split(';')
        title = []
        value = []
        for i in range(len(cookie)):
            parts = cookie[i].split('=')
            if len(parts) == 2:
                title.append(parts[0].strip())
                value.append(parts[1].strip())
        self.Cookie = dict(zip(title, value))
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'vi',
            'cache-control': 'max-age=0',
            'dpr': '1',
            'priority': 'u=0, i',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-full-version-list': '"Not)A;Brand";v="99.0.0.0", "Google Chrome";v="127.0.6533.72", "Chromium";v="127.0.6533.72"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"2.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'viewport-width': '1365',
        }
        self.UID = self.Cookie.get('c_user', '')
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.cookies.update(self.Cookie)
    def getusername(self):
        try:
            response = requests.get(
                f"https://mbasic.facebook.com/{self.UID}/",
                headers=self.headers,
                cookies=self.Cookie
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                username = title_tag.text
                if "Facebook" in username:
                    typewriter("Cookie Sai")
                    return False
                else:
                    return username
        except:
            return False
    def reactpost(self, id, type="like"):
        try:
            type = type.upper()
            response = requests.get(f"https://www.facebook.com/{id}/", headers=self.headers, cookies=self.Cookie)
            if response.status_code == 200:
                parsed_url = urlparse(response.url)
                mbasic_url = f"https://mbasic.facebook.com{parsed_url.path}?{parsed_url.query}"
                time.sleep(12)
                mainurl = requests.get(mbasic_url, headers=self.headers, cookies=self.Cookie).text
            
                reactionpageurl = "https://mbasic.facebook.com/reactions/picker/?" + mainurl.split("/reactions/picker/?")[1].split('"')[0].replace("amp;", "")
                time.sleep(12)
                reactionpage = requests.get(reactionpageurl, headers=self.headers, cookies=self.Cookie).text
                reactionpicker = re.findall(r'/ufi/reaction//?.*?"', reactionpage)
                
                index = 0 if type == "LIKE" else 1 if type == "LOVE" else 2 if type == "CARE" else 3 if type == "HAHA" else 4 if type == "WOW" else 5 if type == "SAD" else 6 if type == "ANGRY" else 7
                url = "https://mbasic.facebook.com" + reactionpicker[index].replace("amp;", "").replace('"', "")
                status = requests.get(url, headers=self.headers, cookies=self.Cookie)
                status.raise_for_status()
                if status.status_code == 200:
                    return True
                else:
                    return False
        except:
            return False
    def reactcomment(self,id,type):
        try:
            idpost,cmtid = id.split("_")
            type = type.upper()
            index = 0 if type == "LIKE" else 1 if type == "LOVE" else 2 if type == "CARE" else 3 if type == "HAHA" else 4 if type == "WOW" else 5 if type == "SAD" else 6 if type == "ANGRY" else 7
            response = requests.get(f"https://www.facebook.com/{id}",headers=self.headers,cookies=self.Cookie)
            if response.status_code == 200:
                parsed_url = urlparse(response.url)
                mbasic_url = f"https://mbasic.facebook.com{parsed_url.path}?{parsed_url.query}"
                time.sleep(12)
                mainurl = requests.get(mbasic_url, headers=self.headers, cookies=self.Cookie).text
                
                reacturl = f"https://mbasic.facebook.com/reactions/picker/?ft_id={cmtid}"+mainurl.split(f"/reactions/picker/?ft_id={cmtid}")[1].split('"')[0].replace("amp;","")
                time.sleep(12)
                reactpage = requests.get(reacturl,headers=self.headers,cookies=self.Cookie).text
                reactionpicker = re.findall(r'/ufi/reaction//?.*?"', reactpage)
                url = "https://mbasic.facebook.com" + reactionpicker[index].replace("amp;", "").replace('"', "")
                status = requests.get(url, headers=self.headers, cookies=self.Cookie)
                status.raise_for_status()
                if status.status_code == 200:
                    return True
                else:
                    return False    
        except:
            return False
    def commentpost(self,id_post, commenttxt):
        try:
            # Gửi yêu cầu GET để lấy trang bài viết
            response = requests.get(
                f"https://www.facebook.com/{id_post}/",
                headers=self.headers,
                cookies=self.Cookie
            )
            
            if response.status_code == 200:
                parsed_url = urlparse(response.url)
                mbasic_url = f"https://mbasic.facebook.com{parsed_url.path}?{parsed_url.query}"
                time.sleep(15)
                mainurl = requests.get(mbasic_url, headers=self.headers, cookies=self.Cookie)
                
                if mainurl.status_code == 200:
                    soup = BeautifulSoup(mainurl.text, 'html.parser')
                    form = soup.find('form', action=lambda x: x and 'comment' in x)
                    
                    if form is None:
                        return False
                    
                    comment_url = "https://mbasic.facebook.com" + form['action']
                    
                    data = {input['name']: input.get('value', '') for input in form.find_all('input') if input.get('name')}
                    data['comment_text'] = commenttxt
                    time.sleep(15)
                    post_response = requests.post(comment_url, headers=self.headers, cookies=self.Cookie, data=data)
                    
                    if post_response.status_code == 200:
                        return True
                    else:
                        return False

        except:
        
            return False
    def follow(self,id):#User,Page
        try:
            response = requests.get(f"https://www.facebook.com/{id}",headers=self.headers,cookies=self.Cookie)
            if response.status_code == 200:
                time.sleep(12)
                parsed_url = urlparse(response.url)
                mbasic_url = f"https://mbasic.facebook.com{parsed_url.path}?{parsed_url.query}"
                mainurl = requests.get(mbasic_url, headers=self.headers, cookies=self.Cookie).text
                time.sleep(12)
                followurl = "https://mbasic.facebook.com/a/subscribe.php?id="+mainurl.split("/a/subscribe.php?id=")[1].split('"')[0].replace("amp;","")
                status = requests.get(followurl,headers=self.headers,cookies=self.Cookie)
                status.raise_for_status()
                if status.status_code == 200:
                    return True
                else:
                    return False
        except:
            return False
    def joingroup(self,id):
        try:
            response = requests.get(f"https://mbasic.facebook.com/{id}",headers=self.headers,cookies=self.Cookie)
            if response.status_code == 200:
                time.sleep(15)
                parsed_url = urlparse(response.url)
                mbasic_url = f"https://mbasic.facebook.com{parsed_url.path}?{parsed_url.query}"
                mainurl = requests.get(mbasic_url, headers=self.headers, cookies=self.Cookie).text
                time.sleep(15)
                grurl = "https://mbasic.facebook.com/a/group/join/?group_id"+mainurl.split("/a/group/join/?group_id")[1].split('"')[0].replace("amp;","")
                status = requests.get(grurl,headers=self.headers,cookies=self.Cookie)
                status.raise_for_status()
                if status.status_code == 200:
                    return True
                else:
                    return False
        except:
            return False
    def share(self, id_post, message):
        try:
            response = requests.get(f"https://www.facebook.com/{id_post}", headers=self.headers, cookies=self.Cookie)
            if response.status_code == 200:
                time.sleep(17)
                parsed_url = urlparse(response.url)
                mbasic_url = f"https://mbasic.facebook.com{parsed_url.path}?{parsed_url.query}"

                mainurl = requests.get(mbasic_url, headers=self.headers, cookies=self.Cookie).text

                parts = mainurl.split('/composer/mbasic/?c_src=share')
                if len(parts) < 2:
                    return False
                
                sharepageurl_part = parts[1].split('"')[0].replace("amp;", "")
                sharepageurl = f"https://mbasic.facebook.com/composer/mbasic/?c_src=share{sharepageurl_part}"
                time.sleep(17)
                sharepage = requests.get(sharepageurl, headers=self.headers, cookies=self.Cookie).text
                soup = BeautifulSoup(sharepage, 'html.parser')
                form = soup.find('form', action=lambda x: x and 'composer/mbasic/' in x)
                
                if form is None:
                    return False
                share_url = "https://mbasic.facebook.com" + form['action']
                data = {input['name']: input.get('value', '') for input in form.find_all('input') if input.get('name')}
                data['xc_message'] = message
                post_response = requests.post(share_url, headers=self.headers, cookies=self.Cookie, data=data)
                
                if post_response.status_code == 200:
                    return True
                else:
                    return False
        
        except:
            return False
        
def main():
    token_tds = load_token()
    if not token_tds:
        token_tds = input("Nhập Token TDS: ")
        save_token(token_tds)
    else:
        a = input("Bạn đã có token, bạn có muốn nhập token mới?(y/n)     :")
        if a.lower() == "y":
            token_tds = input("Nhập Token TDS: ")
            save_token(token_tds)

    tds = TDS(token_tds,None)
    account = tds.get_account_info()
    return account
def filltoken(i=1):
    typewriter("Nhập token Facebook. Dừng thì Enter")
    tokenfb = []
    while True:
        a = input(f"Nhập Token Facebook thứ {i}: ")
        if a:
            tokenfb.append(a)
            i += 1
        else:
            typewriter(f"Danh sách token Facebook: {tokenfb}")
            break
    return tokenfb
i= 1
def doquest(token, cookie, follow, like, likegiare, likesieure, reaction, comment, share, reactcmt, group, page,tg):
    settingdelay()
    logo()
    tds = TDS(token,cookie)
    fb = FB(cookie)
    tds.setnickfb(fb.UID)
    setting = load_token("delaytds.txt").split('|')
    liked = int(setting[0])
    followd = int(setting[1])
    reactiond = int(setting[2])
    commentd = int(setting[3])
    shared = int(setting[4])
    reactcmtd = int(setting[5])
    groupd = int(setting[6])
    paged = int(setting[7])
    questd = int(setting[8])
    
    def printstatus(xu,id,msg="",type="None"):
        global i
        dt = gettime()
        typewriter(f"{Fore.RED}[{i}]{Style.RESET_ALL} | {dt}: {Fore.CYAN}{type}{Style.RESET_ALL} | {Fore.BLUE}{id}{Style.RESET_ALL} | {Fore.GREEN}{xu}{Style.RESET_ALL} | {Fore.MAGENTA}{msg}{Style.RESET_ALL}")
        i+=1
    def cd(seconds):
        while seconds >= 0:
            timeformat = f"Vui lòng đợi {seconds} | Lê Minh Trí     "
            sys.stdout.write('\r' + timeformat + ' ' * (40 - len(timeformat)))
            sys.stdout.flush()
            time.sleep(1)
            seconds -= 1
        sys.stdout.write('\r' + ' ' * 40 + '\r')
        sys.stdout.flush()
    while True:
        
        if follow == True:#ID
            quest = tds.get_quest("follow")
            if quest:
                if "id" in quest[0]:
                    for i in range(len(quest)):
                        state = fb.follow(quest[i]["id"])
                        cd(followd)
                        if state == True:
                            result = tds.getcoin("follow",quest[i]["id"])
                            if result.get("success"):
                                data = result.get("data")
                                printstatus(data["xu"],data["id"],data["msg"],"FOLLOW")
                cd(questd)
            else:
                cd(questd)
        if like == True:#ID
            quest = tds.get_quest("like")
            if quest:
                if "id" in quest[0]:
                    for i in range(len(quest)):
                        state = fb.reactpost(quest[i]["id"],"like")
                        cd(liked)
                        if state == True:
                            result = tds.getcoin("like",quest[i]["id"])
                            if result.get("success"):
                                data = result.get("data")
                                printstatus(data["xu"],data["id"],data["msg"],"LIKE")
                cd(questd)
            else:
                cd(questd)
        if likegiare == True:#ID
            quest = tds.get_quest("likegiare")
            if quest:
                if "id" in quest[0]:
                    for i in range(len(quest)):
                        state = fb.reactpost(quest[i]["id"],"like")
                        cd(liked)
                        if state == True:
                            result = tds.getcoin("like",quest[i]["id"])
                            if result.get("success"):
                                data = result.get("data")
                                printstatus(data["xu"],data["id"],data["msg"],"LIKEGIARE")
                cd(questd)
            else:
                cd(questd)
        if likesieure == True:#ID
            quest = tds.get_quest("likesieure")
            if quest:
                if "id" in quest[0]:
                    for i in range(len(quest)):
                        state = fb.reactpost(quest[i]["id"],"like")
                        cd(liked)
                        if state == True:
                            result = tds.getcoin("like",quest[i]["id"])
                            if result.get("success"):
                                data = result.get("data")
                                printstatus(data["xu"],data["id"],data["msg"],"LIKESIEURE")
                cd(questd)
            else:
                cd(questd)
        if reaction == True:#ID,Type
            quest = tds.get_quest("reaction")
            if quest:
                if "id" in quest[0]:
                    for i in range(len(quest)):
                        state = fb.reactpost(quest[i]["id"],quest[i]["type"])
                        cd(reactiond)
                        if state == True:
                            result = tds.getcoin(quest[i]["type"],quest[i]["id"])
                            if result.get("success"):
                                printstatus(data["xu"],data["id"],data["msg"],quest[i]["type"])
                cd(questd)
            else:
                cd(questd)
        if comment == True:#ID,msg
            quest = tds.get_quest("comment")
            if quest:
                if "id" in quest[0]:
                    for i in range(len(quest)):
                        state = fb.commentpost(quest[i]["id"],quest[i]["msg"])
                        cd(commentd)
                        if state == True:
                            result = tds.getcoin("comment",quest[i]["id"])
                            if result.get("success"):
                                printstatus(data["xu"],data["id"],data["msg"]+" | "+quest[i]["msg"],"COMMENT")
                cd(questd)
            else:
                cd(questd)
        if share == True:#ID
            quest = tds.get_quest("share")
            if quest:
                if "id" in quest[0]:
                    for i in range(len(quest)):
                        state = fb.share(quest[i]["id"],"")
                        cd(shared)
                        if state == True:
                            result = tds.getcoin("share",quest[i]["id"])
                            if result.get("success"):
                                printstatus(data["xu"],data["id"],data["msg"],"SHARE")
                    cd(questd)
            else:
                cd(questd)
        if reactcmt == True:#ID,type
            quest = tds.get_quest("reactcmt")
            if quest:
                if "id" in quest[0]:
                    for i in range(len(quest)):
                        state = fb.reactcomment(quest[i]["id"],quest[i]["type"])
                        cd(reactcmtd)
                        if state == True:
                            result = tds.getcoin(quest[i]["type"]+"CMT",quest[i]["id"])
                            if result.get("success"):
                                printstatus(data["xu"],data["id"],data["msg"],quest[i]["type"]+"CMT")
                cd(questd)
            else:
                cd(questd)
        if group == True:#ID
            quest = tds.get_quest("group")
            if quest:
                if "id" in quest[0]:
                    for i in range(len(quest)):
                        state = fb.joingroup(quest[i]["id"])
                        cd(groupd)
                        if state == True:
                            result = tds.getcoin("group",quest[i]["id"])
                            if result.get("success"):
                                printstatus(data["xu"],data["id"],data["msg"],"GROUP")
                cd(questd)
            else:
                cd(questd)
        if page == True:#ID
            quest = tds.get_quest("page")
            if quest:
                if "id" in quest[0]:
                    for i in range(len(quest)):
                        state = fb.follow(quest[i]["id"])
                        cd(paged)
                        if state == True:
                            result = tds.getcoin("page",quest[i]["id"])
                            if result.get("success"):
                                printstatus(data["xu"],data["id"],data["msg"],"PAGE")
                cd(questd)
            else:
                cd(questd)
        tg-=1
        if tg == 0:
            break

def settingdelay():
    logo()
    setting = load_token("delaytds.txt").split('|')
    like = setting[0]
    follow = setting[1]
    reaction = setting[2]
    comment = setting[3]
    share = setting[4]
    reactcmt = setting[5]
    group = setting[6]
    page = setting[7]
    quest = setting[8]
    typewriter("--------------------------------------------------------------------")
    typewriter("Setting Delay Hiện Tại")
    typewriter("--------------------------------------------------------------------")
    typewriter(f"Delay Like: {like}")
    typewriter(f"Delay Follow: {follow}")
    typewriter(f"Delay Cảm Xúc: {reaction}")
    typewriter(f"Delay Bình Luận: {comment}")
    typewriter(f"Delay Share: {share}")
    typewriter(f"Delay Cảm Xúc Bình Luận: {reactcmt}")
    typewriter(f"Delay Group: {group}")
    typewriter(f"Delay Page: {page}")
    typewriter(f"Delay mỗi loại nhiệm vụ: {quest}")
    typewriter("--------------------------------------------------------------------")
    typewriter("Bạn có muốn giữ setting delay này?")
    typewriter("--------------------------------------------------------------------")
    typewriter("LƯU Ý: NẾU DELAY QUÁ NGẮN SẼ DẪN ĐẾN KHÓA TÀI KHOẢN")
    typewriter("[1]:Giữ lựa chọn hiện tại")
    typewriter("[2]:Sử Dụng Setting Delay Của Riêng Tôi")
    try:
        a = int(input("Nhập: "))
        if a == 2:
            os.system("cls")
            typewriter("--------------------------------------------------------------------")
            typewriter("Nhập Setting Delay Của bạn")
            typewriter("--------------------------------------------------------------------")
            like = input("Delay Like(>30): ")
            follow = input("Delay Follow(>45): ")
            reaction = input("Delay Cảm Xúc(>45): ")
            comment = input("Delay Bình Luận(>60): ")
            share = input("Delay Share(>75): ")
            reactcmt = input("Delay Cảm Xúc Bình Luận(>60): ")
            group = input("Delay Group(>100): ")
            page = input("Delay Page(>100): ")
            typewriter("--------------------------------------------------------------------")
            save_token(f"{like}|{follow}|{reaction}|{comment}|{share}|{reactcmt}|{group}|{page}|{quest}","delaytds.txt")
            typewriter("Đã Lưu Setting")
            os.system("cls")
        elif a:
            pass
        else:
            typewriter("Vui Lòng Nhập Đúng Ký Tự!!!")
            return settingdelay()
    except ValueError:
        typewriter("Vui Lòng Nhập Một Số Nguyên!!!")
        return settingdelay()

def choosequest(TOKEN, COOKIE):
    logo()
    tasks = {
        "1": "Like",
        "2": "Follow",
        "3": "Cảm Xúc",
        "4": "Bình Luận",
        "5": "Chia Sẻ",
        "6": "Cảm Xúc Bình Luận",
        "7": "Tham Gia Nhóm",
        "8": "Thích Trang"
    }
    
    typewriter("--------------------------------------------------------------------")
    typewriter("Chọn Nhiệm Vụ TRAODOISUB.COM")
    typewriter("--------------------------------------------------------------------")
    for number, nv in tasks.items():
        typewriter(f"[{number}]: {nv}")
    typewriter("--------------------------------------------------------------------")
    typewriter("Chọn nhiều Nhiệm vụ nhập: 1+2+3... hoặc chọn hết nhập all")
    typewriter("--------------------------------------------------------------------")
    a = input("Chọn: ")

    if a == "all":
        print("Chọn tất cả nhiệm vụ")
        doquest(TOKEN, COOKIE, True, True, True, True, True, True, True, True, True, True, 10000000000000)
    else:
        selected_tasks = [task.strip() for task in a.split("+")]
        
        # Kiểm tra tính hợp lệ của các nhiệm vụ đã chọn
        valid_tasks = set(tasks.keys())
        if all(task in valid_tasks for task in selected_tasks):
            status = {
                "Like": "1" in selected_tasks,
                "Follow": "2" in selected_tasks,
                "Cảm Xúc": "3" in selected_tasks,
                "Bình Luận": "4" in selected_tasks,
                "Chia Sẻ": "5" in selected_tasks,
                "Cảm Xúc Bình Luận": "6" in selected_tasks,
                "Tham Gia Nhóm": "7" in selected_tasks,
                "Thích Trang": "8" in selected_tasks
            }

            doquest(
                token=TOKEN,
                cookie=COOKIE,
                follow=status.get("Follow", False),
                like=status.get("Like", False),
                likegiare=status.get("Like", False),
                likesieure=status.get("Like", False),
                reaction=status.get("Cảm Xúc", False),
                comment=status.get("Bình Luận", False),
                share=status.get("Chia Sẻ", False),
                reactcmt=status.get("Cảm Xúc Bình Luận", False),
                group=status.get("Tham Gia Nhóm", False),
                page=status.get("Thích Trang", False),
                tg=100000 
            )
        else:
            typewriter("Vui Lòng Nhập Đúng Dạng")
            time.sleep(3)
            return choosequest(TOKEN,COOKIE)

if __name__ == "__main__":
    account = main()
    cookie = input("Nhập Cookie Facebook: ")
    choosequest(account["token"],cookie)