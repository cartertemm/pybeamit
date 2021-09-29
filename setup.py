from setuptools import setup, find_packages

setup(
	name="PyBeamIt",
	version="0.4",
	packages=find_packages(),
	install_requires=open("requirements.txt", "r").read().split("\n"),
	author="Carter Temm",
	author_email="cartertemm@gmail.com",
	description="python wrapper around the just beam it file sharing API",
	license="MIT",
	url="http://github.com/cartertemm/pybeamit",
	long_description=open("readme.md", "r").read(),
	long_description_content_type="text/markdown",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Topic :: Communications :: File Sharing",
	]
)