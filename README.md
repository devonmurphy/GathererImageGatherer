# GathererImageGatherer


scrapeImage.py will download all the card images from http://gatherer.wizards.com/Pages/Default.aspx and saves them in the folder cardImages with their name and set.

buildDatabase.py will create a postgres database of card name, set, and perceptual hash of the artwork from the images downloaded with scrapeImage.py

To run these programs you will need the libraries BeautifulSoup, requests, imagehash, PIL, and psycopg2. 

You will also need a postgres database named cardimages with a table called phash. These sql statements will do that for you.

create database cardimages;
create table phash values(name text, set text, hash text);

