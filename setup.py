from setuptools import setup

setup(
	name = "coursera_offline",

	version = "0.2.5",

	author="Sanketh Mopuru",
	author_email="sanketh.mopuru@gmail.com",

	url='https://github.com/sanketh95/coursera-offline',
	license='GPLv3',

	package_data = {
	        # If any package contains *.txt or *.rst files, include them:
	        '': ['*.rst', '*.md'],
	    },

	description = 'Download Coursera videos for offline viewing',

	install_requires=[
		"pyquery>=1.2.9",
		"python-crontab>=1.8.1",
		"docutils>=0.3"
	],

	keywords = "coursera offline download lecture lectures video videos",

	scripts=['coursera_offline']
	)