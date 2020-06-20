# DUFS (Different User For Steam)

## Table of Contents

- [DUFS (Different User For Steam)](#dufs-different-user-for-steam)
  - [Table of Contents](#table-of-contents)
  - [About <a name = "about"></a>](#about)
  - [Getting Started <a name = "getting_started"></a>](#getting-started)
    - [Compiling](#compiling)
    - [Installing](#installing)
  - [Usage <a name = "usage"></a>](#usage)

## About <a name = "about"></a>

A small script to automatically launch steam games as another user. I mainly wrote this script to allow those suffering from online issues in Halo:MCC to play online. DUFS-Stable.py is the file you should be using as DUFS-Testing most like won't even run it's the file I use to, you guessed it, test out other feature I might implement but probably won't unless specifically requested to.

This software work by temporarily replacing the game exe that steam launches when you press play to kill the steam process and relaunch it as a different specified user.

## Getting Started <a name = "getting_started"></a>

To start off Either download a copy of DUFS.exe from the releases page or if you're one of those sadists that like to compile software from github themselves make a copy of DUFS-Stable.py and compile it into an exe.

### Compiling

If you really want to compile the program yourself use `pyinstaller -F DUFS-Stable.py -n DUFS.exe`. For me the software wouldn't run properly with the `--noconsole` command so you'll just have to put up with a console in the background. Pyinstaller can be installed using `pip install pyinstaller`. If you don't know how to use `pip` or python seriously just use the precompiled exe and skip to the installing section.

### Installing

There are a few things that need to be done to run the software that I couldn't be bothered to automate in the script and you'll need to do. First off open the folder containing the files of the game you wish to use this software for. I'll be using the example of Halo:MCC as that is what this script was mainly written for.

Before running the script 3 things need to be done:

1. Copy DUFS.exe to the path containing the exe steam runs when you press play. For Halo: MCC this is `<steamapps folder>\common\Halo The Master Chief Collection\`

2. Steam also needs to be run as an admin so that it can run DUFS correctly when you press play. There a few ways you can do this so google is your friend here. However I run steam as both an admin and as a high priority process for better steam home streaming performance on boot. To do this I used to use Task Scheduler. Open Task Scheduler and click "Create Task" on the right hand side. Give the task a name and under security options select the user/group you want steam to run as normally. You can use the "Change User or Group" button to do this. Then select "Run only when user is logged on" and tick the "Run with highest privileges" checkbox to have Task Scheduler run the program as an elevated process with high priority. However I now use a program called HiddenStart which can be found [here](https://www.ntwind.com/software/hstart.html)

3. Lastly you will need a second windows user to that steam will be run as. To do this the quick way you can run `net user <username> <password> /add`. If you wish to hide this user from the Windows log in screen you can run this command: `reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList" /v <username here> /t REG_DWORD /d 0 /f`

Now we can configure DUFS. Run `DUFS.exe` manually and you will get several prompts one after the other:

1. First you need to point `DUFS.exe` to your `steam.exe` file. Unless you've installed steam somewhere that isn't the default install location DUFS should automatically be in your steam install folder you just need to select the `steam.exe`.
2. Next you need to point DUFS to the directory the game is installed to.
3. DUFS will now ask if you wish to have the game launched using the games steam game ID. It's probably a good idea to do this as you get controller support through the steam overlay.
4. If you chose to have DUFS launch the game via its steam game ID you now need to enter it. If you don't know what this is head over to <https://steamdb.info/> and search for the game. You'll find the ID there.
5. After that point DUFS to the game executable steam runs when you click play. In my case this is `mcclauncher.exe`
6. The last file you need to point DUFS to is the actual executable of the game. Some times this is different to the executable steam runs when you click play which is why this is asked. For most games you can probably just point to the same executable as the previous step but for games like Halo:MCC or any game with an external launcher you'll need to choose the actual game executable. In my case this is `<steamapps folder>\common\Halo The Master Chief Collection\MCC\Binaries\Win64\MCC-Win64-Shipping.exe`
7. Now DUFS needs to know the name of the user steam will be relaunched as. This is probably case sensitive.
8. Finally DUFS will ask if you want to use Steam Big Picture Mode. This is mainly for people like me who use Steam Home Streaming or use a controller regularly. If you plan on using a controller you need to press yes. After this DUFS will now close itself. You're almost finished setting up DUFS now there is just one thing left to do.
9. The last thing that needs to be done is to compile a batch file that was created by DUFS. During the first time setup process DUFS creates a new folder called DUFS. In here are some files DUFS has created to store any files DUFS uses. In this folder is a batch file named `launchGame.bat`. This file needs to be compiled into an executable of the same name as the executable selected in step 5. Before that however, you need to rename the exe steam runs when you press play to `<fileName>-Temp.exe`. For Halo:MCC this would be `mcclauncher-Temp.exe`. Then you can compile the created batch file into an exe. For this I use [Advanced BAT to EXE Converter](https://www.battoexeconverter.com/) but other software can do the same job. When editing the options Advance BAT to EXE uses before compilation I recommend ticking the "Start Invisible" checkbox. Compile the batch file and save it in the same location as DUFS. For me the batch file `launchGame.bat` is now `mcclauncher.exe` and the original `mcclauncher.exe` is now `mcclauncher-Temp.exe`. Thats the setup done.

## Usage <a name = "usage"></a>

Steam will now relaunch as the specified user entered when initially configuring DUFS and launch the game DUFS is configured to launch. DUFS will then run in the background and periodically check if the game is still running and when it is not DUFS will then relaunch steam as your normal user. All you have to do is press play on the game in the steam library. I do, however recommend taking a look in the `DUFSConfig.ini` file to change DUFS default settings to your needs. For instance if you're running on a conventional hard drive you may need to play with the wait times between steam launches.

| Setting |Function|
|---------|--------|
| steampath | steam.exe path.|
| installlocation | Game path or game launcher path.|
| usegameid | Set to true if you want DUFS to launch the game via it's steam ID or False to have DUFS launch the game via the executable specified in `gamepath`. |
| gameid | The AppID of the game you will be using DUFS to launch. See <https://steamdb.info/> to find this if you don't know it. |
| gamepath | Points to the executable steam launches when you click play. |
| monitorexe | Points to the executable DUFS will monitor to see if the game is still running or not. |
| newuser | The name of the user steam will be relaunched as. |
| bpm | Dictates if steam relaunches in BPM or not. If you plan on using a controller or steam in home streaming this should be set to True. |
| client-gamewaittime | Wait time in seconds between launching steam as the new user and launching the game. On an SSD you can probably get away with 10 seconds. On a HDD this will need to be more probably. |
| processcheckfrequency | Time in seconds between each check for if the game process is still running. Default is 10, I usually set this to 5. |
| highpriority | Dictates if steam is relaunched as high priority. Default is False. Set to True to launch as high priority. |
