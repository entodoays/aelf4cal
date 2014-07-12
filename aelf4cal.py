#!/bin/python3
import datetime, os, re, urllib.request, html.parser, locale, sys
from bs4 import BeautifulSoup
from os.path import expanduser
if sys.platform == "win32":
		locale.setlocale(locale.LC_ALL, 'fra')
else:
		locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')
home = expanduser("~")
now = datetime.datetime.now()#Get today's date
os.chdir(home)
os.chdir('Desktop') #Go to Desktop folder
Base_folder = r'Breviaire_%s-%s-%s' % (now.strftime("%d"), now.strftime("%m"), now.strftime("%y")) #All files will be stored in this date-stamped folder
if not os.path.exists(Base_folder): os.makedirs(Base_folder) #Create a folder with today's date
os.chdir(Base_folder) #Go to the freshly created folder
if now.weekday() != 6:
	idx = (now.weekday() + 1)
else:
	idx = 0
Base_date = now - datetime.timedelta(idx) #Get last Sunday's date
print('Création du dossier %s sur le Bureau\nLe programme téléchargera les textes pour 9 semaines.\nÀ la fin, ajoutez le ficher index.html en Calibre.\n' % Base_folder)
next_date = Base_date
main_index = """
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<meta content="AELF" name="Author"/>
		<meta http-equiv="content-language" content="fr">
		<title>Liturgie des Heures</title>
		</head>
		<body LANG=fr>
		<div>
		<h1>Liturgie des Heures</h1>
		</div>
		<div style="line-height: 150%;">
		<p>
		"""
def aelf_unescape(link,filename):
		"""h = html.parser.HTMLParser()
		with urllib.request.urlopen(link) as fin, open(filename, 'w', encoding='utf-8') as fout:
				for line in fin:
						fout.write(h.unescape(line.decode('utf-8')))
		fout.close()"""
		urllib.request.urlretrieve(link, filename=filename)
		return
