from generate_keywords import *
import os
from PIL import Image, ImageFont, ImageDraw


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Configurations
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

calendar_id = 'calendar2'
path_to_project = '/home/cedric/Documents/Perso/Scratch/wiki-calendar/'

# parameters for keyword generation
language = 'en' #'en' #'fr'
seed_page_id = 'wikipedia' # go on wikipedia and copy past last part of URL..
n_days = 365

shuffle_all = False # if false, pick image inside 10 first in priority

# list of unwanted substrings
unwanted_strings = ['wiki','Wiki','Category', 'List', 'Template', 'Help', 'ISO', 'User','Talk','Portal']

# parameters for image fetching
output_dir = path_to_project+'generated_calendars/Calendar_'+calendar_id #default output dir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# color option: 'BW', 'orange', 'red', b='blue', 'green', None
color_opt = None

#parameters images
path_font1 = path_to_project + 'segoeuib.ttf'
path_font2 = path_to_project + 'segoeuisl.ttf'
width = 2000
height = 1414
margin = int(height/10)
interline = 5
size_font1 = 65
size_font2 = 50


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Get keywords and semantical links
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

calendar_keywords= generate_keywords(output_dir,
                                     language=language,
                                     seed_page_id = seed_page_id,
                                     n_days=n_days,
                                     unwanted_strings=unwanted_strings,
                                     shuffle_all=shuffle_all
                                     )




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Format calendar
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def find_keywords(output_dir):
    list_files = os.listdir(output_dir)
    keywords = []
    for i in range(365):
        file = [f for f in list_files if f'Day{i+1}_' in f]
        if len(file) == 1:
            assert len(file) == 1
            file = file[0]
            keywords.append('_'.join(file.split('_')[1:])[:-4])
    return keywords

calendar_keywords = find_keywords(output_dir)

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

   #legend
    text_img = Image.new('RGBA', img.size, (255,255,255,0))
    draw = ImageDraw.Draw(text_img)
    
    legend1 = str(day)
    legend2 = keyword
    font_type1 = ImageFont.truetype(path_font1,size_font1)
    font_type2 = ImageFont.truetype(path_font2, size_font2)
    w_l1, h_l1 = font_type1.getsize(legend1)
    w_l2, h_l2 = font_type2.getsize(legend2)

    
    left_pos_l1 = int((width-w_l1)/2)
    left_pos_l2 = int((width-w_l2)/2)
    
   
    # legend2=str(legend2.encode('utf-8'))
    if '–' in legend2:
        legend2 = '-'.join(legend2.split('–'))
    try:
        legend2.encode("windows-1252").decode("utf-8", errors='replace')
    except:
        pass


    # legend2 = seed_page_id
    draw.text(xy=(left_pos_l1,height-margin/2 - h_l1-interline/2), fill=(0,0,0,255), text=legend1, font=font_type1)
    draw.text(xy=(left_pos_l2,height-margin/2 +interline/2), fill=(0,0,0,255), text=legend2, font=font_type2)
   
    #save
    out = Image.alpha_composite(img, text_img)
    out = out.convert('RGB')
    out.save(output_dir+'/Day_'+str(365-day)+'.jpg')
