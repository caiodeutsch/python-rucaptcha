from python_rucaptcha import ReCaptchaV2

import asyncio

async def run():
	try:
		result = await ReCaptchaV2.aioReCaptchaV2(rucaptcha_key='aafb515dff0075f94b1f3328615bc0fd')\
						.captcha_handler(site_key='6LcC7SsUAAAAAN3AOB-clPIsrKfnBUlO2QkC_vQ7',
		                                 page_url='http://85.255.8.26/invisible_recaptcha/')
		print(result)
	except Exception as err:
		print(err)


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(run())
	loop.close()
