import requests
import random
import string
from config import *
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram.errors import MessageNotModified
from pyrogram.errors.pyromod import ListenerTimeout

# ✅ In-memory cache for links speed up
shortened_urls_cache = {}

def generate_random_alphanumeric():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(8))

def get_short(url, client):
    # Dynamic Sync: Check if shortner/verification mode is active
    shortner_enabled = getattr(client, 'verify_mode', True)
    if not shortner_enabled:
        return url  # Verification off hai to original link bypass karein

    # Check local cache memory
    if url in shortened_urls_cache:
        return shortened_urls_cache[url]

    try:
        alias = generate_random_alphanumeric()
        short_url = getattr(client, 'short_url', SHORT_URL)
        short_api = getattr(client, 'short_api', SHORT_API)
        
        api_url = f"https://{short_url}/api?api={short_api}&url={url}&alias={alias}"
        response = requests.get(api_url, timeout=10)
        rjson = response.json()

        if rjson.get("status") == "success" and response.status_code == 200:
            shortened_link = rjson.get("shortenedUrl", url)
            shortened_urls_cache[url] = shortened_link
            return shortened_link
    except Exception as e:
        print(f"[Shortener Engine Error] {e}")

    return url  # Fallback token route if api drops

#===============================================================#

@Client.on_message(filters.command('shortner') & filters.private)
async def shortner_command(client: Client, message: Message):
    if not message.from_user.id in client.admins:
        return
    await shortner_panel(client, message)

#===============================================================#

async def shortner_panel(client, query_or_message):
    short_url = getattr(client, 'short_url', SHORT_URL)
    short_api = getattr(client, 'short_api', SHORT_API)
    tutorial_link = getattr(client, 'tutorial_link', "https://t.me/How_to_Download_7x/26")
    
    # Sync with verification settings globally
    shortner_enabled = getattr(client, 'verify_mode', True)
    
    # Live API check status render loop
    if shortner_enabled:
        try:
            test_response = requests.get(f"https://{short_url}/api?api={short_api}&url=https://google.com&alias=test_ping", timeout=5)
            status = "✓ ᴡᴏʀᴋɪɴɢ" if test_response.status_code == 200 else "✗ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ"
        except:
            status = "✗ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ"
    else:
        status = "✗ ᴅɪsᴀʙʟᴇᴅ"
    
    enabled_text = "✓ ᴇɴᴀʙʟᴇᴅ" if shortner_enabled else "✗ ᴅɪsᴀʙʟᴇᴅ"
    toggle_text = "✗ ᴏғғ" if shortner_enabled else "✓ ᴏɴ"
    
    msg = f"""<blockquote>✦ 𝗦𝗛𝗢𝗥𝗧𝗡𝗘𝗥 & 𝗩𝗘𝗥𝗜𝗙𝗜𝗖𝗔𝗧𝗜𝗢𝗡 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦</blockquote>
**<u>ᴄᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴsettings:</u>**
<blockquote>›› **ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ sᴛᴀᴛᴜs:** {enabled_text}
›› **sʜᴏʀᴛɴᴇʀ ᴜʀʟ:** `{short_url}`
›› **sʜᴏʀᴛɴᴇʀ ᴀᴘɪ:** `{short_api[:15]}...`</blockquote> 
<blockquote>›› **ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ:** `{tutorial_link}`
›› **ᴀᴘɪ sᴛᴀᴛᴜs:** {status}</blockquote>

<blockquote>**≡ ᴜsᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴꜰɪɢᴜʀᴇ ʏᴏᴜʀ sʜᴏʀᴛɴᴇʀ sᴇᴛᴛɪɴɢs!**</blockquote>"""
    
    # Create Back Button conditionally
    buttons = [
        [InlineKeyboardButton(f'• {toggle_text} ꜱʜᴏʀᴛɴᴇʀ •', 'toggle_shortner'), InlineKeyboardButton('• ᴀᴅᴅ ꜱʜᴏʀᴛɴᴇʀ •', 'add_shortner')],
        [InlineKeyboardButton('• ꜱᴇᴛ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ •', 'set_tutorial_link')],
        [InlineKeyboardButton('• ᴛᴇꜱᴛ ꜱʜᴏʀᴛɴᴇʀ •', 'test_shortner')]
    ]
    
    if hasattr(query_or_message, 'message'):
        buttons.append([InlineKeyboardButton('◂ ʙᴀᴄᴋ ᴛᴏ ꜱᴇᴛᴛɪɴɢꜱ', 'settings_page_2')])
        
    reply_markup = InlineKeyboardMarkup(buttons)
    image_url = MESSAGES.get("SHORT", "https://telegra.ph/file/8aaf4df8c138c6685dcee-05d3b183d4978ec347.jpg")
    
    if hasattr(query_or_message, 'message'):
        # Crash Bypass: Agar text-only menu se photo menu pe aa rahe ho to media edit kaam karega
        try:
            if query_or_message.message.photo or query_or_message.message.document:
                await query_or_message.message.edit_media(
                    media=InputMediaPhoto(media=image_url, caption=msg),
                    reply_markup=reply_markup
                )
            else:
                # Text input interface layout drops and photo drops fresh
                await query_or_message.message.delete()
                await client.send_photo(
                    chat_id=query_or_message.message.chat.id,
                    photo=image_url,
                    caption=msg,
                    reply_markup=reply_markup
                )
        except MessageNotModified:
            pass
        except Exception:
            await query_or_message.message.reply_photo(photo=image_url, caption=msg, reply_markup=reply_markup)
    else:
        await query_or_message.reply_photo(photo=image_url, caption=msg, reply_markup=reply_markup)

