from subprocess import run

# 1. all necessary imports
# 2. setup all components
# 3. start wifi hot spot and camera recording and straming as a separate process
# 4. while loop running every 10 seconds
#        check power levels (voltage and capacity %)
#        if low
#            send message to iridium
#            stop all processes (camera)
#            shutdown     
#        read all telemetry values and log them
#        every minute (or every 6th iteration) log and send them over iridium


run("shutdown --poweroff now", shell=True)
