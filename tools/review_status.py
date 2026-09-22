# -*- coding: utf-8 -*-
"""
Review state for the scenario pages.

Two different things get called "checked" on this site and they must never be
blurred together:

  VERIFIED   Act numbers, titles, consolidation dates and section numbers. These
             are read out of the AGC text by tools/harvest.py. A machine did it
             and it is reproducible.

  REVIEWED   the plain-English explanation of what a provision does in a given
             situation. That is legal opinion in miniature. Only a person can
             sign it off, and only a person admitted to practise should.

Nothing negative is printed on the page: the standing notice at the foot of every
page carries the general position, professionally worded, and a "not yet reviewed"
badge in a reader's face helps nobody act differently. Only a positive attribution
renders. Move a scenario to "counsel" when a named person admitted to practise has
actually read it and said so, and their name and the date go on the page.
"""

DEFAULT = "checked"

STATES = {
    # Section numbers verified; the explanation has been through the internal
    # panel pass but no admitted counsel has signed it off.
    "checked": {
        "label": "",
        "tone": "neutral",
        "show": False,          # nothing on the page; the standing notice covers it
        "line": "",
    },
    # A named person admitted to practise has read the page and stands behind it.
    "counsel": {
        "label": "Counsel reviewed",
        "tone": "good",
        "show": True,
        "line": ("Act numbers, titles and section numbers on this page are verified against the "
                 "Attorney General's Chambers text, and the notes have been reviewed by counsel."),
    },
    # Something on the page is known to be contested or out of date.
    "flagged": {
        "label": "Under revision",
        "tone": "warn",
        "show": True,
        "line": ("Part of this page is under revision. Read the Act text itself before relying on "
                 "anything here."),
    },
}

# scenario id -> {"status": ..., "reviewers": [...], "date": "YYYY-MM-DD", "note": "..."}
# Anything not listed takes DEFAULT.
REVIEW = {}


def state_for(scenario_id):
    entry = REVIEW.get(scenario_id) or {}
    status = entry.get("status", DEFAULT)
    base = dict(STATES.get(status, STATES[DEFAULT]))
    base["status"] = status
    base.setdefault("show", False)
    base["reviewers"] = entry.get("reviewers") or []
    base["date"] = entry.get("date")
    base["note"] = entry.get("note")
    return base
