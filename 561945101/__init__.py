
"""
anki addon that adds filter-bar to add-on window

copyright 2019- ijgnd

This add-on modifies some functions of aqt/addons.py which is
    Copyright: Ankitects Pty Ltd and contributors


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from anki import version as anki_version
from anki.utils import isMac

old_anki = tuple(int(i) for i in anki_version.split(".")) < (2,1,20) 


"""
Anki 2.1.20 changed the AddonDialog.

So I needed some small adjustments to my original version.

but there's also one crucial line changed in the commit
"fix display errors on macOS after updating add-ons", 
https://github.com/ankitects/anki/commit/49bba16f24bfd7f1094d0328cce7bea40a64e4d3)
which replaces addonList.repaint() with addonList.reset()

This breaks my original method. My approach to filtering the QListWidget is different to filtering in other dialogs (like studydecks where you selected
the deck for the addwindow). In the latter only deck names that match
your search string are added to the widget. This approach doesn't work here
since the method selectedAddons uses the indices of the QListWidget
to query a list of all add-ons.
    def selectedAddons(self) -> List[str]:
        idxs = [x.row() for x in self.form.addonList.selectedIndexes()]
        return [self.addons[idx].dir_name for idx in idxs]
So the indices must match and all add-ons
must be in the QListWidget. But then I need to hide them which is reverted by
addonList.reset() ...
So for MacOS I must overwrite two functions which is more likely
to fail in the future and/or cause weird problems.


Overwriting also means that after enabling an add-on the list is properly 
filtered.
"""


if old_anki:
    from . import filterbar_old
else:
    from . import filterbar_max
