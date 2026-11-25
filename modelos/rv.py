import asyncio
from playwright.async_api import async_playwright
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=await b.new_page(viewport={'width':1080,'height':1920})
    await pg.goto('file:///tmp/usa/rv_fixa.html'); await pg.wait_for_timeout(400)
    await pg.locator('#s').screenshot(path='/tmp/usa/rv_fixa.png',omit_background=True)
    await pg.goto('file:///tmp/usa/rv_logo.html'); await pg.wait_for_timeout(400)
    for i in range(45):
      await pg.evaluate(f'quadro({i/45})')
      await pg.screenshot(path=f'/tmp/usa/lf/{i:03d}.png',clip={'x':0,'y':150,'width':1080,'height':300},omit_background=True)
    await b.close()
asyncio.run(m())
