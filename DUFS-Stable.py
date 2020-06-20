#Modules
import easygui, os, subprocess, configparser, time

if not os.path.exists('DUFS'):
    os.makedirs('DUFS')

#Initial Variables
config = configparser.ConfigParser()
log = open('DUFS/Log.txt', 'w')

#Establish ini file if it does not exist, then quit the script
if not os.path.exists("DUFS/DUFSConfig.ini"):
    gameID = None
    pathSteam = easygui.fileopenbox("Select 'steam.exe'", "Point DUFS to Steam Client", "C:/Program Files (x86)/Steam/*.exe")
    installLocation = easygui.diropenbox('Select game install directory', 'Point DUFS to game install folder', 'C:/Program Files (x86)/Steam/steamapps/common')
    steamOrPath = easygui.ynbox('Tell DUFS to launch the game using it\'s steam game ID?', 'Use GameID')
    if steamOrPath:
        gameID = easygui.enterbox('Enter the steam game ID: (use steamdb.info to find this if you do not know it already)', "Enter Steam Game ID")
    pathGame = easygui.fileopenbox("Select Game exe", "Point DUFS to Game Executable", installLocation)
    monitor = easygui.fileopenbox("Select executable to monitor", "Point DUFS towards the executable DUFS will continually check is running", installLocation)
    usr = easygui.enterbox('Enter new user game will launch as. Needs to be in the pattern DOMAIN\\USER', "Enter new User details")
    bpm = easygui.ynbox('Use Steam Big Picture Mode?', "Use BPM?")
    config['PATHS'] = { 'SteamPath': pathSteam,
                        'InstallLocation': installLocation,
                        'UseGameID': steamOrPath,
                        'GameID': gameID,
                        'GamePath': pathGame,
                        'MonitorEXE': monitor
    }
    config['SETTINGS'] = { 'NewUser': usr,
                           'BPM': bpm,
                           'Client-GameWaitTime': 20,
                           'ProcessCheckFrequency': 10,
                           'HighPriority': False
    }
    with open('DUFS/DUFSConfig.ini', 'w') as ini:
        config.write(ini)
    with open('DUFS/runSteam.bat', 'w') as bat:
        bat.write('cd "' + pathSteam.rsplit('\\', 1)[0] + '" && start' + os.path.basename(pathSteam) + '')
    with open('DUFS/launchGame.bat', 'w') as game:
        game.write('start DUFS.exe')
    quit()

#Open config file
config.read('DUFS/DUFSconfig.ini')

#Kill steam process
process = subprocess.run('TASKLIST', capture_output=True)
if 'steam.exe' in str(process.stdout):
    process = subprocess.run('taskkill /IM "steam.exe" /F', capture_output=True)
    if not process.returncode == 0:
        easygui.msgbox('Something went wrong with killing the steam process. Check DUFSLog.txt for more. Should the issue persist, raise an issue on github', 'Error: Cannot kill steam.exe')
        log.write("Error killing steam process: " + str(process.stderr) + "\n")
        quit()
    log.write("Killed steam successfully. Taskkill returned with status: " + str(process.stdout) + "\n")

#Run steam as new user specified in .ini
if config['SETTINGS']['BPM']:
    log.write("Steam will start in Big Picture Mode \n")
    process = subprocess.run('runas  /user:' + config['SETTINGS']['NewUser'] + ' /savecred "' + config['PATHS']['SteamPath'] + ' -bigpicture"')
else:
    log.write("Steam will start in normally \n")
    process = subprocess.run('runas  /user:' + config['SETTINGS']['NewUser'] + ' /savecred "' + config['PATHS']['SteamPath'] + '"') 
if not process.returncode == 0:
    easygui.msgbox("Something went wrong starting steam as user: " + config['SETTINGS']['NewUser'] + ". Check you have entered the correct details in DUFSConfig.ini", 'Error: Cannot start steam.exe as ' + config['SETTINGS']['newuser'])
    log.write("Error starting steam.exe as new user. runas command exited with error code: " + str(process.returncode) + "\n")
    quit()
