from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.pyromod import ListenerTimeout
from config import *
import humanize
import time

#===============================================================#

@Client.on_callback_query(filters.regex("^settings$"))
async def settings(client, query):
    # Count active force subscription channels by type
    total_fsub = len(getattr(client, 'fsub_dict', {}))
    request_enabled = sum(1 for data in getattr(client, 'fsub_dict', {}).values() if data[2])
    timer_enabled = sum(1 for data in getattr(client, 'fsub_dict', {}).values() if data[3] > 0)
    
    # Count DB channels
    total_db_channels = len(getattr(client, 'db_channels', {}))
    primary_db = getattr(client, 'primary_db_channel', client.db)
    
    msg = f"""<blockquote>✦ sᴇᴛᴛɪɴɢs ᴏꜰ @{client.username} [ᴘᴀɢᴇ 1]</blockquote>
›› **ꜰꜱᴜʙ ᴄʜᴀɴɴᴇʟs:** `{total_fsub}` (ʀᴇǫᴜᴇsᴛ: {request_enabled}, ᴛɪᴍᴇʀ: {timer_enabled})
›› **ᴅʙ ᴄʜᴀɴɴᴇʟs:** `{total_db_channels}` (ᴘʀɪᴍᴀʀʏ: `{primary_db}`)
›› **ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇʀ:** `{getattr(client, 'auto_del', 0)}s`
›› **ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ:** `{"✓ ᴛʀᴜᴇ" if getattr(client, 'protect', False) else "✗ ꜰᴀʟsᴇ"}`
›› **ᴅɪsᴀʙʟᴇ ʙᴜᴛᴛᴏɴ:** `{"✓ ᴛʀᴜᴇ" if getattr(client, 'disable_btn', False) else "✗ ꜰᴀʟsᴇ"}`
›› **ʀᴇᴘʟʏ ᴛᴇxᴛ sᴛᴀᴛᴜs:** `{"✓ sᴇᴛ" if getattr(client, 'reply_text', None) else "✗ ɴᴏɴᴇ"}`
›› **ᴀᴅᴍɪɴs ᴄᴏᴜɴᴛ:** `{len(getattr(client, 'admins', []))}`

__<blockquote>≡ ᴜsᴇ ᴛʜᴇ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ᴍᴀɴᴀɢᴇ ʙᴏᴛ ᴄᴏɴꜰɪɢᴜʀᴀᴛɪᴏɴs!</blockquote>__"""

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('• ꜰꜱᴜʙ ᴄʜᴀɴɴᴇʟꜱ •', 'fsub'), InlineKeyboardButton('• ᴅʙ ᴄʜᴀɴɴᴇʟꜱ •', 'db_channels')],
        [InlineKeyboardButton('• ᴀᴅᴍɪɴꜱ ʟɪꜱᴛ •', 'admins'), InlineKeyboardButton('• ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ •', 'auto_del')],
        [InlineKeyboardButton('• ʜᴏᴍᴇ •', 'home'), InlineKeyboardButton('›› ɴᴇxᴛ ᴘᴀɢᴇ', 'settings_page_2')]
    ])
    
    if query.message.text != msg:
        await query.message.edit_text(msg, reply_markup=reply_markup)
    else:
        await query.answer("Already on Page 1")
    return

#===============================================================#

