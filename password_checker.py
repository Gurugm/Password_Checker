import requests
import hashlib
import sys

def password_check(query_char):
    url = 'https://haveibeenpwned.com/range/' + query_char
    response = requests.get(url)
    print(response)
    if response.status_code != 200:
        raise RuntimeError(f'Error : {response}, please change it')
    return response

def leaks_count(hashes , hashes_to_check ):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h ,count in hashes:
        if h == hashes_to_check :
            return count
    return 0

def hash_converter(password):
    sha1_pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5 , tail = sha1_pass[:5], sha1_pass[5:]
    res = password_check(first5)
    return leaks_count(res , tail)

def main(args):
    for password in args:
        count = hash_converter(password)
        if count :
            print(f'Password was found {count} times . Change it')
        else:
            return ' All Good'
    return 'Done'

if __name__ == '__main__':
    main(sys.argv[1:])