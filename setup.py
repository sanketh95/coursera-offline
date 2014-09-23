from distutils.core import setup

setup(
	name = "Coursera-Offline",

	version = "0.1.0",

	author="Sanketh Mopuru",
	author_email="sanketh.mopuru@gmail.com",

	packages=["argparse", "json", "sys", "urllib2", "cookielib", "random", "time","math","threading", "urllib", "os"],

	description = "Download your favorite course videos from Coursera in one go"
	long_description = open("README.md").read()

	install_requires=[
		"pyquery"
	],

	)