# PyBeamIt

This is a python wrapper around the [just beam it](http://justbeamit.com) API of sorts.

## Usage

Integrating P2P file sharing capability in your application is extremely simple.

First, install requirements with

```pip install -r requirements.txt```

Then:

```
from pybeamit import justBeamIt

j=justBeamIt("file.wav")
#or for multiple files:
j=justBeamIt(("file.wav", "file2.mp3"))
t=j.tokenise()
print("retrieval url for recipient: "+t)
print("starting the transfer")
j.transfer()
print("done")
```

All operations require a justBeamIT object:

```
class justBeamIt(files=[], base_url=None, backend_url=None)
```

Once we have our instance, the following methods are defined:

```
tokenise()
	"""constructs data and returns the token (http://justbeamit.com/token) needed for downloading"""
```

```
transfer(progressCallback)
	"""blocking function that does all the hard work. First wait for a recipient, then perform the transfer.
	progressCallback will be called internally with one parameter, percentage"""
```

## todo

* Add support for receiving files

## contributing

Contributions are appreciated. Submit issues through the issue tracker. New features are accepted through PR's.

## see also

* [beam.py - commandline application for transfering files with just beam it](https://github.com/justbeamit/beam)
