#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import requests

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class RandomJoke(object):

  def __init__(self):
    # get the configuration if needed
    try:
      self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
    except :
      self.config = None

    # start listening to MQTT
    self.start_blocking()

  # --> Sub callback function, one per intent
  def askJoke_callback(self, hermes, intent_message):
    # terminate the session first if not continue
    #hermes.publish_end_session(intent_message.session_id, "")

    # action code goes here...
    #good_category = requests.get("https://api.chucknorris.io/jokes/categories").json();

    category = None
    joke_msg = ''
#    if intent_message.slots.category:
#      category = intent_message.slots.category.first().value
#      # check if the category is valid
#      if category.encode("utf-8") not in good_category:
#        category = None

#    if category is None:
    url = 'https://icanhazdadjoke.com/'
    headers = {'Accept': 'application/json'}
    joke_msg = requests.get(url, headers=headers).json().get('joke')
    print(joke_msg)
#    else:
#      joke_msg = str(requests.get("https://icanhazdadjoke.com/random?category={}".format(category)).json().get("joke"))

    # if need to speak the execution result by tts
    hermes.publish_start_session_notification(intent_message.site_id, joke_msg, "RandomJoke")

  # --> Master callback function, triggered everytime an intent is recognized
  def master_intent_callback(self,hermes, intent_message):
    coming_intent = intent_message.intent.intent_name
    if coming_intent == 'CodeSourceror:askJoke':
      self.askJoke_callback(hermes, intent_message)

  # --> Register callback function and start MQTT
  def start_blocking(self):
    with Hermes(MQTT_ADDR) as h:
      h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
  RandomJoke()
