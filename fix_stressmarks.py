#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8

from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

import string

#cyrillic fixes
replacements = [u"О", u"о́", u"А", u"а́", u"Е", u"е́", u"И", u"и́", u"У" , u"у́", u"Ы", u"ы́", u"Э", u"э́", u"Я", u"я́", u"Ю", u"ю́"]

def flip_it():
	cardCount = mw.col.cardCount()

	ids = mw.col.findCards("")
	k = 0;
	for id in ids:
		card = mw.col.getCard(id)
		answer = card.note().__getitem__("Back");

		new_answer = answer
		for i  in range(0, int((len(replacements))/2)):
			new_answer = string.replace(new_answer, replacements[(i*2)], replacements[(i*2)+1])

		if new_answer != answer:
			print(answer +" --> " + new_answer)
			k += 1
			card.note().__setitem__("Back", new_answer)
			card.note().flush()
	mw.reset()
	showInfo("Finished fixing " + str(k) + " of " + str(len(ids)) +" cards")

action = QAction("fix stressmark", mw)
mw.connect(action, SIGNAL("triggered()"), flip_it)
mw.form.menuTools.addAction(action)
