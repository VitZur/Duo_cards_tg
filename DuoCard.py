import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Разрешаем вложенные циклы событий
nest_asyncio.apply()

stored_words = {}

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я ваш бот.')

async def write(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        word = context.args[0].lower()  # Преобразуем слово в нижний регистр при записи
        user_id = update.message.from_user.id

        # Если есть уже список, добавляем в него
        if user_id in stored_words:
            words_list = stored_words[user_id]
            words_list.append(word)
            if len(words_list) > 20:
                words_list.pop(0)  # Ограничение на количество слов в 20
            stored_words[user_id] = words_list
        else:
            stored_words[user_id] = [word]

        await update.message.reply_text(f"Вы записали слово: {word}")
    else:
        await update.message.reply_text("Пожалуйста, введите слово после команды /write.")

# Измененная функция /output для вывода списка с нумерацией
async def output(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id in stored_words:
        words_list = stored_words[user_id]
        if words_list:
            # Формируем нумерованный список слов
            formatted_list = "\n".join([f"{i+1}. {word}" for i, word in enumerate(words_list)])
            total_count = len(words_list)  # Подсчитываем количество слов
            await update.message.reply_text(f"Ваши записанные слова ({total_count}):\n{formatted_list}")
        else:
            await update.message.reply_text("Ваш список слов пуст.")
    else:
        await update.message.reply_text("Вы еще не записали слова. Используйте команду /write <слово>.")

# Функция для обработки команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Чем могу помочь?')

# Функция для удаления слова по значению
async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    
    if user_id in stored_words:
        words_list = stored_words[user_id]
        
        # Проверяем, было ли передано слово для удаления
        if context.args:
            word_to_delete = context.args[0].lower()  # Преобразуем введенное слово в нижний регистр
            # Сравниваем введенное слово с каждым словом в списке (все преобразуем в нижний регистр)
            matched_word = next((word for word in words_list if word.lower() == word_to_delete), None)

            if matched_word:
                words_list.remove(matched_word)
                await update.message.reply_text(f"Удалено слово: {matched_word}")
                stored_words[user_id] = words_list  # Обновляем список
            else:
                await update.message.reply_text(f"Слово '{word_to_delete}' не найдено в списке. Попробуйте команду /output для вывода списка.")
        else:
            await update.message.reply_text("Пожалуйста, укажите слово для удаления, например, /delete <слово>.")
    else:
        await update.message.reply_text("Вы еще не записали слова. Используйте команду /write <слово>.")

# Основная функция для запуска бота
async def main():
    # Вставьте сюда ваш токен
    application = Application.builder().token("6530829888:AAESSDGHnKBE5tWJ328e3_FmxBdrQCsgnkY").build()

    # Добавляем обработчики для команд /start, /help, /write, /output и /delete
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler('write', write))
    application.add_handler(CommandHandler('output', output))
    application.add_handler(CommandHandler('delete', delete))

    # Запускаем бота и начинаем прослушивание обновлений
    await application.run_polling()

if __name__ == '__main__':
    # Запускаем main в текущем цикле событий
    asyncio.get_event_loop().run_until_complete(main())
