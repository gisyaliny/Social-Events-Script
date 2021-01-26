from __future__ import unicode_literals
from __future__ import print_function

import arcpy
import json
import time
try:
    import urllib.request as request
except ImportError:
    import urllib2 as request

API_URL = "https://api.github.com"
org = 'R-ArcGIS'
project = 'r-bridge'

latest_url = '{API_URL}/repos/{org}/{project}/releases/latest'.format(
             API_URL=API_URL, org=org, project=project)


def save_url(url, output_path):
    """Save a URL to disk."""
    valid_types = ['application/zip', 'application/octet-stream']
    r = None
    for _ in range(5):
        try:
            r = request.urlopen(url)
            break
        except request.HTTPError as e:
            reason = "None given"
            if e.reason:
                reason = e.reason
            arcpy.AddError("Unable to access '{}', (reason: {}).".format(
                url, reason))
        except request.URLError as e:
            arcpy.AddWarning("Access failed, trying again.")
            # retry all URLErrors
            time.sleep(3)

    if r and r.headers['content-type'] in valid_types and r.code == 200:
        arcpy.AddMessage("Saving URL to '{}'".format(output_path))
        with open(output_path, 'wb') as f:
            f.write(r.read())
    else:
        arcpy.AddError("Unable to access '{}', invalid content.".format(url))
        if r:
            arcpy.AddError("Content type: {}, response code: {}".format(
                r.headers['content-type'], r.code))
        msg = "Either a connectivity issue or restrictions on downloading " + \
              "prevented the tool from downloading. Please download the " + \
              "zip manually from {}".format(latest_url) + " and move it to " + \
              "the same location as this toolbox."
        arcpy.AddError(msg)


def parse_json_url(url):
    """Parse and return a JSON response from a URL."""
    res = None
    r = None
    err_msg = None
    for _ in range(5):
        try:
            r = request.urlopen(url)
            if r.code == 200:
                # urllib doesn't know bytestreams
                str_response = r.read().decode('utf-8')
                res = json.loads(str_response)
                break
            else:
                err_msg = "Unable to access'{}', invalid response.".format(url)
        except request.URLError as e:
            err_msg = "Unable to access'{}', error: {}.".format(url, e.reason)
        except LookupError as e:
            err_msg = "Unable to access'{}', lookup error: {}.".format(
                      url, e.reason)
        time.sleep(3)

    if err_msg:
        arcpy.AddWarning(err_msg)

    return res


def release_info():
    """Get latest release version and download URL from
       the GitHub API.

    Returns:
        (download_url, tag_name) tuple.
    """
    download_url = None
    tag = None
    json_r = parse_json_url(latest_url)
    if json_r is not None and 'assets' in json_r:
        assets = json_r['assets'][0]
        if 'browser_download_url' in assets and \
                'tag_name' in json_r:
            download_url = assets['browser_download_url']
            tag = json_r['tag_name']
        if not download_url or not tag:
            arcpy.AddError("Invalid GitHub API response for URL '{}'".format(
                latest_url))

    return (download_url, tag)
