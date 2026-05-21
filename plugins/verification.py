import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from config import *

# Verification panel logic
async def verification_panel(client, query_or_message):
    expiry_time = await client.mongodb.get_global_verify_expiry() # Database se time lein
    verify_mode = getattr(client, 'verify_mode', True)
    
    mode_text = "✓ ᴇɴᴀʙʟᴇᴅ" if verify_mode else "✗ ᴅɪsᴀʙʟᴇᴅ"
    toggle_text = "✗ ᴏғғ" if verify_mode else "✓ ᴏɴ"
    
    msg = f"""<blockquote>✦ 𝗩𝗘𝗥𝗜𝗙𝗜𝗖𝗔𝗧𝗜𝗢𝗡 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦</blockquote>
**<u>ᴄᴜʀʀᴇɴᴛ ꜱᴇᴛᴛɪɴɢꜱ:</u>**
<blockquote>›› **ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴍᴏᴅᴇ:** {mode_text}
›› **ᴇxᴘɪʀʏ ᴛɪᴍᴇ:** `{expiry_time} ꜱᴇᴄᴏɴᴅꜱ`</blockquote> 

<blockquote>**≡ ᴜꜱᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴꜰɪɢᴜʀᴇ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ꜱᴇᴛᴛɪɴɢꜱ!**</blockquote>"""
    
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'• {toggle_text} ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ •', 'toggle_verify')],
        [InlineKeyboardButton('• ꜱᴇᴛ ᴇxᴘɪʀʏ ᴛɪᴍᴇ •', 'set_expiry_time')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ ᴛᴏ ꜱᴇᴛᴛɪɴɢꜱ', 'settings')]
    ])
    
    image_url = MESSAGES.get("SHORT", "https://telegra.ph/file/8aaf4df8c138c6685dcee-05d3b183d4978ec347.jpg")
    
    if hasattr(query_or_message, 'message'):
        await query_or_message.message.edit_media(media=InputMediaPhoto(media=image_url, caption=msg), reply_markup=reply_markup)
    else:
        await query_or_message.reply_photo(photo=image_url, caption=msg, reply_markup=reply_markup)

# Admin callback handlers
@Client.on_callback_query(filters.regex("^toggle_verify$"))
async def toggle_verify(client, query):
    new_status = not getattr(client, 'verify_mode', True)
    client.verify_mode = new_status
    await client.mongodb.update_shortner_setting('verify_mode', new_status) # DB mein save
    await query.answer(f"✓ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ {'ᴇɴᴀʙʟᴇᴅ' if new_status else 'ᴅɪsᴀʙʟᴇᴅ'}!")
    await verification_panel(client, query)

@Client.on_callback_query(filters.regex("^set_expiry_time$"))
async def set_expiry_time(client, query):
    await query.message.edit_text("**ꜱᴇɴᴅ ᴛʜᴇ ɴᴇᴡ ᴇxᴘɪʀʏ ᴛɪᴍᴇ ɪɴ ꜱᴇᴄᴏɴᴅꜱ (ᴇx: 3600):**")
    res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
    try:
        seconds = int(res.text)
        await client.mongodb.set_global_verify_expiry(seconds)
        await query.message.edit_text(f"✅ ᴇxᴘɪʀʏ ᴛɪᴍᴇ ꜱᴇᴛ ᴛᴏ {seconds} ꜱᴇᴄᴏɴᴅꜱ.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]]))
    except:
        await query.message.edit_text("❌ ɪɴᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ!")
