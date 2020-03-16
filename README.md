# DUFS (Different User For Steam)

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

A small script to automatically launch steam games as another user. I mainly wrote this script to allow those suffering from online issues in Halo:MCC to play online. DUFS-Stable.py is the file you should be using as DUFS-Testing most like won't even run it's the file I use to, you guessed it, test out other feature I might implement but probably won't unless specifically requested to.

This software work by temporarily replacing the game exe that steam launches when you press play to kill the steam process and relaunch it as a different specified user.

## Getting Started <a name = "getting_started"></a>

To start off Either download a copy of DUFS.exe from the releases page or if you're one of those sadists that like to compile software from github themselves make a copy of DUFS-Stable.py and compile it into an exe.

### Compiling

If you really want to compile the program yourself use `pyinstaller -F DUFS.py`. For me the software wouldn't run properly with the `--noconsole` command so you'll just have to put up with a console in the background. Pyinstaller can be installed using `pip install pyinstaller`. If you don't know how to use `pip` or python seriously just use the precompiled exe and skip to the installing section.

### Installing

There are a few things that need to be done to run the software that I couldn't be bothered to automate in the script and you'll need to do. First off open the folder containing the files of the game you wish to use this software for. I'll be using the example of Halo:MCC as that is what this script was mainly written for.

Before running the script 3 things need to be done:

1. Copy DUFS.exe to the path containing the exe steam runs when you press play. For Halo: MCC this is `<steamapps folder>\common\Halo The Master Chief Collection\`

2. Steam also needs to be run as an admin so that it can run DUFS correctly when you press play. There a few ways you can do this so google is your friend here. However I run steam as both an admin and as a high priority process for better steam home streaming performance on boot. To do this I use Task Scheduler. Open Task Scheduler and click "Create Task" on the right hand side. Give the task a name and under security options select the user/group you want steam to run as normally. You can use the "Change User or Group" button to do this. Then select "Run only when user is logged on" and tick the "Run with highest privileges" checkbox to have Task Scheduler run the program as an elevated process with high priority.

3. Lastly you will need a second windows user to that steam will be run as.

Now we can configure DUFS. Run `DUFS.exe` manually and you will get several prompts one after the other:

1. First you need to point `DUFS.exe` to your `steam.exe` file. Unless you've installed steam somewhere that isn't the default install location DUFS should automatically be in your steam install folder you just need to select the `steam.exe`.

2. Next you need to point DUFS to the batch executable you compiled named after the exe steam runs when you click play. In my case this is `mcclauncher.exe`

3. The last file you need to point DUFS to is optional in some cases but for Halo:MCC you'll need to do this. If steam does not run the actual game executable and instead runs a launcher for the game like Halo:MCC does you will need to point steam to the actual game executable so that DUFS knows which process to monitor. In my case this is `<steamapps folder>\common\Halo The Master Chief Collection\MCC\Binaries\Win64\MCC-Win64-Shipping.exe`

4. Now DUFS needs to know the name of the user steam will be relaunched as. I think this is case sensitive.

The last thing that needs to be done is to compile a batch file that was created by DUFS. In the folder DUFS is located a batch file will have been created named after the second executable DUFS asked you to point to. In my case this `mcclauncher.bat`. This finally needs to be compiled into an exe of the same name. Before that however, you need to rename the exe steam runs when you press play to `<fileName>-Temp.exe`. For Halo:MCC this would be `mcclauncher-Temp.exe`. Then you can compile the created batch file into an exe. For this I use [Advanced BAT to EXE Converter](https://www.battoexeconverter.com/). When editing the options Advance BAT to EXE uses before compilation I recommend ticking the "Start Invisible" checkbox. Compile the batch file and save it in the same location as DUFS. So for me the batch file `mcclauncher.bat` is now `mcclauncher.exe` and the original `mcclauncher.exe` is now `mcclauncher-Temp.exe`. Thats the setup done.

## Usage <a name = "usage"></a>

Steam will now relaunch as the specified user entered when initially configuring DUFS and launch the game DUFS is configured to launch. DUFS will then run in the background and periodically check if the game is still running and when it is not DUFS will then relaunch steam as your normal user. All you have to do is press play on the game in the steam library. I do, however recommend taking a look in the `DUFSConfig.ini` file to DUFS default settings to your needs. For instance if you're running on a conventional hard drive you may need to play with the wait times between steam launches.

| Setting               | Function                                                                                                    |
|-----------------------|-------------------------------------------------------------------------------------------------------------|
| steampath             | steam.exe path.                                                                                             |
| gamepath              | Game path or game launcher path.                                                                            |
| gamepathalt           | Game path is `gamepath` points to the path of the games launcher.                                           |
| newuser               | The name of the user steam will be relaunched as.                                                           |
| client-gamewaittime   | Wait time in seconds between launching steam as the new user and launching the game.                        |
| processcheckfrequency | Time in seconds between each check for if the game process is still running.                                |
| highpriority          | Dictates is steam is relaunched as high priority. Default is False. Set to True to launch as high priority. |
