from WikiAPI.wikipediaapi.wikipedia import *
import numpy as np
import random
from download_google_images import *
import copy


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
                      unwanted_strings=None,
                      shuffle_all=False
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
    calendar_keywords = [seed_page.displaytitle] # stores all used keywords

    shared_categories = [''] # list of semantical links, wikipedia category shared with previous keyword
    current_page = seed_page
    previous_page = current_page
    next_page = current_page


    for day in days:
        print('Day: ', day)

        links = get_links(current_page)
        success, calendar_keywords, next_page = find_keyword_and_image_in_links(links,
                                                                                unwanted_strings,
                                                                                calendar_keywords,
                                                                                output_dir,
                                                                                day,
                                                                                shuffle_all)
        if success:  # save in case next page is not good enough
            previous_page = current_page


        # if all keywords from the current page were tried and none led to a success:
        # 1) try keywords from previous page
        # 2) use the current keyword one more time and find a picture
        if not success:
            current_page = previous_page
            links = get_links(current_page)
            success, calendar_keywords, next_page= find_keyword_and_image_in_links(links,
                                                                                   unwanted_strings,
                                                                                   calendar_keywords,
                                                                                   output_dir,
                                                                                   day,
                                                                                   shuffle_all)
            if success:
                previous_page = current_page
            else:
                calendar_keywords.append(calendar_keywords[-1])
                print(calendar_keywords[-1])
                next_page = previous_page
                filename= '/Day' + str(day) + '_' + calendar_keywords[-1]
                reject = get_google_image(calendar_keywords[-1], output_dir, filename, shuffle_all=shuffle_all)

        current_page = next_page



    print(calendar_keywords)

    #linksphere
    return calendar_keywords[1:]


def find_keyword_and_image_in_links(links, unwanted_strings, calendar_keywords, output_dir, day, shuffle_all):


    list_keys = sorted(links.keys())
    random.shuffle(list_keys)
    n_keys = len(list_keys)
    success = False
    for k in range(n_keys):
        # check for unwanted pages
        reject = False  # reject current keyword if True
        candidate_keyword = list_keys[k]
        candidate_page = links[list_keys[k]]
        # check that it has not been selected yet
        if candidate_keyword in calendar_keywords:
            reject = True  # reject keyword if keyword already used
            next_page = None
            break
        # check that it does not contain unwanted substring
        if unwanted_strings is not None:
            for strg in unwanted_strings:
                if strg in candidate_keyword:
                    reject = True
                    next_page = None
                    break

        if reject:
            break

        # check whether next page contains more than 10 links
        if len(sorted(get_links(candidate_page).keys())) < 10:
            reject = True
            next_page = None
            break
        # check that we can download a corresponding picture
        filename = '/Day' + str(day) + '_' + candidate_keyword
        reject = get_google_image(candidate_keyword, output_dir, filename, shuffle_all=shuffle_all)

        # if keyword fulfills all requirements and if we found a picture
        if not reject:
            calendar_keywords.append(candidate_keyword)  # add keyword to list
            print(calendar_keywords[-1])
            next_page = candidate_page
            success = True
            break

    return success, calendar_keywords, next_page