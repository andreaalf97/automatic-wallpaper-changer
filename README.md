# automatic-wallpaper-changer
### This is a script that automatically changes your desktop background with the latest pictures from the subreddit [r/MinimalWallpaper](https://www.reddit.com/r/MinimalWallpaper/)

This version is able to download and save all the .jpg and .png pictures that are hosted on [Reddit](www.reddit.com) and [Imgur](http://imgur.com/), which are saved in the local folder `images`, <del>but still has problems with those hosted on [Imgur](http://imgur.com/)

I am currently working on timing the script and making it set the picture as a wallpaper slideshow.

This guide assumes you have Anaconda or Miniconda. If you don't, make sure your python environment has all the packages listed at [wallpaper.yml](wallpaper.yml)

To use this just clone this repo locally and, from the terminal, use the following commands.

Enter this folder:
```
cd YOUR/PATH/TO/automatic-wallpaper-changer
```

Clone the environment:
```
conda env create --file wallpaper.yml
```

You will then need to manually schedule the execution of [main.py](src/main.py) every 30 minutes. This script then automatically checks the last time it changed the wallpaper and the last time it downloaded new images from the subreddit.

Follow these steps to schedule the execution of the script on your Linux machine.

First we create the executable for your machine and change its permissions:
```
echo "conda run -n wallpaper python $PWD/script.py >> $PWD/cron.log 2>&1" > cron_run.sh
```
```
chmod +x ./cron_run.sh
```

Then you need to modify your crontab to execute `cron_run.sh` every 30 minutes.

This can be done by using
```
crontab -e
```
and adding the following line to the crontab file:
```
0,30 0-23 * * * PATH/TO/cron_run.sh
```

Done. To check if everything is working correctly, you can check the `cron.log` file, where the script outputs its stdout and stderr