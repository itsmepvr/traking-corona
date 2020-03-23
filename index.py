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
  response = requests.get("https://corona.lmao.ninja/all")
  response = response.json()
  with open('data.json', 'r+') as f:
    data = json.load(f)
    if(data != response):
      wave_obj = sa.WaveObject.from_wave_file("scream.wav")
      play_obj = wave_obj.play()
      play_obj.wait_done()
      f.seek(0)
      lastUpdated = response['updated'] - data['updated']
      lastUpdated = lastUpdated/1000
      lastUpdated = str(round(lastUpdated/60, 1))
      json.dump(response, f)
      if(data['cases'] != response['cases']):
        newCases = str(response['cases'] - data['cases'])
        print(''+newCases+' Corona Positive cases added in the last '+lastUpdated+' minutes')
      if(data['deaths'] != response['deaths']):
        newDeaths = str(response['deaths'] - data['deaths'])
        print(''+newDeaths+' deaths are reported due to corona in the last '+lastUpdated+' minutes')
        print('Rest In Peace')
      if(data['recovered'] != response['recovered']):
        newDeaths = str(response['recovered'] - data['recovered'])
        print(''+newDeaths+' persons recoverd from corona in the last '+lastUpdated+' minutes')
    else:  
      print('No Changes in the last 1 minute..!!')      

startTracking = RepeatedTimer(60, getResult)

