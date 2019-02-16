
import json
import urllib2
import urlparse
import logging

from enums import *

SIGNAL_ENUM_TO_JMRI_ASPECT = {
	SIGNAL_CLEAR: 'Clear',
	SIGNAL_ADVANCE_APPROACH: 'Advance Approach',
	SIGNAL_APPROACH: 'Approach',
	SIGNAL_APPROACH_CLEAR_SIXTY: 'Approach Clear Sixty',
	SIGNAL_APPROACH_CLEAR_FIFTY: 'Approach Clear Fifty',
	SIGNAL_APPROACH_DIVERGING: 'Approach Diverging',
	SIGNAL_APPROACH_RESTRICTING: 'Approach Restricting',
	SIGNAL_RESTRICTING: 'Restricting',

	SIGNAL_DIVERGING_CLEAR: 'Diverging Clear',
	SIGNAL_DIVERGING_CLEAR_LIMITED: 'Diverging Clear Limited',
	SIGNAL_DIVERGING_ADVANCE_APPROACH: 'Diverging Advance Approach',
	SIGNAL_DIVERGING_APPROACH: 'Diverging Approach',
	SIGNAL_DIVERGING_RESTRICTING: 'Restricting (Diverging)',

	SIGNAL_STOP: 'Stop',
}

# Yup: https://github.com/JMRI/JMRI/blob/master/java/src/jmri/SignalHead.java#L56
HEAD_ENUM_TO_JMRI_NUMBER = {
	HEAD_GREEN: 16,
	HEAD_FLASHING_GREEN: 32,
	HEAD_YELLOW: 4,
	HEAD_FLASHING_YELLOW: 8,
	HEAD_RED: 1,
	HEAD_FLASHING_RED: 2,
	HEAD_DARK: 0,
}

class JMRI(object):
	def __init__(self, jmri_server_address):
		self._jmri_server_address = jmri_server_address

	def _GetJsonData(self, url_path):
		# JMRI JSON docs:
		# http://jmri.sourceforge.net/help/en/html/web/JsonServlet.shtml
		url = urlparse.urljoin(self._jmri_server_address, url_path)
		logging.debug('Fetching JMRI JSON data from %s', url)
		return json.load(urllib2.urlopen(url))

	def GetCurrentTurnoutData(self):
		"""Returns a dictionary of {turnout name} -> {turnout value}."""
		turnout_data_json = self._GetJsonData('/json/turnouts')
		turnout_states = {}

		for turnout in turnout_data_json:
			name = turnout['data']['name']
			state = turnout['data']['state']
			if state == 2:
				turnout_state = TURNOUT_CLOSED
			elif state == 4:
				turnout_state = TURNOUT_THROWN
			else:
				#logging.debug(
				#	'Turnout %s had unknown json state value %s', name, state)
				turnout_state = TURNOUT_UNKNOWN
			turnout_states[name] = turnout_state
		logging.debug('Fetched data for %d turnouts', len(turnout_states))
		return turnout_states

	def GetCurrentSensorData(self):
		"""Returns a dictionary of {sensor name} -> {sensor value}."""
		sensor_data_json = self._GetJsonData('/json/sensors')
		sensor_states = {}

		for sensor in sensor_data_json:
			name = sensor['data']['name']
			state = sensor['data']['state']
			if state == 2:
				sensor_state = SENSOR_ACTIVE
			elif state == 4:
				sensor_state = SENSOR_INACTIVE
			else:
				logging.debug(
					'Sensor %s had unknown json state value %s', name, state)
				sensor_state = SENSOR_UNKNOWN
			sensor_states[name] = sensor_state
		logging.debug('Fetched data for %d sensors', len(sensor_states))
		return sensor_states

	def GetMemoryVariables(self):
		memory_data_json = self._GetJsonData('/json/memory')
		memory_states = {}
		for var in memory_data_json:
			name = var['data']['name']
			val = var['data']['value']
			memory_states[name] = val
		logging.debug('Fetched %d memory values', len(memory_states))
		return memory_states

	def _PostToJMRI(self, url, json_data):
		req = urllib2.Request(url, json_data, {'Content-Type': 'application/json'})
		try:
			f = urllib2.urlopen(req)
		except Exception as err:
			logging.error('JMRI POST failed: %s', err)
			return
		response = f.read()
		f.close()
		logging.debug('JMRI POST response: %s', response)

	def SetSignalHeadAppearance(self, head_name, appearance):
		jmri_number = HEAD_ENUM_TO_JMRI_NUMBER.get(appearance, -1)
		if jmri_number == -1:
			raise RuntimeError('Appearance %s invalid' % appearance)
		path = '/json/signalHead/' + head_name
		url = urlparse.urljoin(self._jmri_server_address, path)

		json_data = json.dumps({
			"type": "signalHead",
			"data": {
				"name": head_name,
				"state": jmri_number,
			}
		})
		logging.debug('Posting signal head change to %s: %s', url, json_data)
		self._PostToJMRI(url, json_data)

	def SetSignalMastAspect(self, mast_name, aspect):
		"""Sets mast_name to an aspect.
		   mast_name matches a signal mast name in JMRI.
		   aspect is a SIGNAL_* enum value.
		"""
		json_state = SIGNAL_ENUM_TO_JMRI_ASPECT.get(aspect)
		if not json_state:
			raise RuntimeError('Aspect invalid')
		path = '/json/signalMast/' + mast_name
		url = urlparse.urljoin(self._jmri_server_address, path)

		json_data = json.dumps({
			"type": "signalMast",
			"data": {
				"name": mast_name,
				"state": json_state,
			}
		})
		logging.debug('Posting signal aspect change to %s: %s', url, json_data)
		self._PostToJMRI(url, json_data)
