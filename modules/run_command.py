import subprocess 

def direct_command(command):
    prosses = subprocess.run(command,shell=True,capture_output=True,text=True)
    return prosses

# add multiple commands functions

def run(command):
    if True: # place conditions to trigger different command functions
        output = direct_command(command)
        return output
    

