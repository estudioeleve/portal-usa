import asyncio
from playwright.async_api import async_playwright
P=[('m_reelsv',1080,1920),('m_reelsv_ex',1080,1920)]
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=await b.new_page(viewport={'width':1600,'height':1920})
    for n,w,h in P:
      await pg.set_viewport_size({'width':w,'height':h}); await pg.goto(f'file:///tmp/usa/{n}.html'); await pg.wait_for_timeout(500)
      await pg.locator('#s').screenshot(path=f'/tmp/usa/{n}.png')
    await b.close()
asyncio.run(m())
