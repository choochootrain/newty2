from bs4 import BeautifulSoup
import os

soup = BeautifulSoup(open(os.path.abspath('articles/Apple.html')))
title = soup.title.string # useful for when we finally plot, want to have titles in points on plot

body = soup.find('div', {'class' : 'body-copy'}) # body is a Tag object
text = body.find_all('p') # extracts all text & CrunchBase module, makes a list

string = ''.join(str(s) for s in text) # converts from list of Tag objects to HTML markup string that NLTK, or whatever sentiment analyzer we build, can run on

# 