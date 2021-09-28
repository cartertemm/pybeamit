import sys
import os
from pybeamit import justBeamIt


url = sys.argv[1]
j = justBeamIt()
if not os.path.isdir("downloaded"):
	os.mkdir("downloaded")
j.download(url, path="downloaded", progress_callback=lambda f:print(f))
