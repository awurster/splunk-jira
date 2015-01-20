#! /opt/splunk/bin/python

"""
description     : Handles alerts created from within Splunk UI and calls relevant script to generate specific types of Jira alerts.
author          : Andrew Wurster
date            : 20150120
version         : 0.3

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
from jira.client import JIRA
import os
import logging
import time

SPLUNK_HOME    = '/opt/splunk'
APPNAME        = 'jira'
APP_DIR        = os.path.join(SPLUNK_HOME, 'etc', 'apps', APPNAME)
RUN_DIR        = os.path.join(APP_DIR, 'bin')
LOG_DIR        = os.path.join(APP_DIR, 'data')
LOG_FILE       = os.path.join(LOG_DIR, 'alert_args.log')
CONFIG_FILE    = os.path.join(APP_DIR, 'local', 'alerts_config.ini')
ALERT_CLASS    = 'secint_investigation'

# Read config file
Config = ConfigParser.ConfigParser()
Config.read(CONFIG_FILE)

DEBUG          = Config.getboolean('general','debug')

JIRA_URL       = Config.get('jira_config', 'url')
JIRA_USER      = Config.get('jira_config', 'username')
JIRA_PASS      = Config.get('jira_config', 'password')
JIRA_DEF_PROJECT = Config.get('jira_config', 'project')
JIRA_DEF_TYPE    = Config.get('jira_config', 'issue_type')

logging.basicConfig(format='%(levelname)s: %(message)s ', filename=LOG_FILE, filemode='a+', level=logging.WARN)

logger = logging.getLogger()
consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)

if DEBUG:
    logger.setLevel(logging.DEBUG)
    logger.debug('Jira Alerts executed with debugging enabled.')
    logger.debug('Splunk script args list: %s', str(sys.argv))


event_data = ''

# set up jira object

#class Alert():
#    def __init__(self,):

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
        logger.debug('Opened raw search data from: %s', search_dump )
    csv_file = StringIO.StringIO(raw_event_data)
    csv_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
    
    event_data = '{noformat}'
    
    for row in csv_reader:
        parsed_event_data = json.loads(row['_raw'])
        event_data += json.dumps(parsed_event_data, indent=4, sort_keys=True) + "\n"
    
    event_data += '{noformat}'
except:
    e = sys.exc_info()[0]
    logger.debug('Unknown exception raised: "%s"', e)


desc = "Splunk link: \n" + search_url + "\n"
desc += "Splunk trigger: \n {noformat}" + search_trigger + "{noformat}\n"
desc += "Event data: \n" + event_data 

new_issue = jira.create_issue(
  project={'key': JIRA_DEF_PROJECT },
  issuetype={'name': JIRA_DEF_TYPE },
  summary=search_summary,
  description=desc
)

logger.debug('Opened new Jira issue: id=%s, summary="%s"', new_issue.id, new_issue.fields.summary)

#if __name__ == "__main__":
#    