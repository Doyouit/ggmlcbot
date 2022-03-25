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

        #--------------잔류용 코드-------------
        if (date == "2022.03.26"):
            diet = "버터장조림비빔밥\n깐풍강정\n가쓰오국\n블루베리그린샐러드\n포기김치\n모닝빵츄러스\n"
        elif (date == "2022.03.27"):
            diet = "소세지하이라이스\n백미밥\n미역장국\n오곡치킨텐더*와사비마요\n크루통시저샐러드\n깍두기\n사과쿠키\n"
        #-------------------------------------

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

        #--------------잔류용 코드-------------
        if (date == "2022.03.26"):
            diet = "버터장조림비빔밥\n깐풍강정\n가쓰오국\n블루베리그린샐러드\n포기김치\n모닝빵츄러스\n"
        elif (date == "2022.03.27"):
            diet = "소세지하이라이스\n백미밥\n미역장국\n오곡치킨텐더*와사비마요\n크루통시저샐러드\n깍두기\n사과쿠키\n"
        #-------------------------------------

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

        if (date == "03.26"):
            diet = "백미밥\n닭곰탕\n찰떡궁합야채조림\n궁중떡볶이\n도토리묵야채무침\n포기김치\n씨리얼&우유\n망고푸딩\n"
        elif (date == "03.28"):
            diet = "백미밥\n부대찌개\n파닭파닭\n매콤감자조림\n달콤멸치볶음\n열무김치\n씨리얼&우유&후라이\n크로와상&잼\n"
        elif (date == "03.29"):
            diet = "불고기전골\n백미밥\n청파래오징어까스\n양념두부조림\n돌자반\n포기김치\n씨리얼&우유\n마들렌\n"
        elif (date == "03.30"):
            diet = "셀프핫도그\n깍두기볶음밥\n스마일감자*케찹\n그린샐러드*드레싱\n씨리얼&우유\n포기김치\n조각파인애플\n"
        elif (date == "03.31"):
            diet = "수육국밥\n백미밥\n김치전/해물파전\n감자꽈리조림\n청고추무침\n석박지\n씨리얼&우유\n몽키바나나도넛\n"
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

        if (date == "03.26"):
            diet = "백미밥\n브로컬리크림스프\n등심돈까스\n감자튀김&케찹\n마카로니샐러드\n포기김치\n짜요짜요\n"
        elif (date == "03.28"):
            diet = "백미밥\n\"큰\"전주식콩나물밥\n제육땅콩강정\n계란장조림\n시금치나물\n포기김치\n오렌지주스\n"
        elif (date == "03.29"):
            diet = "백미밥\n얼갈이된장국\n편마늘제육볶음\n미트볼피망조림\n명업채고추장볶음\n포기김치\n"
        elif (date == "03.30"):
            diet = "순살매콤치밥\n(백미밥)\n배추된장국\n김말이튀김\n미역줄기볶음\n포기김치\n설탕비엔나핫도그\n"
        elif (date == "03.31"):
            diet = "백미밥\n물만두계란국\n새우까스&타르소스\n불맛볶음우동\n크래미맛살겨자냉채\n포기김치\n"
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

        if (date == "03.28"):
            diet = "애플뚱모스\n석류주스\n에너지바\n"
        elif (date == "03.29"):
            diet = "김말이강정\n코코팜포도\n허쉬초코칩쿠키\n"
        elif (date == "03.30"):
            diet = "콘후레이크\n흰우유\n쵸코파이\n"
        elif (date == "03.31"):
            diet = "아메리칸샌드위치\n주스\n떠먹는요구르트\n"
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

                #--------------잔류용 코드-------------
                if (date == "2022.03.26"):
                    diet = "버터장조림비빔밥\n깐풍강정\n가쓰오국\n블루베리그린샐러드\n포기김치\n모닝빵츄러스\n"
                elif (date == "2022.03.27"):
                    diet = "소세지하이라이스\n백미밥\n미역장국\n오곡치킨텐더*와사비마요\n크루통시저샐러드\n깍두기\n사과쿠키\n"
                #-------------------------------------

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

                #--------------잔류용 코드-------------
                if (date == "2022.03.26"):
                    diet = "버터장조림비빔밥\n깐풍강정\n가쓰오국\n블루베리그린샐러드\n포기김치\n모닝빵츄러스\n"
                elif (date == "2022.03.27"):
                    diet = "소세지하이라이스\n백미밥\n미역장국\n오곡치킨텐더*와사비마요\n크루통시저샐러드\n깍두기\n사과쿠키\n"
                #-------------------------------------

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
