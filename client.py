#!/usr/bin/env python3
"""
Client for messenger with chat, tasks, and AI
Features: registration, authentication, chat, task management, AI chat
"""

import socket
import sys


def recv_until_end(sock, timeout=5):
    """Receive data from socket"""
    try:
        old_timeout = sock.gettimeout()
        sock.settimeout(timeout)
        data = sock.recv(8192).decode('utf-8', errors='ignore')
        sock.settimeout(old_timeout)
        return data
    except socket.timeout:
        try:
            sock.settimeout(old_timeout)
        except:
            pass
        return ""


def send_command(sock, command):
    """Send command and receive response"""
    sock.send(command.encode('utf-8') + b'\n')
    return recv_until_end(sock)


def interactive_prompt(sock, prompt_text):
    """Send prompt and receive multiline input until END"""
    sock.send(prompt_text.encode('utf-8') + b'\n')
    lines = []
    print("(type 'END' on new line to finish)")
    while True:
        try:
            line = input()
            if line == 'END':
                sock.send(line.encode('utf-8') + b'\n')
                break
            sock.send(line.encode('utf-8') + b'\n')
            lines.append(line)
        except KeyboardInterrupt:
            sock.send(b'END\n')
            break
    return recv_until_end(sock)


def show_menu():
    """Show main menu"""
    print("""
========================================
     Messenger with Tasks & AI
========================================
1. Chat
2. Tasks
3. AI Chat
4. Help
5. Logout
6. Exit
========================================
""")


def chat_menu(sock):
    """Chat submenu"""
    while True:
        print("\n-- CHAT --")
        print("1. Send message")
        print("2. View messages")
        print("3. Back")
        choice = input("Choice: ").strip()
        
        if choice == '1':
            message = input("Message: ").strip()
            if message:
                response = send_command(sock, f'chat send {message}')
                print(response)
        elif choice == '2':
            count_input = input("Show last N messages (default 100): ").strip()
            count = count_input if count_input else "100"
            response = send_command(sock, f'chat view {count}')
            print(response)
        elif choice == '3':
            break


def task_menu(sock):
    """Task submenu"""
    while True:
        print("\n-- TASKS --")
        print("1. Create task")
        print("2. List tasks")
        print("3. View task")
        print("4. Add description")
        print("5. Add solution")
        print("6. Change status")
        print("7. Delete task")
        print("8. Back")
        choice = input("Choice: ").strip()
        
        if choice == '1':
            title = input("Task title: ").strip()
            if title:
                response = send_command(sock, f'task create {title}')
                print(response)
        elif choice == '2':
            response = send_command(sock, 'task list')
            print(response)
        elif choice == '3':
            task_id = input("Task ID: ").strip()
            if task_id:
                response = send_command(sock, f'task view {task_id}')
                print(response)
        elif choice == '4':
            task_id = input("Task ID: ").strip()
            if task_id:
                response = interactive_prompt(sock, f'task add-desc {task_id}')
                print(response)
        elif choice == '5':
            task_id = input("Task ID: ").strip()
            if task_id:
                response = interactive_prompt(sock, f'task add-sol {task_id}')
                print(response)
        elif choice == '6':
            task_id = input("Task ID: ").strip()
            if task_id:
                print("Statuses: pending, in_progress, solved")
                status = input("New status: ").strip()
                if status:
                    response = send_command(sock, f'task status {task_id} {status}')
                    print(response)
        elif choice == '7':
            task_id = input("Task ID: ").strip()
            if task_id:
                response = send_command(sock, f'task delete {task_id}')
                print(response)
        elif choice == '8':
            break


def ai_menu(sock):
    """AI Chat submenu"""
    while True:
        print("\n-- AI CHAT --")
        print("1. Send message")
        print("2. Clear history")
        print("3. Back")
        choice = input("Choice: ").strip()
        
        if choice == '1':
            message = input("Your message: ").strip()
            if message:
                response = send_command(sock, f'ai {message}')
                print(response)
        elif choice == '2':
            response = send_command(sock, 'ai clear')
            print(response)
        elif choice == '3':
            break


def auth_menu(sock):
    """Authentication menu"""
    while True:
        print("\n========================================")
        print("     Welcome to Messenger")
        print("========================================")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choice: ").strip()
        
        if choice == '1':
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            if username and password:
                response = send_command(sock, f'register {username} {password}')
                print(response)
                if '[OK]' in response:
                    print("✓ Registration successful! Now login with your credentials.")
        elif choice == '2':
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            if username and password:
                response = send_command(sock, f'login {username} {password}')
                print(response)
                if '[OK]' in response:
                    return True
        elif choice == '3':
            return False
    return False


def main():
    """Main client loop"""
    if len(sys.argv) < 2:
        print("Usage: python3 client.py <host:port>")
        print("Example: python3 client.py localhost:7002")
        sys.exit(1)
    
    try:
        host_port = sys.argv[1].split(':')
        host = host_port[0]
        port = int(host_port[1])
    except:
        print("[ERR] Invalid host:port format")
        sys.exit(1)
    
    # Connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except:
        print(f"[ERR] Cannot connect to {host}:{port}")
        sys.exit(1)
    
    # Welcome message
    print(recv_until_end(sock))
    
    # Authentication
    if not auth_menu(sock):
        sock.close()
        print("Goodbye!")
        return
    
    # Main menu loop
    while True:
        show_menu()
        choice = input("Choice: ").strip()
        
        if choice == '1':
            chat_menu(sock)
        elif choice == '2':
            task_menu(sock)
        elif choice == '3':
            ai_menu(sock)
        elif choice == '4':
            response = send_command(sock, 'help')
            print(response)
        elif choice == '5':
            response = send_command(sock, 'logout')
            print(response)
            if '[OK]' in response:
                if not auth_menu(sock):
                    break
        elif choice == '6':
            response = send_command(sock, 'quit')
            print(response)
            break
        else:
            print("[ERR] Invalid choice")
    
    sock.close()


if __name__ == '__main__':
    main()
