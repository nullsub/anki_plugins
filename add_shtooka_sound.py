#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8

import string
import os
import subprocess 
from subprocess import PIPE

from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

sound_dir = "/home/chrisu/projects/flac/"

def add_audio_to_card(card, filename):
	result = subprocess.Popen(["cp", sound_dir + filename, mw.col.media.dir() + "/" + filename], stdout=PIPE, env=my_env)
	result.wait()
	if result.returncode != 0:
		showInfo("error cp " + filename + " to media folder")
		return

	front = card.note().__getitem__("Front")
	word_audio = front + " [sound:" + filename + "]"
	card.note().__setitem__("Front", word_audio)
	card.note().flush()

def add_sound():
	cardCount = mw.col.cardCount()

	ids = mw.col.findCards("tag:add_sound")
	for id in ids:
		card = mw.col.getCard(id)
		question = card.note().__getitem__("Front")
		answer = card.note().__getitem__("Back")
		
		if "[sound:" in question:
			continue #do not try to add sound if card allready has sound

		random_chars = ["<", ">", "&", ";", ".", "?", "!", ",", "+", "-", u" ", "/"]
		for i in range(0, len(random_chars)):
			question = question.replace(random_chars[i], " ")

		found_something = False
		
		all_words = question.split(' ')

		for the_word in all_words:
			word = remove_stressmarks(the_word)

			arg = ("select count(*) from sounds where SWAC_TEXT like \'" + word + "\'")

			result = subprocess.Popen(["/usr/local/bin/swac-get", "sql", arg], stdout=PIPE, env=my_env)
			result.wait()
			output = result.communicate()[0]
			lines = output.split('\n')
			if int(lines[3]) > 1:
				arg = ("select SWAC_HOMOGRAPHIDX from sounds where SWAC_TEXT like \'" + word + "\'")
				result = subprocess.Popen(["/usr/local/bin/swac-get", "sql", arg], stdout=PIPE, env=my_env)
				result.wait()
				output = result.communicate()[0]
				translations = output.split('\n')
				files = ""
				content = False
				for i in range(0, int(lines[3])):
					if translations[3+i] != "":
						content = True
					files += ("%i) " % int(i+1)) + translations[3+i] + "\n"
				if content == False:
					arg = ("select idx from sounds where SWAC_TEXT like \'" + word + "\'")
					result = subprocess.Popen(["/usr/local/bin/swac-get", "sql", arg], stdout=PIPE, env=my_env)
					result.wait()
					output = result.communicate()[0]
					lines = output.split('\n')
					arg = ("select filename from sounds where idx like \'" + lines[3] + "\'")
				else:
					text, ok = QInputDialog.getText(mw, 'Choose word', 'Correct translation for ' +  answer + '/' + word + '\n' + files)
					found_something = True
				
					try: 
						i_input = int(text)	
					except ValueError:
						print("skipping " + word + ". Bad user input")			
						continue
					
					arg = ("select filename from sounds where SWAC_HOMOGRAPHIDX like \'" + translations[3+i_input-1] + "\'")

				result = subprocess.Popen(["/usr/local/bin/swac-get", "sql", arg], stdout=PIPE, env=my_env)
				result.wait()
				output = result.communicate()[0]
				lines = output.split('\n')
				add_audio_to_card(card, lines[3])

				found_something = True

			elif int(lines[3]) == 1:
				arg = ("select filename from sounds where SWAC_TEXT like \'" + word + "\'")
				result = subprocess.Popen(["/usr/local/bin/swac-get", "sql", arg], stdout=PIPE, env=my_env)
				result.wait()
				output = result.communicate()[0]
				lines = output.split('\n')
				add_audio_to_card(card, lines[3])
				found_something = True
			else:
				print(word)

		if found_something == False:
			card.note().addTag("no_sound")
		card.note().flush()
			
	mw.reset()
	showInfo("Finished adding sound to %d cards" % len(ids))


replacements = [u"о", u"о́", u"о" , u"о́", u"а", u"а́", u"а", u"а́", u"е", u"е́",u"е", u"е́", u"и", u"и́", u"и", u"и́",
			u"у" , u"ý", u"у" ,u"у́",  u"у" , u"у́", u"ы", u"ы́", u"ы", u"ы́", u"э", u"э́",u"э", u"э́", u"я", u"я́",
			u"я", u"я́", u"ю", u"ю́", u"ю", u"ю́", u"д", u"Д", u"к", u"К", u"й", u"й́ ", u"б", u"Б"]

def remove_stressmarks(word):
	for i in range(0, int(len(replacements)/2)):
		word = word.replace(replacements[(i*2+1)], replacements[(i*2)])
	return word


my_env = os.environ
my_env['PYTHONIOENCODING'] = 'utf-8'
action = QAction("Add shtooka sounds" , mw)
mw.connect(action, SIGNAL("triggered()"), add_sound)
mw.form.menuTools.addAction(action)

