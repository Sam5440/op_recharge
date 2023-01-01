import asyncio

from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.params import CommandArg

from .api_get import get_pay_url, loop_check
from .img import help_img_create, img_create

sv = on_command("op_recharge", aliases={"oprc","OP充值", "原充值"}, priority=5, block=True)
sv_help = on_command("op_recharge_help", aliases={"oprchelp", "oprc帮助"}, priority=5, block=True)



@sv.handle()
async def preference_update(arg: Message = CommandArg()):
    args = arg.extract_plain_text().strip().split()
    # if not check_priv(session.event, ADMIN):
    #     await session.send("只有管理员才可以充值哦")
    #     return

    try:
        item_id = int(args[0])
        uid = 0 if len(args) == 1 else int(args[1])
        pay_mode = 0 if len(args) < 3 else int(args[2])
    except Exception as e:
        print("[OPRC]", f"在接受充值参数时出现错误: {e}")
        await sv.send("请输入正确的参数,输入oprchelp查看帮助")
        return

    if item_id > 6:
        if uid in [0, 1]:
            pay_mode = uid
            uid = item_id
            item_id = 0
        else:
            await sv.send("请输入正确的参数,输入oprchelp查看帮助")
            return
    if (
        (9999_9999 < uid < 3_9999_9999)
        and (item_id in [0, 1, 2, 3, 4, 5, 6])
        and (pay_mode in [0, 1])
    ):
        # 参数校验成功
        pass
    else:
        await sv.send("请输入正确的参数,输入oprchelp查看帮助")
        return
    print("[OPRC]", f"请求物品ID{item_id}(UID{uid}),支付方式{pay_mode}的支付地址")
    try:
        result = await get_pay_url(uid, item_id, pay_mode)
    except Exception as e:
        print("[OPRC]", f"在请求时出现错误: {e}")
        await sv.send("请求失败,请查看后台输出")
        return
    print("[OPRC]", f"请求物品ID{item_id}(UID{uid}),支付方式{pay_mode}的支付地址成功")
    if result["code"] != 200:
        await sv.send("查询失败 code: " + str(result["code"]))
        return

    img_b64 = await img_create(result)
    await sv.send(MessageSegment.image(f"base64://{img_b64}") + MessageSegment.text("请在2分钟内完成操作"),at_sender=True)
    asyncio.create_task(loop_check(result, uid, sv))


@sv_help.handle()
async def oprc_help():
    help_info = """
[Load Success]
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
    await sv_help.send(MessageSegment.image(f"base64://{img_b64}"), at_sender=True)
