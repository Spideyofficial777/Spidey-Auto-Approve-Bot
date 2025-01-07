import asyncio
import logging
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, UserNotParticipant
from bgremove import RemoveBG
from database import add_user, add_group, all_users, all_groups, users, remove_user

# Configuration
API_ID = ""
API_HASH = ""
BOT_TOKEN = ""
CHANNEL_ID = # Replace with your channel ID
SUDO_USERS = []  # Replace with your admin user ID(s)
MONGO_URI = ""
# Image URLs
welcome_image_url = "https://i.ibb.co/CPxdkHR/IMG-20240818-192201-633.jpg"
background_image_url = "https://i.ibb.co/RymDMxS/66e7d1b6.jpg"

# Initialize the bot
app = Client(
    "approver_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Approve join requests and send a welcome message
@app.on_chat_join_request(filters.group | filters.channel)
async def approve_join_request(_, message):
    try:
        # Approve join request
        await app.approve_chat_join_request(message.chat.id, message.from_user.id)

        # Get the chat (channel/group) details for dynamic name
        chat = await app.get_chat(message.chat.id)
        channel_name = chat.title if chat.title else "our channel"

        # Send welcome message
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🔔 Sᴜʙsᴄʀɪʙᴇ ᴛᴏ Oᴜʀ Cʜᴀɴɴᴇʟ", url="https://youtube.com/@spidey_official_777")],
                [InlineKeyboardButton("💬 Cᴏɴᴛᴀᴄᴛ Sᴜᴘᴘᴏʀᴛ", url="https://t.me/hacker_x_official_777")]
            ]
        )
        await app.send_photo(
            message.from_user.id,
            background_image_url,
            caption=(
                f"<b>Wᴇʟᴄᴏᴍᴇ {message.from_user.mention}\n"
                f"ᴛᴏ {channel_name}</b>"
            ),
            reply_markup=keyboard
        )
    except Exception as err:
        print(f"Error approving join request: {str(err)}")

# Start command handler


