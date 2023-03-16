import subprocess

# Start the shell process
process = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# Send the 'signals' command to the shell and capture its output
command = 'signals\n'.encode('utf-8')
process.stdin.write(command)
output = process.stdout.read().decode('utf-8')

# Print the output
print(output)
