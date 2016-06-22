# GathererImageGatherer

#Dependencies
To run these programs you will need the python libraries BeautifulSoup, requests, imagehash, PIL, and psycopg2. 
<pre>
pip install BeautifulSoup requests imagehash PIL psycopg2
</pre>
#Use
**Download Images**
<pre>
sudo python scrapeImages.py
</pre>

Download all the card images from http://gatherer.wizards.com/Pages/Default.aspx and saves them in the folder cardImages with their name and set.

The folder of pictures ends up being 1.21 GB and takes about 25 minutes to download.
**Setup The Database**

Once you have installed postgres, type these commmands to create the database and table needed for the python script.
<pre>
create database cardimages;
create table phash(name text, set text, hash text);
</pre>

**Build The Database**
<pre>
sudo python buildDatabase.py
</pre>
Populates a table named phash in a SQLdatabase called cardimages with card name, set, and a perceptual hash of the artwork from the images downloaded with scrapeImages.py