log.write("Started steam.exe as " + config['SETTINGS']['NewUser'] + " successfully" + "\n")

#Raise steam.exe priority if highpriority is set to True in DUFSConfig.ini
if config.getboolean('SETTINGS', 'highpriority'):
    process = subprocess.run('wmic process where name="steam.exe" call setpriority "128"')
    if not process.returncode == 0:
        easygui.msgbox("Something went wrong raising the priority of steam. Check DUFSLog.txt for more. Should the issue persist, raise and issue on github", 'Error: Cannot raise priority of steam.exe')
        log.write("Error raising priority of steam.exe: " + str(process.stderr) + "\n")
        quit()
    log.write("Raised steam priority successfully to high" + "\n")

#Wait 60 seconds for Steam Home Streaming users to reconnect
time.sleep(int(config['SETTINGS']['Client-GameWaitTime']))

#Start game
os.rename(config['PATHS']['GamePath'], config['PATHS']['GamePath'] + r'.bak')
os.rename(config['PATHS']['GamePath'].replace('.exe', '-Temp.exe'),  config['PATHS']['GamePath'])

if config['PATHS']['UseGameID']:
    process = subprocess.run(config['PATHS']['SteamPath'] + ' -applaunch ' + config['PATHS']['GameID'])
    log.write("Started game with ID " +  config['PATHS']['GameID'] + " using steam\n")
else:
    process = subprocess.run('runas /savecred /user:' + config['SETTINGS']['NewUser'] + ' /savecred "' + config['PATHS']['GamePath'] + '"')
    processName = os.path.basename(pathGame)
    print('Started game: ' + processName)
    log.write("Started game with process name: " + processName + " using gameexecutable\n")

processName = os.path.basename(config['PATHS']['MonitorEXE'])

#Continuously check if the process still exists
time.sleep(20)

while True:
    print('Process check loop')
    time.sleep(int(config['SETTINGS']['processcheckfrequency']))
    print('Waited ' + config['SETTINGS']['processcheckfrequency'] + " seconds")
    log.write('Checking if the process still exists' + "\n")
    process = subprocess.check_output('TASKLIST /FO "LIST" /FI "IMAGENAME eq ' + processName)
    if not processName in str(process):
        print('Process no longer exists. Killing steam.exe')
        log.write('Process no longer exists' + "\n")
        process = subprocess.run('taskkill /IM "steam.exe" /F', capture_output=True)
        if not process.returncode == 0:
            easygui.msgbox('Something went wrong with killing the steam process. Check DUFSLog.txt for more. Should the issue persist, raise an issue on github', 'Error: Cannot kill steam.exe')
            log.write("Error killing steam process: " + str(process.stderr) + "\n")
            quit()
        log.write("Killed steam successfully. Taskkill returned with status: " + str(process.stdout) + "\n")
        os.rename(config['PATHS']['gamepath'], config['PATHS']['gamepath'].replace('.exe', '-Temp.exe'))
        os.rename(config['PATHS']['gamepath'] + r'.bak', config['PATHS']['gamepath'])
        print("Running steam.exe as normal user")
        subprocess.run('DUFS\\runsteam.bat')
        if config.getboolean('SETTINGS', 'highpriority'):
            process = subprocess.run('wmic process where name="steam.exe" call setpriority "128"')
            if not process.returncode == 0:
                easygui.msgbox("Something went wrong raising the priority of steam. Check DUFSLog.txt for more. Should the issue persist, raise and issue on github", 'Error: Cannot raise priority of steam.exe')
                log.write("Error raising priority of steam.exe: " + str(process.stderr) + "\n")
                quit()
            log.write("Raised steam priority successfully to high" + "\n")
        log.write('DUFS job is done for now, goodbye...')
        log.close()
        print("Job here is done, quitting now..")
        break
