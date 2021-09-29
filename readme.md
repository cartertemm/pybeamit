# PyBeamIt

This is a python wrapper around the unofficial [just beam it](http://justbeamit.com) API. It supports both sending and receiving files.

## Usage

Integrating P2P file sharing capability in your application is extremely simple.

First, install requirements with

```pip install -r requirements.txt```

Then on the sender's machine:

```
from pybeamit import justBeamIt

j=justBeamIt("file.wav")
#or for multiple files:
j=justBeamIt(("file.wav", "file2.mp3"))
t=j.tokenise()
print("retrieval url for recipient: "+t)
print("waiting for recipient...")
j.wait()
print("starting the transfer")
j.transfer()
print("done")
```

On the receiving end:

```
from pybeamit import justBeamIt

url = ""  # e.g. https://www.justbeamit.com/s8x9j
j = justBeamIt()
j.download(url, path="dest")
```

There are also a couple [demos](https://github.com/cartertemm/pybeamit/tree/master/demos).

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
transfer(progress_callback=None)
	blocking function that does all the hard work. First wait for a recipient, then perform the transfer.
	progress_callback will be called internally with one parameter, the percentage of the transfer (0-100).
```

```
download(self, url_or_token, path=None, progress_callback=None, chunk_size=1024)
	Blocking function that initiates a download.
	The downloaded file will be saved in path (if provided) otherwise the current directory.
	progress_callback will be called internally with one parameter, the percentage of the transfer (0-100).
```

## contributing

Contributions are appreciated, thanks for your interest! Submit issues through the tracker. New features are accepted through PRs.

## see also

* [beam.py - commandline application for transfering files with just beam it](https://github.com/justbeamit/beam)
