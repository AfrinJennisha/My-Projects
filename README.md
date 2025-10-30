# SSH Cracker — Lab Project (Educational / Lab Only)

*Author:* Afrin  
*Environment:* Kali Linux VM (attacker) → Localhost / VM (victim)  
*Date:* <replace-with-date>

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
- advance_ssh_brute.py — (optional) multithreaded/advanced version (if added)
- passwords.txt — sample wordlist
- credentials.txt — appended results (proof of run)
- reports/ — generated JSON reports (optional)

Purpose: illustrate recon → access attempt → reporting, and demonstrate mitigations.

---

## Requirements (Kali VM recommended)
- Python 3.8+
- python3-venv (or use get-pip.py if apt unavailable)
- Inside virtualenv:
  - paramiko
  - colorama
- Tools: nmap, hydra (optional), virtualbox (host)

---

## Quick setup (copy-paste sequence)
1. Create project folder and enter it:
```bash
mkdir -p ~/ssh-project && cd ~/ssh-project