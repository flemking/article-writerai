#! /usr/bin/env python3
import sys
import re
import os
import random

import openai
# from .config import *
import requests
# from urllib import parse
from slugify import slugify
from bs4 import BeautifulSoup

from datetime import datetime
import time


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# openai section

def write_article(api_key, the_title, final_questions, template_intro, template_chapitres, template_conclusion):
    currentDateTime = datetime.now().strftime("%Y%m%d-%H%M%S")
    openai.api_key = api_key
    

    response_intro = openai.Completion.create(model="text-davinci-003",
                                            prompt=f"{template_intro.format(the_title)}",
                                            temperature=0.77,
                                            max_tokens=503,
                                            top_p=0.49,
                                            frequency_penalty=0,
                                            presence_penalty=0
                                            )
    response_conclusion = openai.Completion.create(model="text-davinci-003",
                                                prompt=f"{template_conclusion.format(the_title)}",
                                                temperature=0.94,
                                                max_tokens=280,
                                                top_p=0.49,
                                                frequency_penalty=0,
                                                presence_penalty=0
                                                )

    paragraphs = ""
    
    
    for sous_titre in final_questions:
        
        # sous_titre = i
        # found_h3 = []
        # gen_h3 = openai.Completion.create(model="text-davinci-003",
        #                                         prompt="Faire des sous-titres sur '{}'".format(sous_titre),
        #                                         temperature=0.32,
        #                                         max_tokens=3650,
        #                                         top_p=0.5,
        #                                         frequency_penalty=0.2,
        #                                         presence_penalty=0
        #                                         ).choices[0].text

        # chapitres_templates = [
        #     {
        #         'prompt': "Rédige un long texte détaillé de nombreux paragraphes sur '{}'".format(sous_titre),
        #         'temperature':0.2,
        #         'max_tokens':3080,
        #         'top_p':0.5,
        #         'frequency_penalty':0.2,
        #         'presence_penalty':0
        #     },
        #     {
        #         'prompt': "Rédige un long texte détaillé avec des paragraphes et une liste à puces sur '{}'".format(sous_titre),
        #         'temperature':0.33,
        #         'max_tokens':3970,
        #         'top_p':0.5,
        #         'frequency_penalty':0.2,
        #         'presence_penalty':0
        #     },
        #     {
        #         'prompt': """Rédige un long texte détaillé de nombreux paragraphes sur '{}' en suivant le plan suivant : 
        #         {}
        #         NB : Il faut mentionner le sous-titre et repartir à la ligne avant de rédiger son contenu. Il faut aussi rédiger une petite phase avant de rédiger les sous-titres.""".format(sous_titre,gen_h3),
        #         'temperature':0.2,
        #         'max_tokens':3080,
        #         'top_p':0.5,
        #         'frequency_penalty':0.2,
        #         'presence_penalty':0
        #     },
        # ]

        # params = random.choice(chapitres_templates)



        response_article = openai.Completion.create(model="text-davinci-003",
                                                    prompt=f"{template_chapitres.format(the_title)}",
                                                    temperature=0.33,
                                                    max_tokens=2970,
                                                    top_p=0.5,
                                                    frequency_penalty=0.2,
                                                    presence_penalty=0
                                                )

        # sous_titre_image = openai.Image.create(
        # prompt=sous_titre,
        # n=1,
        # size="512x512"
        # )
        # #downloading the images
        # # image = parse.quote_plus(f'{the_title}_{sous_titre}_image.jpg')
        # # image_path = parse.quote(image)
        # image = slugify(f'{the_title}-{sous_titre}-image')
        # image_path = f"{BASE_DIR}/scripts/media/articles/{the_title}-{currentDateTime}/{image}.jpg"
        # with open(image_path, 'wb') as handle:
        #     response = requests.get(sous_titre_image['data'][0]['url'], stream=True)
        #     if not response.ok:
        #         print(response)
        #     for block in response.iter_content(1024):
        #         if not block:
        #             break
        #         handle.write(block)

        #adding p tags
        new_text = response_article.choices[0].text
        new_h3 = [x.strip() for x in gen_h3.split('\n')]
        ptags = [x.strip() for x in new_text.split('\n')]
        # adding h3 and li
        for h3 in new_h3:
            if h3 != '':
                new_text = new_text.replace(h3, f"<h3>{h3}</h3>")
        # text = new_text.split('\n')

        # initializing check character
        check = ['• ','- ']

        res = [x for x in ptags if x.lower().startswith(tuple(check))]
        for t in res:
            new_text = new_text.replace(t, f"<li>{t[2:]}</li>")

        for ptag in ptags:
                    if ptag != '' and '<' not in ptag:
                        new_text = new_text.replace(ptag, f"<p>{ptag}</p>")
        # print result

        soup = BeautifulSoup(new_text, "html.parser")

        ulgroup = 0
        uls = []
        for li in soup.findAll('li'):
                previous_element = li.findPrevious()
                # if <li> already wrapped in <ul>, do nothing
                if previous_element and previous_element.name == 'ul': 
                    continue 
                # if <li> is the first element of a <li> group, wrap it in a new <ul>
                if not previous_element or previous_element.name != 'li':
                    ulgroup += 1
                    ul = soup.new_tag("ul")
                    li.wrap(ul)
                    uls.append(ul)
                # append rest of <li> group to previously created <ul>
                elif ulgroup > 0:
                    uls[ulgroup-1].append(li)
        final_txt = soup.prettify()
        # print(new_h3)

        paragraphs += "\n<br/>" + "\n" + f"\n<h2>{sous_titre}</h2>\n<br/>" + "\n" + final_txt + "\n<br/>"

    # featured_image = openai.Image.create(
    # prompt=the_title,
    # n=1,
    # size="1024x1024"
    # )

    # #downloading the images
    # # image = parse.quote_plus(f'{the_title}.jpg')
    # # image_path = parse.quote(image)
    # image = slugify(f'{the_title}')
    # image_path = f"{BASE_DIR}/scripts/media/articles/{the_title}-{currentDateTime}/{image}.jpg"
    # with open(image_path, 'wb') as handle:
    #     response = requests.get(featured_image['data'][0]['url'], stream=True)
    #     if not response.ok:
    #         print(response)
    #     for block in response.iter_content(1024):
    #         if not block:
    #             break
    #         handle.write(block)

    # # Video youtube generer
    # video_iframe = found_vid(the_title)

    return f"""
    \n<h1>{the_title.upper()}</h1>
    \n<br/>{response_intro.choices[0].text}
    \n<br/>{paragraphs}
    \n<br/><h2>CONCLUSION</h2>\n {response_conclusion.choices[0].text}
    """, currentDateTime



# if __name__ == "__main__":
# @sync_to_async
def main(api_key, title, h2s, template_intro, template_chapitres, template_conclusion):
    paths = {}
    the_title = title
    final_questions = list(h2s)
    # for mc in mots_cles:
    # the_title, final_questions = get_title_and_subtitle(title, google_check)
    output, currentDateTime = write_article(api_key, the_title, final_questions, template_intro, template_chapitres, template_conclusion)
    # currentDateTime = datetime.now().strftime("%Y%m%d-%H%M%S")
    article_name = f"{the_title}-{currentDateTime}.html"
    path = f"{BASE_DIR}/scripts/media/articles/{the_title}-{currentDateTime}/{slugify(the_title)}-{currentDateTime}.html"
    with open(path, "w") as txt:
        txt.write(output)
    paths[the_title] = output
    return paths
