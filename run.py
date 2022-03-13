# -*- coding: UTF-8 -*-
import discord
import os
import random
import asyncio
from discord.ext import commands
import requests
from discord.ext.commands import CommandNotFound
from bs4 import BeautifulSoup
import re
import time
import datetime

# 시작

game = discord.Game("!급식")
bot = commands.Bot(command_prefix='!', status=discord.Status.online, activity=game, help_command=None)

vipColor = 0xaaffaa
imgLink = "https://cdn.discordapp.com/avatars/709953013908766842/a_b892f915dbfc15ceedf8fb75e84b24ba.gif?size=256"


@bot.event
async def on_ready():
    print("봇 시작")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


@bot.command()
async def 급식(ctx, str2=None, str3=None):
    if (str(ctx.author) == "서노#4375"):
        vipColor = 0xdf93c9
        imgLink = "https://cdn.discordapp.com/attachments/712086754307604533/838389103699165184/adadxs.gif"
    elif (str(ctx.author) == "JUGU#0613"):
        vipColor = 0x03fcba
        imgLink = "https://cdn.discordapp.com/attachments/798809167414427671/831441525018722324/mobile2.png"
    elif (str(ctx.author) == "두 름#1111"):
        vipColor = 0xb6abf6
        imgLink = "https://media.discordapp.net/attachments/795638550112239646/841252480771817482/f3d9d176398c5d86.png?width=602&height=602"
    elif (str(ctx.author) == "젠_#7510"):
        vipColor = 0x99ccff
        imgLink = "https://cdn.discordapp.com/attachments/712113092061822986/897650525338755142/unknown.png"
    else:
        vipColor = 0xaaffaa
        imgLink = "https://cdn.discordapp.com/avatars/709953013908766842/41631d6066b3638f5c055b018a55db5d.webp?size=160"

    current = datetime.datetime.now()
    tomorrow = current + datetime.timedelta(days=1)

    if (str2 == None or str2 == "오늘" or str2 == "점심" or str2 == "중식"):
        embed = discord.Embed(title=f":fork_and_knife:   __**겜마고 급식 정보**__", color=vipColor)
        date = ""
        date += str(current.year)
        date += "."
        if (current.month < 10):
            date += "0"
        date += str(current.month)
        date += "."
        date += str(current.day)

        weekday = int(time.strftime('%w', time.localtime(time.time())))
        diet = get_diet(2, str(date), weekday - 1)
        embed.add_field(
            name=f"\n:spoon:" + str(current.year) + "년 " + str(current.month) + "월 " + str(current.day) + "일 급식\n",
            value=f"\n\n" + diet + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
        embed.set_image(
            url="https://media.discordapp.net/attachments/780946215918632990/841259194450575360/5ec527db3bc4f1de.png?width=960&height=228")
    elif (str2 == "내일"):
        embed = discord.Embed(title=f":fork_and_knife:   __**겜마고 급식 정보**__", color=vipColor)
        date = ""
        date += str(tomorrow.year)
        date += "."
        if (current.month < 10):
            date += "0"
        date += str(tomorrow.month)
        date += "."
        date += str(tomorrow.day)

        weekday = int(time.strftime('%w', time.localtime(time.time())))
        diet = get_diet(2, date, weekday)
        embed.add_field(
            name=f"\n:spoon:" + str(tomorrow.year) + "년 " + str(tomorrow.month) + "월 " + str(tomorrow.day) + "일 급식\n",
            value=f"\n\n" + diet + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
        embed.set_image(
            url="https://media.discordapp.net/attachments/780946215918632990/841259194450575360/5ec527db3bc4f1de.png?width=960&height=228")
    elif (str2 == "도움"):
        embed = discord.Embed(title=f":fork_and_knife:   __**명령어**__", color=0xffaaaa)
        embed.add_field(name=f"**!급식 도움**", value=f" - :speech_balloon: 지금 이 메세지를 출력합니다.", inline=False)
        embed.add_field(name=f"**!급식 (오늘)**", value=f" - :spoon: 오늘의 급식을 알려줍니다.", inline=False)
        embed.add_field(name=f"**!급식 내일**", value=f" - :fork_and_knife: 내일의 급식을 알려줍니다.", inline=False)
        embed.add_field(name=f"**!급식 n월n일**", value=f" - :date: 해당되는 날짜의 급식을 알려줍니다.", inline=False)
        embed.add_field(name=f"**!급식 조식(아침)**", value=f" - :chopsticks: 내일의 조식을 알려줍니다.", inline=False)
        embed.add_field(name=f"**!급식 석식(저녁)**", value=f" - :fork_knife_plate: 오늘의 석식을 알려줍니다.", inline=False)
        embed.add_field(name=f"**!급식 간식**", value=f" - :burrito: 오늘의 간식을 알려줍니다.", inline=False)
        embed.add_field(name=f"**!급식 봇정보**", value=f" - :robot: 봇의 정보를 알려줍니다.", inline=False)
        embed.set_image(
            url="https://media.discordapp.net/attachments/780946215918632990/841259194450575360/5ec527db3bc4f1de.png?width=960&height=228")
    elif (str2 == "봇정보"):
        embed = discord.Embed(title=f":information_source: **봇 정보**", color=0xaaaaff)
        embed.set_author(name="겜마고 급식 봇",
                         icon_url="https://cdn.discordapp.com/avatars/823727241573040149/413b9a35a35ae9c49b9c299358eb81cc.png?size=256")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/823727241573040149/413b9a35a35ae9c49b9c299358eb81cc.png?size=256")
        embed.add_field(name=":speech_balloon: **이름**", value="겜마고 급식 봇   ", inline=True)
        embed.add_field(name=":speech_balloon: **설명**", value="경기게임마이스터고 급식 정보를\n제공합니다.", inline=True)
        embed.set_image(
            url="https://media.discordapp.net/attachments/780946215918632990/841259194450575360/5ec527db3bc4f1de.png?width=960&height=228")
        embed.add_field(name="**만든이**", value="이준협", inline=False)
        embed.set_footer(text="마지막 업데이트 날짜 : 2021-05-10")
        await ctx.send(embed=embed)
        return
    elif (str2 == "조식" or str2 == "아침"):
        embed = discord.Embed(title=f":fork_and_knife:   __**겜마고 급식 정보**__", color=vipColor)

        date = ""
        if (tomorrow.month < 10):
            date += "0"

        if (current.hour >= 0):
            if (current.hour <= 1):
                date += str(current.month)
            else:
                date += str(tomorrow.month)
        date += "."

        if (current.hour >= 0):
            if (current.hour <= 1):
                date += str(current.day)

        if (current.hour > 1):
            date += str(tomorrow.day)

        if (date == "03.14"):
            diet = "순대국밥\n백미밥\n의성마늘햄구이\n삼색계란찜\n아삭이고추무침\n섞박지\n씨리얼&우유\n버터롤*딸기잼\n"
        elif (date == "03.15"):
            diet = "백미밥\n김치콩나물국\n돈갈비찜\n해물완자전\n동부묵김가루무침\n열무김치\n씨리얼&우유&후라이\n마들렌\n"
        elif (date == "03.16"):
            diet = "맥모닝*해시브라운\n새우살볶음밥\n치킨텐더\n푸실리샐러드\n씨리얼&우유\n포기김치\n바나나\n"
        elif (date == "03.17"):
            diet = "백미밥\n양송이스프\n등심돈까스\n쫄면야채무침\n건포도단호박범벅\n깍두기\n씨리얼&우유\n크로와상&딸기잼\n"
        elif (date == "03.18"):
            diet = "백미밥\n순두부백탕\n오징어제육불고기\n도톰동그랑땡\n양배추쌈*쌈장\n포기김치\n씨리얼&우유&후라이\n조각사과\n"
        elif (date == "03.21"):
            diet = "백미밥\n쇠고기무국\n훈제오리*무쌈\n꽈리어묵채볶음\n청포묵김가루무침\n포기김치\n씨리얼&우유&후라이\n모닝빵&잼\n"
        elif (date == "03.22"):
            diet = "백미밥\n얼큰육개장\n순살가자미튀김\n모듬소세지야채볶음\n파채콩나물무침\n알타리김치\n씨리얼&우유\n방울토마토\n"
        elif (date == "03.23"):
            diet = "셀프햄버거\n굴소스야채볶음밥\n치즈스틱*케찹\n콘샐러드\n씨리얼&우유\n포기김치\n파인애플\n"
        elif (date == "03.24"):
            diet = "백미밥\n시금치된장국\n돈육김치두루치기\n야채튀김\n레몬미역초무침\n깍두기\n씨리얼&우유\n후라이\n미니와플&잼\n"
        elif (date == "03.25"):
            diet = "백미밥\n사골조랭이떡국\n찢은고기메란장조림\n치킨링강정\n해파리냉채\n포기김치\n씨리얼&우유\n슈크림파이\n"
        else:
            embed.add_field(name=f"\n:spoon:" + str(tomorrow.year) + "년 " + str(tomorrow.month) + "월 " + str(
                tomorrow.day) + "일 (내일) 조식\n", value=f"\n\n" + "조식 정보가 없습니다." + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.",
                            inline=False)
            embed.set_image(
                url="https://media.discordapp.net/attachments/780946215918632990/841259194450575360/5ec527db3bc4f1de.png?width=960&height=228")
            embed.set_footer(text="만든 애 : 이준협", icon_url=imgLink)
            await ctx.send(embed=embed)
            return

        if (current.hour >= 0):
            if (current.hour <= 1):
                embed.add_field(name=f"\n:spoon:" + str(current.year) + "년 " + str(current.month) + "월 " + str(
                    current.day) + "일 (오늘) 조식\n", value=f"\n\n" + diet + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.",
                                inline=False)
                embed.set_image(
                    url="https://media.discordapp.net/attachments/780946215918632990/841259194450575360/5ec527db3bc4f1de.png?width=960&height=228")

        if (current.hour > 1):
            embed.add_field(name=f"\n:spoon:" + str(tomorrow.year) + "년 " + str(tomorrow.month) + "월 " + str(
                tomorrow.day) + "일 (내일) 조식\n", value=f"\n\n" + diet + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.",
                            inline=False)
            embed.set_image(
                url="https://media.discordapp.net/attachments/780946215918632990/841259194450575360/5ec527db3bc4f1de.png?width=960&height=228")


    elif (str2 == "석식" or str2 == "저녁"):
        embed = discord.Embed(title=f":fork_and_knife:   __**겜마고 급식 정보**__", color=vipColor)

        date = ""
        if (current.month < 10):
            date += "0"
        date += str(current.month)
        date += "."
        date += str(current.day)

        if (date == "03.14"):
            diet = "베이컨굴소스볶음밥\n팽이미소국\n왕새우튀김&타르소스\n피망비엔나볶음\n오이무침\n포기김치\n"
        elif (date == "03.15"):
            diet = "잡곡밥\n오징어고추장국\n고구마닭갈비\n두부적조림\n멕시칸샐러드\n포기김치\n"
        elif (date == "03.16"):
            diet = "토마토스파게티\n빅미트볼조림\n추가밥\n마늘바게트\n팝만두케이준샐러드\n포기김치\n망고쥬스\n"
        elif (date == "03.17"):
            diet = "잡곡밥\n북어국\n돈육보쌈\n쌀떡고기산적조림\n쪽파무말랭이무침\n배추겉절이\n매실음료\n"
        elif (date == "03.18"):
            diet = "돈부리덮밥\n백미밥\n고추장찌개\n햄감자채볶음\n도토리묵무침\n깍두기\n"
        elif (date == "03.21"):
            diet = "백미밥\n중국식계란탕\n마파두부덮밥소스\n꿔바로우탕수\n단무지무침\n포기김치\n요구르트\n"
        elif (date == "03.22"):
            diet = "백미밥\n호박고추장국\n바베큐폭찹\n고구마고로케\n오색탕평채\n포기김치\n"
        elif (date == "03.23"):
            diet = "백미밥\n냉이된장국\n돈육두반장볶음\n흑임자깐풍기\n파인애플치커리무침\n깍두기\n"
        elif (date == "03.24"):
            diet = "잡곡밥\n어묵쑥갓국\n두찜st.로제찜닭\n타코야끼&가쓰오부시\n옥수수콘샐러드\n열무김치\n허니버터아몬드\n"
        elif (date == "03.25"):
            diet = "잡곡밥\n북어국\n오징어돈육볶음\n버섯잡채\n브로컬리*초장\n포기김치\n"
        else:
            embed.add_field(
                name=f"\n:spoon:" + str(current.year) + "년 " + str(current.month) + "월 " + str(current.day) + "일 석식\n",
                value=f"\n\n" + "석식 정보가 없습니다." + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
            embed.set_image(
                url="https://media.discordapp.net/attachments/780946215918632990/841259194450575360/5ec527db3bc4f1de.png?width=960&height=228")
            embed.set_footer(text="만든 애 : 이준협", icon_url=imgLink)
            await ctx.send(embed=embed)
            return

        embed.add_field(
            name=f"\n:spoon:" + str(current.year) + "년 " + str(current.month) + "월 " + str(current.day) + "일 석식\n",
            value=f"\n\n" + diet + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
        embed.set_image(
            url="https://media.discordapp.net/attachments/780946215918632990/841259194450575360/5ec527db3bc4f1de.png?width=960&height=228")
    elif (str2 == "간식"):
        embed = discord.Embed(title=f":fork_and_knife:   __**겜마고 급식 정보**__", color=vipColor)

        date = ""
        if (current.month < 10):
            date += "0"
        date += str(current.month)
        date += "."
        date += str(current.day)

        if (date == "03.2"):
            diet = "쵸코카스테라\n빙그레단지바나나우유\n"
        elif (date == "03.3"):
            diet = "햄샌드위치\n오렌지쥬스\n"
        elif (date == "03.4"):
            diet = "감동란(훈제란) 2개\n사이다\n쵸코파이\n"
        elif (date == "03.7"):
            diet = "핫도그*케찹\n쵸코우유\n"
        elif (date == "03.8"):
            diet = "김가루주먹밥\n떠먹는요플레\n후렌치파이\n"
        elif (date == "03.10"):
            diet = "조각피자\n콜라\n"
        elif (date == "03.11"):
            diet = "순살양념치킨\n얼라이브망고주스\n"
        else:
            embed.add_field(
                name=f"\n:spoon:" + str(current.year) + "년 " + str(current.month) + "월 " + str(current.day) + "일 간식\n",
                value=f"\n\n" + "광현이가 안줘서 간식 정보가 없습니다." + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
            embed.set_footer(text="만든 애 : 이준협", icon_url=imgLink)
            await ctx.send(embed=embed)
            return

        embed.add_field(
            name=f"\n:spoon:" + str(current.year) + "년 " + str(current.month) + "월 " + str(current.day) + "일 간식\n",
            value=f"\n\n" + diet + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.", inline=False)
    else:
        if (str2 != None and str3 == None):
            if (str2.find("월") == -1 or str2.find("일") == -1):
                await ctx.send("\"!급식 도움\"을 입력하여 명령어를 확인하세요.")
                return
            else:
                embed = discord.Embed(title=f":fork_and_knife:   __**겜마고 급식 정보**__", color=vipColor)
                inputMonth = str2.split("월")[0]
                inputDay = str2.split("월")[1]
                inputDay = inputDay.split("일")[0]
                customDay = datetime.date(int(datetime.datetime.now().year), int(inputMonth), int(inputDay))

                if (not inputMonth.isdigit() or int(inputMonth) < 1 or int(inputMonth) > 12):
                    await ctx.send("날짜를 정확히 입력해주세요.\n\"!급식 도움\"을 입력하여 명령어를 확인하세요.")
                    return

                if (not inputDay.isdigit() or int(inputDay) < 1 or int(inputDay) > 31):
                    await ctx.send("날짜를 정확히 입력해주세요.\n\"!급식 도움\"을 입력하여 명령어를 확인하세요.")
                    return

                date = ""
                date += str(datetime.datetime.now().year)
                date += "."
                if (int(inputMonth) < 10):
                    date += "0"
                date += inputMonth
                date += "."
                date += inputDay

                weekday = int(customDay.weekday())
                diet = get_diet(2, str(date), weekday)
                embed.add_field(
                    name=f"\n:spoon:" + str(datetime.datetime.now().year) + "년 " + str(inputMonth) + "월 " + str(
                        inputDay) + "일 급식\n", value=f"\n\n" + diet + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.",
                    inline=False)
        elif ((str2 != None and str3 != None)):
            if (str2.find("월") != -1 and str3.find("일") != -1):
                embed = discord.Embed(title=f":fork_and_knife:   __**겜마고 급식 정보**__", color=vipColor)
                inputMonth = str2.split("월")[0]
                inputDay = str3.split("일")[0]
                customDay = datetime.date(int(datetime.datetime.now().year), int(inputMonth), int(inputDay))

                if (not inputMonth.isdigit() or int(inputMonth) < 1 or int(inputMonth) > 12):
                    await ctx.send("날짜를 정확히 입력해주세요.\n\"!급식 도움\"을 입력하여 명령어를 확인하세요.")
                    return

                if (not inputDay.isdigit() or int(inputDay) < 1 or int(inputDay) > 31):
                    await ctx.send("날짜를 정확히 입력해주세요.\n\"!급식 도움\"을 입력하여 명령어를 확인하세요.")
                    return

                date = ""
                date += str(datetime.datetime.now().year)
                date += "."
                if (int(inputMonth) < 10):
                    date += "0"
                date += inputMonth
                date += "."
                date += inputDay
                weekday = int(customDay.weekday())
                diet = get_diet(2, str(date), weekday)
                embed.add_field(
                    name=f"\n:spoon:" + str(datetime.datetime.now().year) + "년 " + str(inputMonth) + "월 " + str(
                        inputDay) + "일 급식\n", value=f"\n\n" + diet + "\n\"!급식 도움\"을 입력하여 더 많은 명령어를 확인하세요.",
                    inline=False)
            else:
                await ctx.send("\"!급식 도움\"을 입력하여 명령어를 확인하세요.")
                return
        else:
            await ctx.send("\"!급식 도움\"을 입력하여 명령어를 확인하세요.")
            return
    embed.set_footer(text="만든 애 : 이준협", icon_url=imgLink)
    await ctx.send(embed=embed)


@급식.error
async def message_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("!급식 (오늘) 또는 !급식 내일")
    if isinstance(error, commands.BadArgument):
        await ctx.send("잘못된 입력입니다.")


@bot.command()
async def 급식공지(ctx, *, msg):
    if (str(ctx.author) == "이준협#7777"):
        embed = discord.Embed(title=f":warning:  __**공지사항**__", color=0xff4444)
        embed.add_field(name=f"**급식 관련**", value=f"" + msg, inline=False)
        embed.set_footer(text="만든 애 : 이준협",
                         icon_url="https://cdn.discordapp.com/avatars/709953013908766842/a_b892f915dbfc15ceedf8fb75e84b24ba.gif?size=256")
        await bot.get_guild(795318898656018444).get_channel(795320243772981258).send(embed=embed)


def get_html(url):
    _html = ""
    resp = requests.get(url)
    if resp.status_code == 200:
        _html = resp.text
    return _html


def get_diet(code, ymd, weekday):
    schMmealScCode = code  # int
    schYmd = ymd  # str

    num = weekday + 1  # int 0월1화2수3목4금5토6일

    URL = (
            "https://stu.goe.go.kr/sts_sci_md01_001.do?"
            "schulCode=J100000476&schulCrseScCode=4&schulKndScCode=04"
            "&schMmealScCode=%d&schYmd=%s" % (schMmealScCode, schYmd)
    )
    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.find_all("tr")
    element = element[2].find_all('td')
    try:
        element = element[num]  # num
        element = str(element)
        element = element.replace('[', '')
        element = element.replace(']', '')
        element = element.replace('<br/>', '\n')
        element = element.replace('<td class="textC last">', '')
        element = element.replace('<td class="textC">', '')
        element = element.replace('</td>', '')
        element = element.replace('(h)', '')
        element = element.replace('.', '')
        element = re.sub(r"\d", "", element)
    except:
        element = " "
    return element


access_token = os.environ['BOT_TOKEN']
bot.run(access_token)
