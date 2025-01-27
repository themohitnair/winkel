from playwright.async_api import async_playwright
import asyncio

BASE_URL = "https://parents.msrit.edu/"
SUBSID = [
    "newparents",
    "parentseven",
    "parentsodd",
]


async def get_student_name(page):
    student_name_element = await page.query_selector(".cn-stu-data.cn-stu-data1 h3")

    if student_name_element:
        student_name = await student_name_element.text_content()
        return student_name.strip()
    else:
        return None


async def verify(
    usn: str, day: str, month: int, year: str, first_name: str, last_name: str
) -> bool:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        for subsidiary in SUBSID:
            await page.goto(f"{BASE_URL}{subsidiary}/")

            await page.fill("#username", usn)

            await page.wait_for_selector("#dd")
            await page.select_option("#dd", label=str(day))
            await page.select_option("#mm", label=month)
            await page.select_option("#yyyy", label=str(year))

            await page.click(".cn-login-btn")
            await asyncio.sleep(1)

            close_buttons = await page.query_selector_all(
                ".uk-button.uk-button-default.uk-modal-close"
            )
            if len(close_buttons) > 1:
                await close_buttons[1].click()
            else:
                print("Second close button not found")

            await asyncio.sleep(1)

            name = await get_student_name(page)

            exp_name = f"{first_name} {last_name}".upper()

            if exp_name == name:
                return True

            await page.screenshot(path=f"{subsidiary}.png")

        await browser.close()

        return False
