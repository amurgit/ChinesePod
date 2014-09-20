# -*- coding: utf-8 -*-
import os
import re
import shutil
from os.path import join, getsize
from pyquery import PyQuery as pq

input_dir = '/home/dx/ChinesePod/'
output_dir = '/home/dx/Desktop/CP/'
needftypes = ['Dialog', 'HTML_text', 'Podcast']
#find . \( -name *.rar \) | xargs -I {} unrar x {}

def getlevel(lessonid):
	level = ''
	if lessonid.find('A') == 0: level = '1 Newbie'
	if lessonid.find('B') == 0: level = '2 Elementary'
	if lessonid.find('C') == 0: level = '3 Intermediate'
	if lessonid.find('D') == 0: level = '4 Upper-Intermediate'
	if lessonid.find('E') == 0: level = '5 Advanced'
	if lessonid.find('F') == 0: level = '6 Media'
	if lessonid.find('Q') == 0: level = 'Qing Wen'
	return level

def getlessonid(filename):
	lid = re.sub('([A-F][0-9]{4}).*', r'\1', filename)
	if re.match('[A-F][0-9]+$',lid):
		return lid
	else:
		lid = re.sub('(QW[0-9]{4}).*', r'\1', filename)
		if re.match('QW[0-9]+$',lid):
			return lid
		else:
			return ''

def getftype(filename):
	ftype = ''
	if re.match('([A-F]|QW)[0-9]{4}dg', filename): ftype = 'Dialog'
	if re.match('([A-F]|QW)[0-9]{4}\.html?', filename): ftype = 'HTML_text'
	if re.match('([A-F]|QW)[0-9]{4}trad\.html?', filename): ftype = 'Trad_HTML_text'
	if re.match('([A-F]|QW)[0-9]{4}pr', filename): ftype = 'Podcast'
	if re.match('([A-F]|QW)[0-9]{4}rv', filename): ftype = 'Review'
	if re.match('([A-F]|QW)[0-9]{4}\.pdf', filename): ftype = 'PDF_text'
	if re.match('([A-F]|QW)[0-9]{4}trad\.pdf', filename): ftype = 'Trad_PDF_text'
	return ftype

allfilesd = {}
allfilesl = []
for root, dirs, files in os.walk(input_dir):
	for file1 in files:
		if file1.endswith('.html') or file1.endswith('.htm'):
			lessonid = getlessonid(file1)
			if re.match('([A-F]|QW)[0-9]+$',lessonid):
				level = getlevel(lessonid)
				link = join(root, file1)
	 			doc = pq(filename = link)
	 			theme = doc.find('h1').text().split(' - ')[-1].replace('Key Vocabulary Supplementary Vocabulary','')
	 			theme = re.sub('\([A-FQ][0-9]+\)','', theme).strip()
	 			theme = re.sub('\(QQW[0-9]+\)','', theme).strip()
	 			allfilesl.append(lessonid)
	 			allfilesd[lessonid] = {'id': lessonid, 'theme': theme, 'level': level}

i = 0
for root, dirs, files in os.walk(input_dir):
	for file1 in files:
		lessonid = getlessonid(file1)
		ftype = getftype(file1)
		if lessonid and lessonid in allfilesl and ftype and ftype in needftypes:
			old_fullpath = join(root, file1)
			out_subdir = output_dir+allfilesd[lessonid]['level']
			if not os.path.exists(out_subdir):
				os.makedirs(out_subdir)
			out_subsubdir = out_subdir+'/'+ftype
			if not os.path.exists(out_subsubdir):
				os.makedirs(out_subsubdir)

			fformat = file1.split('.')[-1]
			fname = '.'.join(file1.split('.')[:-1])
			new_fname = fname+' '+allfilesd[lessonid]['theme']+'.'+fformat
	 		new_fname = new_fname.replace('/',' on ')
	 		new_fname = new_fname.replace('?',u'？')
	 		new_fname = new_fname.replace(':',' -') #Android fix
			new_fullpath = out_subsubdir+'/'+new_fname
			old_path = (root+'/'+file1).replace('//','/')
	 		i = i+1
	 		if not os.path.isfile(new_fullpath):
				shutil.copyfile(old_path, new_fullpath)
				print '#'+str(i)+' '+new_fullpath.encode('utf-8')

# print 'Rename tracks ok.'
