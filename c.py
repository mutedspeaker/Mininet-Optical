import subprocess

# Run a command and capture its output
cmd = "ls -l"
output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
print(output)
