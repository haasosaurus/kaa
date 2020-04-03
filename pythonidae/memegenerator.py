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

    def skyrim(self, status: str, level: str) -> io.BytesIO:
        """skyrim skill level meme"""

        final_size = [300, 200]
        imgx = 300
        final_text = status.upper() + ' : ' + level
        offset_counter = 0
        while (self.get_size(final_text)[0] > (final_size[0] - 100) ):
            final_size[0] += 300
            offset_counter += 1
        final_image = Image.new('RGB', final_size, color = '#FFF')
        count = 0
        for x in range(0, offset_counter + 1):
            final_image.paste(self.skyrim_bg, (count, 0))
            count += imgx
        draw = ImageDraw.Draw(final_image)
        posx = (final_image.width - self.get_size(final_text)[0]) / 2
        posy = (final_image.height - self.get_size(final_text)[1]) / 2
        draw.text((posx + 3, posy + 3), final_text, fill='black', font=self.skyrim_font)
        draw.text((posx, posy), final_text, fill='white', font=self.skyrim_font)

        buf = io.BytesIO()
        final_image.save(buf, format='png')
        buf.seek(0)
        return buf

    def get_size(self, text):
        return self.skyrim_font.getsize(text)

    def oneDoesNotSimply(self, text) -> io.BytesIO:
        """
        The 'one does not simply' meme from Lord of the Rings.
        More : https://knowyourmeme.com/memes/one-does-not-simply-walk-into-mordor
        """

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
