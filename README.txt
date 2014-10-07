ABOUT COURSERA OFFLINE

coursera_offline helps you download all your favorite course videos from Coursera at once. 


INSTALLATION INSTRUCTIONS

1. Open up a terminal and change the directory to the folder containing the coursera_offline files.
2. Run the command `sudo python setup.py install`
3. Run the script using the command coursera_offline

FEATURES

1. All the videos are downloaded according to the folder structure and you don't need to take care of sorting the videos into separate folders manually.
2. You need not track the order of the videos/weeks as the script intentionally renames them so that the video and week order is maintained.
3. The downloads are lightning fast as the videos are downloaded parallely.
4. The script creates a crontab entry automatically to fetch any newly added videos in the course. You can also force synch with Coursera just by running a simple command.
5. The script also downloads the subtitles automatically and saves them in Subs folder. So when you play the videos using VLC, the subs are automatically loaded.
6. The script saves a data.json file in the course directory. This has all the information required to fetch the videos. So even if you lose some videos or if you forget the course name, as long as you have the data.json file, you can always re-downlaod the lost videos.

REQUIRES
1. python2.7
2. pyquery 1.2.9
3. python-crontab 1.8.1

USAGE

usage: coursera_offline [-h] [-s SHORTNAME] [-e EMAIL] [-p PASSWORD] [-S] [-f]
                        [-d DIR] [-a [AUTO]]

optional arguments:
  -h, --help            show this help message and exit
  -s SHORTNAME, --shortname SHORTNAME
                        Short name of the course being downloaded. This option
                        is required when running the script for the first time
  -e EMAIL, --email EMAIL
                        Email id registered with Coursera
  -p PASSWORD, --password PASSWORD
                        Coursera Password
  -S, --synch           Give this flag to synch with Coursera
  -f, --file            Give this flag to force the script to obtain the
                        course information from data.json instead of Coursera
  -d DIR, --dir DIR     Give this option to save the videos in the path
                        specified as argument. Defaults to Present Working
                        Directory (PWD).
  -a [AUTO], --auto [AUTO]
                        Give this option to create a crontab entry inorder to
                        automatically synch with Coursera. Argument must one
                        among 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'.
                        The argument is optional and defaults to 'SUN'


## Some sample invocations

**Note:** In order to download some courses, you need to be registered for them in Coursera site before running the script.

Let's say you're downloading a course called **Introduction to Logic** and you want to download it to the `~/Logic`
 directory.

#### First time download

```
coursera_offline -d ~/Logic -s intrologic-005 -e <email> -p <password>
```

Do this to download the video lectures arranged as per weeks. This creates the `Logic` directory in the home directory (if it doesn't exist) and downloads all the videos into this directory. This also creates a `data.json` file that contains all the information requried to download the videos.

The argument **intrologic-005** is called the **shortname** and is unique for every course. It can be obtained from the class url. For example for the course under discussion, the url is https://class.coursera.org/intrologic-005.

##### Obtaining the shortname

* Signin to Coursera from [here](https://accounts.coursera.org/signin).
* You'll be redirected to a page containing all your registered courses.
* Choose the course you want to download and click the **Go to class** button.
* You'll be redirected to the class page whose url looks like 
`https://class.coursera.org/<short name>`.
* Copy the short name.

**Note:** If the `-d` options is not given, the videos will be downloaded to the current working directory.

#### Synching

```
coursera_offline -d ~/Logic -S -e <email> -p <password>
```

Okay, so you've been a few weeks into the course, now u need to fetch the updated videos. Don't worry, there's a way to do it !
The above command takes care of fetching the updated video content and synching it with your local directories.

#### Auto Synch

```
coursera_offline -a <Day of the week> -s intrologic-005 -e <email> -p <password>
```

You're downloading the course for the first time, and you don't want to keep using the 'Synch' command whenever you want to update the video content, you can just pass the `-a` flag which creates a crontab entry for the Synch command whch will be run at 11:59:59 pm on that particular day of the week. If no day is specified, it is defaulted to **Sunday**. 

**Note:** You can still force the script to synch with Coursera by using the Synch command described above.

#### Fetch using file

```
coursera_offline -d ~/Logic -f -e <email> -p <password>
```
So, you might be wondering the point of saving the `data.json`, right ? That wasn't totally pointless. The file's data is acquired by fetching the coursera video lectures page, parsing the html content. All the information required to download that course's videos is in that file. So, as long as you have the file, you can download the course without fetching the lecture page and the above command is the way to do it.
