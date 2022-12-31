import requests,os,hashlib
api = ""
api_md5_ok = "fdbbfcd6f5049afc12a06da130e6657f"
# 获得当前文件路径,从当前文件同路径下api.txt中读取api地址
with open(os.path.dirname(os.path.abspath(__file__)) + "/api.txt", "r") as f:
    api = f.read()
# md5加密后打印api地址
api_md5 = f"{api}0/123962012/0"
api_md5 = (hashlib.md5(api_md5.encode(encoding='UTF-8')).hexdigest())
if api_md5_ok != api_md5:
    print("op_recharge:api地址错误,群内下载")
    exit()

def get_between(s, start, end):
    return (s.split(start)[1]).split(end)[0]


def get_pay_url(
    uid: int = 123962012,
    item_id: int = 0,
    pay_mode: int = 0,
) -> dict:
    """_summary_

    Args:
        uid (int, optional): _description_. Defaults to 123962012.
        item_id (int, optional): _description_. Defaults to 0.
        pay_mode (int, optional): _description_. Defaults to 0.

    Returns:
        result (dict): query_url,code,thing, thing_img_url, order_id, pay_url, price, qrcode_b64
    """
    uid, item_id, pay_mode = str(uid), str(item_id), str(pay_mode)
    url = f"{api}{item_id}/{uid}/{pay_mode}"
    r = requests.get(url)

    r_text = requests.get(url).text
    # print(r_text)
    result = {
        "query_url": url,
        "code": r.status_code,
    }
    if result["code"] != 200:
        return result
    result["thing"] = get_between(
        r_text, '        <h2>', '</h2><img src="'
    )
    result["thing_img_url"] = get_between(
        r_text, '</h2><img src="', '" alt="thing" style="width: 5%;">'
    )
    result["order_id"] = get_between(r_text, "<br>order:", "<br>url:")
    result["pay_url"] = get_between(r_text, "<br>url:", "</p>")
    result["price"] = get_between(r_text, '<p style="position: relative; z-index: 999;">price:￥', "<br>")
    result["qrcode_b64"] = get_between(
        r_text, ' <img src="data:;base64,', '" alt="qrcode" style="margin-top: -40px;">'
    )
    return result

def check(order_id,uid):
        # http://box.fuckmys.tk/check/1609168475074437120/123962012
    url = f'{api.replace("topup/","check/")}{str(order_id)}/{str(uid)}'
    print(url)
    # r = requests.get(url)
    r_text = requests.get(url).text
    print(r_text)
    return r_text
if __name__ == "__main__":
    # print(get_pay_url())
    check("1609168475074437120",123962012)
