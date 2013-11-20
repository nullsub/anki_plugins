from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

def flip_it():
	cardCount = mw.col.cardCount()

	ids = mw.col.findCards("tag:flip-front-back")
	for id in ids:
		card = mw.col.getCard(id)
		question = card.note().__getitem__("Front");
		answer = card.note().__getitem__("Back");
		card.note().__setitem__("Front",  answer)
		card.note().__setitem__("Back", question)
		card.note().flush()
	mw.reset()
	showInfo("Finished flipping %d" % len(ids))

action = QAction("Flip front-back", mw)
mw.connect(action, SIGNAL("triggered()"), flip_it)
mw.form.menuTools.addAction(action)
