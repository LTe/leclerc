import asyncio
import os
from pyppeteer import launch
from flask import Flask, request, send_file

WAIT_TIME = 500
HEADLESS = True if os.getenv('HEADLESS') == 'true' else False

async def main():
    args = ['--no-sandbox']
    browser = await launch(handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False, headless=HEADLESS, args=args)
    page = await browser.newPage()
    await page.goto('https://www.leclerc24.pl/login/')

    await page.setViewport({'width': 1600, 'height': 900, 'deviceScaleFactor': 2});

    email_field = await page.J('input[type=email]');
    password_field = await page.J('input[type=password]')
    login_button = await page.J('button[name=login]')

    await email_field.type(os.environ.get('EMAIL'))
    await password_field.type(os.environ.get('PASSWORD'))
    await page.waitFor(WAIT_TIME)
    await login_button.click()

    await page.waitForNavigation()

    await page.goto('https://www.leclerc24.pl/order/process')

    next_action_button = await page.J('.client-panel-footer-buttons-right button')
    await page.waitFor(WAIT_TIME)
    await next_action_button.click()

    await page.waitForNavigation()
    await page.waitFor(WAIT_TIME)

    delivery_type = await page.J('label[for=deliveryType1]')
    await delivery_type.click()

    next_action_button = await page.J('.client-panel-footer-buttons-right button.btn-success')
    await next_action_button.click()

    await page.waitForNavigation()
    await page.waitFor(WAIT_TIME)

    cancel_type = await page.J('label[for=unavailable3]')
    await cancel_type.click()

    next_action_button = await page.J('.client-panel-footer-buttons-right button.btn-success')
    await next_action_button.click()

    await page.waitForNavigation()

    await page.waitFor(WAIT_TIME * 2)

    await page.screenshot({'path': '/tmp/screenshot.png', 'fullPage': True})
    await browser.close()

def delivery(request):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(main())

    f = open("/tmp/screenshot.png", "r")

    return send_file(f,
        attachment_filename = 'terminy.png',
        as_attachment=False,
        cache_timeout=-1,
        mimetype='image/png')


