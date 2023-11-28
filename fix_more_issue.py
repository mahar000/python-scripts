import paramiko
import time


def receive_data(channel):
    output = b''
    while True:
        if channel.recv_ready():
            chunk = channel.recv(4096)
            output += chunk
            decoded_chunk = chunk.decode("utf-8", errors="ignore")
            print(decoded_chunk, end='')
            if "--More--" in decoded_chunk:
                # Send space to get more data
                channel.send(' ')
                time.sleep(1)
            else:
                break
        else:
            break
    return output.decode("utf-8", errors="ignore")


# SSH connection parameters
hostname = 'x.x.x.x'
port = 22  # Replace with the actual port number
username = 'x'
password = 'xxxx'  # Or use key-based authentication

try:
    # Create an SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the SSH server
    client.connect(hostname, port=port, username=username, password=password)

    # Open a subshell
    channel = client.invoke_shell()

    # Send commands to the subshell
    commands = [

        'show system maintenance',
        'show ip bgp summary all-vrfs',
        'exit',
    ]

    for command in commands:
        channel.send(command + '\n')

        output = receive_data(channel)
        print(output)

except paramiko.AuthenticationException:
    print("Authentication failed")
except paramiko.SSHException as e:
    print("SSH error:", str(e))
finally:
    client.close()
