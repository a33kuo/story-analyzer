# -*- coding: utf-8 -*-

import simplejson
import os
import urllib, urllib2

root_url = 'http://conceptnet5.media.mit.edu/data/'

def get_assertions(concept=None, lang='en', \
		normalized=True, conceptnet_only=True, num_assertions=None):
	"""
	Get assertions of a concept from ConceptNet 5
	"""
	if concept is None:
		return []
	assertions = []
	params = {}
	query_url = root_url + 'concept/' + lang + '/' + concept
	params['get'] = 'incoming_assertions'
	data = urllib.urlencode(params)
	request = urllib2.Request('%s?%s' % (query_url.encode('utf-8'), data))
	while request:
		try:
			result = simplejson.load(urllib2.urlopen(request))
		except:
			return assertions
		flag_next = False
		if 'error' in result.keys():
			break
		for assertion in result['incoming_assertions']:
			if 'next' not in assertion.keys():
				if 'conceptnet' not in assertion['dataset'] and conceptnet_only:
					continue
				arg1 = assertion['args'][0].split('/')[-1]
				arg2 = assertion['args'][1].split('/')[-1]
				relation = assertion['relation'].split('/')[-1]
				if normalized == True and 'normalized' in assertion.keys():
					if assertion['normalized'] == True:
						assertions.append((relation, arg1, arg2))
				else:
					assertions.append((relation, arg1, arg2))
				if len(assertions) == num_assertions:
					break
			else:
				request = urllib2.Request('%s' % (assertion['next'].encode('utf-8')))
				flag_next = True
		if num_assertions != None and len(assertions) == num_assertions:
			break
		if flag_next is False:
			break
	return assertions

if __name__ == '__main__':
	print get_assertions('mit')
