import socket
from common_ports import ports_and_services as po

def get_open_ports(target: str, port_range: list, verbose=False):
	'''
	Function that checks a target for open ports
	:target: URL or ip
	:port_range: list of two ints, lower and upper range
	:verbose: optional param to return result in descriptive printable format
	:return: list of open ports in given range
	'''
	# define URL and IP based on the given target. Return error message
	# if hostname or IP are invalid
	if target[0].isalpha():
		url = target
		try:
			ip = socket.gethostbyname(url)
		except:
			return "Error: Invalid hostname"
	else:
		ip = target
		try:
			ip = socket.gethostbyname(ip).split()[0]
		except:
			return 'Error: Invalid IP address'
		else:
			try:
				url = socket.gethostbyaddr(ip)[0]
			except:
				url = None

	# create list for open ports
	open_ports = []
	# create socket for every port in given range and check if it's
	# possible to connect.
	for port in range(port_range[0], port_range[1]+1):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# if no error when connecting, add port to the list of open ports
		if not s.connect_ex((ip, port)):
			open_ports.append(port)
		s.close()
			
	# if 'verbose mode' is True, create a descriptive result
	if verbose:
		output = [0, 1]
		output[0] = f'Open ports for {url} ({ip})' if ip and url else f'Open ports for {ip}'
		output[1] = 'PORT     SERVICE'
		for port in open_ports:
			port = f'{port:<4}     {po[port]}'
			output.append(port)

		open_ports = '\n'.join(output)

	return open_ports
