import re
import urllib.request
import urllib.error
import json
import smtplib
from email.mime.text import MIMEText
import keyring

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
emailBody = ''
for keyword in keywords:
    emailBody += keyword + ':\n'
    keyword = str.replace(keyword, ' ', '+')
    r = {}
    i = 0
    while (i < 20) & (r == {}):
        i += 1
        try:
            r = urllib.request.urlopen('https://api.oznzb.com/api?extended=1&o=json&t=search&q=' + keyword + '&apikey=' + api)
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