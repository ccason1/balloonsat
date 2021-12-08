from subprocess import run

# 1. all necessary imports
# 2. setup all components
# 3. start wifi hot spot and streaming as a separate process
# 4. while loop running with 10 seconds delay after last iteration
#        check power levels (voltage and capacity %)
#        if low
#            attempt to send message over iridium
#            if unsuccessful
#                alert to streaming webpage (???)
#            stop all spawned processes
#            shutdown     
#        read all telemetry values and log them
#        every minute (or every 6th iteration) attempt to send them over iridium


run("shutdown --poweroff now", shell=True)
