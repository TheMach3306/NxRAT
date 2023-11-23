import os, sys, socket 

def client():
    message = "Hello from the client..."
    
    host_ip = "192.168.0.159"
    host_port = 90
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect the client socket
    client_socket.connect((host_ip, host_port))
    
    sysname = os.uname().sysname
    
    # Send the sysname to the server
    client_socket.send(sysname.encode())
    
    try:
        commands = client_socket.recv(2048).decode()
        
        while str(commands.lower()) != "exit":
            if commands.lower() == "exit":
                client_socket.close(); exit(0)
                
            if commands.lower() == "message":
                i=1
                if i == 1:
                    i = i + 1
                    client_socket.send(message.encode())
    
    except KeyboardInterrupt:
        client_socket.close(); exit(1)
                
                
client()