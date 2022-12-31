from .api_get import get_pay_url
from hoshino import Service
from hoshino.priv import check_priv, ADMIN
from .img import img_create
sv = Service("op_recharge")

@sv.on_command("op充值", aliases=("OP充值", "原充值"))
async def preference_update(session):
    args = session.current_arg_text.strip().split()
    print(args)
    try:
        item_id = int(args[0])
        uid = 0 if len(args)==1 else int(args[1])
        pay_mode = 0 if len(args)==1 else int(args[2])
    except Exception as e:
        print(e)
        await session.send("请输入正确的参数,如:op充值 商品id(0六元6月卡) uid 支付方式(0支付宝1微信)")
        return
    print(item_id, uid, pay_mode)
    if item_id > 6:
        if uid == 0:
            uid = item_id
            item_id = 0
        else:
            await session.send("请输入正确的参数,如:op充值 商品id(0六元6月卡) uid 支付方式(0支付宝1微信)")
            return
    if not check_priv(session.event, ADMIN):
        await session.send("只有管理员才可以充值哦")
        return

    result = get_pay_url(uid, item_id,pay_mode)
    
    if result['code'] != 200:
        await session.send("查询失败 code: " + str(result['code']))
        return
    # result['thing'] = result['thing'].replace("thing:", "")
    # pay_mode = "微信" if pay_mode == 1 else "支付宝"
    # await session.send(
    #     f"正在给UID:{uid}用{pay_mode}充值ID{item_id}\n"
    #     f"商品名称：{result['thing']}"
    #     f"[CQ:image,file={result['thing_img_url']}]\n"
    #     f"商品价格：{result['price']}\n"
    #     f"订单号：{result['order_id']}\n"
    #     f"[CQ:image,file=base64://{result['qrcode_b64']}]"
    # )
    img_b64 = img_create(result)
    # print(img_b64)
    # byte2str
    # img_b64 = img_b64.decode()
    await session.send( f"[CQ:image,file=base64://{img_b64}]")

