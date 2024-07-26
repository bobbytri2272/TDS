import requests
import os

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
    def getcoin(self, type:str,id):
        url = f"https://traodoisub.com/api/coin/?type={type.upper()}&id={id}&access_token={self.Token}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            print(data)
        except requests.exceptions.RequestException as e:
            return {str(e)}

    def get_quest(self, type:str,):
        url = f"https://traodoisub.com/api/?fields={type.lower()}&access_token={self.Token}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            print(data)
        except requests.exceptions.RequestException as e:
            return {str(e)}

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
    account = main()
    tds = TDS(account["token"])
    tds.get_quest("reaction")
    #fbtoken = filltoken()
