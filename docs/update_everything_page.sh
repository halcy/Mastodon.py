#!/bin/bash
echo "Every function on a huge CTRL-F-able page" > 15_everything.rst
echo "=========================================" >> 15_everything.rst
echo ".. py:module:: mastodon" >> 15_everything.rst
echo ".. py:class: Mastodon" >> 15_everything.rst
echo "" >> 15_everything.rst
cat 01_general.rst 02_return_values.rst 03_errors.rst 04_auth.rst 05_statuses.rst 06_accounts.rst 07_timelines.rst 08_instances.rst 09_notifications.rst 10_streaming.rst 11_misc.rst 12_utilities.rst 13_admin.rst | grep -E "automethod|autoclass" >> 15_everything.rst
echo "" >> 15_everything.rst
