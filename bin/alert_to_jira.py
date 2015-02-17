#! /opt/splunk/bin/python

"""
description     : Handles alerts created from within Splunk UI and calls relevant script to generate specific types of Jira alerts.
author          : Andrew Wurster
date            : 20150128
version         : 0.4

Splunk script arg listing:

# $0 = Script name
# $1 = Number of events returned
# $2 = Search terms
# $3 = Fully qualified query string
# $4 = Name of saved search
# $5 = Trigger reason (i.e. "The number of events was greater than 1")
# $6 = Browser URL to view the saved search
# $7 = This option has been deprecated and is no longer used
# $8 = File where the results for this search are stored (contains raw results) 
"""

import os
import sys
import json
import gzip
import csv
import StringIO
import ConfigParser
from jira.client import JIRA  # eventually pull this one out
import os
import logging
import time
import re
import jiracommon

# row={}
# results=[]
# keywords, options = splunk.Intersplunk.getKeywordsAndOptions()
# 
# # Get configuration values from config.ini
# local_conf = jiracommon.getLocalConf()
# 
# # Set up authentication variables
# username = local_conf.get('jira', 'username')
# password = local_conf.get('jira', 'password')
# auth = username + ':' + password
# authencode = base64.b64encode(auth)
# 
# # Set up URL prefix
# hostname = local_conf.get('jira', 'hostname')
# protocol = local_conf.get('jira', 'jira_protocol')
# port = local_conf.get('jira', 'jira_port')
# jiraserver = protocol + '://' + hostname + ':' + port
# 
# pattern = '%Y-%m-%dT%H:%M:%S'
# datepattern = "(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})"
# datevalues = re.compile(datepattern)
# option = sys.argv[1]



SPLUNK_HOME    = '/opt/splunk'
APPNAME        = 'jira'
APP_DIR        = os.path.join(SPLUNK_HOME, 'etc', 'apps', APPNAME)
RUN_DIR        = os.path.join(APP_DIR, 'bin')
LOG_DIR        = os.path.join(APP_DIR, 'data')
LOG_FILE       = os.path.join(LOG_DIR, 'alert_args.log')
CONFIG_FILE    = os.path.join(APP_DIR, 'local', 'config.ini')
ALERT_CLASS    = 'secint_investigation'

# Read config file
Config = ConfigParser.ConfigParser()
Config.read(CONFIG_FILE)

DEBUG          = Config.getboolean('general','debug')

JIRA_PROTOCOL  = Config.get('jira', 'protocol')
JIRA_HOST      = Config.get('jira', 'hostname')
JIRA_PATH      = Config.get('jira', 'path')
JIRA_PORT      = Config.get('jira', 'port')
JIRA_URL       = JIRA_PROTOCOL + "://" + JIRA_HOST + ":" + JIRA_PORT + JIRA_PATH

JIRA_USER      = Config.get('jira', 'username')
JIRA_PASS      = Config.get('jira', 'password')

JIRA_DEF_PROJECT = Config.get('jira', 'project')

DEF_TYPE    = Config.get('alert', 'issue_type')
DEF_LABELS  = Config.get('alert', 'labels')
DEF_REGEX   = Config.get('alert', 'regex')
DEF_CFIELDS = Config.get('alert', 'custom_fields')

logging.basicConfig(format='%(levelname)s: %(message)s ', filename=LOG_FILE, filemode='a+', level=logging.WARN)

logger = logging.getLogger()
consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)

if DEBUG:
    logger.setLevel(logging.DEBUG)
    logger.debug('Jira Alerts executed with debugging enabled.')
    logger.debug('Splunk script args list: %s', str(sys.argv))


# Initialise vars
event_data = ''
issue_fields = {}



# set up jira object

class Alert():
    def __init__(self,**kwargs):
        pass

    def get_config():
        pass
    
    def get_jira():
        pass

jira = JIRA(options = {'server': JIRA_URL}, basic_auth=(JIRA_USER, JIRA_PASS))

logger.debug('Opened connection to JIRA jira_user=%s, jira_url=%s', JIRA_USER, JIRA_URL)


try:
    search_trigger = sys.argv[3]
    search_summary = sys.argv[4]
    search_url = sys.argv[6]
    search_dump = sys.argv[8]
    
    with gzip.open(search_dump, 'rb') as raw_file:
        raw_event_data = raw_file.read()
        print "\n\n%s\n\n" % raw_event_data
        logger.debug('Opened raw search data from: %s', search_dump )
    csv_file = StringIO.StringIO(raw_event_data)
    csv_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
    
    #print dir(csv_reader)
    event_data += '\t'.join([k for k in csv_reader.fieldnames]) +"\n"
    
    for row in csv_reader:
        print row.items()
        event_data += '\t'.join([v for v in row.values()]) + "\n"
        #event_data += json.dumps(parsed_event_data, indent=4, sort_keys=True) + "\n"
    logger.debug('event_data=%s' % event_data)

except:
    import traceback
    logger.debug('Exception raised: "%s"', sys.exc_info()[0] )
    logger.debug('Exception value: "%s"', traceback.print_tb( sys.exc_info()[2] ) )
    #logger.debug(sys.exc_info())

def parse_summary(search_summary):
    matches = re.match(DEF_REGEX,search_summary).groupdict()
    summary = {}
    for k,v in matches.items():
        summary[k] = v
    
    summary['labels'] = summary['labels'].split('-')
    summary['summary'] = summary['summary'].strip()
    return summary

def parse_trigger(event_data):
    pass

# def parse_results(event_data):
#    results = 
#    pass

parsed_summary = parse_summary(search_summary)

desc =  ('h3. Splunk Link:\n' +
        '\t[' +  parsed_summary['summary'] + '|' + search_url + ']\n')
desc += ('h3. Search Query:\n' +
        '{noformat}\n' +
        search_trigger +
        '{noformat}\n')
desc += ('h3. Event Data:\n' +
        '{noformat}\n' +
        event_data +
        '{noformat}\n')
desc += ('h3. Alert Confidence\n' +
        '\t' + parsed_summary['customfield_20481'] +'\n')

issue_fields['project'] = {'key': JIRA_DEF_PROJECT}
issue_fields['issuetype'] = {'name': DEF_TYPE }
issue_fields['description'] = desc
issue_fields['summary'] = parsed_summary['summary']
issue_fields['labels'] = DEF_LABELS.split(',')
issue_fields['labels'].extend( parsed_summary['labels'] )

issue_fields['labels'] = [l.lower() for l in issue_fields['labels']]

new_issue = jira.create_issue(fields=issue_fields)

logger.debug('Sending data: key=%s, name="%s"', JIRA_DEF_PROJECT, DEF_TYPE)
logger.debug('Opened new Jira issue: id=%s, summary="%s"', new_issue.id, new_issue.fields.summary)

#if __name__ == "__main__":
#    
