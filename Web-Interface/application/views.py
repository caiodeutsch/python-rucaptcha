from flask import Response, render_template, request
from application import app
import os
import random
import json
import requests

from .key_captcha_parser import key_captcha_data_handler
from .solve_media_captcha_check import SolveMedia
from .dbconnect import Database


@app.route('/', methods=["GET", "POST"])
@app.route('/index/', methods=["GET", "POST"])
def index():
    payload = {
        "common_captcha_source": common_captcha_source(),
        "fun_captcha_source": fun_captcha_source(),
        "text_captcha_source": text_captcha_source(),
        "key_captcha_data": key_captcha_data_handler(),
        "media_captcha_source": media_captcha_source()
    }
    # Обработка ПОСТ запросов
    if request.method == 'POST':
        # Обработка solvemedia капчи
        if "solvemedia_btn" in request.form:
            return SolveMedia().answer_handler(request.form["adcopy_response"],
                                               request.form["adcopy_challenge"],
                                               request.environ['REMOTE_ADDR'])

        # обработка обычной капчи-изображения
        elif 'common_captcha_btn' in request.form:
            pass

        # обработка капчи-текста
        elif 'text_captcha_btn' in request.form:
            pass

    return render_template('base.html', doc='/index.html', payload=payload)


@app.route('/invisible_recaptcha/', methods=["GET", "POST"])
def invisible_recaptcha():
    # Обработка ПОСТ запросов
    if request.method == 'POST':
        if "recaptcha_invisible_btn" in request.form:
            print(request.form)

    return render_template('base.html', doc='/invisible_recaptcha.html')


# Функция которая возвращает рандомное изображение обычной капчи
def common_captcha_source():
    # Получаем список всех изображений и возвращаем рандомную картинку
    images_list = os.listdir('application/static/image/common_image_example/')
    return random.choice(images_list)


# Функция которая возвращает рандомное изображение обычной капчи
def fun_captcha_source():
    # Получаем список всех изображений и возвращаем рандомную картинку
    images_list = os.listdir('application/static/image/fun_captcha_example/')
    return random.choice(images_list)


# Функция которая возвращает рандомное изображение обычной капчи
def media_captcha_source():
    # Получаем список всех изображений и возвращаем рандомную картинку
    images_list = os.listdir('application/static/media/solvemedia_audio/')
    return random.choice(images_list)


# Функция которая возвращает рандомный вопрос текстовой капчи
def text_captcha_source():
    # Получаем список всех изображений и возвращаем рандомную картинку
    text_captcha_list = Database().get_text_captcha()
    return random.choice(text_captcha_list)


'''
API responses
'''


@app.route('/api/', methods=["GET", "POST"])
def api():
    # Обработка ПОСТ запросов
    if request.method == 'POST':
        # Обработка обычной капчи
        if "common_captcha_btn" in request.form:
            # Проверяем капчу и ответ на соответсвие
            return common_captcha_answer(request.form["common_captcha_src"],
                                         request.form["common_captcha_answer"])

        # Solvemedia капча
        elif "solvemedia_btn" in request.form:
            return SolveMedia().answer_handler(request.form["adcopy_response"],
                                               request.form["adcopy_challenge"],
                                               request.environ['REMOTE_ADDR'])

    # Обработка ГЕТ запросов
    elif request.method == 'GET':
        if "get_common_captcha" in request.args["captcha_type"]:
            data = {'captcha_src': "http://85.255.8.26/static/image/common_image_example/" + common_captcha_source()}

            js = json.dumps(data)

            response = Response(js, status=200, mimetype='application/json')
            response.headers['Link'] = 'http://85.255.8.26/'
            return response


# Обработчик капчи изображением
def common_captcha_answer(captcha_name, user_answer):
    if user_answer == captcha_name.split(".")[0]:
        data = {'request': 'OK'}

        js = json.dumps(data)

        response = Response(js, status=200, mimetype='application/json')
        response.headers['Link'] = 'http://85.255.8.26/'

        return response
    else:
        data = {'request': 'FAIL'}

        js = json.dumps(data)

        response = Response(js, status=200, mimetype='application/json')
        response.headers['Link'] = 'http://85.255.8.26/'

        return response


# ERRORS
@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', doc='mistakes/404.html')


@app.errorhandler(500)
def page_not_found(e):
    return render_template('base.html', doc='mistakes/500.html')
