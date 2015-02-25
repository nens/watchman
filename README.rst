watchman
==========================================

Introduction

Usage, etc.


Post-nensskel setup TODO
------------------------

Here are some instructions on what to do after you've created the project with
nensskel.

- Fill in a short description on https://github.com/lizardsystem/watchman or
  https://github.com/nens/watchman if you haven't done so already.

- Use the same description in the ``setup.py``'s "description" field.

- Fill in your username and email address in the ``setup.py``, see the
  ``TODO`` fields. If you use it, also check the ``bower.json``.

- Also add your name to ``CREDITS.rst``. It is open source software, so you
  should claim credit!

- Check https://github.com/nens/watchman/settings/collaboration if the team
  "Nelen & Schuurmans" has access.

- Add a new jenkins job at
  http://buildbot.lizardsystem.nl/jenkins/view/djangoapps/newJob or
  http://buildbot.lizardsystem.nl/jenkins/view/libraries/newJob . Job name
  should be "watchman", make the project a copy of the existing "lizard-wms"
  project (for django apps) or "nensskel" (for libraries). On the next page,
  change the "github project" to ``https://github.com/nens/watchman/`` and
  "repository url" fields to ``git@github.com:nens/watchman.git`` (you might
  need to replace "nens" with "lizardsystem"). The rest of the settings should
  be OK.

- The project is prepared to be translated with Lizard's
  `Transifex <http://translations.lizard.net/>`_ server. For details about
  pushing translation files to and fetching translation files from the
  Transifex server, see the ``nens/translations`` `documentation
  <https://github.com/nens/translations/blob/master/README.rst>`_.
