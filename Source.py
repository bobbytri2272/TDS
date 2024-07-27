import requests, re
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
    def __init__(self, token) -> None:
        self.Token = token

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
            quests = [data[i]['id'] for i in range(len(data))]
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
        except Exception as e:
            print(f"Error: {e}")
            return False
    def reactpost(self, id_post, type="like"):
        try:
            type = type.upper()
            response = requests.get(f"https://mbasic.facebook.com/{id_post}/", headers=self.headers, cookies=self.Cookie).text

            reactionpageurl = "https://mbasic.facebook.com/reactions/picker/?" + response.split("/reactions/picker/?")[1].split('"')[0].replace("amp;", "")
            reactionpage = requests.get(reactionpageurl, headers=self.headers, cookies=self.Cookie).text
            reactionpicker = re.findall(r'/ufi/reaction//?.*?"', reactionpage)
            
            index = 0 if type == "LIKE" else 1 if type == "LOVE" else 2 if type == "CARE" else 3 if type == "HAHA" else 4 if type == "WOW" else 5 if type == "SAD" else 6 if type == "ANGRY" else 7
            url = "https://mbasic.facebook.com" + reactionpicker[index].replace("amp;", "").replace('"', "")
            print(url)
            #status = requests.get(url, headers=self.headers, cookies=self.Cookie)
            #status.raise_for_status()
            #if status.status_code == 200:
                #return True
            #else:
             #   return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return 
    def reactcomment(self,id,type):
        try:
            postid,cmtid = id.split("_")
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
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return 
    def commentpost(self,id_post, commenttxt):
        try:
            response = requests.get(f"https://mbasic.facebook.com/{id_post}/", headers=self.headers, cookies=self.Cookie).text
            soup = BeautifulSoup(response, 'html.parser')
            form = soup.find('form', action=lambda x: x and 'comment' in x)
            
            if form is None:
                print("Comment form not found.")
                return False
            commenturl = "https://mbasic.facebook.com" + form['action']
            
            data = {input['name']: input.get('value', '') for input in form.find_all('input') if input.get('name')}
            data['comment_text'] = commenttxt 
            post_response = requests.post(commenturl, headers=self.headers, cookies=self.Cookie, data=data)
            if post_response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    def follow(self,id):
        try:
            response = requests.get(f"https://mbasic.facebook.com/{id}",headers=self.headers,cookies=self.Cookie).text
            followurl = "https://mbasic.facebook.com/a/subscribe.php?id="+response.split("/a/subscribe.php?id=")[1].split('"')[0].replace("amp;","")
            status = requests.get(followurl,headers=self.headers,cookies=self.Cookie)
            status.raise_for_status()
            if status.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    def share(self, id, message):
        try:
            response = requests.get(f"https://mbasic.facebook.com/{id}", headers=self.headers,cookies= self.Cookie).text
            sharepage = "https://mbasic.facebook.com/composer/mbasic/?c_src=share"+response.split("/composer/mbasic/?c_src=share")[1].split('"')[0].replace("amp;","")
            print(sharepage)
            
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

    tds = TDS(token_tds)
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

if __name__ == "__main__":
    #account = main()
    #tds = TDS(account["token"])
    #quest = tds.get_quest("like")
    #print(quest)
    ck = FB("sb=DLGeZkksd8rSOfprbOZRysMN;c_user=100094335661588;datr=z92hZivEL2EMf6QxumHYsy-7;m_page_voice=100094335661588;ps_l=1;ps_n=1;m_pixel_ratio=1;wd=1920x953;fr=1GLY6oZVV0MugnE4t.AWVk-tsISz-erjSS4GnLG5MESe0.BmpInk..AAA.0.0.BmpInk.AWV8Tbd44lA;xs=15%3AsFUGVUeyi-oR5g%3A2%3A1721843873%3A-1%3A6277%3A%3AAcWKOF-MYFrX2Dm_SBzugCXp8oJokSnZQrgnc7Iw5w;presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1722059743212%2C%22v%22%3A1%7D;m_ls=%7B%22100094335661588%22%3A%7B%22c%22%3A%7B%221%22%3A%22HCwAABbsCBbo6_yvBRMFFqjYkfWgwi0A%22%2C%2295%22%3A%22HCwAABZ8FtzL7MULEwUWqNiR9aDCLQA%22%7D%2C%22d%22%3A%22983d3f54-ea63-494e-af0d-684dea5c669c%22%2C%22s%22%3A%220%22%2C%22u%22%3A%22jhe19a%22%7D%2C%2261563503390738%22%3A%7B%22c%22%3A%7B%221%22%3A%22HCwRAAAWKhbY_bnZAhMFFqTAgey7_xsA%22%2C%2295%22%3A%22HCwRAAAWDBbiz9_IChMFFqTAgey7_xsA%22%7D%2C%22d%22%3A%2278d6d33e-b40e-472b-8260-3ead89470196%22%2C%22s%22%3A%220%22%2C%22u%22%3A%22my5qid%22%7D%7D;")
    ck.reactpost("461041163519394","love")
