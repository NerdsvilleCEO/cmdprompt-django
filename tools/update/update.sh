#!/usr/bin/env bash

#
# The idea:
#  * git-pull the repository
#  * if the repository has changed, kill off the django servers causing the app to restart
#
# Would be even better if we could touch it only after actual code files have changed,
# but this will do fine for now.

# Get to our root directory
UPDDIR=$(dirname $0)
cd $UPDDIR

# Unconditionally update the static content (we don't need to reload
# lighttpd for this, so there is no need to actually check for last
# updates or anything like that)
cd $UPDDIR/../../../pgweb-static
git pull -q >/dev/null 2>&1


# Now do a conditional update of the main repo
cd $UPDDIR

# Sleep 10 seconds to avoid interfering with the automirror scripts that
# also run exactly on the minute.
sleep 10

# Pull changes from the git repo
git pull -q >/dev/null 2>&1

# Figure out if something changed
git log -n1 --pretty=oneline > /tmp/pgweb.update
if [ -f "lastupdate" ]; then
   cmp lastupdate /tmp/pgweb.update >/dev/null 2>&1
   if [ "$?" == "0" ]; then
      # No change, so don't reload
      rm -f /tmp/pgweb.update
      exit
   fi
fi

# Cause reload
#echo Reloading website due to updates
sudo pkill -f ^python.*pgweb/manage.py

# Update the file listing the latest update
mv -f /tmp/pgweb.update lastupdate

# Hit the web app a couple of times, since in some cases lighttpd
# generates a 503 error on the first one or two hits. Make sure
# we eat these up, instead of the mirror checker or even worse,
# an end user.
wget --header "Host: www.postgresql.org" http://localhost/web_sync_timestamp -O /dev/null -q
sleep 1
wget --header "Host: www.postgresql.org" http://localhost/web_sync_timestamp -O /dev/null -q
