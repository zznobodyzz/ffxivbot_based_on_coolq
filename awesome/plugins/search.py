from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, NLPResult
from common import *
from nonebot.helpers import render_expression
import requests
import bs4
from bs4 import BeautifulSoup
import urllib  
__plugin_name__ = 'search(游戏物品查询)'
__plugin_usage__ = '-search 物品名 例: -search 鞣革工作服'


def get_item_info(bs):
    get_ways = bs.find_all(class_='toctext')
    get_way = []
    if get_ways != None:
        for info in get_ways:
            if info.string == '通过商店购买' or info.string == '通过副本获得' or info.string == '通过兑换获得' or info.string == '通过使用物品获得':
                get_way.append(info.string)
    item_title = bs.find(class_='infobox-item--name-title infobox-title rarity-rare')
    if item_title == None:
        item_title = bs.find(class_='infobox-item--name-title infobox-title rarity-common')
        if item_title == None:
            return None
    item_category = bs.find(class_='infobox-item--name-category')
    item_base_list = bs.find_all(class_='infobox-item--base-stat-item')
    item_level = bs.find(class_='infobox-item--level')
    item_require = bs.find(class_='infobox-item--require')
    block_list = bs.find_all(class_='ff14-content-box-block')
    attr_list = []
    for block in block_list:
        b = block.find(class_='ff14-content-box-block--title')
        if b != None:
            if b.string != '其他站点链接' and b.string != '各语言名称' and b.string != '基本信息':
                attr_list.append(block)
    attr_msg = ''
    #获取物品名称
    if item_title != None:
        item_title_text = item_title.get_text().strip()
        if item_title.img and item_title.img.attrs["alt"]=="Hq.png":
            item_title_text += "(HQ)"
        attr_msg = '物品名称: ' + item_title_text + ' '
    #获取物品种类
    if item_category != None:
        attr_msg += item_category.string + '\n'
    #获取物品基础性能
    if item_base_list != None:
        for item_base in item_base_list:
            counter = 0
            for base in item_base.children:
                if base.string != None:
                    attr_msg += base.string
                if counter == 0:
                    attr_msg += ':'
                counter += 1
            attr_msg += '\n'
    #获取物品品级和使用限制
    if item_level != None:
        attr_msg += item_level.string + ' '
        for require in item_require.children:
            attr_msg += require.text
        attr_msg += '\n'
    #获取额外属性
    if attr_list != []:
        for block in attr_list:
            item_attr = block.find_all('p')
            if item_attr is not None:
                counter = 0
                for attr in item_attr:
                    attr_msg += attr.text.strip() + ' '
                    counter += 1
                    if counter % 2 == 0:
                        attr_msg += '\n'
            item_attr = block.find_all('li')
            if item_attr is not None:
                counter = 0
                for attr in item_attr:
                    if attr.text.strip() == '':
                        continue
                    attr_msg += attr.text.strip()
                    if attr.find('i') != None and attr.i['class'] != None:
                        if "fa-times" in attr.i['class']:
                            attr_msg += 'X'
                        elif "fa-circle-o" in attr.i['class']:
                            attr_msg += '√'
                    attr_msg += ' '
                    counter += 1
                    if counter % 2 == 0:
                        attr_msg += '\n'
            if attr_msg[-1] != '\n':
                attr_msg += '\n'
    if get_way != []:
        attr_msg += '获得方式:\n'
        wa = bs.find_all('span',class_='mw-headline')
        for span in wa:
            if span.string in get_way:
                attr_msg += span.string + '\n\t'
                if span.string == '通过兑换获得':
                    t = span.find_next('span',class_="item-baseinfo")
                    t = t.find_next('span',class_="item-baseinfo")
                    attr_msg += t.string + '\n\t'
                    t = t.find_next('td')
                    for tt in t.children:
                        if isinstance(tt, bs4.element.Tag) == False or tt.string is not None:
                            attr_msg += tt.string + '\n\t'
                    attr_msg = attr_msg[:-1]
                elif span.string == '通过使用物品获得':
                    t = span.find_next('a')
                    attr_msg += t['title'] + '\n'
                elif span.string == '通过副本获得':
                    t = span.find_next('div', class_= 'instance-list--name')
                    attr_msg += t.next_element.text + '\n'
                elif span.string == '通过商店购买':
                    t = span.find_next('p')
                    p = t.next_element
                    n = p.next_element
                    attr_msg += t.next_element + p.next_element.string 
                    if n['class'] == "item-number":
                        attr_msg += '金币'
                    attr_msg += '\n'
                    t = t.find_next('td')
                    for tt in t.children:
                        if isinstance(tt, bs4.element.Tag) == False or tt.string is not None:
                            attr_msg += tt.string + '\n\t'
                    t = t.find_next('td')
                    for tt in t.children:
                        if isinstance(tt, bs4.element.Tag) == False or tt.string is not None:
                            attr_msg += tt.string + '\n\t'
                    attr_msg = attr_msg[:-1]
                    
    attr_msg = attr_msg[:-1]
    
    return attr_msg

def search_item(name):
    head={'authority':'ff14.huijiwiki.com',
        'method':'GET',
        'path':'/wiki/%s:%s' %(urllib.parse.quote("物品"),urllib.parse.quote(name)),
        'scheme':'https',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9',
        'referer':'https://ff14.huijiwiki.com/wiki/ItemSearch?name=%s' %(urllib.parse.quote(name)),
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    search_url = "https://ff14.huijiwiki.com/wiki/" + urllib.parse.quote("物品") + ':' + urllib.parse.quote(name)
    try:
        r = requests.get(search_url, headers = head)
        bs = BeautifulSoup(r.text, 'html.parser')
        res_data = get_item_info(bs)
        if res_data == None:
            return "未找到该物品,请尝试自行搜索orz:\nhttps://ff14.huijiwiki.com/"
        return res_data
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
        return "与服务器通信错误"
    
        
   


@on_command('search', aliases=('查物品','搜物品'))
async def search(session: CommandSession):
    receive_command = session.current_arg
    name = receive_command.strip()
    send_msg = search_item(name)
    if send_msg == '':
        send_msg = "小雷没有找到" + name + '呢，你该不会是瞎填的吧'
    await session.send(send_msg)