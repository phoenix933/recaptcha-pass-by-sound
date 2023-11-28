import asyncio
from pyppeteer import launch
from capmonstercloudclient import CapMonsterClient, ClientOptions
from capmonstercloudclient.requests import RecaptchaV2ProxylessRequest
import random
import json
import os
import sys



current_directory = os.getcwd()


# async def save_text_as_txt(content):
#     # os.makedirs(os.path.dirname("save_datas"), exist_ok=True)
#     try:
#         with open(file_path, "w") as f:
#             json.dump(content, f)
#         # with open(file_path, "w", encoding="utf-8") as file:
#         #     file.write(content)
#     except:
#         pass


async def main():
    limit_count = 5
    count = 0
    browser = None
    url = "https://www.parkers.co.uk/car-specs/"
    browser = await launch(
        options={
            "headless": False,#True
            # "ignoreDefaultArgs": "--disable extensions",
            "args": [
                "--no-sandbox",
                "--disable-setuid-sandbox",
            ],
        }
    )
    await browser.setDefaultTimeout(3000)
    page = await browser.newPage()
    await page.goto(url)
    
    
    await page.waitFor(2000)
    
    
    try:
        # oneModal = await page.querySelector("#onesignal-slidedown-cancel-button")
        # await oneModal.click()
        oneModal = await page.querySelector("button.message-component.message-button.no-children.focusable.sp_choice_type_11.last-focusable-el")
        await oneModal.click()
    except Exception as e:
        print(e)
    
    
    
    
    
    
    
    
    
    
    txt_vrm_lookup = await page.querySelector("input.vrm-lookup__input")
    await txt_vrm_lookup.type("RJ59FGO",{"delay":100})
    
    await page.waitFor(1000)
    
    # txt_vrm_button = await page.querySelector("button.vrm-lookup__button.button")
    # await txt_vrm_button.click()
    
    await page.keyboard.press('Tab')
    await page.waitFor(1000)
    await page.keyboard.press('Space')
        
    element = await page.querySelector("#g-recaptcha")
    website_key = await page.evaluate(
        '(element) => element.getAttribute("data-sitekey")', element
    )

    capMonsterOptions = ClientOptions(
        api_key="3e79c97ba8afa9fb6bd60335e0e2b852"
    )

    task_id = RecaptchaV2ProxylessRequest(  # ! HcaptchaRequest
        websiteUrl=url,
        websiteKey=website_key,
    )

    cap_monster_client = CapMonsterClient(options=capMonsterOptions)

    solution = await cap_monster_client.solve_captcha(task_id)
    print(solution)
    if solution:
        captcha_key = solution["gRecaptchaResponse"]

    await page.waitFor(2000)
    await page.waitForSelector("iframe")
    await page.evaluate(
        "(element, captchaKey) => element.value = captchaKey",
        await page.querySelector('textarea[name="g-recaptcha-response"]'),
        captcha_key,
    )
    await page.waitFor(2000)
    # await page.evaluate(
    #     "(element) => element.click()",
    #     await page.querySelector('button.vrm-lookup__button.button')
    # )
    await page.waitFor(20000000)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    # asyncio.get_event_loop().run_until_complete(save_text_as_txt(f'{token}.json',"HERE"))
