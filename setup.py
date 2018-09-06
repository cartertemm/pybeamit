from setuptools import setup, find_packages

setup(
	name="PyBeamIt",
	version="0.1",
	packages=find_packages(),
	install_requires=open("requirements.txt", "r").read().split("\n"),
	author="Carter Temm",
	author_email="crtbraille@gmail.com",
	description="python wrapper around the just beam it file sharing API",
	license="MIT",
	url="http://github.com/cartertemm/pybeamit",
	long_description=open("readme.md", "r").read(),
)