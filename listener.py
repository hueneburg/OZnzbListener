import re
import urllib.request
import urllib.error
import json
import smtplib
from email.mime.text import MIMEText
import keyring
import sys


arguments = ['-a', '-d', '-e', '-h', '-k', '-r', 's', '-p', '-u', '--add-keyword', '--delete-keyword', '--api',
             '--add-receiver', '--delete-receiver', '--sender', '--server', '--ssl', '--user', '--password',
             '--status', '--help']


def add_keywords(args, index):
    f = open('data.conf', 'r')
    lines = f.readlines()
    f.close()
    f = open('data.conf', 'w')
    for line in lines:
        if line.startswith('keyword'):
            keywords = re.findall('keywords:.*', line)[0]
            keywords = re.findall('\'.*?\'', keywords)
            buffer = []
            for keyword in keywords:
                buffer.append(re.findall('[^\']+', keyword)[0])
            keywords = buffer
            index += 1
            while index < len(args):
                if args[index] in arguments:
                    break
                else:
                    if not args[index] in keywords:
                        keywords.append(args[index])
                index += 1
            line = 'keywords:' + str(keywords) + '\n'
        f.write(line)
    f.close()
    return index


def delete_keywords(args, index):
    f = open('data.conf', 'r')
    lines = f.readlines()
    f.close()
    f = open('data.conf', 'w')
    for line in lines:
        if line.startswith('keyword'):
            keywords = re.findall('keywords:.*', line)[0]
            keywords = re.findall('\'.*?\'', keywords)
            buffer = []
            for keyword in keywords:
                buffer.append(re.findall('[^\']+', keyword)[0])
            keywords = buffer
            index += 1
            while index < len(args):
                if args[index] in arguments:
                    break
                else:
                    if args[index] in keywords:
                        keywords.remove(args[index])
                index += 1
            line = 'keywords:' + str(keywords) + '\n'
        f.write(line)
    f.close()
    return index


def change_api(args, index):
    f = open('data.conf', 'r')
    lines = f.readlines()
    f.close()
    f = open('data.conf', 'w')
    for line in lines:
        if line.startswith('api'):
            api = re.findall('api:.+', line)[0]
            api = re.findall('\'.+\'', api)[0]
            api = re.findall('[^\']+', api)[0]
            index += 1
            while index < len(args):
                if args[index] in arguments:
                    break
                else:
                    api = args[index]
                index += 1
            line = 'api:\'' + api + '\'\n'
        f.write(line)
    f.close()
    return index


def add_receivers(args, index):
    f = open('data.conf', 'r')
    lines = f.readlines()
    f.close()
    f = open('data.conf', 'w')
    for line in lines:
        if line.startswith('receiver'):
            receivers = re.findall('receivers:.*', line)[0]
            receivers = re.findall('\'.*?\'', receivers)
            buffer = []
            for receiver in receivers:
                buffer.append(re.findall('[^\']+', receiver)[0])
            receivers = buffer
            index += 1
            while index < len(args):
                if args[index] in arguments:
                    break
                else:
                    if not args[index] in receivers:
                        receivers.append(args[index])
                index += 1
            line = 'receivers:' + str(receivers) + '\n'
        f.write(line)
    f.close()
    return index


def delete_receivers(args, index):
    f = open('data.conf', 'r')
    lines = f.readlines()
    f.close()
    f = open('data.conf', 'w')
    for line in lines:
        if line.startswith('receiver'):
            receivers = re.findall('receivers:.*', line)[0]
            receivers = re.findall('\'.*?\'', receivers)
            buffer = []
            for receiver in receivers:
                buffer.append(re.findall('[^\']+', receiver)[0])
            receivers = buffer
            index += 1
            while index < len(args):
                if args[index] in arguments:
                    break
                else:
                    if args[index] in receivers:
                        receivers.remove(args[index])
                index += 1
            line = 'receivers:' + str(receivers) + '\n'
        f.write(line)
    f.close()
    return index


