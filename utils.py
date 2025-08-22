import pathlib
import requests
import time

def DivideTLEs(path: pathlib.Path):
    dataFolder = pathlib.Path(f"./data/{path.stem[:-7]}-data")
    dataFolder.mkdir(parents=True, exist_ok=True)
    cnt = 0
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("1 "):
                SatelName = line[2:7]
                of = open(f"{dataFolder}/{path.stem[:-7]}-{SatelName}.tle", "w")
                cnt += 1
            of.write(line)
            if line.startswith("2 "):
                of.close()
                of = None
    print(f"Total: {cnt}")


def FetchAllData(config: dict):

    # ---------- 参数 ----------
    USERNAME = config["Username"]
    PASSWORD = config["Password"]
    # ---------- 登录 ----------
    login_url = "https://www.space-track.org/ajaxauth/login"
    session = requests.Session()
    resp = session.post(login_url, data={"identity": USERNAME, "password": PASSWORD})
    resp.raise_for_status()          # 登录失败会抛出异常

    # ---------- 查询 ----------

    for key, spec in config["Satellites"].items():
        query_url = (
            f"https://www.space-track.org/basicspacedata/query/class/gp"
            f"{spec['Query']}"
        )
        print(query_url)

        resp = session.get(query_url)
        resp.raise_for_status()

        # ---------- 保存 ----------
        OUT_FILE = pathlib.Path(f"./data/{key.lower()}_latest.tle")
        OUT_FILE.write_text(resp.text, encoding="utf-8")
        print(f"已保存 {len(resp.text.splitlines())} 行 TLE 到 {OUT_FILE.resolve()}")
        time.sleep(30)

# OneWeb:
#     Name: OneWeb
#     Query: /OBJECT_NAME/ONEWEB~~/orderby/epoch%20desc/format/tle

def FetchDatabyName(
        config: dict,
        name: str,
        like: bool = True,
        orderby: str = "desc",
        format: str = "tle"):
    USERNAME = config["Username"]
    PASSWORD = config["Password"]
    login_url = "https://www.space-track.org/ajaxauth/login"
    session = requests.Session()
    resp = session.post(login_url, data={"identity": USERNAME, "password": PASSWORD})
    resp.raise_for_status()          # 登录失败会抛出异常

    query_url = (
        f"https://www.space-track.org/basicspacedata/query/class/gp"
        f"/OBJECT_NAME/{name}"
    )
    if like:
        query_url += "~~"
    query_url += f"/orderby/epoch%20{orderby}/format/{format}"
    print(query_url)

    resp.session.get(query_url)
    resp.raise_for_status()
    # ---------- 保存 ----------
    OUT_FILE = pathlib.Path(f"./data/{name.lower()}_latest.tle")
    OUT_FILE.write_text(resp.text, encoding="utf-8")
    print(f"已保存 {len(resp.text.splitlines())} 行 TLE 到 {OUT_FILE.resolve()}")


    
if __name__ == '__main__':
    FetchDatabyName("ONEWEB")