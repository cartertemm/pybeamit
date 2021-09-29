import sys
import os
from pybeamit import JustBeamIt


url = sys.argv[1]
j = JustBeamIt()
if not os.path.isdir("downloaded"):
	os.mkdir("downloaded")
j.download(url, path="downloaded", progress_callback=lambda f:print(f))
