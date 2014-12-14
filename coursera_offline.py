#!/usr/bin/python

import argparse
import json
import sys
import urllib2
import cookielib
import random
import urllib
import threading
import os
from pyquery import PyQuery as pq
from crontab import CronTab

AUTH_URL = 'https://accounts.coursera.org/api/v1/login'
CLASS_VIDEO_URL_TEMPLATE = 'https://class.coursera.org/%s/lecture'
BASE_URL = 'https://www.coursera.org'

_204_DOMAIN = '.coursera.org'
_204_PATH = '/'

TIMEOUT = 300

DEFAULT_HEADERS = {
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36',
    'Accept' : '*/*',
    'Accept-Encoding' : 'gzip,deflate,sdch',
    'Accept-Language' : 'en-US,en;q=0.8',
    'Connection' : 'keep-alive'
}

SUB_DIR = 'Subs'
VID_EXT = '.mp4'
SUB_EXT = '.srt'
DATA_FILE = 'data.json'
COOKIE_FILE = 'cookie.cookies'
COURSE_DIR = os.getcwd()

class Downloader(threading.Thread):
    """Instance of threading.Thread class.
    Takes a URL and downloads the video present in the url"""
    def __init__(self, url, savepath, cookie, is_sub=False):
        threading.Thread.__init__(self)
        self.url = url
        self.savepath = savepath
        self.cookie = cookie
        self.is_sub = is_sub

    def run(self):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        print 'Downloading to %s' % absolute_path(self.savepath)
        f = None
        try:
            req = urllib2.Request(self.url)
            if self.is_sub:
                flags = 'w'
            else:
                flags = 'wb'
            f = open(absolute_path(self.savepath), flags)
            f.write(opener.open(req).read())
            f.close()
        except Exception, e:
            if f is not None:
                f.close()
            if path_exists(self.savepath):
                os.remove(absolute_path(self.savepath))

        print 'Download finished for %s' % absolute_path(self.savepath)

def exit_with_message(msg):
    # Print the msg and exit the script
    print msg
    sys.exit()
    
def has_cookiefile():
    return path_exists(COOKIE_FILE)

