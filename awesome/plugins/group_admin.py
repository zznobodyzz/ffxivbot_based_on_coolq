from nonebot import on_notice, NoticeSession

__plugin_name__ = 'group_admin(群消息)'

# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def _(session: NoticeSession):
    # 发送欢迎消息
    await session.send('欢迎新大佬~~~')
    await session.send('麻烦将群名片修改成游戏内昵称哟~')
    return