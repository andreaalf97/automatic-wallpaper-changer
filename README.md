# automatic-wallpaper-changer
### This is a script that automatically changes your desktop background with the latest pictures from the subreddit [r/Wallpaper](https://www.reddit.com/r/Wallpaper/)

This version is able to download and save all the .jpg and .png pictures that are hosted on [Reddit](www.reddit.com) and [Imgur](http://imgur.com/), which are saved in the local folder `images`, <del>but still has problems with those hosted on [Imgur](http://imgur.com/)

This guide assumes you have Anaconda or Miniconda. If you don't, make sure your python environment has all the packages listed at [wallpaper.yml](wallpaper.yml)

To use this tool, just clone this repo locally and, from the terminal, use the following commands.

Enter this folder:
```
cd YOUR/PATH/TO/automatic-wallpaper-changer
```

Clone the conda environment:
```
conda env create --file wallpaper.yml
```

You will then need to manually schedule the execution of [script.py](script.py) every 30 minutes. This script then automatically checks the last time it changed the wallpaper and the last time it downloaded new images from the subreddit.

Follow these steps to schedule the execution of the script on your Linux machine.

First we create the executable for your machine and change its permissions.

Create the file with:
```
nano cron_run.sh
```
And copy the following code inside
```
user=$(whoami)

fl=$(find /proc -maxdepth 2 -user $user -name environ -print -quit)
while [ -z $(grep -z DBUS_SESSION_BUS_ADDRESS "$fl" | cut -d= -f2- | tr -d '\000' ) ]
do
  fl=$(find /proc -maxdepth 2 -user $user -name environ -newer "$fl" -print -quit)
done

export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS "$fl" | cut -d= -f2-)

#echo "DBUS=$DBUS_SESSION_BUS_ADDRESS"

PATH/TO/anaconda3/bin/conda run -n wallpaper python PATH/TO/automatic-wallpaper-changer/script.py
```
where you have to change the PATH/TO/ parts. Then we make this script executable with
```
chmod +x ./cron_run.sh
```

Then you need to modify your crontab to execute `cron_run.sh` every 10 minutes.

This can be done by using
```
crontab -e
```
and adding the following line to the crontab file:
```
0-59/10 0-23 * * * /home/andreaalf/Documents/Other/automatic-wallpaper-changer/cron_run.sh >> /home/andreaalf/Documents/Other/automatic-wallpaper-changer/cron.log 2>&1
```
Crontab explanation:
* `0-59/10` means that the script will be run every 10 minutes
* `0-23` means every hour of the day

Done. To check if everything is working correctly, you can check the `cron.log` file, where the script outputs its stdout and stderr
