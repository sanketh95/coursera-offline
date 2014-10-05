from setuptools import setup

setup(
	name = "Coursera Offline",

	version = "0.1.0",

	author="Sanketh Mopuru",
	author_email="sanketh.mopuru@gmail.com",

	url='https://github.com/sanketh95/coursera-offline',
	license='GPL',

	description = "Download Coursera videos for offline viewing",
	long_description = open("README.txt").read(),

	install_requires=[
		"pyquery"
	],

	)