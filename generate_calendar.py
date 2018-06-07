from generate_keywords import *
import os
from PIL import Image, ImageFont, ImageDraw

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Configurations
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

calendar_id = '1'
path_to_project = './'

# parameters for keyword generation
language = 'en' #'en' #'fr'
seed_page_id = 'Flower' # go on wikipedia and copy past last part of URL..
n_days = 200


# list of unwanted substrings
unwanted_strings = ['wiki','Wiki','Category', 'List', 'Template', 'Help', 'ISO', 'User']

# parameters for image fetching
output_dir = path_to_project+'generated_calendars/Calendar_'+calendar_id #default output dir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# color option: 'BW', 'orange', 'red', b='blue', 'green', None
color_opt = None

#parameters images
path_font = path_to_project + 'NotoSans_Bold.ttf'
width = 1170
height = 824
margin = int(height/10)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Get keywords and semantical links
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

calendar_keywords= generate_keywords(output_dir,
                                     language=language,
                                     seed_page_id = seed_page_id,
                                     n_days=n_days,
                                     unwanted_strings=unwanted_strings
                                     )
# save to text file
with open(output_dir+'/calendar_keywords', 'w') as f:
    for item in calendar_keywords:
        f.write("%s\n" % item)



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Format calendar
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
with open (output_dir+'/calendar_keywords', "r") as myfile:
    calendar_keywords=myfile.readlines()
for i in range(len(calendar_keywords)):
    calendar_keywords[i] = calendar_keywords[i].replace('\n', '')

days = [n_days - i for i in range(n_days)]
for i in range(n_days):
    day = days[i]
    keyword  = calendar_keywords[i]
    img = Image.new('RGBA', (width, height), color='white')
    image = Image.open(output_dir+'/Day'+str(day)+'_'+keyword)
    w,h = image.size
    ratio = min(width / w, (height-margin) / h)
    if width/w<(height-margin)/h:
        mode='side'
    else:
        mode='top'
    image = image.resize((int(w*ratio),int(h*ratio)))
    w,h = image.size
    # compute position top left corner
    if mode=='side':
        left_pos = 0
        top_pos = int((height-margin-h)/2)
    elif mode=='top':
        top_pos = 0
        left_pos = int((width-w)/2)
    # paste picture onto white background
    img.paste(image,(left_pos,top_pos))

    legend = 'Day '+str(day)+': '+keyword
    font_type = ImageFont.truetype(path_font,26)
    w_text, h_text = font_type.getsize(legend)
    left_pos_txt = int((width-w_text)/2)
    text_img = Image.new('RGBA', img.size, (255,255,255,0))
    draw = ImageDraw.Draw(text_img)
    draw.text(xy=(left_pos_txt,height-margin + int((margin-h_text)/2)), fill=(0,0,0,255), text=legend, font=font_type)
    out = Image.alpha_composite(img, text_img)
    out.save(output_dir+'/Day_'+str(day)+'.png')
