import justbeamit

j=justbeamit.justBeamIt("file.wav")
t=j.tokenise()
print("retrieval url: "+t)
print("starting the transfer")
j.transfer()
print("done")