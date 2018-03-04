from WikiAPI.wikipediaapi.wikipedia import *
import numpy as np
import random
from download_bing_images import *
from download_google_images import *



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# definition of functions to extract/print links and categories
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def print_links(page):
    links = page.links
    for title in sorted(links.keys()):
        print("%s: %s" % (title, links[title]))

def get_links(page):
    return page.links

def get_categories(page):
    return page.categories

def print_categories(page):
    categories = page.categories
    for title in sorted(categories.keys()):
        print("%s: %s" % (title, categories[title]))

def generate_keywords(output_dir,
                      language='fr',
                      seed_page_id='chat',
                      n_days=5,
                      mode='v2',
                      unwanted_strings=None,
                      ):


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Creation of first page
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    wiki_wiki = Wikipedia(language)
    seed_page = wiki_wiki.page(seed_page_id)
    assert seed_page.exists(), 'start_page does not exist, wrong id string'

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Main loop
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    days = [n_days-i for i in range(n_days)]
    calendar_keywords = [seed_page.displaytitle]
    shared_categories = [''] # list of semantical links, wikipedia category shared with previous keyword
    current_page = seed_page

    if mode == 'v1':
        for i in days:
            try:
                print('Day: ',i)
                links = get_links(current_page)
                list_keys = sorted(links.keys())
                random.shuffle(list_keys)
                n_keys = len(list_keys)
                success=False
                for k in range(n_keys):
                    # check for unwanted pages
                    reject = False
                    candidate_keyword = list_keys[k]
                    candidate_page = links[list_keys[k]]
                    # check that it has not been selected yet
                    for o in range(1):
                        if candidate_keyword in calendar_keywords:
                            reject = True
                            break
                        # check that it does not contain unwanted substring
                        if unwanted_strings is not None:
                            for strg in unwanted_strings:
                                if strg in candidate_keyword:
                                    reject=True
                                    break
                        if reject:
                            break
                        # check whether next page contains more than 5 links
                        if len(sorted(get_links(candidate_page).keys()))<10:
                            reject = True
                            break
                        # check that we can download a picture
                        filename = '/Day' + str(i) + '_' + candidate_keyword
                        reject = get_google_image(candidate_keyword, output_dir, filename)
                    if not reject:
                        calendar_keywords.append(candidate_keyword)
                        print(calendar_keywords[-1])
                        previous_page = current_page
                        current_page = candidate_page
                        success=True
                        break

                if not success:
                    calendar_keywords.append(calendar_keywords[-1])
                    print(calendar_keywords[-1])
                    current_page = previous_page
                    filename= '/Day' + str(i) + '_' + calendar_keywords[-1]
                    reject = get_google_image(calendar_keywords[-1], output_dir, filename)
            except:
                stop=1


    print(calendar_keywords)
    print(shared_categories)

    #linksphere
    return calendar_keywords[1:],shared_categories[1:]

