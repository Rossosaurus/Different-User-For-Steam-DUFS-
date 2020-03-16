#Modules
import easygui, os, subprocess, configparser, time

#Initial Variables
config = configparser.ConfigParser()
log = open('DUFSLog.txt', 'w')

#Establish ini file if it does not exist, then quit the script
if not os.path.exists("DUFSConfig.ini"):
    pathSteam = easygui.fileopenbox("Select 'steam.exe'", "Point DUFS to Steam Client", "C:/Program Files (x86)/Steam/*.exe")
    pathGame = easygui.fileopenbox("Select Game exe", "Point DUFS to Game Executable", "C:/Program Files (x86)/Steam/steamapps/common/*.exe")
    pathGame2 = easygui.fileopenbox("Select Alt Game exe", "Point DUFS to alternate executable", "C:/Program Files (x86)/Steam/steamapps/common/*.exe")
    usr = easygui.enterbox('Enter new user game will launch as. Needs to be in the pattern DOMAIN\\USER', "Enter new User details")
    config['PATHS'] = { 'SteamPath': pathSteam,
                        'GamePath': pathGame,
                        'GamePathAlt': pathGame2
    }
    config['SETTINGS'] = { 'NewUser': usr,
                           'Client-GameWaitTime': 30,
                           'ProcessCheckFrequency': 15,
                           'HighPriority': False
    }
    with open('DUFSConfig.ini', 'w') as ini:
        config.write(ini)
    with open('runSteam.bat', 'w') as bat:
        bat.write('cd "' + pathSteam.rsplit('\\', 1)[0] + '" && start' + os.path.basename(pathSteam) + '')
    with open(str(os.path.basename(pathGame)).replace('.exe', '') + '.bat', 'w') as game:
        game.write('start DUFS.exe')
    quit()

#Open config file
config.read('DUFSconfig.ini')
os.rename(config['PATHS']['gamepath'], config['PATHS']['gamepath'] + r'.bak')
os.rename(config['PATHS']['gamepath'].replace('.exe', '-Temp.exe'),  config['PATHS']['gamepath'])

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
process = subprocess.run('runas /savecred /user:' + config['SETTINGS']['newuser'] + ' "' + config['PATHS']['steampath'] + '"')
if not process.returncode == 0:
    easygui.msgbox("Something went wrong starting steam as user: " + config['SETTINGS']['newuser'] + ". Check you have entered the correct details in DUFSConfig.ini", 'Error: Cannot start steam.exe as ' + config['SETTINGS']['newuser'])
    log.write("Error starting steam.exe as new user. runas command exited with error code: " + str(process.returncode) + "\n")
    quit()
log.write("Started steam.exe as " + config['SETTINGS']['newuser'] + " successfully" + "\n")

#Raise steam.exe priority if highpriority is set to True in DUFSConfig.ini
if config.getboolean('SETTINGS', 'highpriority'):
    process = subprocess.run('wmic process where name="steam.exe" call setpriority "128"')
    if not process.returncode == 0:
        easygui.msgbox("Something went wrong raising the priority of steam. Check DUFSLog.txt for more. Should the issue persist, raise and issue on github", 'Error: Cannot raise priority of steam.exe')
        log.write("Error raising priority of steam.exe: " + str(process.stderr) + "\n")
        quit()
    log.write("Raised steam priority successfully to high" + "\n")

#Wait 60 seconds for Steam Home Streaming users to reconnect
time.sleep(int(config['SETTINGS']['client-gamewaittime']))

#Start game
pathGame = config['PATHS']['gamepath']
process = subprocess.run('runas /savecred /user:' + config['SETTINGS']['newuser'] + ' "' + pathGame + '"')
processName = os.path.basename(pathGame)
print('Started game: ' + processName)
log.write("Started game: " + processName + "\n")

if config['PATHS']['gamepathalt'] != "":
    processName = os.path.basename(config['PATHS']['gamepathalt'])

#Continuously check if the process still exists
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
        subprocess.run('.\\runsteam.bat')
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