def change_sender(args, index):
    f = open('data.conf', 'r')
    lines = f.readlines()
    f.close()
    f = open('data.conf', 'w')
    for line in lines:
        if line.startswith('sender'):
            sender = re.findall('sender:.+', line)[0]
            sender = re.findall('\'.+\'', sender)[0]
            sender = re.findall('[^\']+', sender)[0]
            index += 1
            while index < len(args):
                if args[index] in arguments:
                    break
                else:
                    sender = args[index]
                index += 1
            line = 'sender:\'' + sender + '\'\n'
        f.write(line)
    f.close()
    return index


def change_server(args, index):
    f = open('data.conf', 'r')
    lines = f.readlines()
    f.close()
    f = open('data.conf', 'w')
    for line in lines:
        if line.startswith('server'):
            server = re.findall('server:.+', line)[0]
            server = re.findall('\'.+\'', server)[0]
            server = re.findall('[^\']+', server)[0]
            index += 1
            while index < len(args):
                if args[index] in arguments:
                    break
                else:
                    pw = keyring.get_password('password', server)
                    user = keyring.get_password('username', server)
                    keyring.delete_password('password', server)
                    keyring.delete_password('username', server)
                    server = args[index]
                    keyring.set_password('password', server, pw)
                    keyring.set_password('username', server, user)
                index += 1
            line = 'server:\'' + server + '\'\n'
        f.write(line)
    f.close()
    return index


def toggle_ssl(args, index):
    f = open('data.conf', 'r')
    lines = f.readlines()
    f.close()
    f = open('data.conf', 'w')
    for line in lines:
        if line.startswith('ssl'):
            ssl = re.findall('ssl:.+', line)[0]
            ssl = re.findall('\'.+\'', ssl)[0]
            ssl = re.findall('[^\']+', ssl)[0]
            if ssl == 'yes':
                ssl = 'no'
            else:
                ssl = 'yes'
            line = 'ssl:\'' + ssl + '\'\n'
        f.write(line)
    f.close()
    return index + 1


def change_user(args, index):
    server = re.findall('server:.+', open('data.conf', 'r').read())[0]
    server = re.findall('\'[^\']+\'', server)[0]
    server = re.findall('[^\']+', server)[0]
    index += 1
    if not args[index] in arguments:
        keyring.set_password('username', server, args[index])
    return index + 1


def change_password(args, index):
    server = re.findall('server:.+', open('data.conf', 'r').read())[0]
    server = re.findall('\'[^\']+\'', server)[0]
    server = re.findall('[^\']+', server)[0]
    index += 1
    if not args[index] in arguments:
        keyring.set_password('password', server, args[index])
    return index + 1


def show_status(args, index):
    options = open('data.conf', 'r').read()
    server = re.findall('server:.+', options)[0]
    server = re.findall('\'[^\']+\'', server)[0]
    server = re.findall('[^\']+', server)[0]
    while options.endswith('\n'):
        options = options[:-1]
    print(options)
    print('username:\'' + keyring.get_password('username', server) + '\'')
    return index + 1


def switch_argument(args, index):
    arg = args[index]
    if (arg == '-k') | (arg == '--add-keyword'):
        return add_keywords(args, index)
    elif (arg == '-d') | (arg == '--delete-keyword'):
        return delete_keywords(args, index)
    elif (arg == '-a') | (arg == '--api'):
        return change_api(args, index)
    elif (arg == '-r') | (arg == '--add-receiver'):
        return add_receivers(args, index)
    elif (arg == '--delete-receiver'):
        return delete_receivers(args, index)
    elif (arg == '-s') | (arg == '--sender'):
        return change_sender(args, index)
    elif (arg == '-h') | (arg == '--server'):
        return change_server(args, index)
    elif (arg == '-e') | (arg == '-ssl'):
        return toggle_ssl(args, index)
    elif (arg == '-u') | (arg == '--user'):
        return change_user(args, index)
    elif (arg == '-p') | (arg == '--password'):
        return change_password(args, index)
    elif arg == '--status':
        return show_status(args, index)
    else:
        return show_help(args, index)