@Client.on_callback_query(filters.regex("^settings_page_2$"))
async def settings_page_2(client, query):
    verify_status = "✓ ᴇɴᴀʙʟᴇᴅ" if getattr(client, 'verify_mode', True) else "✗ ᴅɪsᴀʙʟᴇᴅ"
    verify_expire = getattr(client, 'verify_expire_time', 86400) 
    expire_hours = round(verify_expire / 3600, 1)
    
    msg = f"""<blockquote>✦ sᴇᴛᴛɪɴɢs ᴏꜰ @{client.username} [ᴘᴀɢᴇ 2]</blockquote>
›› **sʜᴏʀᴛɴᴇʀ ᴜʀʟ:** `{getattr(client, 'short_url', 'ɴᴏᴛ sᴇᴛ')}`
›› **ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ sᴛᴀᴛᴜs:** `{verify_status}`
›› **ᴠᴇʀɪꜰy ᴇxᴘɪʀᴇ ᴛɪᴍᴇ:** `{expire_hours} ʜᴏᴜʀs` (`{verify_expire}s`)
›› **ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ:** `{getattr(client, 'tutorial_link', 'ɴᴏᴛ sᴇᴛ')}`

**<u>ᴄᴜʀʀᴇɴᴛ ᴀsꜱᴇᴛꜱ ᴏᴠᴇʀᴠɪᴇᴡ:</u>**
›› **sᴛᴀʀᴛ ɪᴍᴀɢᴇ:** `{"✓ sᴇᴛ" if client.messages.get('START_PHOTO') else "✗ ᴇᴍᴘᴛʏ"}`
›› **ꜰᴏʀᴄᴇ sᴜʙ ɪᴍᴀɢᴇ:** `{"✓ sᴇᴛ" if client.messages.get('FSUB_PHOTO') else "✗ ᴇᴍᴘᴛʏ"}`
›› **sᴛᴀʀᴛ ᴍᴇssᴀɢᴇ:** <pre>{client.messages.get('START', 'ᴇᴍᴘᴛʏ')[:30]}...</pre>

__<blockquote>≡ ᴍᴀɴᴀɢᴇ ᴍᴇᴅɪᴀ, ᴛᴇxᴛs, ᴀɴᴅ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴛɪᴍᴇʀs ʜᴇʀᴇ!</blockquote>__"""

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('• ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ •', 'protect'), InlineKeyboardButton('• ᴘʜᴏᴛᴏs ᴍᴇɴᴜ •', 'photos')],
        [InlineKeyboardButton('• ᴛᴇxᴛs ᴍᴇɴᴜ •', 'texts'), InlineKeyboardButton('⏱️ ᴠᴇʀɪꜰy ᴇxᴘɪʀy', 'set_verify_expire')],
        [InlineKeyboardButton('‹ ᴘʀᴇᴠ ᴘᴀɢᴇ', 'settings'), InlineKeyboardButton('• ʜᴏᴍᴇ •', 'home')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)
    return

#===============================================================#

