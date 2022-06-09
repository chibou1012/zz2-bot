import json
import os
import discord
import requests
import asyncio
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("Discord_Token")

client = discord.Client()


@client.event
async def on_ready():
    # channel = await client.fetch_channel(os.getenv('Channel_id'))
    # await channel.send("機器人已進入頻道")
    print("DC Bot is activated")


@client.event
async def send_msg(embed):
    channel = await client.fetch_channel(os.getenv("Channel_id"))
    await channel.send(embed=embed)


ChannelStatus = False
zz2Status = False


async def Check_Online():
    global ChannelStatus
    global zz2Status
    await client.wait_until_ready()

    while True:
        

        yt_result = requests.get(
            url="https://www.youtube.com/c/KitsuKitsuCh%E7%8B%B8%E7%8B%B8%E5%85%92"
        )

        found = False

        s = BeautifulSoup(yt_result.content, "html.parser")
        scripts = s.find_all("script")
        for script in scripts:
            if '"style":"LIVE","icon":{"iconType":"LIVE"}' in script.text:
                data: str = script.text[20:-1]

                obj = json.loads(data.strip())

                title = obj["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0][
                    "tabRenderer"
                ]["content"]["sectionListRenderer"]["contents"][0][
                    "itemSectionRenderer"
                ][
                    "contents"
                ][
                    0
                ][
                    "channelFeaturedContentRenderer"
                ][
                    "items"
                ][
                    0
                ][
                    "videoRenderer"
                ][
                    "title"
                ][
                    "runs"
                ][
                    0
                ][
                    "text"
                ]

                streamURL = obj["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][
                    0
                ]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0][
                    "itemSectionRenderer"
                ][
                    "contents"
                ][
                    0
                ][
                    "channelFeaturedContentRenderer"
                ][
                    "items"
                ][
                    0
                ][
                    "videoRenderer"
                ][
                    "videoId"
                ]

                thumbnail = obj["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][
                    0
                ]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0][
                    "itemSectionRenderer"
                ][
                    "contents"
                ][
                    0
                ][
                    "channelFeaturedContentRenderer"
                ][
                    "items"
                ][
                    0
                ][
                    "videoRenderer"
                ][
                    "thumbnail"
                ][
                    "thumbnails"
                ][
                    0
                ][
                    "url"
                ]

                found = True

        try:

            if not zz2Status and found:
                ChannelStatus = True
                zz2Status = True
                
                embed = discord.Embed(title="開台啦!", description="狸狸兒 已經開台拉")
                
                embed.add_field(name="實況標題", value=title)
                embed.add_field(
                    name="實況網址",
                    value=f"https://www.youtube.com/watch?v={streamURL}",
                    inline=False,
                )
                embed.set_image(url=thumbnail)

                await send_msg(embed)
            if zz2Status and not found:
                zz2Status = False
                ChannelStatus = False
                embed = discord.Embed(title="悲報!", description="狸狸兒主播 已經關台了")

                await send_msg(embed)
        except Exception as e:
            print(str(e))

        await asyncio.sleep(1)


if __name__ == "__main__":
    # Check_Online()
    client.loop.create_task(Check_Online())
    client.run(TOKEN)
