#!/usr/bin/env python

import imaplib
import email
from email.header import decode_header
import json

cnt = 0
obj = imaplib.IMAP4_SSL('imap.gmail.com', '993')
# add the line here that includes gmail login info [dont leak secrets :)]
obj.select("inbox")

return_code, data = obj.search(None, '(UNSEEN X-GM-RAW "category:primary")')
count = len(data[0].split())
if count == 0:
    print("")
output = {
    "text": count,
    "alt": "",
    "tooltip": "",
}
tooltip = ""

for num in data[0].split():
    typ, msg_data = obj.fetch(num, '(BODY.PEEK[])')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            # Parse the email message
            msg = email.message_from_bytes(response_part[1])

            # Decode the email's 'From' field
            sender = msg["From"]
            decoded_sender, encoding = decode_header(sender)[0]
            # print(decoded_sender, type(decoded_sender))

            if isinstance(decoded_sender, bytes):
                decoded_sender = decoded_sender.decode(
                    encoding if encoding else "utf-8")

            # Decode the email's 'Subject' field
            subject = msg["Subject"]
            decoded_subject, encoding = decode_header(subject)[0]
            # print(decoded_subject, type(decoded_subject))

            if isinstance(decoded_subject, bytes):
                decoded_subject = decoded_subject.decode(
                    encoding if encoding else "utf-8")

            # Add to the tooltip string
            if tooltip == "":
                tooltip = decoded_sender
            else:
                tooltip += decoded_subject

output['tooltip'] = tooltip
print(json.dumps(output))

obj.close()
obj.logout()
