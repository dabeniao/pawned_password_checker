# Thanks to the API and data provided by https://haveibeenpwned.com

from getpass import getpass
import hashlib
import http.client

def checkLeak(password):

    sha1 = hashlib.sha1()
    sha1.update(password)
    password_hash = sha1.hexdigest()
    password_hash = password_hash.upper()

    conn = http.client.HTTPSConnection("api.pwnedpasswords.com")
    headers = { "Add-Padding": "true" }
    conn.request("GET", "/range/" + password_hash[:5], {}, headers)

    response = conn.getresponse()
    if response.status != 200:
        print('network error')
        return

    response_body = response.read().decode('utf-8')

    for line in response_body.split('\n'):
        subhash, count = line.split(':')
        count = int(count)
        if count <= 0:
            continue
        if password_hash[5:] == subhash:
            print("{} occurrences found".format(count))
            return

    print('not leaked')


def main():
    try:
        while True:
            password = None
            password = getpass().encode('utf-8')
            checkLeak(password)
    except EOFError:
        print()


if __name__ == '__main__':
    main()

