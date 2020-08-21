Changelog of watchman
===================================================


0.1 (unreleased)
----------------

- Initial project structure created with nensskel 1.35.

- Match on pathname instead of filename.

- Auto creating 'accepted' and 'rejected' folders.

- Match relevant library versions with those of lizard-nxt to prevent this
  issue https://github.com/celery/celery/issues/4356.

- Bumped celery to 4.3

- Fixed bug with undefined connection.

- Uniquify filenames when copying to long-term storage.

- Add a 'kwargs' key to the PATTERNS in the celery config. This enables setting
  custom priority, queue, expires, etc. for some path patterns.
