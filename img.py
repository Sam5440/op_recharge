# 导入PIL
import asyncio
from pathlib import Path
import requests, os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from base64 import b64decode, b64encode
if __name__ != "__main__":
    from .decorate import run_sync
path = Path(__file__).parent  # 获取文件所在目录的绝对路径# Path是路径对象，必须转为str之后ImageFont才能读取
font_cn_path = str(path / "pcrcnfont.ttf")
# font_cn_path = "C:/Windows/Fonts/simhei.ttf"


@run_sync
def img_create(recharge_info: dict, show: bool = False) -> str:
    img = Image.new("RGBA", (900, 800), color=(255, 255, 255))
    if "alipay" in recharge_info["pay_url"]:
        pay_img_url = "https://pp.myapp.com/ma_icon/0/icon_5294_1671098444/256"
    else:
        pay_img_url = "https://pp.myapp.com/ma_icon/0/icon_10910_1670844838/256"
    pay_img = Image.open(BytesIO(requests.get(pay_img_url).content))
    pay_img = pay_img.convert("RGBA")
    pay_img = pay_img.resize((275, 275))
    img.paste(pay_img, (600, 120), pay_img)
    # 下载图片,并转换为image对象(rgba)黏贴进图片
    thing_img = Image.open(
        BytesIO(requests.get(recharge_info["thing_img_url"]).content)
    )
    thing_img = thing_img.convert("RGBA")
    # thing_img = thing_img.resize((600, 600))
    # img.paste(thing_img, (-20, 40), thing_img)
    thing_img = thing_img.resize((500, 500))
    img.paste(thing_img, (25, 145), thing_img)
    # 把recharge_info['qrcode_b64']转图片缩放成300*300,粘贴到img左下角
    img_qrcode = Image.open(BytesIO(b64decode(recharge_info["qrcode_b64"])))
    img_qrcode = img_qrcode.resize((300, 300))
    img.paste(img_qrcode, (600, 500))

    # 创建画笔
    draw = ImageDraw.Draw(img)
    # 创建字体
    font = ImageFont.truetype(font_cn_path, 50)
    # 写入文字
    draw.text(
        (20, 20),
        "商品:" + recharge_info["thing"].replace("for ", "\nUID : "),
        font=font,
        fill=(0, 0, 0),
    )
    len_price = len(recharge_info["price"])*13
    draw.text(
        (660-len_price, 450),
        "价格:" + recharge_info["price"] + "元",
        font=font,
        fill=(0, 0, 0),
    )

    draw.text(
        (20, 650),
        "订单号:",
        font=font,
        fill=(0, 0, 0),
    )

    draw.text(
        # (120, 670),
        (20, 715),
        recharge_info["order_id"],
        font=font,
        fill=(0, 0, 0),
    )
    draw.text(
        (645, 30),
        "[OPRC]",
        font=font,
        fill=(0, 0, 0),
    )
    if show:
        img.show()
    # 转rgb通道
    img = img.convert("RGB")
    # img转base64
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    # return img_byte_arr
    img_base64 = b64encode(img_byte_arr).decode()
    return img_base64
if __name__ == "__main__":
    #img test
    test = {
        "query_url": "http://box.fuckmys.tk/topup/0/123962012/0",
        "code": 200,
        "thing": "创世结晶×60 for 123962012",
        "thing_img_url": "https://uploadstatic.mihoyo.com/payment-center/2022/09/07/0f362595da2e37a7a8fde1bb120656d2_594155779359709441.png",
        "order_id": "1609131332658593792",
        "pay_url": "https://qr.alipay.com/bax035162f6xvlbe4tqd30b9",
        "price": "6",
        "qrcode_b64": "iVBORw0KGgoAAAANSUhEUgAAAXIAAAFyAQAAAADAX2ykAAACkElEQVR4nO2aQW7bMBBF31QEvKSAHiBHkW7QIxW9mXUUH8CAtDRA4XdBUnYcpE1QWbXa4SIxxLf4wOBzhsMx8Zk1fPkUDs4777zzzjvv/Hu8lRWof8ysnwIw1b1+Qz3Or8x3kqSxfJTGRvrRzgY0kiS95h+tx/mV+ak6tBtng3gxiAnrIXt6Yz3Or8OH+w/DSwoMfSPrTgExbavH+cfy0tgIKEez9X9Zj/N/xlf/RgETWHecA8QRmGYTE9y2QJ5Nv/Mf4gczM2sBpoPoTgHrs3/nXD5vq8f5lfjs36tDNbyk+qttKMbeTo/z6/KUy0+UKHehVJNwlOiU0BHKFer4bPqd//Wq/p1CgnguVVW+H+WNFrvhn02/8x/ih3Y2HacAnS5Gdyp1l/VR3t/YMb/UzyNGPAeYWgQpAHNgMNDw7Vy5Z9Pv/G9WNme3OLQbm5x1gZKES072/LtDvsZ3hFJkRUnHmO570l5f7ZKvvoyJGsumRjWHuzrZ47tf3vp8FickJXJVdWQ26XRQrrm21OP8WvxNf8NywmXO3wwCRkx5V9vocX5d/qa+qof01cmSjtXYfj7vki9hvJZRALl+zgGFpab2+O6Pr/FdLkld7U/m0BbE/btTvubaOKLBAKaWpWpOVndl2+hx/hF8Pp+XJkd+EfyuixVPjxvrcX4tfqmVAWiSIAUxtVDs/DUxWJM20uP8Q/ilV2X9dLh5Lqyl88VKOn5S/c6/t276k9311TcPYS3L70d75e/nJzX0hoaXi5WeRzwHAV5f/St8LKm2jGPRiMHnr/bKv5mfhADd6SCG3qAOdvj77z75On+VV1OHsMZmqa+Wnofn3x3yb+Yn879Xrwoqgd9Cj/POO++8887/D/xPpc+m4P982c4AAAAASUVORK5CYII=",  # ok
    }
    img_create(test,True)

# b64_img = img_create()

@run_sync
def help_img_create(help_info):
    img = Image.new("RGBA", (900, 800), color=(255, 255, 255))
    # 创建画笔
    draw = ImageDraw.Draw(img)
    # 创建字体
    font = ImageFont.truetype(font_cn_path, 50)
    # 写入文字
    draw.text(
        (10, 20),
        help_info,
        font=font,
        fill=(0, 0, 0),
    )
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    # return img_byte_arr
    img_base64 = b64encode(img_byte_arr).decode()
    return img_base64



    # task = []
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.gather(*task))
    # loop.close()