import sqlite3
import logme


@logme.log(config='db_log_info', name='Database')
class Database:
    def __init__(self):
        self.db_connect = sqlite3.connect('python_rucaptcha.db')
        self.db_cursor = self.db_connect.cursor()

    # Создаём таблицы для работы
    def creating_tables(self):
        self.logger.info('Text - Created table;')

        # Добавляем таблицу c текстовой капчёй
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS text_captcha(
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  captcha_text TEXT UNIQUE ,
                                  captcha_key TEXT);''')

        # Вносим изменения
        self.db_connect.commit()
    
    # Получение списка вопросов и ответов тектсовой капчи
    def get_text_captcha(self):
        try:
            self.db_cursor.execute('''SELECT id, captcha_text, captcha_key FROM text_captcha''')

            self.logger.info('Text - text captcha data selected;')

            return self.db_cursor.fetchall()
        except Exception as err:

            self.logger.error(f'Text - text captcha data NOT selected; Error - {err} .')

    # Получение списка вопросов и ответов тектсовой капчи
    def get_text_captcha_answer(self, question_id: int):
        try:
            self.db_cursor.execute(f'''SELECT captcha_key FROM text_captcha WHERE id={question_id}''')

            self.logger.info('Text - text captcha answer data selected;')

            return self.db_cursor.fetchone()
        except Exception as err:

            self.logger.error(f'Text - text captcha answer data NOT selected; Error - {err} .')

    # Закрываем соединение с БД
    def __del__(self):
        self.db_connect.close()
