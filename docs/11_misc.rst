Misc: Markers, reports
======================
.. py:module:: mastodon
    :no-index:
.. py:class: Mastodon

Markers
-------
These functions allow you to interact with the timeline "last read" markers,
to allow for persisting where the user was reading a timeline between sessions
and clients / devices.


Reading
~~~~~~~
.. automethod:: Mastodon.markers_get

Writing
~~~~~~~
.. automethod:: Mastodon.markers_set

Reports
-------

Reading
~~~~~~~
In Mastodon versions before 2.5.0 this function allowed for the retrieval
of reports filed by the logged in user. It has since been removed.

.. automethod:: Mastodon.reports

Writing
~~~~~~~
This function allows you to report a user to the instance moderators as well as to
the users home instance.

.. automethod:: Mastodon.report
    