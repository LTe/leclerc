import asyncio
import os
from pyppeteer import launch
from flask import Flask, request, send_file

async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto('https://www.leclerc24.pl/login/')

    await page.setViewport({'width': 1600, 'height': 900, 'deviceScaleFactor': 2});

    email_field = await page.J('input[type=email]');
    password_field = await page.J('input[type=password]')
    login_button = await page.J('button[name=login]')

    await email_field.type(os.environ.get('EMAIL'))
    await password_field.type(os.environ.get('PASSWORD'))
    await page.waitFor(1000)
    await login_button.click()

    await page.waitForNavigation()

    search_field = await page.J('input[aria-label=Wyszukiwarka]')
    search_button = await page.J('button[title=Szukaj]')

    await search_field.type('lego')
    await page.waitFor(1000)
    await search_button.click()

    await page.waitForNavigation()

    basket_icon = await page.J("button[title='Dodaj do koszyka']")
    await basket_icon.click()
    await page.waitFor(1000)

    await page.goto('https://www.leclerc24.pl/order/process')

    next_action_button = await page.J('.client-panel-footer-buttons-right button')
    await page.waitFor(1000)
    await next_action_button.click()

    await page.waitForNavigation()
    await page.waitFor(1000)

    delivery_type = await page.J('label[for=deliveryType1]')
    await delivery_type.click()

    next_action_button = await page.J('.client-panel-footer-buttons-right button.btn-success')
    await next_action_button.click()

    await page.waitForNavigation()
    await page.waitFor(1000)

    cancel_type = await page.J('label[for=unavailable3]')
    await cancel_type.click()

    next_action_button = await page.J('.client-panel-footer-buttons-right button.btn-success')
    await next_action_button.click()

    await page.waitForNavigation()

    await page.waitFor(2000)

    await page.screenshot({'path': 'example.png', 'fullPage': True})
    await browser.close()

def delivery(request):
    asyncio.get_event_loop().run_until_complete(main())

    f = open("example.png", "r")
    file = f.read()

    return send_file(file,
        attachment_filename = 'terminy.png',
        as_attachment=True,
        mimetype='image/png')


