#
# PyBeamIt
# A quick and easy wrapper over the justbeamit.com service to facilitate p2p file sharing in a variety of applications
# more at https://github.com/cartertemm/pybeamit
# Copyright (c) 2021 Carter Temm <cartertemm@gmail.com>
# distributed under the terms of the MIT license, which should have been included along with this code
# if not, see https://opensource.org/licenses/MIT
#


import os
import json
import mimetypes

# py 3 compat
try:
	from urllib.parse import urljoin
except (ModuleNotFoundError, ImportError):
	from urlparse import urljoin

import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor


class JustBeamItError(Exception):
	pass


class JustBeamIt:
	"""Wrapper around the justbeamit.com p2p file sharing service"""

	def __init__(self, files=[], base_url=None, backend_url=None):
		if not base_url:
			base_url = "https://www.justbeamit.com"
		self.base_url = base_url
		if not backend_url:
			backend_url = "https://www.justbeamit.com/ping?server_root=1"
		self.backend_url = backend_url
		self.backend = None
		self.token = None
		self.files = files
		if isinstance(self.files, str):
			self.files = [self.files]

	def get_backend(self):
		"""returns the API backend URL. This is called internally along with tokenise... So basic usage doesn't require interaction from the caller"""
		r = requests.get(self.backend_url)
		r.raise_for_status()
		self.backend = r.json()["serverRoot"]

	def tokenise(self):
		"""Initiates the transfer with a backend server, returning a URL for download.
		note: This must be called on the sender's machine."""
		if not self.files:
			raise JustBeamItError("no files provided")
		if not self.backend:
			self.get_backend()
		files = [
			(
				{
					"fileName": os.path.basename(i),
					"fileSize": os.path.getsize(i),
					"fileExtensionType": os.path.splitext(i)[1][1:],
				}
			)
			for i in self.files
		]
		r = requests.post(
			self.backend + "/token", data={"files": json.dumps(files), "type": "CLI"}
		)
		r.raise_for_status()
		self.token = r.json()["token"]
		return self.base_url + "/" + self.token

	def wait(self):
		"""Blocks until a recipient is available to receive the file."""
		# we expect a token to be generated beforehand, a transfer would be pointless otherwise
		if not self.token:
			raise JustBeamItError("must generate a token (tokenise) first")
		# a keep alive request that blocks until a recipiant is available to receive the file
		r = requests.get(
			self.backend + "/wait", params={"type": "CLI", "token": self.token}
		)
		r.raise_for_status()
		rjson = r.json()
		if "validToken" in rjson and not rjson["validToken"]:
			raise JustBeamItError("invalid token")

	def transfer(self, progress_callback=None):
		"""Perform the transfer, blocking until complete.
		progress_callback will be called internally with one parameter, percentage

		note: As of version 0.3, wait must be called first to ensure the other peer is ready to receive the file.
		"""
		if not progress_callback or not callable(progress_callback):
			progress_callback = lambda mon: None
		for i, f in enumerate(self.files):
			type = mimetypes.guess_type(f)
			file_obj = open(f, "rb")
			m = MultipartEncoder(
				{
					"file": (
						os.path.basename(f),
						file_obj,
						(type[0] if type[0] else "application/octet-stream"),
					)
				}
			)
			cb = lambda mon:progress_callback((mon.bytes_read/mon.len)*100)
			monitor = MultipartEncoderMonitor(m, cb)
			r = requests.post(
				self.backend + "/upload",
				data=monitor,
				params={"type": "CLI", "token": self.token, "index": i},
				headers={"Content-Type": monitor.content_type},
			)

	def get_info(self, url_or_token):
		"""Retrieves info about the transfer for the provided URL or token."""
		if not self.backend:
			self.get_backend()
		token = self._parse_token(url_or_token)
		info_url = urljoin(self.backend, "info")
		r = requests.get(info_url, {"token": token, "type": "CLI"})
		r.raise_for_status()
		return r.json()

	def download(self, url_or_token, path=None, progress_callback=None, chunk_size=1024):
		"""Blocking function that initiates a download.
		The downloaded file will be saved in path (if provided) otherwise the current directory.
		progress_callback will be called internally with one parameter, percentage.
		"""
		if not progress_callback or not callable(progress_callback):
			progress_callback = lambda mon: None
		if not self.backend:
			self.get_backend()
		token = self._parse_token(url_or_token)
		download_url = urljoin(self.backend, "download")
		r = requests.get(download_url, {"token": token, "type": "CLI"}, stream=True)
		r.raise_for_status()
		# invalid tokens are indicated in the body of a request with a successful status code
		try:
			json = r.json()
			if not json.get("validToken", True):
				raise JustBeamItError("Either the provided token is invalid or the transfer hasn't yet been initiated by sender")
		except ValueError:
			pass
		length = int(r.headers["Content-Length"])
		# parse the destination filename from the Content-Disposition header
		fn = r.headers.get("Content-Disposition")
		if not fn:
			raise JustBeamItError("Failed to locate file name from Content-Disposition header")
		fn = fn[fn.find("filename=")+10:-1]
		path = os.path.join(path or os.curdir, fn)
		downloaded = 0
		with open(path, "wb") as f:
			for chunk in r.iter_content(chunk_size):
				print((downloaded/length)*100)
				downloaded += f.write(chunk)
				progress_callback((downloaded/length)*100)

	def _parse_token(self, url_or_token):
		if "/" in url_or_token:
			# trim trailing "/"
			url_or_token = url_or_token.rstrip("/")
			url_or_token = url_or_token.split("/")[-1]
		return url_or_token


# backward compatibility
justbeamitError = JustBeamItError
justBeamIt = JustBeamIt
