"""AFK Plugin for @FridayOT
Syntax: .afk REASON"""
import asyncio
import datetime
from datetime import datetime

from telethon import events
from telethon.tl import functions, types

from fridaybot import CMD_HELP, lang

global USER_AFK  # pylint:disable=E0602
global afk_time  # pylint:disable=E0602
global last_afk_message  # pylint:disable=E0602
global afk_start
global afk_end
USER_AFK = {}
afk_time = None
last_afk_message = {}
afk_start = {}

if lang == "si":

    @friday.on(
        events.NewMessage(pattern=r"\.afk ?(.*)", outgoing=True)
    )  # pylint:disable=E0602
    async def _(event):
        if event.fwd_from:
            return
        global USER_AFK  # pylint:disable=E0602
        global afk_time  # pylint:disable=E0602
        global last_afk_message  # pylint:disable=E0602
        global afk_start
        global afk_end
        global reason
        USER_AFK = {}
        afk_time = None
        last_afk_message = {}
        afk_end = {}
        start_1 = datetime.now()
        afk_start = start_1.replace(microsecond=0)
        reason = event.pattern_match.group(1)
        if not USER_AFK:  # pylint:disable=E0602
            last_seen_status = await borg(  # pylint:disable=E0602
                functions.account.GetPrivacyRequest(
                    types.InputPrivacyKeyStatusTimestamp()
                )
            )
            if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
                afk_time = datetime.datetime.now()  # pylint:disable=E0602
            USER_AFK = f"yes: {reason}"  # pylint:disable=E0602
            if reason:
                await borg.send_message(
                    event.chat_id,
                    f"**මම දැන් Offline යනවා 👀.** \n__Offline යන්න හේතුව__ `{reason}`",
                )
            else:
                await borg.send_message(
                    event.chat_id, f"**මම දැන් Busy ඒක නිසා Offline යනවා**."
                )
            await asyncio.sleep(5)
            await event.delete()
            try:
                await borg.send_message(  # pylint:disable=E0602
                    Config.PRIVATE_GROUP_ID,  # pylint:disable=E0602
                    f"#AfkLogger Afk Is Active And Reason is {reason}",
                )
            except Exception as e:  # pylint:disable=C0103,W0703
                logger.warn(str(e))  # pylint:disable=E0602

    @friday.on(events.NewMessage(outgoing=True))  # pylint:disable=E0602
    async def set_not_afk(event):
        global USER_AFK  # pylint:disable=E0602
        global afk_time  # pylint:disable=E0602
        global last_afk_message  # pylint:disable=E0602
        global afk_start
        global afk_end
        back_alive = datetime.now()
        afk_end = back_alive.replace(microsecond=0)
        if afk_start != {}:
            total_afk_time = str((afk_end - afk_start))
        current_message = event.message.message
        if ".afk" not in current_message and "yes" in USER_AFK:  # pylint:disable=E0602
            shite = await borg.send_message(
                event.chat_id,
                "__Pro is Back Alive__\n**තව දුරටත් Offline නෙමෙයි.**\n `මම Offline හිටිය කාලය :``"
                + total_afk_time
                + "`",
            )
            try:
                await borg.send_message(  # pylint:disable=E0602
                    Config.PRIVATE_GROUP_ID,  # pylint:disable=E0602
                    "#AfkLogger User is Back Alive ! No Longer Afk ",
                )
            except Exception as e:  # pylint:disable=C0103,W0703
                await borg.send_message(  # pylint:disable=E0602
                    event.chat_id,
                    "Please set `PRIVATE_GROUP_ID` "
                    + "for the proper functioning of afk functionality "
                    + "Please Seek Support in @FridayOT\n\n `{}`".format(str(e)),
                    reply_to=event.message.id,
                    silent=True,
                )
            await asyncio.sleep(5)
            await shite.delete()
            USER_AFK = {}  # pylint:disable=E0602
            afk_time = None  # pylint:disable=E0602

    @friday.on(
        events.NewMessage(  # pylint:disable=E0602
            incoming=True, func=lambda e: bool(e.mentioned or e.is_private)
        )
    )
    async def on_afk(event):
        if event.fwd_from:
            return
        global USER_AFK  # pylint:disable=E0602
        global afk_time  # pylint:disable=E0602
        global last_afk_message  # pylint:disable=E0602
        global afk_start
        global afk_end
        back_alivee = datetime.now()
        afk_end = back_alivee.replace(microsecond=0)
        if afk_start != {}:
            total_afk_time = str((afk_end - afk_start))
        afk_since = "**a while ago**"
        current_message_text = event.message.message.lower()
        if "afk" in current_message_text:
            # fridaybot's should not reply to other fridaybot's
            # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
            return False
        if USER_AFK and not (await event.get_sender()).bot:  # pylint:disable=E0602
            if afk_time:  # pylint:disable=E0602
                now = datetime.datetime.now()
                datime_since_afk = now - afk_time  # pylint:disable=E0602
                time = float(datime_since_afk.seconds)
                days = time // (24 * 3600)
                time = time % (24 * 3600)
                hours = time // 3600
                time %= 3600
                minutes = time // 60
                time %= 60
                seconds = time
                if days == 1:
                    afk_since = "**Yesterday**"
                elif days > 1:
                    if days > 6:
                        date = now + datetime.timedelta(
                            days=-days, hours=-hours, minutes=-minutes
                        )
                        afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                    else:
                        wday = now + datetime.timedelta(days=-days)
                        wday.strftime("%A")
                elif hours > 1:
                    f"`{int(hours)}h{int(minutes)}m` **ago**"
                elif minutes > 0:
                    f"`{int(minutes)}m{int(seconds)}s` **ago**"
                else:
                    f"`{int(seconds)}s` **ago**"
            msg = None
            message_to_reply = (
                f"**මම දැන් පොඩ්ඩක් Busy.. ඒක නිසා ටිකකට ඔන්ලයින් නෑ**  \n**ඕෆ්ලයින් ගිය කාලය** : `{total_afk_time}`\n**හේතුව** : `{reason}`"
                + f"\n\nමම ඉක්මනටම ආපහු එන්නම්!"
                if reason
                else f"**මම දැන් ඕෆ්ලයින්**\n ඕෆ්ලයින් ගිය කාලය : `{total_afk_time}` \n මම ඉක්මනටම ආපහු එන්නම්"
            )
            msg = await event.reply(message_to_reply)
            await asyncio.sleep(5)
            if event.chat_id in last_afk_message:  # pylint:disable=E0602
                await last_afk_message[event.chat_id].delete()  # pylint:disable=E0602
            last_afk_message[event.chat_id] = msg  # pylint:disable=E0602


