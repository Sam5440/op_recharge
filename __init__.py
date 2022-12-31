from .api_get import get_pay_url
from hoshino import Service
from hoshino.priv import check_priv, ADMIN

sv = Service("op_recharge")

@sv.on_command("op充值", aliases=("OP充值", "原充值"))
async def preference_update(session):
    args = session.current_arg_text.strip().split()
    try:
        item_id = int(args[0])
        uid = int(args[1])
    except:
        await session.send("请输入正确的参数")
        return
    
    if not check_priv(session.event, ADMIN):
        await session.send("只有管理员才可以充值哦")
        return

    result = get_pay_url(uid, item_id)
    
    if result['code'] != 200:
        await session.send("查询失败 code: " + str(result['code']))
        return
    result['thing'] = result['thing'].replace("thing:", "")
    await session.send(
        f"商品名称：{result['thing']}"
        f"[CQ:image,file={result['thing_img_url']}]\n"
        f"商品价格：{result['price']}\n"
        f"订单号：{result['order_id']}\n"
        f"[CQ:image,file=base64://{result['qrcode_b64']}]"
    )
