from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, NLPResult
import requests
from bs4 import BeautifulSoup

__plugin_name__ = 'gas(查油价)'
__plugin_usage__ = '-gas 城市 城区'


def get_city_area_url(city):
    url = 'http://youjia.chemcp.com/youjiamap.asp'
    data = None
    try:
        web_data = requests.get(url)
        web_data.encoding = 'gbk'
        soup = BeautifulSoup(web_data.text, "html.parser")
        result = soup.find_all('a')
        c = ''
        for res in result:
            if res.string == None:
                continue
            if city in res.string:
                data = res['href']
                c = res.string
                break
        if c == '':
            return None, None
        return 'http://youjia.chemcp.com' + data, c
    except Exception as e:
        print(e)
        return None, None
        
    
def get_gas_price(url, city, area):
    data = ''
    try:
        web_data = requests.get(url)
        web_data.encoding = 'gbk'
        soup = BeautifulSoup(web_data.text, "html.parser")
        result = soup.find_all('td', attrs = {'bgcolor': '#FFFFFF'})
        for res in result:
            if area in res.string:
                index = result.index(res)
                data = city + res.string + ':\n'
                data += '89号汽油 : ' + result[index + 1].string + '\n'
                data += '92号汽油 : ' + result[index + 2].string + '\n'
                data += '95号汽油 : ' + result[index + 3].string + '\n'
                data += '0号柴油 : ' + result[index + 4].string
        if data == '':
            return '获取失败'
        else:
            return data
    except Exception as e:
        print(e)
        return '获取失败'
    


@on_command('gas', aliases=('油价'))
async def gas(session: CommandSession):
    receive_command = session.current_arg
    element = receive_command.split(' ')
    if len(element) != 2:
        await session.send(__plugin_usage__)
        return
    url, city = get_city_area_url(element[0])
    if url == None:
        await session.send('不支持的城市')
        return
    data = get_gas_price(url, city, element[1])
    await session.send(data)