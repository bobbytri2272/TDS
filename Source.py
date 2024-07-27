import requests, re,time
import os
from bs4 import BeautifulSoup

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
                print(f"Người dùng: {user} | Số xu: {xu}")
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
                    print("Cookie Sai")
                    return False
                else:
                    return username
        except:
            return False
    def reactpost(self, id, type="like"):
        try:
            type = type.upper()
            response = requests.get(f"https://mbasic.facebook.com/{id}/", headers=self.headers, cookies=self.Cookie).text
            
            reactionpageurl = "https://mbasic.facebook.com/reactions/picker/?" + response.split("/reactions/picker/?")[1].split('"')[0].replace("amp;", "")
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
            response = requests.get(f"https://mbasic.facebook.com/{id}",headers=self.headers,cookies=self.Cookie).text
            reacturl = f"https://mbasic.facebook.com/reactions/picker/?ft_id={cmtid}"+response.split(f"/reactions/picker/?ft_id={cmtid}")[1].split('"')[0].replace("amp;","")
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
            response = requests.get(f"https://mbasic.facebook.com/{id_post}/", headers=self.headers, cookies=self.Cookie).text
            soup = BeautifulSoup(response, 'html.parser')
            form = soup.find('form', action=lambda x: x and 'comment' in x)
            
            if form is None:
                return False
            commenturl = "https://mbasic.facebook.com" + form['action']
            
            data = {input['name']: input.get('value', '') for input in form.find_all('input') if input.get('name')}
            data['comment_text'] = commenttxt 
            post_response = requests.post(commenturl, headers=self.headers, cookies=self.Cookie, data=data)
            if post_response.status_code == 200:
                return True
            else:
                return False
        except:
            return False
    def follow(self,id):#User,Page
        try:
            response = requests.get(f"https://mbasic.facebook.com/{id}",headers=self.headers,cookies=self.Cookie).text
            followurl = "https://mbasic.facebook.com/a/subscribe.php?id="+response.split("/a/subscribe.php?id=")[1].split('"')[0].replace("amp;","")
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
            response = requests.get(f"https://mbasic.facebook.com/{id}",headers=self.headers,cookies=self.Cookie).text
            grurl = "https://mbasic.facebook.com/a/group/join/?group_id"+response.split("/a/group/join/?group_id")[1].split('"')[0].replace("amp;","")
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
            response = requests.get(f"https://mbasic.facebook.com/{id_post}", headers=self.headers, cookies=self.Cookie).text
            
            parts = response.split('/composer/mbasic/?c_src=share')
            if len(parts) < 2:
                return False
            
            sharepageurl_part = parts[1].split('"')[0].replace("amp;", "")
            sharepageurl = f"https://mbasic.facebook.com/composer/mbasic/?c_src=share{sharepageurl_part}"
            
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
    print("Nhập token Facebook. Dừng thì Enter")
    tokenfb = []
    while True:
        a = input(f"Nhập Token Facebook thứ {i}: ")
        if a:
            tokenfb.append(a)
            i += 1
        else:
            print("Danh sách token Facebook:",tokenfb)
            break
    return tokenfb

def doquest(token, cookie, follow, like, likegiare, likesieure, reaction, comment, share, reactcmt, group, page,tg):
    tds = TDS(token,cookie)
    fb = FB(cookie)
    timedelay = 15
    while True:
        
        if follow == True:#ID
            quest = tds.get_quest("follow")
            if "id" in quest[0]:
                print("Follow:",quest)
                for i in range(len(quest)):
                    state = fb.follow(quest[i]["id"])
                    if state == True:
                        time.sleep(timedelay)
                        print(tds.getcoin("follow",quest[i]["id"]))
            else:
                time.sleep(30)
        if like == True:#ID
            quest = tds.get_quest("like")
            if "id" in quest[0]:
                print("Like:",quest)
                for i in range(len(quest)):
                    state = fb.reactpost(quest[i]["id"],"like")
                    if state == True:
                        time.sleep(timedelay)
                        print(tds.getcoin("like",quest[i]["id"]))
            else:
                time.sleep(30)
        if likegiare == True:#ID
            quest = tds.get_quest("likegiare")
            if "id" in quest[0]:
                print("Like Gia Re:",quest)
                for i in range(len(quest)):
                    state = fb.reactpost(quest[i]["id"],"like")
                    if state == True:
                        time.sleep(timedelay)
                        print(tds.getcoin("likegiare",quest[i]["id"]))
            else:
                time.sleep(30)
        if likesieure == True:#ID
            quest = tds.get_quest("likesieure")
            if "id" in quest[0]:
                print("Like Sieu Re:",quest)
                for i in range(len(quest)):
                    state = fb.reactpost(quest[i]["id"],"like")
                    if state == True:
                        time.sleep(timedelay)
                        print(tds.getcoin("likesieure",quest[i]["id"]))
            else:
                time.sleep(30)
        if reaction == True:#ID,Type
            quest = tds.get_quest("reaction")
            if "id" in quest[0]:
                print("Cam Xuc:",quest)
                for i in range(len(quest)):
                    state = fb.reactpost(quest[i]["id"],quest[i]["type"])
                    if state == True:
                        time.sleep(timedelay)
                        print(tds.getcoin(quest[i]["type"],quest[i]["id"]))
            else:
                time.sleep(30)
        if comment == True:#ID,msg
            quest = tds.get_quest("comment")
            if "id" in quest[0]:
                print("Comment:",quest)
                for i in range(len(quest)):
                    state = fb.commentpost(quest[i]["id"],quest[i]["msg"])
                    if state == True:
                        time.sleep(timedelay)
                        print(tds.getcoin("comment",quest[i]["id"]))
            else:
                time.sleep(30)
        if share == True:#ID
            quest = tds.get_quest("share")
            if "id" in quest[0]:
                print("Share:",quest)
                for i in range(len(quest)):
                    state = fb.share(quest[i]["id"],"")
                    if state == True:
                        time.sleep(timedelay)
                        print(tds.getcoin("share",quest[i]["id"]))
            else:
                time.sleep(30)
        if reactcmt == True:#ID,type
            quest = tds.get_quest("reactcmt")
            if "id" in quest[0]:
                print("Cam Xuc Comment:",quest)
                for i in range(len(quest)):
                    state = fb.reactcomment(quest[i]["id"],quest[i]["type"])
                    if state == True:
                        time.sleep(timedelay)
                        print(tds.getcoin("reactcmt",quest[i]["id"]))
            else:
                time.sleep(30)
        if group == True:#ID
            quest = tds.get_quest("group")
            if "id" in quest[0]:
                print("Group:",quest)
                for i in range(len(quest)):
                    state = fb.joingroup(quest[i]["id"])
                    if state == True:
                        time.sleep(timedelay)
                        print(tds.getcoin("group",quest[i]["id"]))
            else:
                time.sleep(30)
        if page == True:#ID
            quest = tds.get_quest("page")
            if "id" in quest[0]:
                print("Page:",quest)
                for i in range(len(quest)):
                    state = fb.follow(quest[i]["id"])
                    if state == True:
                        time.sleep(timedelay)
                        print(tds.getcoin("follow",quest[i]["id"]))
            else:
                time.sleep(30)
        tg-=1
        if tg == 0:
            break
    
        

if __name__ == "__main__":
    account = main()
    cookie = input("Nhập Cookie Facebook: ")
    tds = TDS(account["token"],cookie)
    fb = FB(cookie)
    doquest(account["token"],cookie,True,True,True,True,True,True,True,True,True,True,10)
    
    
