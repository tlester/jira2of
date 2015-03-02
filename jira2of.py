import subprocess
import os
import shutil
import sys
import re
import httplib
import urllib
import urllib2

# Call jira_wget.sh, then read in file from /tmp/jira.json.  From there parse the json.