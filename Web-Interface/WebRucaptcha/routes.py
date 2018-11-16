import os
import random
import json

import logme
from flask import Flask
from flask import Response, render_template, request

from WebRucaptcha.key_captcha_parser import key_captcha_data_handler
from WebRucaptcha.solve_media_captcha_check import SolveMedia
from WebRucaptcha.dbconnect import Database

from WebRucaptcha import app


@app.route('/', methods=["GET", "POST"])
@app.route('/index/', methods=["GET", "POST"])
@logme.log(config='web_log_info', name='WebRucaptcha')
def index(logger=None):
    payload = {
        "common_captcha_source": common_captcha_source(),
        "fun_captcha_source": fun_captcha_source(),
        "text_captcha_source": text_captcha_source(),
        "key_captcha_data": key_captcha_data_handler(),
        "media_captcha_source": media_captcha_source()
    }
    logger.info(f'Page - index, request - {request.method}, from - {request.remote_addr}')
    # Обработка ПОСТ запросов
    if request.method == 'POST':
        # Обработка solvemedia капчи
        if "solvemedia_btn" in request.form:
            logger.info('Media captcha button click')
            return SolveMedia().answer_handler(request.form["adcopy_response"],
                                               request.form["adcopy_challenge"],
                                               request.environ['REMOTE_ADDR'])

        # обработка обычной капчи-изображения
        elif 'common_captcha_btn' in request.form:
            logger.info('Image captcha button click')
            # Проверяем капчу и ответ на соответсвие
            return common_captcha_answer(request.form["common_captcha_src"],
                                         request.form["common_captcha_answer"])

        # обработка капчи-текста
        elif 'text_captcha_btn' in request.form:
            logger.info('Text captcha button click')
            # Проверяем капчу и ответ на соответсвие
            return text_captcha_answer(request.form["text_captcha_btn"],
                                       request.form["text_captcha_answer"])

    return render_template('base.html', doc='/index.html', payload=payload)


@app.route('/invisible-recaptcha/', methods=["GET", "POST"])
@logme.log(config='web_log_info', name='WebRucaptcha')
def invisible_recaptcha(logger=None):
    logger.info(f'Page - invisible-recaptcha, request - {request.method}, from - {request.remote_addr}')
    # Обработка ПОСТ запросов
    if request.method == 'POST':
        if "recaptcha_invisible_btn" in request.form:
            pass

    return render_template('base.html', doc='/invisible_recaptcha.html')


# Функция которая возвращает рандомное изображение обычной капчи
def common_captcha_source():
    # Получаем список всех изображений и возвращаем рандомную картинку
    images_list = os.listdir('WebRucaptcha/static/image/common_image_example/')
    return random.choice(images_list)


# Функция которая возвращает рандомное изображение обычной капчи
def fun_captcha_source():
    # Получаем список всех изображений и возвращаем рандомную картинку
    images_list = os.listdir('WebRucaptcha/static/image/fun_captcha_example/')
    return random.choice(images_list)


# Функция которая возвращает рандомное изображение обычной капчи
def media_captcha_source():
    # Получаем список всех изображений и возвращаем рандомную картинку
    images_list = os.listdir('WebRucaptcha/static/media/solvemedia_audio/')
    return random.choice(images_list)


# Функция которая возвращает рандомный вопрос текстовой капчи
def text_captcha_source():
    # Получаем список всех изображений и возвращаем рандомную картинку
    text_captcha_list = Database().get_text_captcha()
    return random.choice(text_captcha_list) if text_captcha_list else False


'''
API responses
'''


@app.route('/api/', methods=["GET", "POST"])
def api():
    # Обработка GET запросов
    if request.method == 'GET':
        if "get_common_captcha" in request.args["captcha_type"]:
            data = {'captcha_src': f"{request.host_url}static/image/common_image_example/" + common_captcha_source()}

            js = json.dumps(data)

            response = Response(js, status=200, mimetype='application/json')
            response.headers['Link'] = request.host_url
            return response
        else:
            response = Response(status=500, mimetype='application/json')
            response.headers['Link'] = request.host_url
            return response

    else:

        response = Response(status=500, mimetype='application/json')
        response.headers['Link'] = request.host_url
        return response


# Обработчик капчи изображением
def common_captcha_answer(captcha_name, user_answer):
    if user_answer == captcha_name.split(".")[0]:
        data = {'request': 'OK'}

        js = json.dumps(data)

        response = Response(js, status=200, mimetype='application/json')
        response.headers['Link'] = request.host_url

        return response
    else:
        data = {'request': 'FAIL'}

        js = json.dumps(data)

        response = Response(js, status=200, mimetype='application/json')
        response.headers['Link'] = request.host_url

        return response


# Обработчик текстовой капчи
def text_captcha_answer(captcha_id: int, user_answer: str):
    # получаем верный ответ на текстовую капчу
    truth_answer = Database().get_text_captcha_answer(question_id = captcha_id)[0]
    # сравниваем ответы и возвращаем результат
    if truth_answer == user_answer:
        data = {'request': 'OK'}

        js = json.dumps(data)

        response = Response(js, status=200, mimetype='application/json')
        response.headers['Link'] = request.host_url

        return response
    else:
        data = {'request': 'FAIL'}

        js = json.dumps(data)

        response = Response(js, status=200, mimetype='application/json')
        response.headers['Link'] = request.host_url

        return response


# ERRORS
@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', doc='mistakes/404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('base.html', doc='mistakes/500.html')
