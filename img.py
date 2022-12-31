# 导入PIL
from base64 import b64decode, b64encode
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont
from nonebot.utils import run_sync

path = Path(__file__).parent  # 获取文件所在目录的绝对路径# Path是路径对象，必须转为str之后ImageFont才能读取
font_cn_path = str(path / "pcrcnfont.ttf")


async def img_create(recharge_info: dict, pay_mode: int = 0, show: bool = False) -> str:
    img = Image.new("RGBA", (900, 800), color=(255, 255, 255))
    print(recharge_info.items())
    thing_img_url = str(recharge_info["thing_img_url"])
    if pay_mode == 0:
        pay_img_url = "https://pp.myapp.com/ma_icon/0/icon_5294_1671098444/256"
    elif pay_mode == 1:
        pay_img_url = "https://pp.myapp.com/ma_icon/0/icon_10910_1670844838/256"
    else:
        return "支付方式错误"
    pay_img = Image.open(BytesIO(requests.get(pay_img_url).content))
    pay_img = pay_img.convert("RGBA")
    pay_img = pay_img.resize((275, 275))
    img.paste(pay_img, (600, 120), pay_img)
    # 下载图片,并转换为image对象(rgba)黏贴进图片
    thing_img = Image.open(BytesIO(requests.get(thing_img_url).content))
    thing_img = thing_img.convert("RGBA")
    thing_img = thing_img.resize((600, 600))
    img.paste(thing_img, (-20, 40), thing_img)
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

    draw.text(
        (650, 450),
        "价格:" + recharge_info["price"] + "元",
        font=font,
        fill=(0, 0, 0),
    )

    draw.text(
        (20, 600),
        "订单号:",
        font=font,
        fill=(0, 0, 0),
    )

    draw.text(
        # (120, 670),
        (20, 670),
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
    # img转base64
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    # return img_byte_arr
    img_base64 = b64encode(img_byte_arr).decode()
    return img_base64


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