@app.on_message(filters.command("start"))
async def start(_, message):
    try:
        # Check if the user is a member of the required channel
        await app.get_chat_member(CHANNEL_ID, message.from_user.id)

        if message.chat.type == enums.ChatType.PRIVATE:
            # Step 1: Send animated "Hello Baby" message
            m = await message.reply_text("ʜᴇʟʟᴏ ʙᴀʙʏ, ʜᴏᴡ ᴀʀᴇ ʏᴏᴜ \nᴡᴀɪᴛ ᴀ ᴍᴏᴍᴇɴᴛ ʙᴀʙʏ . . .")
            await asyncio.sleep(0.4)
            await m.edit_text("🎊")
            await asyncio.sleep(0.5)
            await m.edit_text("⚡")
            await asyncio.sleep(0.5)
            await m.edit_text("ꜱᴛᴀʀᴛɪɴɢ ʙᴀʙʏ...")
            await asyncio.sleep(0.4)
            await m.delete()

            # Step 2: Send a sticker and delete after 1 second
            m = await message.reply_sticker("CAACAgUAAxkBAAECroBmQKMAAQ-Gw4nibWoj_pJou2vP1a4AAlQIAAIzDxlVkNBkTEb1Lc4eBA")
            await asyncio.sleep(1)
            await m.delete()

            # Step 3: Send the final welcome message
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("➕ Aᴅᴅ Mᴇ ᴛᴏ Yᴏᴜʀ Cʜᴀɴɴᴇʟ ➕", url="https://t.me/SPIDER_MAN_GAMING_bot?startchannel=Bots4Sale&admin=invite_users+manage_chat")],
                    [
                        InlineKeyboardButton("🚀 Cʜᴀɴɴᴇʟ", url="https://t.me/+cMlrPqMjUwtmNTI1"),
                        InlineKeyboardButton("💬 Sᴜᴘᴘᴏʀᴛ", url="https://t.me/SPIDEYOFFICIAL777")
                    ],
                    [InlineKeyboardButton("➕ Aᴅᴅ Mᴇ ᴛᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ➕", url="https://t.me/SPIDER_MAN_GAMING_bot?startgroup=true")]
                ]
            )
            await message.reply_photo(
                welcome_image_url,
                caption=(
                    f"<b>🦊 Hᴇʟʟᴏ {message.from_user.mention}!\n\n"
                    "I'ᴍ ᴀɴ ᴀᴜᴛᴏ-ᴀᴘᴘʀᴏᴠᴇ [ᴀᴅᴍɪɴ](https://t.me/hacker_x_official_777) [Jᴏɪɴ Rᴇǫᴜᴇsᴛs](https://t.me/telegram/153) ʙᴏᴛ.\n"
                    "I ᴄᴀɴ ᴀᴘᴘʀᴏᴠᴇ ᴜsᴇʀs ɪɴ Gʀᴏᴜᴘs/Cʜᴀɴɴᴇʟs. Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ ᴀɴᴅ [ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴛᴏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴀᴅᴅ ᴍᴇᴍʙᴇʀs Pᴇʀᴍɪssɪᴏɴ]()\n\n"
                    "__ᴘᴏᴡᴇʀᴇᴅ ʙʏ: [@Hᴀᴄᴋᴇʀ_x_ᴏғғɪᴄɪᴀʟ_𝟽𝟽𝟽](https://t.me/hacker_x_official_777)__</b>"
                ),
                reply_markup=keyboard
            )

        elif message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
    # Step 1: Send Group Message
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🕵️  Sᴛᴀʀᴛ Mᴇ ɪɴ Pʀɪᴠᴀᴛᴇ 🕵️", url="https://t.me/SPIDER_MAN_GAMING_bot")]]
    )
    await message.reply_text(
        f"<b>👋 Hᴇʟʟᴏ {message.from_user.first_name}!\nWʀɪᴛᴇ ᴍᴇ ᴘʀɪᴠᴀᴛᴇʟʏ ғᴏʀ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟs.</b>",
        reply_markup=keyboard
    )


    except UserNotParticipant:
        # Handle cases where the user is not a member of the required channel
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🚀 Jᴏɪɴ Oᴜʀ Cʜᴀɴɴᴇʟ", url="https://t.me/+cMlrPqMjUwtmNTI1")],
                [InlineKeyboardButton("🔄 Cʜᴇᴄᴋ Aɢᴀɪɴ 🔄", callback_data="chk")]
            ]
        )
        await message.reply_text(
            f"<b>⚠️ Aᴄᴄᴇss Dᴇɴɪᴇᴅ! ⚠️\n\n🔥Hᴇʟʟᴏ {message.from_user.mention}!\n\n"
            " Jᴏɪɴ ᴛʜᴇ ᴏғғɪᴄɪᴀʟ Sᴘɪᴅᴇʏ Nᴇᴛᴡᴏʀᴋ! 🔥\n"
            "🌟 Uɴʟᴏᴄᴋ ᴇxᴄʟᴜsɪᴠᴇ ᴄᴏɴᴛᴇɴᴛ ᴀɴᴅ ᴅɪᴠᴇ ɪɴᴛᴏ ᴛʜᴇ ᴡᴏʀʟᴅ ᴏғ ʜᴇʀᴏᴇs!\n\n"
            "👉 [✨ Sᴘɪᴅᴇʏ Oғғɪᴄɪᴀʟ ✨](https://t.me/SPIDEYOFFICIAL777)</b>",
            reply_markup=keyboard
        )


        elif message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
    # Step 1: Send Group Message
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🕵️  Sᴛᴀʀᴛ Mᴇ ɪɴ Pʀɪᴠᴀᴛᴇ 🕵️", url="https://t.me/SPIDER_MAN_GAMING_bot")]]
    )
    await message.reply_text(
        f"<b>👋 Hᴇʟʟᴏ {message.from_user.first_name}!\nWʀɪᴛᴇ ᴍᴇ ᴘʀɪᴠᴀᴛᴇʟʏ ғᴏʀ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟs.</b>",
        reply_markup=keyboard
    )



    except UserNotParticipant:
        # Handle cases where the user is not a member of the required channel
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🚀 Jᴏɪɴ Oᴜʀ Cʜᴀɴɴᴇʟ", url="https://t.me/+cMlrPqMjUwtmNTI1")],
                [InlineKeyboardButton("🔄 Cʜᴇᴄᴋ Aɢᴀɪɴ 🔄", callback_data="chk")]
            ]
        )
        await message.reply_text(
            f"<b>⚠️ Aᴄᴄᴇss Dᴇɴɪᴇᴅ! ⚠️\n\n🔥Hᴇʟʟᴏ {message.from_user.mention}!\n\n"
                   " Jᴏɪɴ ᴛʜᴇ ᴏғғɪᴄɪᴀʟ Sᴘɪᴅᴇʏ Nᴇᴛᴡᴏʀᴋ! 🔥\n"
            "🌟 Uɴʟᴏᴄᴋ ᴇxᴄʟᴜsɪᴠᴇ ᴄᴏɴᴛᴇɴᴛ ᴀɴᴅ ᴅɪᴠᴇ ɪɴᴛᴏ ᴛʜᴇ ᴡᴏʀʟᴅ ᴏғ ʜᴇʀᴏᴇs!\n\n"
            "👉 [✨ Sᴘɪᴅᴇʏ Oғғɪᴄɪᴀʟ ✨](https://t.me/SPIDEYOFFICIAL777)</b>",
            reply_markup=keyboard
        )


