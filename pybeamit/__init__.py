import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import os
import json
import mimetypes

class justbeamitError(Exception):
	pass

class justBeamIt:
	"""Wrapper around the justbeamit.com p2p file sharing service"""

	def __init__(self, files=[], base_url=None, backend_url=None):
		if not base_url:
			base_url="https://www.justbeamit.com"
		self.base_url=base_url
		if not backend_url:
			backend_url="https://www.justbeamit.com/ping?server_root=1"
		self.backend_url=backend_url
		self.backend=None
		self.token=None
		self.files=files
		if not self.files:
			raise justbeamitError("no files provided")
		if type(self.files)==str:
			self.files=[self.files]

	def get_backend(self):
		"""returns the API backend URL. This is called internally along with tokenise... So basic usage doesn't require interaction from the caller"""
		r=requests.get(self.backend_url)
		r.raise_for_status()
		self.backend=r.json()["serverRoot"]

	def tokenise(self):
		"""constructs data and returns the token (http://justbeamit.com/token) needed for downloading"""
		if not self.backend:
			self.get_backend()
		files=[({"fileName": os.path.basename(i), "fileSize": os.path.getsize(i), "fileExtensionType": os.path.splitext(i)[1][1:]}) for i in self.files]
		r=requests.post(self.backend+"/token", data={"files": json.dumps(files), "type": "CLI"})
		r.raise_for_status()
		self.token=r.json()["token"]
		return self.base_url+"/"+self.token

	def transfer(self, progressCallback=None):
		"""blocking function that does all the hard work. First wait for a recipient, then perform the transfer.
		progressCallback will be called internally with one parameter, percentage"""
		if not progressCallback:
			progressCallback=lambda mon:None
		#we expect a token to be generated beforehand, a transfer would be pointless otherwise
		if not self.token:
			raise justbeamitError("must generate a token (tokenise) first")
		r=requests.get(self.backend+"/wait",params={"type": "CLI", "token": self.token})
		#a keep alive request that blocks until a recipiant is available to receive the file
		r.raise_for_status()
		rjson=r.json()
		if "validToken" in rjson and not rjson["validToken"]:
			raise justbeamitError("invalid token")
		for i, f in enumerate(self.files):
			type=mimetypes.guess_type(f)
			file_obj=open(f, "rb")
			m=MultipartEncoder({"file": (os.path.basename(f), file_obj, (type[0] if type[0] else "application/octet-stream"))})
			monitor=MultipartEncoderMonitor(m, progressCallback)
			r=requests.post(self.backend+"/upload", data=monitor, params={"type": "CLI", "token": self.token, "index": i}, headers={"Content-Type": monitor.content_type})