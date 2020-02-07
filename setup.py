import os
import sys

def kill():
	os.system("ps aux | grep ython | grep qr_code | awk '{print $2}' | xargs kill -9")

def setup(mode):
	if mode == 'kill':
		kill()
		return

	RUN_COMMAND = 'nohup python3 -u qr_code.py &'

	if mode != 'debug':
		r = os.system('sudo pip3 install -r requirements.txt')

	kill()

	if mode.startswith('debug'):
		os.system(RUN_COMMAND[6:-2])
	else:
		os.system(RUN_COMMAND)


if __name__ == '__main__':
	if len(sys.argv) > 1:
		setup(sys.argv[1])
	else:
		setup('')