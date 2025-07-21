import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- ВАШИ ДАННЫЕ ---
TELEGRAM_BOT_TOKEN = '7528447125:AAFud0fUTnZFmIo7sL6QUoVDHcBUFBjqegc'
ADMIN_USER_ID = 5159138688
ACTIVATION_KEY = '''vless://6d2d1202-b84b-459c-9dbe-66a984730225@193.124.254.181:443?type=tcp&security=reality&pbk=st953crlEoQu2lefGdJkUxkn-8-nSzZDBID0_OlKuVM&fp=chrome&sni=www.microsoft.com&sid=a0&spx=%2F&flow=xtls-rprx-vision#Riga-k90z3fdq'''
# -----------------------------------------

# Функция, которая запускается при команде /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("🔑 Получить ключ активации", callback_data='request_key')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        'Здравствуйте! Чтобы получить ключ для активации приложения, нажмите на кнопку ниже. '
        'Ваш запрос будет отправлен администратору на одобрение.',
        reply_markup=reply_markup
    )

# Функция обработки нажатий на кнопки
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    # Если пользователь нажал "Получить ключ"
    if query.data == 'request_key':
        user = query.from_user
        user_info = f"Пользователь: {user.full_name}\nUsername: @{user.username}\nID: {user.id}"
        
        # Создаем кнопки "Одобрить" и "Отклонить" для администратора
        keyboard = [
            [
                InlineKeyboardButton("✅ Одобрить", callback_data=f'approve_{user.id}'),
                InlineKeyboardButton("❌ Отклонить", callback_data=f'decline_{user.id}')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Отправляем запрос администратору
        await context.bot.send_message(
            chat_id=ADMIN_USER_ID,
            text=f"Новый запрос на получение ключа:\n\n{user_info}",
            reply_markup=reply_markup
        )
        
        # Сообщаем пользователю, что его запрос отправлен
        await query.edit_message_text(text="✅ Ваш запрос отправлен администратору. Пожалуйста, ожидайте ответа.")

    # Если администратор нажал "Одобрить" или "Отклонить"
    else:
        action, user_id_str = query.data.split('_')
        user_id = int(user_id_str)
        
        if action == 'approve':
            # --- ИСПРАВЛЕННАЯ СТРОКА ЗДЕСЬ ---
            await context.bot.send_message(
                chat_id=user_id,
                text=f"🎉 Ваш запрос одобрен\! Ваш ключ активации:\n\n```{ACTIVATION_KEY}```",
                parse_mode='MarkdownV2'
            )
            # Редактируем сообщение у администратора, чтобы показать, что запрос обработан
            await query.edit_message_text(text=f"✅ Запрос от пользователя {user_id} одобрен. Ключ отправлен.")
        
        elif action == 'decline':
            # Сообщаем пользователю об отказе
            await context.bot.send_message(chat_id=user_id, text="😔 К сожалению, ваш запрос на получение ключа был отклонен.")
            # Редактируем сообщение у администратора
            await query.edit_message_text(text=f"❌ Запрос от пользователя {user_id} отклонен.")

def main() -> None:
    """Запуск бота."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()