#Download the files for 9 weeks
for i in range(1, 64):   
		print ('Téléchargement des textes de %s-%s-%s...' % (next_date.strftime("%d"), next_date.strftime("%m"), next_date.strftime("%y")))
		next_folder = r'%s-%s-%s' % (next_date.strftime("%y"), next_date.strftime("%m"), next_date.strftime("%d"))
		if not os.path.exists(next_folder): os.makedirs(next_folder)
		os.chdir(next_folder)
		site_date = "%s/%s/%s" % (next_date.day, next_date.month, next_date.year)
		next_link = "http://www.aelf.org/office-messe?desktop=1&date_my=%s" % (site_date)
		aelf_unescape(next_link,'0_Messe.html')
		laudes_link = "http://www.aelf.org/office-laudes?desktop=1&date_my=%s" % (site_date)
		aelf_unescape(laudes_link,'1_Laudes.html')
		lectures_link = "http://www.aelf.org/office-lectures?desktop=1&date_my=%s" % (site_date)
		aelf_unescape(lectures_link,'2_Lectures.html')
		tierce_link = "http://www.aelf.org/office-tierce?desktop=1&date_my=%s" % (site_date)
		aelf_unescape(tierce_link,'3_Tierce.html')
		sexte_link = "http://www.aelf.org/office-sexte?desktop=1&date_my=%s" % (site_date)
		aelf_unescape(sexte_link,'4_Sexte.html')
		none_link = "http://www.aelf.org/office-none?desktop=1&date_my=%s" % (site_date)
		aelf_unescape(none_link,'5_None.html')
		vepres_link = "http://www.aelf.org/office-vepres?desktop=1&date_my=%s" % (site_date)
		aelf_unescape(vepres_link,'6_Vepres.html')
		complies_link = "http://www.aelf.org/office-complies?desktop=1&date_my=%s" % (site_date)
		aelf_unescape(complies_link,'7_Complies.html')
		html_doc = urllib.request.urlopen(next_link).read()
		#Extract ordo
		soup = BeautifulSoup(html_doc)
		ordo_text = soup.find("div", {"class": "bloc"})
		text_file = open("index.html", "w", encoding='utf-8')
		for hidden in ordo_text.find_all("div", {"class": "date"}):
				hidden.decompose()
		for hidden in ordo_text.find_all('img'):
				hidden.decompose()
		for hidden in ordo_text.find_all(id='maBulle'):
				hidden.decompose()
		part1 = """
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		</head>
		<body>
		"""
		part3 = """
		<div style="text-align: center; font-size:130%; line-height:150%"><a href="0_Messe.html">Messe</a>&nbsp;&nbsp;|&nbsp;&nbsp;
		<a href="1_Laudes.html">Laudes</a>&nbsp;&nbsp;|&nbsp;&nbsp;
		<a href="2_Lectures.html">Lectures</a>&nbsp;&nbsp;|&nbsp;&nbsp;
		<a href="3_Tierce.html">Tierce</a>&nbsp;&nbsp;|&nbsp;&nbsp;
		<a href="4_Sexte.html">Sexte</a>&nbsp;&nbsp;|&nbsp;&nbsp;
		<a href="5_None.html">None</a>&nbsp;&nbsp;|&nbsp;&nbsp;
		<a href="6_Vepres.html">Vepres</a>&nbsp;&nbsp;|&nbsp;&nbsp;
		<a href="7_Complies.html">Complies</a>
		<br><br>
		</div>
		<div style="text-align: center; font-size:130%;"><a href="../index.html">Retour</a></div></body>
		</html>
		"""
		joined = "%s<h2>%s</h2>%s%s" % (part1, site_date, ordo_text, part3)
		text_file.write(joined)
		text_file.close()
		#Clean pages
		for filename in os.listdir('.'):
				if re.match(r'\d.*', filename):
						with open(filename, 'rb') as messy:
								soup = BeautifulSoup(messy)
						messy.close()
						while True:
							h2 = soup.find('h2')
							if not h2:
								break
							h2.name = 'h3'
						for remove in soup.find_all(attrs={'class':['clr', 'goTop', 'print_only', 'change_country', 'abonnement', 'current', 'bloc', 'degre', 'base']}):
								remove.decompose()
						for remove in soup.find_all(id=['bas', 'menuHorizontal', 'colonneDroite', 'colonneGauche', 'font-resize', 'print_link', 'titre']):
								remove.decompose()
						for remove in soup.find_all('script'):
								remove.decompose()
						for remove in soup.find_all('link', attrs={'rel':'shortcut icon'}):
								remove.decompose()
						for remove in soup.find_all('link', attrs={'rel':'rss feed'}):
								remove.decompose()
						for tag in soup.find_all('font', attrs={'size':'2'}):
							del tag['size']
						for tag in soup.find_all('font', attrs={'size':'1'}):
							del tag['size']
						for tag in soup.find_all('font', attrs={'color':'#FF0000'}):
							tag['size'] = "1"
							tag.insert(len(tag.contents), """ """)
						for tag in soup.find_all('font'):
							del tag['face']
						cleaned = str(soup)
						with_retour = re.sub(r'<!--Fin div contenu-->', r'<div style="text-align: center; font-size:130%; line-height:150%"><a href="index.html">Retour</a></div>', cleaned)
						output_file = open(filename, "w", encoding='utf-8')
						output_file.write(with_retour)
		# Go to parent folder and add 1 day
		os.chdir("..")
		if next_date.weekday() == 6:
				date_link = '</p><p><b><a href="%s/index.html">%s-%s</a></b>&nbsp; |&nbsp; ' % (next_folder, next_date.strftime("%d"), next_date.strftime("%m")) #Add link to main index
		else:
				date_link = '<a href="%s/index.html">%s-%s</a>&nbsp; |&nbsp; ' % (next_folder, next_date.strftime("%d"), next_date.strftime("%m")) #Add link to main index
		main_index = main_index + date_link
		next_date = Base_date + datetime.timedelta(days=i)
#Close main index file
print('\nPréparation de l\'index (à ajouter à Calibre)')
main_index = main_index + '</p></div><div>© AELF</div></body></html>'
text_file = open("index.html", "w", encoding='utf-8')
text_file.write(main_index)
text_file.close()