#===============================================================#

@Client.on_callback_query(filters.regex("^shortner$"))
async def shortner_callback(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ!', show_alert=True)
    await query.answer()
    await shortner_panel(client, query)

#===============================================================#

@Client.on_callback_query(filters.regex("^toggle_shortner$"))
async def toggle_shortner(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜis!', show_alert=True)
    
    current_status = getattr(client, 'verify_mode', True)
    new_status = not current_status
    client.verify_mode = new_status
    
    # Persistence to database
    await client.mongodb.update_bot_setting("verification_mode", new_status)
    
    status_text = "ᴇɴᴀʙʟᴇᴅ" if new_status else "ᴅɪsᴀʙʟᴇᴅ"
    await query.answer(f"✓ sʜᴏʀᴛɴᴇʀ / ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ {status_text}!")
    await shortner_panel(client, query)

#===============================================================#

@Client.on_callback_query(filters.regex("^add_shortner$"))
async def add_shortner(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ!', show_alert=True)
    
    await query.answer()
    current_url = getattr(client, 'short_url', SHORT_URL)
    current_api = getattr(client, 'short_api', SHORT_API)
    
    msg = f"""<blockquote>**ꜱᴇᴛ ꜱʜᴏʀᴛɴᴇʀ ꜱᴇᴛᴛɪɴɢꜱ:**</blockquote>
**ᴄᴜʀʀᴇɴᴛ ꜱᴇᴛᴛɪɴɢꜱ:**
• **ᴜʀʟ:** `{current_url}`
• **ᴀᴘɪ:** `{current_api[:15]}...`

__<blockquote>**≡ ꜱᴇɴᴅ ɴᴇᴡ ꜱʜᴏʀᴛɴᴇʀ ᴜʀʟ ᴀɴᴅ ᴀᴘɪ ɪɴ ᴛʜɪꜱ ꜰᴏʀᴍᴀᴛ ɪɴ ᴛʜᴇ ɴᴇxᴛ 60 ꜱᴇᴄᴏɴᴅꜱ!**</blockquote>__

**ꜰᴏʀᴍᴀᴛ:** `ᴜʀʟ ᴀᴘɪ`
**ᴇxᴀᴍᴘʟᴇ:** `inshorturl.com 9435894656863495834957348`"""
    
    # Text transition panel layout logic execution
    if query.message.photo or query.message.document:
        await query.message.delete()
        sent_msg = await client.send_message(query.message.chat.id, msg)
        msg_id_to_listen = sent_msg
    else:
        await query.message.edit_text(msg)
        msg_id_to_listen = query.message

    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        response_text = res.text.strip()
        
        parts = response_text.split()
        if len(parts) >= 2:
            new_url = parts[0].replace('https://', '').replace('http://', '').replace('/', '')
            new_api = ' '.join(parts[1:])  
            
            if new_url and '.' in new_url and len(new_api) > 10:
                client.short_url = new_url
                client.short_api = new_api
                
                await client.mongodb.update_shortner_setting('short_url', new_url)
                await client.mongodb.update_shortner_setting('short_api', new_api)
                
                # Clear existing shortened links cache on api change
                global shortened_urls_cache
                shortened_urls_cache.clear()
                
                await msg_id_to_listen.edit_text(f"**✓ ꜱʜᴏʀᴛɴᴇʀ ꜱᴇᴛᴛɪɴɢꜱ ᴜᴘᴅᴀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**\n\n**ɴᴇᴡ ᴜʀʟ:** `{new_url}`\n**ɴᴇᴡ ᴀᴘɪ:** `{new_api[:15]}...`", 
                                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'shortner')]]))
            else:
                await msg_id_to_listen.edit_text("**✗ ɪɴᴠᴀʟɪᴅ ꜰᴏʀᴍᴀᴛ! ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ᴜʀʟ ᴀɴᴅ ᴀᴘɪ ᴋᴇʏ.**", 
                                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'shortner')]]))
        else:
            await msg_id_to_listen.edit_text("**✗ ɪɴᴠᴀʟɪᴅ ꜰᴏʀᴍᴀᴛ! ᴘʟᴇᴀꜱᴇ ᴜꜱᴇ: `ᴜʀʟ ᴀᴘɪ`**", 
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'shortner')]]))
    except ListenerTimeout:
        await msg_id_to_listen.edit_text("**⏰ ᴛɪᴍᴇᴏᴜᴛ! ᴛʀʏ ᴀɢᴀɪɴ.**", 
                                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'shortner')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^set_tutorial_link$"))
