import os

calendar_path = "/home/cedric/Documents/Perso/Scratch/wiki-calendar/generated_calendars/Calendar_calendar1/calendar/"

text = '<div class="gallery" data-columns="3">'
for i in range(365):
    text += f'\n\t<img src="/images/projects/wiki/calendar/Day_{i}.jpg">'
text+='\n</div>'
print(text)
