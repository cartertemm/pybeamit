from pybeamit import JustBeamIt


j = JustBeamIt("resources/file.wav")
t = j.tokenise()
print("retrieval URL:", t)
print("waiting for recipient...")
j.wait()
print("starting the transfer")
j.transfer(progress_callback=lambda f:print(f))
print("done")
