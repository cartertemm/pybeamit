# PyBeamIt

This is a python wrapper around the unofficial [just beam it](http://justbeamit.com) API. It supports both sending and receiving files.

## Installation

Via pip:
```
$ pip install pybeamit
```
Or from source:
```
$ git clone https://github.com/cartertemm/pybeamit.git
$ pip install .
```

## Usage

Integrating P2P file sharing capability in your application is extremely simple.

On the sender's machine:

```
from pybeamit import JustBeamIt

j = JustBeamIt("file.wav")
#or for multiple files:
j = JustBeamIt(("file.wav", "file2.mp3"))
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
from pybeamit import JustBeamIt

url = ""  # e.g. https://www.justbeamit.com/s8x9j
j = JustBeamIt()
j.download(url, path="dest")
```

There are also a couple [demos](https://github.com/cartertemm/pybeamit/tree/master/demos).

All operations require a JustBeamIt object:

```
class JustBeamIt(files=[], base_url=None, backend_url=None)
```

Once you have an instance, the following methods are defined:

```
tokenise()
	Initiates the transfer with a backend server, returning a URL for download.
	note: This must be called on the sender's machine.
```

```
wait()
	Blocks until a recipient is available to receive the file.
```

```
transfer(progress_callback=None)
	Perform the transfer, blocking until complete.
	progress_callback will be called internally with one parameter, percentage
	note: As of version 0.3, wait must be called first to ensure the other peer is ready to receive the file.
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