else:

    @friday.on(
        events.NewMessage(pattern=r"\.afk ?(.*)", outgoing=True)
    )  # pylint:disable=E0602
    async def _(event):
        if event.fwd_from:
            return
        global USER_AFK  # pylint:disable=E0602
        global afk_time  # pylint:disable=E0602
        global last_afk_message  # pylint:disable=E0602
        global afk_start
        global afk_end
        global reason
        USER_AFK = {}
        afk_time = None
        last_afk_message = {}
        afk_end = {}
        start_1 = datetime.now()
        afk_start = start_1.replace(microsecond=0)
        reason = event.pattern_match.group(1)
        if not USER_AFK:  # pylint:disable=E0602
            last_seen_status = await borg(  # pylint:disable=E0602
                functions.account.GetPrivacyRequest(
                    types.InputPrivacyKeyStatusTimestamp()
                )
            )
            if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
                afk_time = datetime.datetime.now()  # pylint:disable=E0602
            USER_AFK = f"yes: {reason}"  # pylint:disable=E0602
            if reason:
                await borg.send_message(
                    event.chat_id,
                    f"**My Master Seems To Be Too Busy 👀.** \n__He Going Afk Because Of__ `{reason}`",
                )
            else:
                await borg.send_message(
                    event.chat_id, f"**I Am Busy And I Am Going Afk**."
                )
            await asyncio.sleep(5)
            await event.delete()
            try:
                await borg.send_message(  # pylint:disable=E0602
                    Config.PRIVATE_GROUP_ID,  # pylint:disable=E0602
                    f"#AfkLogger Afk Is Active And Reason is {reason}",
                )
            except Exception as e:  # pylint:disable=C0103,W0703
                logger.warn(str(e))  # pylint:disable=E0602

    @friday.on(events.NewMessage(outgoing=True))  # pylint:disable=E0602
    async def set_not_afk(event):
        global USER_AFK  # pylint:disable=E0602
        global afk_time  # pylint:disable=E0602
        global last_afk_message  # pylint:disable=E0602
        global afk_start
        global afk_end
        back_alive = datetime.now()
        afk_end = back_alive.replace(microsecond=0)
        if afk_start != {}:
            total_afk_time = str((afk_end - afk_start))
        current_message = event.message.message
        if ".afk" not in current_message and "yes" in USER_AFK:  # pylint:disable=E0602
            shite = await borg.send_message(
                event.chat_id,
                "__Pro is Back Alive__\n**No Longer afk.**\n `I Was afk for:``"
                + total_afk_time
                + "`",
            )
            try:
                await borg.send_message(  # pylint:disable=E0602
                    Config.PRIVATE_GROUP_ID,  # pylint:disable=E0602
                    "#AfkLogger User is Back Alive ! No Longer Afk ",
                )
            except Exception as e:  # pylint:disable=C0103,W0703
                await borg.send_message(  # pylint:disable=E0602
                    event.chat_id,
                    "Please set `PRIVATE_GROUP_ID` "
                    + "for the proper functioning of afk functionality "
                    + "Please Seek Support in @FridayOT\n\n `{}`".format(str(e)),
                    reply_to=event.message.id,
                    silent=True,
                )
            await asyncio.sleep(5)
            await shite.delete()
            USER_AFK = {}  # pylint:disable=E0602
            afk_time = None  # pylint:disable=E0602

    @friday.on(
        events.NewMessage(  # pylint:disable=E0602
            incoming=True, func=lambda e: bool(e.mentioned or e.is_private)
        )
    )
    async def on_afk(event):
        if event.fwd_from:
            return
        global USER_AFK  # pylint:disable=E0602
        global afk_time  # pylint:disable=E0602
        global last_afk_message  # pylint:disable=E0602
        global afk_start
        global afk_end
        back_alivee = datetime.now()
        afk_end = back_alivee.replace(microsecond=0)
        if afk_start != {}:
            total_afk_time = str((afk_end - afk_start))
        afk_since = "**a while ago**"
        current_message_text = event.message.message.lower()
        if "afk" in current_message_text:
            # fridaybot's should not reply to other fridaybot's
            # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
            return False
        if USER_AFK and not (await event.get_sender()).bot:  # pylint:disable=E0602
            if afk_time:  # pylint:disable=E0602
                now = datetime.datetime.now()
                datime_since_afk = now - afk_time  # pylint:disable=E0602
                time = float(datime_since_afk.seconds)
                days = time // (24 * 3600)
                time = time % (24 * 3600)
                hours = time // 3600
                time %= 3600
                minutes = time // 60
                time %= 60
                seconds = time
                if days == 1:
                    afk_since = "**Yesterday**"
                elif days > 1:
                    if days > 6:
                        date = now + datetime.timedelta(
                            days=-days, hours=-hours, minutes=-minutes
                        )
                        afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                    else:
                        wday = now + datetime.timedelta(days=-days)
                        wday.strftime("%A")
                elif hours > 1:
                    f"`{int(hours)}h{int(minutes)}m` **ago**"
                elif minutes > 0:
                    f"`{int(minutes)}m{int(seconds)}s` **ago**"
                else:
                    f"`{int(seconds)}s` **ago**"
            msg = None
            message_to_reply = (
                f"**My Boss is Afk**  \n**AFKT** : `{total_afk_time}`\n**Reason** : `{reason}`"
                + f"\n\nHe Will Reply To You Soon!"
                if reason
                else f"**My Master is Afk**\n AFK : `{total_afk_time}` He Will Comeback Soon"
            )
            msg = await event.reply(message_to_reply)
            await asyncio.sleep(5)
            if event.chat_id in last_afk_message:  # pylint:disable=E0602
                await last_afk_message[event.chat_id].delete()  # pylint:disable=E0602
            last_afk_message[event.chat_id] = msg  # pylint:disable=E0602


CMD_HELP.update(
    {
        "afk": ".afk <Reason> \
\nUsage: Gets You Afk"
    }
)