@Client.on_callback_query(filters.regex("^set_verify_expire$"))
async def set_verify_expire(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
        
    current_seconds = getattr(client, 'verify_expire_time', 86400)
    current_hours = round(current_seconds / 3600, 1)
    
    msg = f"""<blockquote>✦ ᴄʜᴀɴɢᴇ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴇxᴘɪʀy</blockquote>
›› **ᴄᴜʀʀᴇɴᴛ ᴠᴀʟɪᴅɪᴛy:** `{current_hours} ʜᴏᴜʀs` (`{current_seconds}s`)

__sᴇɴᴅ ᴛʜᴇ ɴᴇᴡ ᴇxᴘɪʀy ᴛɪᴍᴇ ɪɴ **ʜᴏᴜʀs** (ᴘᴏsɪᴛɪᴠᴇ ɪɴᴛᴇɢᴇʀ) ᴡɪᴛʜɪɴ ᴛʜᴇ ɴᴇxᴛ 60 sᴇᴄᴏɴᴅs!__

**💡 ᴇxᴀᴍᴘʟᴇs:**
• `1` = 1 ʜᴏᴜʀ (3600s)
• `24` = 24 ʜᴏᴜʀs (86400s)"""
    
    await query.answer()
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        input_text = res.text.strip()
        
        if input_text.isdigit():
            hours = int(input_text)
            if hours > 0:
                calculated_seconds = hours * 3600
                client.verify_expire_time = calculated_seconds
                
                # Agar aap database use kar rahe hain toh yahan update ki command add kar dein
                # Example: await client.mongodb.update_bot_setting("verify_expire_time", calculated_seconds)
                
                return await query.message.edit_text(
                    f"**✓ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴇxᴘɪʀy ᴛɪᴍᴇ sᴇᴛ ᴛᴏ `{hours}` ʜᴏᴜʀs!**",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ ᴛᴏ ᴘᴀɢᴇ 2', 'settings_page_2')]])
                )
            else:
                return await query.message.edit_text("**✗ ᴛɪᴍᴇ ᴍᴜsᴛ ʙᴇ ɢʀᴇᴀᴛᴇʀ ᴛʜᴀɴ 0!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings_page_2')]]))
        else:
            return await query.message.edit_text("**✗ ɪɴᴠᴀʟɪᴅ ɴᴜᴍᴇʀɪᴄ ɪɴᴘᴜᴛ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings_page_2')]]))
            
    except ListenerTimeout:
        return await query.message.edit_text("**⏰ ʟɪsᴛᴇɴᴇʀ ᴛɪᴍᴇᴏᴜᴛ! ᴘʟᴇᴀsᴇ ᴛʀy ᴀɢᴀɪɴ.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings_page_2')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^fsub$"))
async def fsub(client, query):
    if client.fsub_dict:
        channel_list = []
        for channel_id, channel_data in client.fsub_dict.items():
            channel_name = channel_data[0] if channel_data and len(channel_data) > 0 else "Unknown"
            request_status = "✓ ʀᴇǫᴜᴇsᴛ" if channel_data[2] else "✗ ʀᴇǫᴜᴇsᴛ"
            timer_status = f"ᴛɪᴍᴇʀ: {channel_data[3]}ᴍ" if channel_data[3] > 0 else "ᴛɪᴍᴇʀ: ∞"
            channel_list.append(f"• `{channel_name}` (`{channel_id}`) - {request_status}, {timer_status}")
        
        channels_display = "\n".join(channel_list)
    else:
        channels_display = "_ɴᴏ ꜰᴏʀᴄᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ᴄʜᴀɴɴᴇʟs ᴄᴏɴғɪɢᴜʀᴇᴅ_"
    
    msg = f"""<blockquote>✦ ꜰᴏʀᴄᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴ sᴇᴛᴛɪɴɢs</blockquote>
›› **ᴄᴏɴғɪɢᴜʀᴇᴅ ᴄʜᴀɴɴᴇʟs:**
{channels_display}

__ᴜsᴇ ᴛʜᴇ ᴀᴘᴘʀᴏᴘʀɪᴀᴛᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴀᴅᴅ ᴏʀ ʀᴇᴍᴏᴠᴇ ᴀ ꜰᴏʀᴄᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ᴄʜᴀɴɴᴇʟ!__"""

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('›› ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ', 'add_fsub'), InlineKeyboardButton('›› ʀᴇᴍᴏᴠᴇ ᴄʜᴀɴɴᴇʟ', 'rm_fsub')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)
    return

#===============================================================#

@Client.on_callback_query(filters.regex("^db_channels$"))
async def db_channels(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    
    db_channels = getattr(client, 'db_channels', {})
    if db_channels:
        channel_list = []
        for channel_id_str, channel_data in db_channels.items():
            channel_name = channel_data.get('name', 'Unknown')
            is_primary = "✓ ᴘʀɪᴍᴀʀʏ" if channel_data.get('is_primary', False) else "• sᴇᴄᴏɴᴅᴀʀʏ"
            is_active = "✓ ᴀᴄᴛɪᴠᴇ" if channel_data.get('is_active', True) else "✗ ɪɴᴀᴄᴛɪᴠᴇ"
            channel_list.append(f"• `{channel_name}` (`{channel_id_str}`)\n  {is_primary} | {is_active}")
        
        channels_display = "\n\n".join(channel_list)
    else:
        channels_display = "_ɴᴏ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟs ᴄᴏɴғɪɢᴜʀᴇᴅ_"
    
    primary_db = getattr(client, 'primary_db_channel', client.db)
    
    msg = f"""<blockquote>✦ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟs sᴇᴛᴛɪɴɢs</blockquote>
›› **ᴄᴜʀʀᴇɴᴛ ᴘʀɪᴍᴀʀʏ ᴅʙ:** `{primary_db}`
›› **ᴛᴏᴛᴀʟ ᴅʙ ᴄʜᴀɴɴᴇʟs:** `{len(db_channels)}`

**ᴄᴏɴғɪɢᴜʀᴇᴅ ᴄʜᴀɴɴᴇʟs:**
{channels_display}

__ᴜsᴇ ᴛʜᴇ ᴀᴘᴘʀᴏᴘʀɪᴀᴛᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟs!__"""

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('›› ᴀᴅᴅ ᴅʙ', 'add_db_channel'), InlineKeyboardButton('›› ʀᴇᴍᴏᴠᴇ ᴅʙ', 'rm_db_channel')],
        [InlineKeyboardButton('›› sᴇᴛ ᴘʀɪᴍᴀʀʏ', 'set_primary_db'), InlineKeyboardButton('›› sᴛᴀᴛᴜs', 'toggle_db_status')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)
    return

#===============================================================#

@Client.on_callback_query(filters.regex("^add_db_channel$"))
async def add_db_channel(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    
    await query.answer()
    msg = f"""<blockquote>✦ ᴀᴅᴅ ɴᴇᴡ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟ</blockquote>
__sᴇɴᴅ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ɪᴅ (ɴᴇɢᴀᴛɪᴠᴇ ɪɴᴛᴇɢᴇʀ ᴠᴀʟᴜᴇ) ᴏғ ᴛʜᴇ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴀᴅᴅ ɪɴ ᴛʜᴇ ɴᴇxᴛ 60 sᴇᴄᴏɴᴅs!__

**ᴇxᴀᴍᴘʟᴇ:** `-1001234567675`"""
    
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        channel_id_text = res.text.strip()
        
        if not channel_id_text.lstrip('-').isdigit():
            return await query.message.edit_text("**✗ ɪɴᴠᴀʟɪᴅ ᴄʜᴀɴɴᴇʟ ɪᴅ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        
        channel_id = int(channel_id_text)
        db_channels = getattr(client, 'db_channels', {})
        if str(channel_id) in db_channels:
            return await query.message.edit_text("**✗ ᴄʜᴀɴɴᴇʟ ᴀʟʀᴇᴀᴅʏ ᴀᴅᴅᴇᴅ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        
        try:
            chat = await client.get_chat(channel_id)
            test_msg = await client.send_message(chat_id=channel_id, text="ᴛᴇsᴛɪɴɢ ᴅʙ ᴄʜᴀɴɴᴇʟ ᴀᴄᴄᴇss")
            await test_msg.delete()
            
            channel_data = {
                'name': chat.title,
                'is_primary': len(db_channels) == 0,
                'is_active': True,
                'added_by': query.from_user.id
            }
            
            await client.mongodb.add_db_channel(channel_id, channel_data)
            
            if not hasattr(client, 'db_channels'):
                client.db_channels = {}
            client.db_channels[str(channel_id)] = channel_data
            
            if channel_data['is_primary']:
                client.primary_db_channel = channel_id
                await client.mongodb.set_primary_db_channel(channel_id)
            
            await query.message.edit_text(f"**✓ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟ ᴀᴅᴅᴇᴅ!**\n\n›› **ᴄʜᴀɴɴᴇʟ:** `{chat.title}`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        except Exception as e:
            await query.message.edit_text(f"**✗ ᴇʀʀᴏʀ ᴀᴄᴄᴇssɪɴɢ ᴄʜᴀɴɴᴇʟ!**\n\n›› `{str(e)}`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
    except ListenerTimeout:
        await query.message.edit_text("**⏰ ᴛɪᴍᴇᴏᴜᴛ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^rm_db_channel$"))
async def rm_db_channel(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    
    await query.answer()
    db_channels = getattr(client, 'db_channels', {})
    
    if not db_channels:
        return await query.message.edit_text("**✗ ɴᴏ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟs!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
    
    msg = "<blockquote>✦ ʀᴇᴍᴏᴠᴇ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟ</blockquote>\n**ᴀᴠᴀɪʟᴀʙʟᴇ ᴄʜᴀɴɴᴇʟs:**\n"
    for channel_id_str, channel_data in db_channels.items():
        is_primary = " (ᴘʀɪᴍᴀʀʏ)" if channel_data.get('is_primary', False) else ""
        msg += f"• `{channel_data.get('name', 'Unknown')}` - `{channel_id_str}`{is_primary}\n"
    
    msg += "\n__sᴇɴᴅ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ɪᴅ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʀᴇᴍᴏᴠᴇ!__"
    
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        channel_id_text = res.text.strip()
        
        if not channel_id_text.lstrip('-').isdigit():
            return await query.message.edit_text("**✗ ɪɴᴠᴀʟɪᴅ ᴄʜᴀɴɴᴇʟ ɪᴅ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        
        channel_id = int(channel_id_text)
        
        if str(channel_id) not in db_channels:
            return await query.message.edit_text("**✗ ᴄʜᴀɴɴᴇʟ ɴᴏᴛ ꜰᴏᴜɴᴅ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        
        if db_channels[str(channel_id)].get('is_primary', False) and len(db_channels) > 1:
            return await query.message.edit_text("**✗ ᴄᴀɴɴᴏᴛ ʀᴇᴍᴏᴠᴇ ᴘʀɪᴍᴀʀʏ ᴄʜᴀɴɴᴇʟ ꜰɪʀsᴛ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        
        channel_name = db_channels[str(channel_id)].get('name', 'Unknown')
        await client.mongodb.remove_db_channel(channel_id)
        del client.db_channels[str(channel_id)]
        
        await query.message.edit_text(f"**✓ ᴄʜᴀɴɴᴇʟ ʀᴇᴍᴏᴠᴇᴅ!**\n\n**ʀᴇᴍᴏᴠᴇᴅ:** `{channel_name}`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
    except ListenerTimeout:
        await query.message.edit_text("**⏰ ᴛɪᴍᴇᴏᴜᴛ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^set_primary_db$"))
async def set_primary_db(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    
    await query.answer()
    db_channels = getattr(client, 'db_channels', {})
    
    if not db_channels:
        return await query.message.edit_text("**✗ ɴᴏ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟs ᴀᴠᴀɪʟᴀʙʟᴇ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
    
    msg = "<blockquote>✦ sᴇᴛ ᴘʀɪᴍᴀʀʏ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟ</blockquote>\n**ᴀᴠᴀɪʟᴀʙʟᴇ ᴄʜᴀɴɴᴇʟs:**\n"
    for channel_id_str, channel_data in db_channels.items():
        is_primary = " (ᴄᴜʀʀᴇɴᴛ ᴘʀɪᴍᴀʀʏ)" if channel_data.get('is_primary', False) else ""
        msg += f"• `{channel_data.get('name', 'Unknown')}` - `{channel_id_str}`{is_primary}\n"
    
    msg += "\n__sᴇɴᴅ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ɪᴅ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴇᴛ ᴀs ᴘʀɪᴍᴀʀʏ!__"
    
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        channel_id_text = res.text.strip()
        
        if not channel_id_text.lstrip('-').isdigit():
            return await query.message.edit_text("**✗ ɪɴᴠᴀʟɪᴅ ɪᴅ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        
        channel_id = int(channel_id_text)
        
        if str(channel_id) not in db_channels:
            return await query.message.edit_text("**✗ ᴄʜᴀɴɴᴇʟ ɴᴏᴛ ꜰᴏᴜɴᴅ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        
        await client.mongodb.set_primary_db_channel(channel_id)
        
        for ch_id, ch_data in client.db_channels.items():
            ch_data['is_primary'] = (int(ch_id) == channel_id)
        
        client.primary_db_channel = channel_id
        client.db = channel_id
        
        await query.message.edit_text("**✓ ᴘʀɪᴍᴀʀʏ ᴅᴀᴛᴀʙᴀsᴇ ᴜᴘᴅᴀᴛᴇᴅ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
    except ListenerTimeout:
        await query.message.edit_text("**⏰ ᴛɪᴍᴇᴏᴜᴛ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^toggle_db_status$"))
async def toggle_db_status(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    
    await query.answer()
    db_channels = getattr(client, 'db_channels', {})
    if not db_channels:
        return await query.message.edit_text("**✗ ɴᴏ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟs!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
    
    msg = "<blockquote>✦ ᴛᴏɢɢʟᴇ ᴄʜᴀɴɴᴇʟ sᴛᴀᴛᴜs</blockquote>\n**ᴀᴠᴀɪʟᴀʙʟᴇ ᴄʜᴀɴɴᴇʟs:**\n"
    for channel_id_str, channel_data in db_channels.items():
        status = "🟢 ᴀᴄᴛɪᴠᴇ" if channel_data.get('is_active', True) else "🔴 ɪɴᴀᴄᴛɪᴠᴇ"
        msg += f"• `{channel_data.get('name', 'Unknown')}` - `{channel_id_str}` ({status})\n"
    
    msg += "\n__sᴇɴᴅ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ɪᴅ!__"
    
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        channel_id_text = res.text.strip()
        
        if not channel_id_text.lstrip('-').isdigit():
            return await query.message.edit_text("**✗ ɪɴᴠᴀʟɪᴅ ɪᴅ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
            
        channel_id = int(channel_id_text)
        if str(channel_id) not in db_channels:
            return await query.message.edit_text("**✗ ᴄʜᴀɴɴᴇʟ ɴᴏᴛ ꜰᴏᴜɴᴅ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
            
        new_status = await client.mongodb.toggle_db_channel_status(channel_id)
        if new_status is not None:
            client.db_channels[str(channel_id)]['is_active'] = new_status
            await query.message.edit_text("**✓ sᴛᴀᴛᴜs ᴜᴘᴅᴀᴛᴇᴅ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        else:
            await query.message.edit_text("**✗ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴜᴘᴅᴀᴛᴇ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
    except ListenerTimeout:
        await query.message.edit_text("**⏰ ᴛɪᴍᴇᴏᴜᴛ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^admins$"))
async def admins(client, query):
    if not (query.from_user.id == OWNER_ID):
        return await query.answer('✗ ᴛʜɪs ᴄᴀɴ ᴏɴʟy ʙᴇ ᴜsᴇᴅ ʙy ᴏᴡɴᴇʀ.', show_alert=True)
        
    msg = f"""<blockquote>✦ ᴀᴅᴍɪɴ sᴇᴛᴛɪɴɢs</blockquote>
**ᴀᴅᴍɪɴ ᴜsᴇʀ ɪᴅs:** {", ".join(f"`{a}`" for a in client.admins)}

__ᴜsᴇ ᴛʜᴇ ᴀᴘᴘʀᴏᴘʀɪᴀᴛᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴀᴅᴅ ᴏʀ ʀᴇᴍᴏᴠᴇ ᴀɴ ᴀᴅᴍɪɴ!__"""

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('›› ᴀᴅᴅ ᴀᴅᴍɪɴ', 'add_admin'), InlineKeyboardButton('›› ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴ', 'rm_admin')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)
    return

#===============================================================#

@Client.on_callback_query(filters.regex("^photos$"))
async def photos(client, query):
    msg = f"""<blockquote>✦ ᴘʜᴏᴛᴏ ᴄᴏɴꜰɪɢᴜʀᴀᴛɪᴏɴs</blockquote>
**sᴛᴀʀᴛ ᴘʜᴏᴛᴏ:** `{client.messages.get("START_PHOTO", "ɴᴏɴᴇ")}`
**ꜰsᴜʙ ᴘʜᴏᴛᴏ:** `{client.messages.get('FSUB_PHOTO', 'ɴᴏɴᴇ')}`

__ᴜsᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ᴍᴀɴᴀɢᴇ ɪᴍᴀɢᴇs!__"""

    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(('ꜱᴇᴛ' if not client.messages.get("START_PHOTO") else 'ᴄʜᴀɴɢᴇ') + '\nꜱᴛᴀʀᴛ ᴘʜᴏᴛᴏ', callback_data='add_start_photo'),
            InlineKeyboardButton(('ꜱᴇᴛ' if not client.messages.get("FSUB_PHOTO") else 'ᴄʜᴀɴɢᴇ') + '\nꜰꜱᴜʙ ᴘʜᴏᴛᴏ', callback_data='add_fsub_photo')
        ],
        [
            InlineKeyboardButton('ʀᴇᴍᴏᴠᴇ\nꜱᴛᴀʀᴛ ᴘʜᴏᴛᴏ', callback_data='rm_start_photo'),
            InlineKeyboardButton('ʀᴇᴍᴏᴠᴇ\nꜰꜱᴜʙ ᴘʜᴏᴛᴏ', callback_data='rm_fsub_photo')
        ],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ ᴛᴏ ᴘᴀɢᴇ 2', callback_data='settings_page_2')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)
    return

#===============================================================#

@Client.on_callback_query(filters.regex("^protect$"))
async def protect(client, query):
    client.protect = not client.protect
    await query.answer(f"✓ ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ ᴛᴏɢɢʟᴇᴅ ᴛᴏ: {client.protect}")
    return await settings_page_2(client, query)

#===============================================================#

@Client.on_callback_query(filters.regex("^auto_del$"))
async def auto_del(client, query):
    msg = f"""<blockquote>✦ ᴄʜᴀɴɢᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇ</blockquote>
**ᴄᴜʀʀᴇɴᴛ ᴛɪᴍᴇʀ:** `{client.auto_del}s`

__ᴇɴᴛᴇʀ ɴᴇᴡ ɪɴᴛᴇɢᴇʀ ᴠᴀʟᴜᴇ ᴏꜰ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇʀ ɪɴ sᴇᴄᴏɴᴅs!__
__(ᴋᴇᴇᴘ 0 ᴛᴏ ᴅɪsᴀʙʟᴇ)__"""
    
    await query.answer()
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        timer = res.text.strip()
        
        # Tuple condition bug fixed here: startswith(('+', '-'))
        if timer.isdigit() or (timer.startswith(('+', '-')) and timer[1:].isdigit()):
            timer = int(timer)
            if timer >= 0:
                client.auto_del = timer
                return await query.message.edit_text(f'**✓ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇʀ sᴇᴛ ᴛᴏ {timer} sᴇᴄᴏɴᴅs!**', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]]))
            else:
                return await query.message.edit_text("**✗ ɴᴏ ᴄʜᴀɴɢᴇs ᴍᴀᴅᴇ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]]))
        else:
            return await query.message.edit_text("**✗ ɪɴᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀ ᴠᴀʟᴜᴇ!!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]]))
    except ListenerTimeout:
        return await query.message.edit_text("**⏰ ᴛɪᴍᴇᴏᴜᴛ! ᴛʀy ᴀɢᴀɪɴ.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^texts$"))
async def texts(client, query):
    msg = f"""<blockquote>✦ ᴛᴇxᴛ ᴄᴏɴꜰɪɢᴜʀᴀᴛɪᴏɴs</blockquote>
**sᴛᴀʀᴛ ᴍᴇssᴀɢᴇ:**
<pre>{client.messages.get('START', 'ᴇᴍᴘᴛʏ')}</pre>
**ꜰsᴜʙ ᴍᴇssᴀɢᴇ:**
<pre>{client.messages.get('FSUB', 'ᴇᴍᴘᴛʏ')}</pre>
**ᴀʙᴏᴜᴛ ᴍᴇssᴀɢᴇ:**
<pre>{client.messages.get('ABOUT', 'ᴇᴍᴘᴛʏ')}</pre>
**ʀᴇᴘʟʏ ᴍᴇssᴀɢᴇ:**
<pre>{getattr(client, 'reply_text', 'ᴇᴍᴘᴛʏ')}</pre>"""

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('ꜱᴛᴀʀᴛ ᴛᴇxᴛ', 'start_txt'), InlineKeyboardButton('ꜰꜱᴜʙ ᴛᴇxᴛ', 'fsub_txt')],
        [InlineKeyboardButton('ʀᴇᴘʟʏ ᴛᴇxᴛ', 'reply_txt'), InlineKeyboardButton('ᴀʙᴏᴜᴛ ᴛᴇxᴛ', 'about_txt')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ ᴛᴏ ᴘᴀɢᴇ 2', 'settings_page_2')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)
    return

#===============================================================#

@Client.on_callback_query(filters.regex('^rm_start_photo$'))
async def rm_start_photo(client, query):
    client.messages['START_PHOTO'] = ''
    await query.answer("✓ sᴛᴀʀᴛ ᴘʜᴏᴛᴏ ʀᴇᴍᴏᴠᴇᴅ!")
    await photos(client, query)

#===============================================================#

@Client.on_callback_query(filters.regex('^rm_fsub_photo$'))
async def rm_fsub_photo(client, query):
    client.messages['FSUB_PHOTO'] = ''
    await query.answer("✓ ꜰsᴜʙ ᴘʜᴏᴛᴏ ʀᴇᴍᴏᴠᴇᴅ!")
    await photos(client, query)

#===============================================================#

@Client.on_callback_query(filters.regex("^add_start_photo$"))
async def add_start_photo(client, query):
    msg = f"""<blockquote>✦ ᴄʜᴀɴɢᴇ sᴛᴀʀᴛ ɪᴍᴀɢᴇ</blockquote>
**ᴄᴜʀʀᴇɴᴛ:** `{client.messages.get('START_PHOTO', 'ɴᴏɴᴇ')}`

__ᴇɴᴛᴇʀ ɴᴇᴡ ʟɪɴᴋ ᴏʀ sᴇɴᴅ ᴛʜᴇ ᴘʜᴏᴛᴏ (ᴡɪᴛʜɪɴ 60s)!__"""
    
    await query.answer()
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=(filters.text | filters.photo), timeout=60)
        
        # Tuple condition bug fixed here: startswith(('https://', 'http://'))
        if res.text and res.text.startswith(('https://', 'http://')):
            client.messages['START_PHOTO'] = res.text
            return await query.message.edit_text("**✓ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ sᴇᴛ ᴀs sᴛᴀʀᴛ ᴘʜᴏᴛᴏ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
        elif res.photo:
            loc = await res.download()
            client.messages['START_PHOTO'] = loc
            return await query.message.edit_text("**✓ ɪᴍᴀɢᴇ ʜᴀs ʙᴇᴇɴ sᴇᴛ ᴀs sᴛᴀʀᴛ ᴘʜᴏᴛᴏ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
        else:
            return await query.message.edit_text("**✗ ɪɴᴠᴀʟɪᴅ ꜰᴏʀᴍᴀᴛ! ᴍᴜsᴛ sᴛᴀʀᴛ ᴡɪᴛʜ ʜᴛᴛᴘ/ʜᴛᴛᴘs.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
    except ListenerTimeout:
        return await query.message.edit_text("**⏰ ᴛɪᴍᴇᴏᴜᴛ! ᴛʀy ᴀɢᴀɪɴ.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^add_fsub_photo$"))
async def add_fsub_photo(client, query):
    msg = f"""<blockquote>✦ ᴄʜᴀɴɢᴇ ꜰsᴜʙ ɪᴍᴀɢᴇ</blockquote>
**ᴄᴜʀʀᴇɴᴛ:** `{client.messages.get('FSUB_PHOTO', 'ɴᴏɴᴇ')}`

__ᴇɴᴛᴇʀ ɴᴇᴡ ʟɪɴᴋ ᴏʀ sᴇɴᴅ ᴛʜᴇ ᴘʜᴏᴛᴏ (ᴡɪᴛʜɪɴ 60s)!__"""
    
    await query.answer()
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=(filters.text | filters.photo), timeout=60)
        
        # Tuple condition bug fixed here: startswith(('https://', 'http://'))
        if res.text and res.text.startswith(('https://', 'http://')):
            client.messages['FSUB_PHOTO'] = res.text
            return await query.message.edit_text("**✓ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ sᴇᴛ ᴀs ꜰsᴜʙ ᴘʜᴏᴛᴏ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
        elif res.photo:
            loc = await res.download()
            client.messages['FSUB_PHOTO'] = loc
            return await query.message.edit_text("**✓ ɪᴍᴀɢᴇ ʜᴀs ʙᴇᴇɴ sᴇᴛ ᴀs ꜰsᴜʙ ᴘʜᴏᴛᴏ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
        else:
            return await query.message.edit_text("**✗ ɪɴᴠᴀʟɪᴅ ꜰᴏʀᴍᴀᴛ! ᴍᴜsᴛ sᴛᴀʀᴛ ᴡɪᴛʜ ʜᴛᴛᴘ/ʜᴛᴛᴘs.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
    except ListenerTimeout:
        return await query.message.edit_text("**⏰ ᴛɪᴍᴇᴏᴜᴛ! ᴛʀy ᴀɢᴀɪɴ.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
