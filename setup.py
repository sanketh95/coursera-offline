from setuptools import setup

setup(
	name = "coursera_offline",

	version = "0.1.1",

	author="Sanketh Mopuru",
	author_email="sanketh.mopuru@gmail.com",

	url='https://github.com/sanketh95/coursera-offline',
	license='GPLv3',

	description = 'Download Coursera videos for offline viewing',

	install_requires=[
		"pyquery"
	],


	scripts=['coursera_offline']
	)