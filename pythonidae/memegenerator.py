# coding=utf-8


import io
import pathlib

from PIL import Image, ImageDraw, ImageFont


class MemeGenerator:
    def __init__(self):
        self.skyrim_font = ImageFont.truetype('impact.ttf', 60)
        self.skyrim_bg = Image.open('cogs/meme-templates/skyrimStatusMemeBackground.png', 'r')
        self.aliens_font = ImageFont.truetype('impact.ttf', 50)
        self.aliens_bg = Image.open('cogs/meme-templates/history-aliens.jpg')
        self.simply_font = ImageFont.truetype('impact.ttf', 42)
        self.simply_bg = Image.open('cogs/meme-templates/one-does-not-simply.jpg')
        self.toystory_font = ImageFont.truetype('impact.ttf', 45)
        self.toystory_bg = Image.open('cogs/meme-templates/woody-buzz.jpg')

    def skyrim(self, skill: str, level: str) -> io.BytesIO:
        """skyrim skill level meme"""

        skill = skill[:100]
        level = level[:100]
        img_size = [300, 200]
        tile_width = 300
        text = skill.upper() + ' : ' + level
        text_width, text_height = self.skyrim_font.getsize(text)
        tiles = 0
        while text_width > (img_size[0] - 100):
            img_size[0] += 300
            tiles += 1
        img = Image.new('RGB', img_size, color = '#FFF')
        for x in range(0, tile_width * (tiles + 1), tile_width):
            img.paste(self.skyrim_bg, (x, 0))
        draw = ImageDraw.Draw(img)
        posx = (img.width - text_width) / 2
        posy = (img.height - text_height) / 2
        draw.text((posx + 3, posy + 3), text, fill='black', font=self.skyrim_font)
        draw.text((posx, posy), text, fill='white', font=self.skyrim_font)

        buf = io.BytesIO()
        img.save(buf, format='png')
        buf.seek(0)
        return buf

    def oneDoesNotSimply(self, text) -> io.BytesIO:
        """
        The 'one does not simply' meme from Lord of the Rings.
        More : https://knowyourmeme.com/memes/one-does-not-simply-walk-into-mordor
        """

        text = text[:100]
        img = self.simply_bg.copy()
        draw = ImageDraw.Draw(img)

        w, h = draw.textsize(text, self.simply_font)
        self.draw_text_with_outline(draw, text, img.width / 2 - w / 2, 280, self.simply_font)
        buf = io.BytesIO()
        img.save(buf, format='png')
        buf.seek(0)
        return buf

    def historyAliensGuy(self, text) -> io.BytesIO:
        """
        History.com's Aliens guy42
        More : https://knowyourmeme.com/memes/ancient-aliens
        """

        text = text[:100]
        img = self.aliens_bg.copy()
        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(text, self.aliens_font)
        self.draw_text_with_outline(draw, text, img.width / 2 - w / 2, 377, self.aliens_font)
        buf = io.BytesIO()
        img.save(buf, format='png')
        buf.seek(0)
        return buf

    def toyStoryMeme(self, text: str) -> io.BytesIO:
        """toystory meme"""

        text = text[:100]
        img = self.toystory_bg.copy()
        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(text, self.toystory_font)
        w1, h1 = draw.textsize(text + ' Everywhere', self.toystory_font)
        self.draw_text_with_outline(draw, str(text).capitalize(), img.width / 2 - w / 2, 2, self.toystory_font)
        self.draw_text_with_outline(draw, str(text).capitalize() + ' Everywhere', img.width / 2 - w1 / 2, 250, self.toystory_font)
        buf = io.BytesIO()
        img.save(buf, format='png')
        buf.seek(0)
        return buf

    def draw_text_with_outline(
            self,
            draw: ImageDraw.Draw,
            text: str,
            x: float,
            y: int,
            fnt: ImageFont.FreeTypeFont
    ) -> None:
        draw.text((x - 2, y - 2), text, (0, 0, 0), font=fnt)
        draw.text((x + 2, y - 2), text, (0, 0, 0), font=fnt)
        draw.text((x + 2, y + 2), text, (0, 0, 0), font=fnt)
        draw.text((x - 2, y + 2), text, (0, 0, 0), font=fnt)
        draw.text((x, y), text, (255, 255, 255), font=fnt)
