import random
import base64

symbols = "1234567890-=qwertyuiop[]asdfghjkl;,:zxcvbnm.?!@#$%^<>&*()_+"

def create_token():
	code_str = ''
	for i in range(30):
		rand_num = random.randint(0, 58)
		code_str += symbols[rand_num]

	bytes_url_decode_str = base64.urlsafe_b64encode(bytes(code_str, 'utf-8'))
	url_decode_str = bytes_url_decode_str.decode('utf-8')
	return code_str, url_decode_str
