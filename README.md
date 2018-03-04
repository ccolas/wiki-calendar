# wiki-calendar
Perform a semantical exploration of Wikipedia's content and create a calendar of corresponding illustrations.

The script generate_calendar can be run to perform a semantical exploration of Wikipedia's pages and create a calendar
of corresponding illustrations. Select the number of days, the first wikipedia page and the language as parameters.

The script finds a random link in the wikipedia page, then goes to Google Image and selects on of the 10 first images.
this image, the day and the keyword are then printed on a white page, to become a calendar page.

This can be seen as an artistical project, aiming at exploring human knowledge as stored in Wikipedia by jumping from links
to links, generally related semantically. 

We use the wikipedia's api (that be found here: https://github.com/martin-majlis/Wikipedia-API) and script to scrap Google Images
(to be found here: https://gist.github.com/genekogan/ebd77196e4bf0705db51f86431099e57)

Author: Cédric Colas

Email: cdric.colas@gmail.com
