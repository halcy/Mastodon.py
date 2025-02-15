#!/bin/bash
echo "Every function on a huge CTRL-F-able page" > 15_everything.rst
echo "=========================================" >> 15_everything.rst
echo ".. py:module:: mastodon" >> 15_everything.rst
echo "   :no-index:" >> 15_everything.rst
echo ".. py:class: Mastodon" >> 15_everything.rst
echo "" >> 15_everything.rst
cat 01_general.rst 02_return_values.rst 03_errors.rst 04_auth.rst 05_statuses.rst 06_accounts.rst 07_timelines.rst 08_instances.rst 09_notifications.rst 10_streaming.rst 11_misc.rst 12_utilities.rst 13_admin.rst | grep -E "automethod|autoclass" >> 15_everything.rst
echo "" >> 15_everything.rst

# Now go through 15_everything.rst and add  :no-index: to all the automethods and autoclasses
# This is because we don't want to index them, as they are already indexed in their own pages
# sed -i 's/automethod::/automethod:: :no-index:/g' 15_everything.rst
# sed -i 's/autoclass::/autoclass:: :no-index:/g' 15_everything.rst
# not quite right - the :no-index: needs to be on the next line, and we need to keep what comes after the :: (the thing to actually be documented), so capture that and put it in the replacement
sed -i 's/\(automethod::\|autoclass::\) \(.*\)/\1 \2\n   :no-index:/g' 15_everything.rst

