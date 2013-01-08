#bingPaper_v1.0.py
# Author: 			Yugarshi Mondal
# Version: 			1.0
# Description: 		This script uses PIL to modify the image
# Notes: 			The bash script passes a strings into the script. They are stored in
#					sys.argv. You can bypass this script if you just want the wallpaper and
#					no writing. I orginally used the Unity color theme to set the color of
#					the boxes, but I opted to create my own algorithm. Basically this ensures
#					that the background color of the box isn't white. You'll notice that the
#					screenshot of my desktop is different from the image this produces. I'm
#					working on a 1440x900 desktop. You'll need to move the boxes and text around
#					for the proportions to be right on another screen resolution.

# sys.argv array:
# 0. name of program
# 1."$picName"
# 2."$picAuth"
# 3."$picAssc"
# 4."$picCapt"
# 5."saveDir"
# 6."procDir"
# 7."alpha"

import Image, sys, ImageDraw, ImageFont, datetime

# initalize fontfile
fontfile = r"/usr/share/fonts/truetype/msttcorefonts/arial.ttf"

# open jpeg / save as png / reopen png
# png needs to be used, otherwise the jpeg
# compression alters the clarity of the image
im = Image.open(sys.argv[5]+sys.argv[1])

# ...create png path & reopen png
procPath = sys.argv[6]+sys.argv[1]
procPath = procPath[0:len(procPath)-4]+'.png'
im.save(procPath, "PNG")
im = Image.open(procPath)

# box color -- sum(RGB) < 550 to select dark colors, differences between RGB > 120 to avoid greys and whites
pixdata = im.load()
totR = 0
totG = 0
totB = 0
count = 0

for y in xrange(im.size[1]):
	for x in xrange(im.size[0]):
		if (sum(pixdata[x, y]) < 550) & (max(abs(pixdata[x,y][0]-pixdata[x,y][1]),abs(pixdata[x,y][2]-pixdata[x,y][1]),abs(pixdata[x,y][0]-pixdata[1,1][2])) > 120):
			totR = totR + pixdata[x,y][0]
			totG = totG + pixdata[x,y][1]
			totB = totB + pixdata[x,y][2]
			count = count + 1

# in case the previous analysis doesn't pick up any pixels
if count == 0:
	count = 1
	totR = 40
	totG = 40
	totB = 40

# create transparent boxes -- dim of top box effects lines 52 & 56 as well
bottomBox=Image.new('RGBA',(1366,35), color=(int(totR/count),int(totG/count),int(totB/count),int(sys.argv[7])))
topBox=Image.new('RGBA',(350,35), color=(int(totR/count),int(totG/count),int(totB/count),int(sys.argv[7])))

# create draw objects to write text on the bottomBox
caption = ImageDraw.Draw(bottomBox)
authInfo = ImageDraw.Draw(bottomBox)
font = ImageFont.truetype(fontfile, 11)
# ... splice together authInfo and tablulate right 
# justification (text positioned by top left corener)
authInfoText = sys.argv[2] + ' | ' + sys.argv[3]
x_width, x_dummy = authInfo.textsize(authInfoText,font = font)
# print authInfo & caption to bottomBox
authInfo.text((1287-x_width,10),authInfoText, font = font, fill = 'ghostwhite')
caption.text((80,10), sys.argv[4], font = font, fill = 'ghostwhite')

# create draw objects to write text on the topBox
todaysDate = ImageDraw.Draw(topBox)
now = datetime.datetime.now()
dateText = now.strftime("%A, %B, %d %Y")
x_width, x_dummy = todaysDate.textsize(dateText,font = font)
todaysDate.text((271-x_width,10), dateText, font = font, fill = 'ghostwhite')

# paste the box with text onto background image
im.paste(bottomBox,(0, 710, 1366, 745),mask=bottomBox)
im.paste(topBox,(1016, 65, 1366, 100),mask=topBox)
im.save(procPath)
