# -*- coding: utf-8 -*-


# standard library modules
import io
import pathlib

# third-party packages
from PIL import Image, ImageDraw, ImageFont


class MemeGenerator:
    def __init__(self) -> None:
        """initializer"""

        # fonts
        font_directory = 'resources/fonts'
        font_name = 'impact.ttf'
        font_path = str(pathlib.Path(font_directory, font_name))
        self.skyrim_font = ImageFont.truetype(font_path, 60)
        self.aliens_font = ImageFont.truetype(font_path, 50)
        self.simply_font = ImageFont.truetype(font_path, 42)
        self.simply_font_small = ImageFont.truetype(font_path, 28)
        self.toystory_font = ImageFont.truetype(font_path, 45)

        template_directory = 'resources/images/meme-templates'

        skyrim_template_name = 'skyrimStatusMemeBackground.png'
        skyrim_template_path = str(pathlib.Path(template_directory, skyrim_template_name))
        self.skyrim_bg = Image.open(skyrim_template_path, 'r')

        aliens_template_name = 'history-aliens.jpg'
        aliens_template_path = str(pathlib.Path(template_directory, aliens_template_name))
        self.aliens_bg = Image.open(aliens_template_path, 'r')

        simply_template_name = 'one-does-not-simply.jpg'
        simply_template_path = str(pathlib.Path(template_directory, simply_template_name))
        self.simply_bg = Image.open(simply_template_path, 'r')

        toystory_template_name = 'woody-buzz.jpg'
        toystory_template_path = str(pathlib.Path(template_directory, toystory_template_name))
        self.toystory_bg = Image.open(toystory_template_path, 'r')

    def skyrim(self, skill: str, level: str) -> io.BytesIO:
        """skyrim skill level meme"""

        skill = skill[:100]
        level = level[:100]
        img_width = 300
        img_height = 200
        tile_width = img_width
        text = skill.upper() + ' : ' + level
        text_width, text_height = self.skyrim_font.getsize(text)
        tiles = 0
        while text_width > (img_width - 100):
            img_width += 300
            tiles += 1
        img = Image.new('RGB', (img_width, img_height), color = '#FFF')
        for x in range(0, tile_width * (tiles + 1), tile_width):
            img.paste(self.skyrim_bg, (x, 0))
        draw = ImageDraw.Draw(img)
        text_x = (img.width - text_width) / 2
        text_y = (img.height - text_height) / 2
        draw.text(
            (text_x + 3, text_y + 3),
            text,
            fill='black',
            font=self.skyrim_font
        )
        draw.text(
            (text_x, text_y),
            text,
            fill='white',
            font=self.skyrim_font
        )
        buf = io.BytesIO()
        img.save(buf, format='png')
        buf.seek(0)
        return buf

    def oneDoesNotSimply(self, text: str) -> io.BytesIO:
        """
        The 'one does not simply' meme from Lord of the Rings.
        More:
        https://knowyourmeme.com/memes/one-does-not-simply-walk-into-mordor
        """

        text = text.upper()
        if len(text) > 15:
            font = self.simply_font_small
            wrap = True
            small = True
        else:
            font = self.simply_font
            wrap = False
            small = False
        if wrap:
            sz = 30
            text = text[:100]
            l = [[]]
            cnt = 0
            for word in text.split():
                if (new_cnt := cnt + len(word)) <= sz:
                    l[-1].append(word)
                    cnt = new_cnt
                else:
                    cnt = len(word)
                    l.append([word])
            text = '\n'.join(' '.join(x) for x in l)
            lines = text.count('\n')
        else:
            lines = 1
        img = self.simply_bg.copy()
        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(text, font)
        if small:
            bottom_text_y = 285
            bottom_text_y -= 25 * lines
        else:
            bottom_text_y = 280
        self.draw_text_with_outline(
            draw,
            text,
            img.width / 2 - w / 2,
            bottom_text_y,
            font
        )
        buf = io.BytesIO()
        img.save(buf, format='png')
        buf.seek(0)
        return buf

    def historyAliensGuy(self, text: str) -> io.BytesIO:
        """
        History.com's Aliens guy42
        More : https://knowyourmeme.com/memes/ancient-aliens
        """

        text = text[:100]
        img = self.aliens_bg.copy()
        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(text, self.aliens_font)
        self.draw_text_with_outline(
            draw,
            text,
            img.width / 2 - w / 2,
            377,
            self.aliens_font
        )
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
        self.draw_text_with_outline(
            draw,
            str(text).capitalize(),
            img.width / 2 - w / 2,
            2,
            self.toystory_font
        )
        self.draw_text_with_outline(
            draw,
            str(text).capitalize() + ' Everywhere',
            img.width / 2 - w1 / 2,
            250,
            self.toystory_font
        )
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
