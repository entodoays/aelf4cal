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
print('Création du dossier %s sur le Bureau\nLe programme téléchargera les textes pour 4 semaines.\nÀ la fin, ajoutez le ficher index.html en Calibre.\n' % Base_folder)
next_date = Base_date
user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0'
headers={'User-Agent':user_agent,} 
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
		<div style="line-height:150%; text-align: center;">
		"""
def aelf_unescape(link,filename):
		try: 
			request=urllib.request.Request(link,None,headers) #The assembled request
			response = urllib.request.urlopen(request)
			html_heure = response.read()
			html_heure = html_heure.decode('utf-8')
			output_file = open(filename, "w", encoding='utf-8')
			output_file.write(str(html_heure))
		except urllib.error.URLError as e:
			print(e.reason)
		return
#Download the files for 4 weeks
for i in range(1, 29):   
		print ('Téléchargement des textes de %s-%s-%s...' % (next_date.strftime("%d"), next_date.strftime("%m"), next_date.strftime("%y")))
		next_folder = r'%s-%s-%s' % (next_date.strftime("%y"), next_date.strftime("%m"), next_date.strftime("%d"))
		if not os.path.exists(next_folder): os.makedirs(next_folder)
		os.chdir(next_folder)
		site_date = "%s-%s-%s" % (next_date.year, next_date.strftime("%m"), next_date.strftime("%d"))
		next_link = "http://www.aelf.org/%s/romain/messe" % (site_date)
		aelf_unescape(next_link,'0_Messe.html')
		laudes_link = "http://www.aelf.org/%s/romain/laudes" % (site_date)
		aelf_unescape(laudes_link,'1_Laudes.html')
		lectures_link = "http://www.aelf.org/%s/romain/lectures" % (site_date)
		aelf_unescape(lectures_link,'2_Lectures.html')
		tierce_link = "http://www.aelf.org/%s/romain/tierce" % (site_date)
		aelf_unescape(tierce_link,'3_Tierce.html')
		sexte_link = "http://www.aelf.org/%s/romain/sexte" % (site_date)
		aelf_unescape(sexte_link,'4_Sexte.html')
		none_link = "http://www.aelf.org/%s/romain/none" % (site_date)
		aelf_unescape(none_link,'5_None.html')
		vepres_link = "http://www.aelf.org/%s/romain/vepres" % (site_date)
		aelf_unescape(vepres_link,'6_Vepres.html')
		complies_link = "http://www.aelf.org/%s/romain/complies" % (site_date)
		aelf_unescape(complies_link,'7_Complies.html')
		try: 
			request=urllib.request.Request(next_link,None,headers) #The assembled request
			response = urllib.request.urlopen(request)
			html_doc = response.read()
			html_doc = html_doc.decode('utf-8')
		except urllib.error.URLError as e:
			print(e.reason)
		#Extract ordo and create day index file
		soup = BeautifulSoup(html_doc, "lxml")
		ordo_text = soup.find("div", {"class": "heading-day"})
		text_file = open("index.html", "w", encoding='utf-8')
		for hidden in ordo_text.find_all("div", {"class": ['btn btn-default btn-aelf btn-red m-t-10', 'btn btn-default btn-aelf myDatePicker', 'dropdown m-t-10', 'block-buttons-navigation only-tablet m-t-10']}):
				hidden.decompose()
		for hidden in ordo_text.find_all("a", {"class": ['btn btn-default btn-aelf myDatePicker', 'btn btn-default btn-aelf btn-red m-t-10']}):
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
		<div style="text-align: center; font-size:130%;">
		"""
		if i != 1:
			hier = next_date + datetime.timedelta(days=-1)
			part4 = "<a href=\"../" + str(r'%s-%s-%s' % (hier.strftime("%y"), hier.strftime("%m"), hier.strftime("%d"))) + "/index.html\">Jour-</a>&nbsp;&nbsp;<a href=\"../index.html\">Retour</a>"
		else:
			part4 = """
		<a href="../index.html">Retour</a>
		"""
		if i != 63:
			demain = next_date + datetime.timedelta(days=1)
			part5 = "&nbsp;&nbsp;<a href=\"../" + str(r'%s-%s-%s' % (demain.strftime("%y"), demain.strftime("%m"), demain.strftime("%d"))) + "/index.html\">Jour+</a></div></body>"
		else:
			part5 = "</div></body></html>"
		joined = "%s%s%s%s%s" % (part1, ordo_text, part3, part4, part5)
		text_file.write(joined)
		text_file.close()
		#Clean pages
		for filename in os.listdir('.'):
				if re.match(r'\d.*', filename):
						with open(filename, 'rb') as messy:
								soup = BeautifulSoup(messy, "lxml")
						messy.close()
						while True:
							h2 = soup.find('h2')
							if not h2:
								break
							h2.name = 'h3'
						for remove in soup.find_all(attrs={'class':['menu-secondary-mobile', 'col-sm-3 col-md-2', 'col-sm-5 col-md-5', 'col-sm-7', 'col-sm-9 col-md-5', 'container-toolbar']}):
								remove.decompose()
						for remove in soup.find_all(id=['middle-col', 'toolbar', 'menu-mobile', 'header']):
								remove.decompose()
						for remove in soup.find_all('script'):
								remove.decompose()
						cleaned = str(soup)
						with_retour = re.sub(r'</body>', r'<div style="text-align: center; font-size:130%; line-height:150%"><a href="index.html">Retour</a></div></body>', cleaned)
						with_retour = re.sub(r'(</br>){2,}', r'\n <p>&nbsp;</p> \n', with_retour) #Remove extra blank lines
						with_retour = re.sub(r'</br/>\s?</br/>', r'\n <p>&nbsp;</p> \n', with_retour) #replace <br> <br> with empty paragraphs
						output_file = open(filename, "w", encoding='utf-8')
						output_file.write(with_retour)
		# Go to parent folder and add 1 day
		os.chdir("..")
		if next_date.weekday() == 6:
				date_link = '<br><b><a href="%s/index.html">%s-%s</a></b>&nbsp; |&nbsp; ' % (next_folder, next_date.strftime("%d"), next_date.strftime("%m")) #Add link to main index
		else:
				date_link = '<a href="%s/index.html">%s</a>&nbsp; |&nbsp; ' % (next_folder, next_date.strftime("%d")) #Add link to main index
		main_index = main_index + date_link
		next_date = Base_date + datetime.timedelta(days=i)
#Close main index file
print('\nPréparation de l\'index (à ajouter à Calibre)')
main_index = main_index + '</div><div>© AELF</div></body></html>'
text_file = open("index.html", "w", encoding='utf-8')
text_file.write(main_index)
text_file.close()
