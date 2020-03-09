#Modules
import easygui, os, subprocess, configparser, time

#Initial Variables
config = configparser.ConfigParser()
log = open('DUFSLog.txt', 'w')

#Establish ini file if it does not exist, then quit the script
if not os.path.exists("DUFSConfig.ini"):
    pathSteam = easygui.fileopenbox("Select 'steam.exe'", "Point DUFS to Steam Client", "C:/Program Files (x86)/Steam/*.exe")
    pathGame = easygui.fileopenbox("Select Game exe", "Point DUFS to Game Executable", "C:/Program Files (x86)/Steam/steamapps/common/*.exe")
    usr = easygui.enterbox('Enter new user game will launch as. Needs to be in the pattern DOMAIN\\USER', "Enter new User details")
    config['PATHS'] = { 'SteamPath': pathSteam,
                        'GamePath': pathGame
    }
    config['SETTINGS'] = { 'NewUser': usr,
                           'Client-GameWaitTime': 60,
                           'ProcessCheckFrequency': 30,
                           'HighPriority': False }
    with open('DUFSConfig.ini', 'w') as ini:
        config.write(ini)
    quit()

#Open config file
config.read('DUFSconfig.ini')

#Kill steam process
process = subprocess.run('TASKLIST', capture_output=True)
if 'steam.exe' in process.stdout:
    process = subprocess.run('taskkill /IM "steam.exe /F', capture_output=True)
    if not process.returncode == 0:
        easygui.msgbox('Something went wrong with killing the steam process. Check DUFSLog.txt for more. Should the issue persist, raise an issue on github', 'Error: Cannot kill steam.exe')
        log.write("Error killing steam process: " + str(process.stderr))
        quit()
    log.write("Killed steam successfully. Taskkill returned with status: " + str(process.stdout))

#Run steam as new user specified in .ini
process = subprocess.run('runas' + ' /savecred' + ' /user:' + config['SETTINGS']['newuser'] + ' "' + config['PATHS']['steampath'] + '"')
if not process.returncode == 0:
    easygui.msgbox("Something went wrong starting steam as user: " + config['SETTINGS']['newuser'] + ". Check you have entered the correct details in DUFSConfig.ini", 'Error: Cannot start steam.exe as ' + config['SETTINGS']['newuser'])
    log.write("Error starting steam.exe as new user. runas command exited with error code: " + str(process.returncode))
    quit()
log.write("Started steam.exe as " + config['SETTINGS']['newuser'] + " successfully")

#Raise steam.exe priority if highpriority is set to True in DUFSConfig.ini
if config['SETTINGS']['highpriority']:
    process = subprocess.run('wmic process where name="steam.exe" call setpriority "128"')
    if not process.returncode == 0:
        easygui.msgbox("Something went wrong raising the priority of steam. Check DUFSLog.txt for more. Should the issue persist, raise and issue on github", 'Error: Cannot raise priority of steam.exe')
        log.write("Error raising priority of steam.exe: " + str(process.stderr))
        quit()
    log.write("Raised steam priority successfully to high")

#Wait 60 seconds for Steam Home Streaming users to reconnect
time.sleep(int(config['SETTINGS']['client-gamewaittime']))

#Start game
process = subprocess.Popen('"' + config['PATHS']['gamepath'] + '"')
gamePID = process.pid

#Continuously check if the process still exists
while True:
    time.sleep(config['SETTINGS']['processcheckfrequency'])
    log.write('Checking if the process still exists')
    try:
        os.kill(gamePID, 0)
    except OSError:
        log.write('Process no longer exists')
        process = subprocess.run('taskkill /IM "steam.exe" /F', capture_output=True)
        if not process.returncode == '0':
            easygui.msgbox('Something went wrong with killing the steam process. Check DUFSLog.txt for more. Should the issue persist, raise an issue on github', 'Error: Cannot kill steam.exe')
            log.write("Error killing steam process: " + str(process.stderr))
            quit()
        log.write("Killed steam successfully. Taskkill returned with status: " + str(process.stdout))
        subprocess.run(config['PATHS']['steampath'])
        quit()