@app.on_callback_query(filters.regex("chk"))
async def check_subscription(_, callback_query):
    try:
        # Check if the user has joined the required channel
        await app.get_chat_member(CHANNEL_ID, callback_query.from_user.id)

        # User is subscribed, send the final welcome message
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("➕ Aᴅᴅ Mᴇ ᴛᴏ Yᴏᴜʀ Cʜᴀɴɴᴇʟ ➕", url="https://t.me/SPIDER_MAN_GAMING_bot?startchannel=Bots4Sale&admin=invite_users+manage_chat")],
                [
                    InlineKeyboardButton("🚀 Cʜᴀɴɴᴇʟ", url="https://t.me/+cMlrPqMjUwtmNTI1"),
                    InlineKeyboardButton("💬 Sᴜᴘᴘᴏʀᴛ", url="https://t.me/SPIDEYOFFICIAL777")
                ],
                [InlineKeyboardButton("➕ Aᴅᴅ Mᴇ ᴛᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ➕", url="https://t.me/SPIDER_MAN_GAMING_bot?startgroup=true")]
            ]
        )

        await callback_query.message.edit_text(
            f"<b>🦊 Hᴇʟʟᴏ {callback_query.from_user.mention}!\n\n"
            "I'ᴍ ᴀɴ ᴀᴜᴛᴏ-ᴀᴘᴘʀᴏᴠᴇ [ᴀᴅᴍɪɴ](https:t.me/Hacker_X_official_777) [Jᴏɪɴ Rᴇǫᴜᴇsᴛs](https://t.me/telegram/153) ʙᴏᴛ.\n"
            "I ᴄᴀɴ ᴀᴘᴘʀᴏᴠᴇ ᴜsᴇʀs ɪɴ Gʀᴏᴜᴘs/Cʜᴀɴɴᴇʟs. Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ ᴀɴᴅ [ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴛᴏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴀᴅᴅ ᴍᴇᴍʙᴇʀs Pᴇʀᴍɪssɪᴏɴ]\n\n"
            "__ᴘᴏᴡᴇʀᴇᴅ ʙʏ: [@Hᴀᴄᴋᴇʀ_x_ᴏғғɪᴄɪᴀʟ_𝟽𝟽𝟽](https://t.me/hacker_x_official_777)__</b>",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )

    except UserNotParticipant:
        # User is not subscribed, ask them to join the channel again
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🚀 Jᴏɪɴ Oᴜʀ Cʜᴀɴɴᴇʟ", url="https://t.me/+cMlrPqMjUwtmNTI1")],
                [InlineKeyboardButton("🔄 Cʜᴇᴄᴋ Aɢᴀɪɴ 🔄", callback_data="chk")]
            ]
        )
        await callback_query.answer(
            "🙅 Yᴏᴜ ᴀʀᴇ ɴᴏᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ. Pʟᴇᴀsᴇ ᴊᴏɪɴ ᴀɴᴅ ᴄʟɪᴄᴋ 'Cʜᴇᴄᴋ Aɢᴀɪɴ' ᴛᴏ ᴄᴏɴғɪʀᴍ.", show_alert=True
        )
        await callback_query.message.edit_text(
            f"<b>⚠️ Aᴄᴄᴇss Dᴇɴɪᴇᴅ! ⚠️\n\n🔥Hᴇʟʟᴏ {callback_query.from_user.mention}!\n\n"
            " Jᴏɪɴ ᴛʜᴇ ᴏғғɪᴄɪᴀʟ Sᴘɪᴅᴇʏ Nᴇᴛᴡᴏʀᴋ! 🔥\n"
            "🌟 Uɴʟᴏᴄᴋ ᴇxᴄʟᴜsɪᴠᴇ ᴄᴏɴᴛᴇɴᴛ ᴀɴᴅ ᴅɪᴠᴇ ɪɴᴛᴏ ᴛʜᴇ ᴡᴏʀʟᴅ ᴏғ ʜᴇʀᴏᴇs!\n\n"
            "👉 [✨ Sᴘɪᴅᴇʏ Oғғɪᴄɪᴀʟ ✨](https://t.me/SPIDEYOFFICIAL777)</b>",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )

        
