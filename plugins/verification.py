from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from config import *



# Main Panel function (Jo button click par call hoga)
@Client.on_callback_query(filters.regex("^verification_menu$"))
async def verification_panel(client, query):
    expiry_time = await client.mongodb.get_global_verify_expiry()
    verify_mode = getattr(client, 'verify_mode', True)
    
    mode_text = "✓ ᴇɴᴀʙʟᴇᴅ" if verify_mode else "✗ ᴅɪsᴀʙʟᴇᴅ"
    toggle_text = "✗ ᴛᴏɢɢʟᴇ ᴏꜰꜰ" if verify_mode else "✓ ᴛᴏɢɢʟᴇ ᴏɴ"
    
    msg = f"""<blockquote>✦ 𝗩𝗘𝗥𝗜𝗙𝗜𝗖𝗔𝗧𝗜𝗢𝗡 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦</blockquote>
<blockquote>›› **ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴍᴏᴅᴇ:** {mode_text}
›› **ᴇxᴘɪʀʏ ᴛɪᴍᴇ:** `{expiry_time} ꜱᴇᴄᴏɴᴅꜱ`</blockquote>"""
    
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'• {toggle_text} •', 'toggle_verify')],
        [InlineKeyboardButton('• ꜱᴇᴛ ᴇxᴘɪʀʏ ᴛɪᴍᴇ •', 'set_expiry_time')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ ᴛᴏ ꜱᴇᴛᴛɪɴɢꜱ', 'settings')]
    ])
    
    await query.message.edit_text(msg, reply_markup=reply_markup)

# Logic handlers
@Client.on_callback_query(filters.regex("^toggle_verify$"))
async def toggle_verify(client, query):
    new_status = not getattr(client, 'verify_mode', True)
    client.verify_mode = new_status
    # Database mein update
    await client.mongodb.update_shortner_setting('verify_mode', new_status)
    await verification_panel(client, query)

@Client.on_callback_query(filters.regex("^set_expiry_time$"))
async def set_expiry_time(client, query):
    await query.message.edit_text("**ꜱᴇɴᴅ ᴛʜᴇ ɴᴇᴡ ᴇxᴘɪʀʏ ᴛɪᴍᴇ ɪɴ ꜱᴇᴄᴏɴᴅꜱ:**")
    res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
    try:
        seconds = int(res.text)
        await client.mongodb.set_global_verify_expiry(seconds)
        await verification_panel(client, query)
    except:
        await query.message.edit_text("❌ ɪɴᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'verification_menu')]]))
