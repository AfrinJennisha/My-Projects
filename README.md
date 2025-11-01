# SSH Cracker 

*Author:* Afrin Jennisha 
*Environment:* Kali Linux VM (attacker) → Localhost / VM (victim)  
*Date:* 1st Nov 2025

---

## ⚠ Safety & Ethics
This project is *for educational purposes only*.  
*Always* obtain explicit permission before testing any system you do not own.  
Do not run brute-force tools against office or public systems.

---

## Project overview
A small, reproducible lab demonstrating SSH credential brute-force (safe, local).  
Includes:
- ssh_bruteforce.py — sequential Python brute-force using paramiko
- passwords.txt — sample wordlist
- credentials.txt — appended results (proof of run)
- reports/ — generated JSON reports 

Purpose: illustrate recon → access attempt → reporting, and demonstrate mitigations.

---

## Requirements (Kali VM recommended)
- Python 3.8+
- python3-venv (or use get-pip.py if apt unavailable)
- Inside virtualenv:
  - paramiko
  - colorama
- Tools:  virtualbox (host)

---

## Quick setup (copy-paste sequence)
1. Create project folder and enter it:
   ```bash
      mkdir -p ~/ssh-project && cd ~/ssh-project

2.Create & activate a Python virtual environment (recommended):
      python3 -m venv ~/ssh-env
      source ~/ssh-env/bin/activate
3. Inside the venv install libs:
      pip install --upgrade pip
      pip install paramiko colorama
4.Ensure ssh_bruteforce.py and passwords.txt are in the folder:
      ls -l ssh_bruteforce.py passwords.txt
      chmod +x ssh_bruteforce.py
5.Ensure the SSH server (target) is running (on victim VM / localhost):
      # on the target system
            sudo apt install -y openssh-server
            sudo systemctl enable --now ssh
6.How to run (examples)
      Sequential demo (local):
            python3 ./ssh_bruteforce.py 127.0.0.1 -u victim -P ./passwords.txt
7.If target is on LAN:
```````python3 ./ssh_bruteforce.py 192.168.1.33 -u testuser -P ./passwords.txt --delay 0.5

8.Expected output
        Lines per attempt:
            [-] 1/5 Failed: 123456

            [...]

            [+] SUCCESS: victim@127.0.0.1 password: Victim@123

On success, the found credential is appended to credentials.txt.

9.Saving reports 
A sample JSON report template (create reports/<timestamp>.json):

# reliable timestamp variables
ts=$(date +%Y%m%dT%H%M%S)
# fallback for systems without --iso-8601
iso=$(date --iso-8601=seconds 2>/dev/null || date +"%Y-%m-%dT%H:%M:%S%z")

# safe counts/values
wordcount=0
[ -f ~/ssh-project/passwords.txt ] && wordcount=$(wc -l < ~/ssh-project/passwords.txt)

found=false
grep -q ":" ~/ssh-project/credentials.txt 2>/dev/null && found=true

cred=""
[ -f ~/ssh-project/credentials.txt ] && cred=$(tail -n 1 ~/ssh-project/credentials.txt)

# write the JSON report
cat > ~/ssh-project/reports/run-${ts}.json <<JSON
{
  "timestamp":"${iso}",
  "target":"127.0.0.1",
  "user":"victim",
  "wordlist_count":${wordcount},
  "found":${found},
  "credential":"${cred}",
  "notes":"Local lab run — Kali attacker → localhost victim"
}
JSON

10.Defences to demonstrate
    ->Disable password auth (strong mitigation):
               Edit /etc/ssh/sshd_config → set PasswordAuthentication no
               sudo systemctl restart ssh
    ->Enforce key-only logins + PermitRootLogin no
    ->Install and configure fail2ban (or demonstrate simple iptables rate-limit)
    ->Show logs: sudo tail -n 50 /var/log/auth.log
```bash

mkdir -p ~/ssh-project && cd ~/ssh-project
