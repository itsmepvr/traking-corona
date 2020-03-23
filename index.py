import requests
from threading import Timer
import json
import datetime
import simpleaudio as sa

class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer     = None
    self.interval   = interval
    self.function   = function
    self.args       = args
    self.kwargs     = kwargs
    self.is_running = False
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self._timer = Timer(self.interval, self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False

def getResult():
  newData = requests.get("https://corona.lmao.ninja/all")
  newData = newData.json()
  with open('data.json', 'r+') as f:
    oldData = json.load(f)
    if(oldData != newData):
      wave_obj = sa.WaveObject.from_wave_file("scream.wav")
      play_obj = wave_obj.play()
      play_obj.wait_done()
      f.seek(0)
      lastUpdated = newData['updated'] - oldData['updated']
      lastUpdated = lastUpdated/1000
      lastUpdated = str(round(lastUpdated/60, 1))
      json.dump(newData, f)
      if(oldData['cases'] != newData['cases']):
        newCases = str(newData['cases'] - oldData['cases'])
        print(''+newCases+' Corona Positive cases added in the last '+lastUpdated+' minutes')
      if(oldData['deaths'] != newData['deaths']):
        newDeaths = str(newData['deaths'] - oldData['deaths'])
        print(''+newDeaths+' deaths are reported due to corona in the last '+lastUpdated+' minutes')
        print('Rest In Peace')
      if(oldData['recovered'] != newData['recovered']):
        newDeaths = str(newData['recovered'] - oldData['recovered'])
        print(''+newDeaths+' persons recoverd from corona in the last '+lastUpdated+' minutes')
    else:  
      print('No Changes in the last 1 minute..!!')      

startTracking = RepeatedTimer(60, getResult)

