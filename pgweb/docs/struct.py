from django.db import connection
from core.models import Version

def get_struct():
	currentversion = Version.objects.get(current=True)

	# Can't use a model here, because we don't (for some reason) have a
	# hard link to the versions table here
	curs = connection.cursor()
	curs.execute("SELECT d.version, d.file, v.docsloaded, v.testing FROM docs d INNER JOIN core_version v ON v.tree=d.version ORDER BY d.version DESC")

	# Start priority is higher than average but lower than what we assign
	# to the current version of the docs.
	docprio = 0.8
	lastversion = None

	for version, filename, loaded, testing in curs.fetchall():
		# Decrease the priority with 0.1 for every version of the docs
		# we move back in time, until we reach 0.1. At 0.1 it's unlikely
		# to show up in a general search, but still possible to reach
		# through version specific searching for example.
		if lastversion != version:
			if docprio > 0.2:
				docprio -= 0.1
			lastversion = version

		yield ('docs/%s/static/%s' % (version==0 and 'devel' or version,
									  filename),
			   testing and 0.1 or docprio, # beta/rc versions always get 0.1 in prio
			   loaded)

		# Also yield the current version urls, with the highest
		# possible priority
		if version == currentversion.tree:
			yield ('docs/current/static/%s' % filename,
				   1.0, loaded)
