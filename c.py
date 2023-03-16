import subprocess

# Run a shell command and capture its output
command = "ls -l"
result = subprocess.run(command, shell=True, capture_output=True, text=True)

# Print the output to the terminal
print(result.stdout)
