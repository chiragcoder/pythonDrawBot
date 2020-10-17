import sys
import os
import json
import requests  # to sent GET requests
from bs4 import BeautifulSoup  # to parse HTML
from PIL import Image
import pyautogui

# from command line argument
requestedImage = sys.argv[1]
print('Requested image : ', requestedImage)


GOOGLE_IMAGE = \
    'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

SAVE_FOLDER = 'images'

# The User-Agent request header contains a characteristic string
# that allows the network protocol peers to identify the application type,
# operating system, and software version of the requesting software user agent.
# needed for google search
usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

image_name = ''

print('Starting..')

if not os.path.exists(SAVE_FOLDER):
    os.mkdir(SAVE_FOLDER)

toFind = requestedImage + ' sketch'
noOfImages = 1

print('Start searching...')

# get url query string
searchurl = GOOGLE_IMAGE + 'q=' + toFind
print(searchurl)

# request url, without usr_agent the permission gets denied
response = requests.get(searchurl, headers=usr_agent)
html = response.text

soup = BeautifulSoup(html, 'html.parser')
soup = BeautifulSoup(response.text, 'html.parser')
results = soup.findAll('img', {'class': 'rg_i Q4LuWd'})

# gathering requested number of list of image links with data-src attribute
# continue the loop in case query fails for non-data-src attributes
count = 0
links = []
for res in results:
    try:
        link = res['data-src']
        links.append(link)
        count += 1
        if (count >= noOfImages):
            break

    except KeyError:
        continue

print(f'Downloading {len(links)} images....')

# Access the data URI and download the image to a file
for i, link in enumerate(links):
    response = requests.get(link)

    #global image_name
    image_name = SAVE_FOLDER + '/' + toFind + str(i + 1) + '.jpg'
    with open(image_name, 'wb') as fh:
        fh.write(response.content)


print('Saved image : ',image_name)

# Transforming to pure black/white image..
print('Transforming to pure black/white image..')
img = Image.open(image_name)
thresh = 200
fn = lambda x : 255 if x > thresh else 0
converted = img.convert('L').point(fn, mode='1')

processedImageName = SAVE_FOLDER + '/' + requestedImage+'_processed'+'.png'
converted.save(processedImageName)

print('Transformed pure black/white image : '+processedImageName)
print(converted.width)
print(converted.height)

#Drawing starts
print('Drawing starts')

#window to Draw in drawize : x -> 637 to 1280,  y -> 135 to 555
x_padding = 637
y_padding = 135

#so that drawing dosent go out of window
max_scale_x = int(643/converted.width)
max_scale_y = int(420/converted.height)

scaleMultiplier = max_scale_x if max_scale_x < max_scale_y else max_scale_y

print('scaleMultiplier',scaleMultiplier)

count = 0
#For loop to extract and print all pixels
for y in range(converted.height):
  #print('')

  for x in range(converted.width):
    #getting pixel value using getpixel() method
    #print(x,'|',y,'|',converted.getpixel((x,y)), end='\t', sep='')
    if(converted.getpixel((x,y)) == 0):
      count = count + 1
      x_cordinate = x*scaleMultiplier + x_padding
      y_cordinate = y*scaleMultiplier + y_padding

      #To increase speed, printing every 4th pixel
      if(count%4 == 0):
        pyautogui.click(x_cordinate, y_cordinate)