async def set_tutorial_link(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ!', show_alert=True)
    
    await query.answer()
    current_tutorial = getattr(client, 'tutorial_link', "https://t.me/How_to_Download_7x/26")
    msg = f"""<blockquote>****\x1b[1mꜱᴇᴛ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ:\x1b[1m****</blockquote>
**ᴄᴜʀʀᴇɴᴛ ᴛᴜᴛᴏʀɪᴀʟ:** `{current_tutorial}`

__sᴇɴᴅ ᴛʜᴇ ɴᴇᴡ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ ɪɴ ᴛʜᴇ ɴᴇxᴛ 60 sᴇᴄᴏɴᴅs!__
**ᴇxᴀᴍᴘʟᴇ:** `https://t.me/How_to_Download_7x/26`"""
    
    if query.message.photo or query.message.document:
        await query.message.delete()
        sent_msg = await client.send_message(query.message.chat.id, msg)
        msg_id_to_listen = sent_msg
    else:
        await query.message.edit_text(msg)
        msg_id_to_listen = query.message
        
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        new_tutorial = res.text.strip()
        
        # Proper Python tuple verification fix inside conditions
        if new_tutorial and new_tutorial.startswith(('https://', 'http://')):
            client.tutorial_link = new_tutorial
            await client.mongodb.update_shortner_setting('tutorial_link', new_tutorial)
            await msg_id_to_listen.edit_text(f"**✓ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ ᴜᴘᴅᴀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**", 
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'shortner')]]))
        else:
            await msg_id_to_listen.edit_text("**✗ ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ ꜰᴏʀᴍᴀᴛ! ᴍᴜꜱᴛ ꜱᴛᴀʀᴛ ᴡɪᴛʜ https:// ᴏʀ http://**", 
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'shortner')]]))
    except ListenerTimeout:
        await msg_id_to_listen.edit_text("**⏰ ᴛɪᴍᴇᴏᴜᴛ! ᴛʀʏ ᴀɢᴀɪɴ.**", 
                                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'shortner')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^test_shortner$"))
async def test_shortner(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ!', show_alert=True)
    
    await query.answer()
    
    # Render layout switch logic check to handle if photo drops or normal edits apply
    if query.message.photo or query.message.document:
        await query.message.delete()
        status_msg = await client.send_message(query.message.chat.id, "**🔄 ᴛᴇꜱᴛɪɴɢ ꜱʜᴏʀᴛɴᴇʀ ᴄᴏɴɴᴇᴄᴛɪᴏɴ...**")
    else:
        await query.message.edit_text("**🔄 ᴛᴇꜱᴛɪɴɢ ꜱʜᴏʀᴛɴᴇʀ ᴄᴏɴɴᴇᴄᴛɪᴏɴ...**")
        status_msg = query.message
    
    short_url = getattr(client, 'short_url', SHORT_URL)
    short_api = getattr(client, 'short_api', SHORT_API)
    
    try:
        test_url = "https://google.com"
        alias = generate_random_alphanumeric()
        api_url = f"https://{short_url}/api?api={short_api}&url={test_url}&alias={alias}"
        
        response = requests.get(api_url, timeout=10)
        rjson = response.json()
        
        if rjson.get("status") == "success" and response.status_code == 200:
            short_link = rjson.get("shortenedUrl", "")
            msg = f"""**✅ ꜱʜᴏʀᴛɴᴇʀ ᴛᴇꜱᴛ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ!**

**ᴛᴇꜱᴛ ᴜʀʟ:** `{test_url}`
**ꜱʜᴏʀᴛ ᴜʀʟ:** `{short_link}`
**ʀᴇꜱᴘᴏɴꜱᴇ:** `{rjson.get('status', 'Unknown')}`"""
        else:
            msg = f"""**❌ ꜱʜᴏʀᴛɴᴇʀ ᴛᴇꜱᴛ ꜰᴀɪʟᴇfailed!**

**ᴇʀʀᴏʀ:** `{rjson.get('message', 'Unknown error')}`
**ꜱᴛᴀᴛᴜꜱ ᴄᴏᴅᴇ:** `{response.status_code}`"""
            
    except Exception as e:
        msg = f"**❌ ꜱʜᴏʀᴛɴᴇʀ ᴛᴇꜱᴛ ꜰᴀɪʟᴇᴅ!**\n\n**ᴇʀʀᴏʀ:** `{str(e)}`"
    
    await status_msg.edit_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'shortner')]]))
