import asyncio
from .api_get import get_pay_url, loop_check
from hoshino import Service
from hoshino.priv import check_priv, ADMIN
from .img import help_img_create, img_create

sv = Service("op_recharge")


@sv.on_command("oprc", aliases=("OP充值", "op充值"))
async def oprc(session):
    args = session.current_arg_text.strip().split()
    print(args)
    try:
        item_id = int(args[0])
        uid = 0 if len(args) == 1 else int(args[1])
        pay_mode = 0 if len(args) < 3 else int(args[2])
    except Exception as e:
        print(e)
        await session.send("请输入正确的参数,如:oprc 商品id uid 支付方式(0or1)")
        return
    print(item_id, uid, pay_mode)
    if item_id > 6:
        if uid == 0:
            uid = item_id
            item_id = 0
        else:
            await session.send("请输入正确的参数,如:op充值 商品id(0六元6月卡) uid 支付方式(0支付宝1微信)")
            return
        
    # if not check_priv(session.event, ADMIN):
    #     await session.send("只有管理员才可以充值哦")
    #     return

    result = await get_pay_url(uid, item_id, pay_mode)

    if result["code"] != 200:
        await session.send("查询失败 code: " + str(result["code"]))
        return

    img_b64 = await img_create(result)
    await session.send(f"[CQ:image,file=base64://{img_b64}]请在2分钟内完成操作",at_sender = True)
    # loop.create_task  创建loop_check任务
    asyncio.create_task(loop_check(result, uid, session))

@sv.on_command("oprc帮助", aliases=("oprchelp", "oprcshop"))
async def oprc_help(session):
    help_info = """
oprc help
/oprc item_id uid pay_mode
arg list:
[item_id(0),uid,pay_mode(0)] 
num in () is default.
pay_mode:
0->ali 1->wx
item_id:
0->60 1->300...
but 6->30day card
    """.strip()
    img_b64 = await help_img_create(help_info)
    await session.send(f"[CQ:image,file=base64://{img_b64}]",at_sender = True)
