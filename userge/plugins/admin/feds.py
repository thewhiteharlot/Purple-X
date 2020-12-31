"""Federations"""

# Noob code by @lostb053 <telegram> / Lostb053 <GitHub user>.
# Suggestions are welcomed as am not a python developer

import asyncio

from userge import Message, get_collection, userge


@userge.on_cmd(
    "addf",
    about={
        "header": "Add a chat to fed list",
        "description": "Add a chat to fed list where message is to be sent",
        "usage": "{tr}addfed",
    },
)
async def addf_(message: Message):
    await asyncio.gather(
        get_collection("fed_chats").insert_one(
            {
                "_id": str(message.chat.id),
                "name": str(message.chat.title),
            }
        ),
    )
    await message.edit("`Chat added to fed`", del_in=5)


@userge.on_cmd(
    "delf",
    about={
        "header": "Remove a chat from fed list",
        "description": "Remove a chat from fed list",
        "usage": "{tr}delfed",
    },
)
async def delf_(message: Message):
    await asyncio.gather(
        get_collection("fed_chats").delete_one({"_id": str(message.chat.id)}),
    )
    await message.edit("`Chat removed from fed`", del_in=5)


@userge.on_cmd(
    "fban",
    about={
        "header": "Fban user",
        "description": "Fban the user from the list of fed",
        "usage": "{tr}fban (username or reply to user or id)|reason",
    },
)
async def fban_(message: Message):
    replied = message.reply_to_message
    if replied:
        if not message.input_str:
            return await message.edit(
                "`Please specify a reason to fban user`", del_in=10
            )
        user_id = (
            replied.forward_from.id if replied.forward_from else replied.from_user.id
        )
        reason = message.input_str
    else:
        if "|" not in message.input_str:
            return await message.edit(
                "`Please specify a reason to fban user`", del_in=10
            )
        user_id, reason = message.input_str.split("-")
    try:
        user = await message.client.get_users(user_id)
    except Exception:
        await message.edit("I don't know that User...")
        return
    a = ""
    async for chat in get_collection("fed_chats").find():
        a += str(chat["_id"])
    b = str(a)
    c = b.split("-")
    c.remove("")
    ap = "-"
    fl = prepend(c, ap)
    for n, i in enumerate(fl):
        await userge.send_message(fl[n], f"/fban {user.id} {reason}")
    await message.edit(
        f"User [{user.first_name}](tg://user?id={user.id}) with id {user.id} Fbanned for reason:\n {reason}",
        del_in=5,
    )


@userge.on_cmd(
    "unfban",
    about={
        "header": "Unfban user",
        "description": "Unfban the user from the list of fed",
        "usage": "{tr}Unfban (username or reply to user or id)",
    },
)
async def unfban_(message: Message):
    user_id = message.input_str
    replied = message.reply_to_message
    if not user_id:
        user_id = (
            replied.forward_from.id if replied.forward_from else replied.from_user.id
        )
    try:
        user = await message.client.get_users(user_id)
    except Exception:
        await message.edit("I don't know that User...")
        return
    async for chat in get_collection("fed_chats").find():
        a += str(chat["_id"])
    b = str(a)
    c = b.split("-")
    c.remove("")
    ap = "-"
    fl = prepend(c, ap)
    for n, i in enumerate(fl):
        await userge.send_message(fl[n], f"/unfban {user.id}")
    await message.edit(
        f"User [{user.first_name}](tg://user?id={user.id}) with id {user.id} Unfbanned",
        del_in=5,
    )


@userge.on_cmd(
    "feds",
    about={
        "header": "Fed Chat List",
        "description": "Get a list of chats added in fed",
        "usage": "{tr}feds",
    },
)
async def fban_lst_(message: Message):
    out_str = "🚷 **FED CHATS** 🚷\n\n"
    async for chat in get_collection("fed_chats").find():
        out_str += f" {chat['name']} 🆔 `{chat['_id']}`\n"
    await message.edit(out_str)


def prepend(list, str):
    str += "{0}"
    list = [str.format(i) for i in list]
    return list
