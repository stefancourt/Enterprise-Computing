import os
import requests
import KE
import STT
import TTS

def alexa(x):
  return apply(TTS.tts,apply(KE.ke,apply(STT.stt,x)))

def apply(f,x):
  if x != None:
    return f(x)
  else:
    return None

if __name__ == "__main__":
  t = open("question.wav","rb").read()
  u = alexa(t)
  if u != None: open("answer.wav","wb").write(u)
