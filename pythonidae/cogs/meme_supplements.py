from PIL import Image, ImageDraw, ImageFont
import os

class SyrimStatusMeme:
	font = ImageFont.truetype("impact.ttf", 60)
	background = Image.open('cogs/meme-templates/skyrimStatusMemeBackground.png', 'r')
	finalText = ""
	finalSize = [300, 200]
	imgx = 300
	finalImage = None
	imageSaved = False
	saveFilename = None

	def __init__(self, status, level):
		self.finalText = status.upper() + " : " + level
		offset_counter = 0
		while (self.GetSize()[0] > (self.finalSize[0] - 100) ):
			self.finalSize[0] += 300
			offset_counter += 1
		backgroundImage = Image.new(
			'RGB',
			self.finalSize,
			color = '#FFF'
			)

		count = 0
		for x in range(0, offset_counter + 2):
			backgroundImage.paste(self.background, (count, 0))
			count += self.imgx
		draw = ImageDraw.Draw(backgroundImage)
		posx = (backgroundImage.width - self.GetSize()[0]) / 2
		posy = (backgroundImage.height - self.GetSize()[1])  / 2
		draw.text((posx + 3, posy + 3), self.finalText, fill="black", font=self.font)
		draw.text((posx, posy), self.finalText, fill="white", font=self.font)
		self.finalImage = backgroundImage

	def SaveFile(self, filename):
		self.imageSaved = True
		self.finalImage.save(filename)

	def RemoveFile(self):
		if self.imageSaved:
			os.remove(self.saveFilename)
		else:
			print("[!] Image was not saved to disk yet")

	def GetSize(self):
		return self.font.getsize(self.finalText)


def drawTextWithOutline(draw, text, x, y, fsize):
    draw.text((x-2, y-2), text,(0,0,0),font=fsize)
    draw.text((x+2, y-2), text,(0,0,0),font=fsize)
    draw.text((x+2, y+2), text,(0,0,0),font=fsize)
    draw.text((x-2, y+2), text,(0,0,0),font=fsize)
    draw.text((x, y), text, (255,255,255), font=fsize)
    return


class ClassicMemes:
	def oneDoesNotSimply(text):
		"""
		The "one does not simply" meme from Lord of the Rings. 
		More : https://knowyourmeme.com/memes/one-does-not-simply-walk-into-mordor
		"""
		img = Image.open("cogs/meme-templates/one-does-not-simply.jpg")
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype("impact.ttf", 42)
		w, h = draw.textsize(text, font)
		drawTextWithOutline(draw,text, img.width/2 - w/2, 280, font)
		img.save("out.jpg")

	def historyAliensGuy(text):
		"""
		History.com's Aliens guy42
		More : https://knowyourmeme.com/memes/ancient-aliens
		"""
		img = Image.open("cogs/meme-templates/history-aliens.jpg")
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype("impact.ttf", 50)
		w, h = draw.textsize(text, font)
		drawTextWithOutline(draw,text, img.width/2 - w/2, 377, font)
		img.save("out.jpg")

	def toyStoryMeme(text):
		img = Image.open("cogs/meme-templates/woody-buzz.jpg")
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype("impact.ttf", 45)
		w, h = draw.textsize(text, font)
		w1, h1 = draw.textsize(text + " Everywhere", font)
		drawTextWithOutline(draw,str(text).capitalize(), img.width/2 - w/2, 2, font)
		drawTextWithOutline(draw,str(text).capitalize() + " Everywhere", img.width/2 - w1/2, 250, font)
		img.save("out.jpg")