@app.on_message(filters.command("users") & filters.user(SUDO_USERS))
async def dbtool(_, m: Message):
    """Displays total stats for users and groups."""
    total_users = all_users()
    total_groups = all_groups()
    total = total_users + total_groups
    await m.reply_text(f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{total_users}`
👥 Groups : `{total_groups}`
🚧 Total users & groups : `{total}`
""")

@app.on_message(filters.command("user") & filters.user(SUDO_USERS))
async def list_users(_, m: Message):
    """Lists all users in the bot database with an enhanced layout."""
    user_list = users.find()  # Assuming `users` is your database collection
    user_info = []

    for user in user_list:
        user_id = user.get("user_id")
        user_name = user.get("user_name", "No Name")  # Fallback for missing names
        user_info.append(f"👤 **Name**: `{user_name}`\n🆔 **ID**: `{user_id}`\n")

    if not user_info:
        await m.reply_text("🚫 **No users found in the database.**")
        return

    # Add separators between users
    formatted_user_info = "\n──────────────\n".join(user_info)

    # Paginate if the list is too long for a single message
    if len(formatted_user_info) > 4000:
        chunks = [formatted_user_info[i:i + 4000] for i in range(0, len(formatted_user_info), 4000)]
        for chunk in chunks:
            await m.reply_text(f"👥 **User List:**\n\n{chunk}")
    else:
        await m.reply_text(f"👥 **User List:**\n\n{formatted_user_info}")



# Broadcast command
@app.on_message(filters.command("bcast") & filters.user(SUDO_USERS))
async def bcast(_, m: Message):
    allusers = users  # Database call or list of users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():  # Make sure `allusers.find()` is correct based on your DB
        try:
            userid = usrs["user_id"]
            await m.reply_to_message.copy(int(userid))
            success += 1
        except UserIsBlocked:
            blocked += 1
        except InputUserDeactivated:
            deactivated += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            failed += 1

    await lel.edit(
        f"`✅  Sᴇɴᴛ Tᴏ {success} ᴜsᴇʀs\n❌ Bʟᴏᴄᴋᴇᴅ: {blocked}\n"
        f"❌ Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ: {deactivated}\n❌ Fᴀɪʟᴇᴅ: {failed}`"
    )
    
@app.on_message(filters.command("fcast") & filters.user(SUDO_USERS))
async def fcast(_, m: Message):
    if not m.reply_to_message:
        return await m.reply_text("Please reply to a message to broadcast.")

    allusers = users  # Assuming 'users' is a database object
    lel = await m.reply_text("`⚡️ Processing...`")

    success = 0
    failed = 0
    deactivated = 0
    blocked = 0

    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            # Forward message to each user
            await m.reply_to_message.forward(int(userid))
            success += 1
            await asyncio.sleep(0.5)  # Small delay to avoid API limits

        except FloodWait as ex:
            logging.warning(f"FloodWait triggered. Sleeping for {ex.value} seconds.")
            await asyncio.sleep(ex.value)
            await m.reply_to_message.forward(int(userid))
        except InputUserDeactivated:
            logging.warning(f"User {userid} is deactivated.")
            deactivated += 1
            remove_user(userid)  # Assuming remove_user removes the user from the database
        except UserIsBlocked:
            logging.warning(f"User {userid} has blocked the bot.")
            blocked += 1
        except Exception as e:
            logging.error(f"Error occurred for user {userid}: {e}")
            failed += 1

    await lel.edit(
        f"✅ Successfully sent to `{success}` users.\n"
        f"❌ Failed to `{failed}` users.\n"
        f"👾 Found `{blocked}` blocked users.\n"
        f"👻 Found `{deactivated}` deactivated users."
    )
    


print("""
  ____  ____ ___ ____  _______   __
 / ___||  _ \_ _|  _ \| ____\ \ / /
 \___ \| |_) | || | | |  _|  \ V / 
  ___) |  __/| || |_| | |___  | |  
 |____/|_|  |___|____/|_____| |_|  
""")


app.run()
