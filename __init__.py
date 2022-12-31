import asyncio

from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg

from .api_get import get_pay_url, loop_check
from .img import img_create

sv = on_command("op_recharge", aliases={"OP充值", "原充值"}, priority=5, block=True)


@sv.handle()
async def preference_update(arg: Message = CommandArg()):
    args = arg.extract_plain_text().strip().split()
    logger.info(args)
    try:
        item_id = int(args[0])
        uid = 0 if len(args) == 1 else int(args[1])
        pay_mode = 0 if len(args) < 3 else int(args[2])
    except Exception as e:
        logger.error(e)
        await sv.finish("请输入正确的参数,如:op充值 商品id uid 支付方式(0支付宝1微信)")
    logger.info(f"item_id:{item_id},uid:{uid},pay_mode:{pay_mode}")
    if item_id > 6:
        if uid == 0:
            uid = item_id
            item_id = 0
        else:
            await sv.finish("请输入正确的参数,如:op充值 商品id(0六元6月卡) uid 支付方式(0支付宝1微信)")
    # if not SUPERUSER:
    #     await sv.finish("只有管理员才可以充值哦")

    result = await get_pay_url(uid, item_id, pay_mode)

    if result['code'] != 200:
        await sv.finish("查询失败 code: " + str(result['code']))

    img_b64 = await img_create(result)
    await sv.send(f"[CQ:image,file=base64://{img_b64}]请在2分钟内完成操作", at_sender=True)
    # loop.create_task  创建loop_check任务
    asyncio.create_task(loop_check(result, uid, sv))