def show_help(args, index):
    separator = ''
    print('Usage:\nlistener.py [(-k|--add-keyword) KEYWORDS] [(-d|--delete-keyword) KEYWORDS] [(-a|--api) APIKEY] '
          '[(-r|--add-receiver) RECEIVERS] [--delete-receiver RECEIVERS] [(-s|--sender) SENDER] [(-h|--server) SERVER] '
          '[(-e|--ssl)] [(-u|--user) USER] [(-p|--password) PASSWORD] [--status] [--help]')
    print(separator)
    print('(-k|--add-keyword) KEYWORDS: Adds the keywords to the keyword list. Keywords are separated by a whitespace.')
    print(separator)
    print('(-d|--delete-keyword) KEYWORDS: Removes keywords from the list. Keywords are separated by a whitespace.')
    print(separator)
    print('(-a|--api) APIKEY: Changes the api key.')
    print(separator)
    print('(-r|--add-receiver) RECEIVERS: Adds new receivers to the list. Receivers are separated by a whitespace.')
    print(separator)
    print('--delete-receiver RECEIVERS: Removes receivers from the list. Receivers are separated by a whitespace.')
    print(separator)
    print('(-s|--sender) SENDER: Changes the sender.')
    print(separator)
    print('(-h|--server) SERVER: Changes the SMTP-server.')
    print(separator)
    print('(-e|--ssl): Toggles whether to use ssl or not.')
    print(separator)
    print('(-u|--user) USER: Changes the username for the SMTP-server.')
    print(separator)
    print('(-p|--password) PASSWORD: Changes the password for the SMTP-server.')
    print(separator)
    print('--status: Prints the configuration (except password).')
    print(separator)
    print('--help: Prints this page.')
    return index + 1


def send():
    options = (open('data.conf', 'r').read())
    api = re.findall('api:.+', options)[0]
    api = re.findall('\'.+\'', api)[0]
    api = re.findall('[^\']+', api)[0]
    receivers = re.findall('receivers:.*', options)[0]
    receivers = re.findall('\'.*?\'', receivers)
    buffer = []
    for receiver in receivers:
        buffer.append(re.findall('[^\']+', receiver)[0])
    receivers = buffer
    sender = re.findall('sender:.+', options)[0]
    sender = re.findall('\'[^\']+\'', sender)[0]
    sender = re.findall('[^\']+', sender)[0]
    keywords = re.findall('keywords:.*', options)[0]
    keywords = re.findall('\'.*?\'', keywords)
    buffer = []
    for keyword in keywords:
        buffer.append(re.findall('[^\']+', keyword)[0])
    keywords = buffer
    server = re.findall('server:.+', options)[0]
    server = re.findall('\'[^\']+\'', server)[0]
    server = re.findall('[^\']+', server)[0]
    port = re.findall('port:\d+', options)[0]
    port = re.findall('\d+', port)[0]
    ssl = re.findall('ssl:.+', options)[0]
    if ssl.endswith('yes'):
        ssl = True
    else:
        ssl = False

    emailBody = ''
    for keyword in keywords:
        emailBody += keyword + ':\n'
        keyword = str.replace(keyword, ' ', '+')
        r = {}
        i = 0
        while (i < 20) & (r == {}):
            i += 1
            try:
                r = urllib.request.urlopen(
                    'https://api.oznzb.com/api?extended=1&o=json&t=search&q=' + keyword + '&apikey=' + api)
            except urllib.error.URLError:
                r = {}

        if r == {}:
            emailBody += 'An error occurred (probably connection refused, which is a server error)'
        else:
            channel = json.loads(r.read().decode('utf-8'))['channel']
            for item in channel['item']:
                print('Link:  ' + item['link'])
                print('Title: ' + item['title'])
                print('Desc:  ' + item['description'])
        emailBody += '\n\n'

    msg = MIMEText(emailBody)
    msg['Subject'] = 'UseNet News'
    msg['From'] = sender
    msg['To'] = receivers

    user = keyring.get_password('username', server)
    pw = keyring.get_password('password', server)
    smtp = {}
    if ssl:
        smtp = smtplib.SMTP_SSL(host=server, port=port)
    else:
        smtp = smtplib.SMTP(host=server, port=port)

    smtp.login(user, pw)
    smtp.send_message(msg)
    smtp.quit()


args = sys.argv
if len(args) == 0:
    send()
else:
    i = 1
    while i < len(args):
        i = switch_argument(args, i)