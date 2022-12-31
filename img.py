# 导入PIL
import requests, os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from base64 import b64decode, b64encode


# 创建空白画布
def create_white_img():
    img = Image.new("RGBA", (900, 800), color=(255, 255, 255))
    return img

def img_create(recharge_info: dict) -> str:
    img = create_white_img()
    thing_img_url = recharge_info["thing_img_url"]
    if "alipay" in recharge_info["pay_url"]:
        pay_img_url = "https://pp.myapp.com/ma_icon/0/icon_5294_1671098444/256"
    else:
        pay_img_url = "https://pp.myapp.com/ma_icon/0/icon_10910_1670844838/256"
    pay_img = Image.open(BytesIO(requests.get(pay_img_url).content))
    pay_img = pay_img.convert("RGBA")
    pay_img = pay_img.resize((275, 275))
    img.paste(pay_img, (600, 120),pay_img)
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
    font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 50)
    # 写入文字
    draw.text(
        (10, 20),
        "商品:" + recharge_info["thing"].replace("for ", "For UID"),
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
        (40, 600),
        "订单号:",
        font=font,
        fill=(0, 0, 0),
    )
    
    draw.text(
        (120, 670),
        recharge_info["order_id"] ,
        font=font,
        fill=(0, 0, 0),
    )
    # img转base64
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    img_base64 = b64encode(img_byte_arr)
    return img_base64.decode()

# b64_img = img_create()