def parse_arguments():
    # Uses argparse.Argument parser to parse
    # Commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--shortname", help="""Short name of the course being downloaded.
        This option is required when running the script for the first time""")
    parser.add_argument("-e", "--email", help="Email id registered with Coursera")
    parser.add_argument("-p", "--password", help="Coursera Password")
    parser.add_argument("-S", "--synch", help="Give this flag to synch with Coursera", action='store_true')
    parser.add_argument("-f","--file", help="""Give this flag to force the script to obtain the course information from data.json 
        instead of Coursera""", action='store_true')
    parser.add_argument("-d", "--dir", help="Give this option to save the videos in the path specified as argument.\
     Defaults to Present Working Directory (PWD).")
    parser.add_argument("-a", "--auto", 
        help="Give this option to create a crontab entry inorder to automatically synch with Coursera.\
        Argument must one among 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'. The argument is optional and\
        defaults to 'SUN'",
        nargs='?',
        const='SUN',
        default=None)
    args = parser.parse_args()

    return args

def validate_arguments(args):
    # Checks if both username and password are provided
    # Exits the script if either username or password is
    # not provided. 
    if not args:
        exit_with_message('')

    if not args.email or not args.password:
        if not has_cookiefile():
            exit_with_message('Please provide both email and password')

    count = 0
    if args.shortname is not None: count += 1
    if args.synch: count +=1
    if args.file: count +=1

    if count is 0:
        exit_with_message('One of the options -s, -S, -f must be given')

def create_class_url(classname):
    if classname in ('', None):
        exit_with_message('Invalid class name')
    return CLASS_VIDEO_URL_TEMPLATE % classname

def absolute_path(rel_path):
    # Return the path relative to course dir
    return os.path.join(COURSE_DIR, rel_path)

def parse_data_file():
    # Parse the course data file
    if not path_exists(DATA_FILE):
        exit_with_message('Data file does not exist')

    try:
        f = open(absolute_path(DATA_FILE))
        parsed_json = json.load(f)
        f.close()
    except Exception,e :
        exit_with_message(e)

    if not parsed_json.has_key('cname') or not parsed_json.has_key('data'):
        exit_with_message('Invalid json file')

    return parsed_json

def login(email, password):
    # Logs into coursera and sets the cookie
    # Spoofs the requests to Coursera servers to login
    # Returns the cookie jar
    cookie_jar = cookielib.LWPCookieJar(absolute_path(COOKIE_FILE))
    if has_cookiefile():
        cookie_jar.load(ignore_discard=True)
        if isLoggedIn(cookie_jar):
            return cookie_jar
        elif not email or not password:
            exit_with_message('Provide email and password')
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))

    csrf2_token = 'csrf2_token_' + csrfMake(8)
    csrf2_token_value = csrfMake()
    csrf_token = csrfMake()

    csrf2 = cookielib.Cookie(version=0,
                        name=csrf2_token,
                        value=csrf2_token_value,
                        domain=_204_DOMAIN,
                        domain_specified=False,
                        domain_initial_dot=False,
                        path=_204_PATH,
                        path_specified=False,
                        secure=False,
                        expires=None,
                        comment=None,
                        comment_url=None,
                        rest={'HttpOnly':None},
                        rfc2109=False,
                        discard=False,
                        port=None,
                        port_specified=False)

    csrf = cookielib.Cookie(version=0,
                    name='csrftoken',
                    value=csrf_token,
                    domain=_204_DOMAIN,
                    domain_specified=False,
                    domain_initial_dot=False,
                    path=_204_PATH,
                    path_specified=False,
                    secure=False,
                    expires=None,
                    comment=None,
                    comment_url=None,
                    rest={'HttpOnly':None},
                    rfc2109=False,
                    discard=False,
                    port=None,
                    port_specified=False)

    cookie_jar.set_cookie(csrf)
    cookie_jar.set_cookie(csrf2)

    new_headers = DEFAULT_HEADERS
    new_headers['Referer'] = 'https://accounts.coursera.org/signin'
    new_headers['X-CSRFToken'] = csrf_token
    new_headers['X-CSRF2-Token'] = csrf2_token_value
    new_headers['X-CSRF2-Cookie'] = csrf2_token
    new_headers['Origin'] = 'https://accounts.coursera.org'
    new_headers['X-Requested-With'] = 'XMLHttpRequest'
    new_headers['Content-Type'] = 'application/x-www-form-urlencoded'

    data = {
        'email' : email,
        'password' : password,
        'webrequest' : 'true'
    }

    login_req = urllib2.Request(AUTH_URL, urllib.urlencode(data), new_headers)
    login_res = None
    try:
        login_res = opener.open(login_req)
    except Exception, e:
        print e
        sys.exit()
    if not isLoggedIn(cookie_jar):
        exit_with_message('Login Failed. Try again later')
    cookie_jar.save(ignore_discard=True)
    return cookie_jar

def download(parsed_json, cookie):
    # Downloads the videos in parsed json
    # using the cookie which is logged in
    if COURSE_DIR is not '':
        create_folder('')

    # Start the download
    threads = []
    week_count = 0
    print 'Downloading videos'
    for sub_json in parsed_json['data']:
        folder_name = str(week_count) + '-' + sub_json['title'].replace('/','-').replace(',','-').replace(':','-')
        week_count += 1
        create_folder(folder_name)
        create_folder(os.path.join(folder_name, SUB_DIR))
        count = 0
        for vid_info in sub_json['links']:

            url = vid_info['link']
            title = vid_info['title']
            old_vid_path = os.path.join(folder_name, title + VID_EXT)
            old_sub_path = os.path.join(folder_name, SUB_DIR, title + SUB_EXT)
            title = title.replace(':', '-').replace('/', '-').replace(',','-')
            suburl = vid_info['sub_link']
            sub_path = os.path.join(folder_name, SUB_DIR, str(count) + '-' + title+SUB_EXT)
            vid_path = os.path.join(folder_name, str(count) + '-' + title+VID_EXT)
            count += 1
            if path_exists(vid_path) or path_exists(old_vid_path):
                print 'Skipping %s' % vid_path
            else:
                d = Downloader(url, vid_path, cookie)    
                threads.append(d)

            if path_exists(sub_path):
                print 'Skipping %s' % sub_path
            elif path_exists(old_sub_path):
                d = Downloader(suburl, old_sub_path, cookie, True)
                threads.append(d)
            else:
                d = Downloader(suburl, sub_path, cookie, True)
                threads.append(d)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def path_exists(path):
    return os.path.exists(absolute_path(path))

def create_folder(foldername):
    # Creates the folders for each week
    # Checks if a folder with that name already exists
    # Skip if it exists
    if path_exists(foldername):
        return False
    os.makedirs(absolute_path(foldername))
    return True

def data_file_exists():
    return path_exists(DATA_FILE)

def set_course_dir(dir):
    if not dir:
        return
    global COURSE_DIR
    COURSE_DIR = dir;

def schedule_synch(day, email, password):
    if not day:
        exit_with_message('Failed to schedule synch: Invalid day')
    if not email or not password:
        exit_with_message('Invalid username and password')
    day = day.upper()
    if not day in ['MON','TUE','WED','THU','FRI','SAT','SUN']:
        exit_with_message('Failed to schedule synch: Invalid day')
    user_cron = CronTab(user=True)
    cmd = "%s -d %s -S -e %s -p %s" % (os.path.abspath(__file__), COURSE_DIR, email, password)
    job = user_cron.new(command=cmd)
    job.hour.on(11)
    job.minute.on(59)
    job.dow.on(day)
    user_cron.write()
    print 'Cron Job added'

def main():
    args = parse_arguments()
    validate_arguments(args)
    if args.dir is not None:
        set_course_dir(os.path.abspath(args.dir))
    if args.shortname is not None:
        if data_file_exists():
            exit_with_message('Looks like a course already exists here.')
        shortname = args.shortname
    else:
        parsed_json = parse_data_file()
        shortname = parsed_json['cname']

    print 'Logging in'
    cookie_logged_in = login(args.email, args.password)
    if not cookie_logged_in:
        exit_with_message('Login Failed.')

    if not args.file:
        parsed_json = get_course_info(shortname, cookie_logged_in)    
    download(parsed_json, cookie_logged_in)
    save_data_file(parsed_json)
    if args.auto is not None:
        schedule_synch(args.auto, args.email, args.password)        

def save_data_file(parsed_json):
    if not parsed_json:
        exit_with_message('Invalid data to save')
    try:
        f = open(absolute_path(DATA_FILE), 'w')
        f.write(json.dumps(parsed_json))
        f.close()
    except Exception, e:
        exit_with_message('Failed to save the JSON file')

def get_course_info(shortname, cookie):
    print 'Getting course information %s' % shortname
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    url = create_class_url(shortname)
    response_html = None

    print 'Fetching course videos page'
    try:
        req = urllib2.Request(url)
        res = opener.open(req)
        response_html = res.read()
    except Exception, e:
        print e

    if not response_html:
        exit_with_message('Failed to fetch the course information')

    doc = None
    try:
        doc = pq(response_html)
    except Exception, e:
        exit_with_message(e)

    if not doc:
        exit_with_message('Failed to parse the html file')

    course_info_json = {'cname': shortname, 'data':[]}
    html_headers = doc('.course-item-list-header')
    try:
        for index, html_header in enumerate(html_headers):
            div_elem = pq(html_header)
            week_title = div_elem('h3').text()
            selection_list =doc('.course-item-list-section-list').eq(index)
            list_items = selection_list('li')
            parsed_json = {'title': week_title, 'links': []}
            for list_item in list_items:
                list_elem = pq(list_item)
                anchor_elems = list_elem('a')
                vid_title = pq(anchor_elems[0]).text()
                vid_link = pq(anchor_elems[len(anchor_elems) - 1]).attr('href')
                sub_link = pq(anchor_elems[len(anchor_elems) - 2]).attr('href')
                parsed_json['links'].append({'title':vid_title, 'link':vid_link, 'sub_link':sub_link})
            course_info_json['data'].append(parsed_json)
    except Exception, e:    
        exit_with_message('Invalid HTML file receieved')

    return course_info_json

def isLoggedIn(cookie):
    # Checks if the cookie object has cookies 
    # necessary for auth
    # returns False if None
    # returns False if CAUTH cookie is absent, True otherwise
    if not cookie: return False
    for index, cookie in enumerate(cookie):
        if cookie.name == 'CAUTH':
            return True
    return False

def csrfMake(length=None, chars=None):
    output = []
    if length is None:
        length = 24
    if chars is None:
        chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    for i in range(length):
        output.append(chars[int(random.random() * len(chars))])
    return ''.join(output )

if __name__ == "__main__":
    main()