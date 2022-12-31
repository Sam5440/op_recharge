from .api_get import get_pay_url
from hoshino import Service
from hoshino.priv import check_priv, ADMIN
from .img import img_create

sv = Service("opc",enable_on_default=False,visible=False)


@sv.on_command("opc", aliases=("OP充值", "op充值"))
async def preference_update(session):
    args = session.current_arg_text.strip().split()
    print(args)
    try:
        item_id = int(args[0])
        uid = 0 if len(args) == 1 else int(args[1])
        pay_mode = 0 if len(args) < 3 else int(args[2])
    except Exception as e:
        print(e)
        await session.send("请输入正确的参数,如:opc 商品id uid 支付方式(0支付宝1微信)")
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

    result = get_pay_url(uid, item_id, pay_mode)

    if result["code"] != 200:
        await session.send("查询失败 code: " + str(result["code"]))
        return

    img_b64 = img_create(result)
    await session.send(f"[CQ:image,file=base64://{img_b64}]")
