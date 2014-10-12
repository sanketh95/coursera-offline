from setuptools import setup

setup(
	name = "coursera_offline",

	version = "0.2.4",

	author="Sanketh Mopuru",
	author_email="sanketh.mopuru@gmail.com",

	url='https://github.com/sanketh95/coursera-offline',
	license='GPLv3',

	install_requires = ['docutils>=0.3'],

	package_data = {
	        # If any package contains *.txt or *.rst files, include them:
	        '': ['*.rst', '*.md'],
	    },

	description = 'Download Coursera videos for offline viewing',

	install_requires=[
		"pyquery",
		"python-crontab"
	],

	keywords = "coursera offline download lecture lectures video videos",

	scripts=['coursera_offline']
	)