# Coursera Offline

This is a script to download the video lectures of the courses that you have registered to, in one go.

## Usage

```
usage: coursera_offline.py [-h] [-s SHORTNAME] [-e EMAIL] [-p PASSWORD] [-S]
                           [-f FILE]

optional arguments:
  -h, --help            show this help message and exit
  -s SHORTNAME, --shortname SHORTNAME
                        Short name of the course being downloaded
  -e EMAIL, --email EMAIL
                        Email id registered with Coursera
  -p PASSWORD, --password PASSWORD
                        Coursera Password
  -S, --synch           Hit the coursera servers and synch the Video list
  -f FILE, --file FILE  Read contents of the json file and download the course

```

## Installation

* Make sure you have python version 2.7 installed. If you don't have python, get it from [here](link1)
* If you have python and are not sure of the version, type `python -V` in the terminal. If it says 2.7.x+ then you're okay. Otherwise, go to the link provided above.
* Download the project from here.
* Open a terminal, cd into the the directory you have just downloaded.
* Run the command 
 
      ``` python setup.py install```

