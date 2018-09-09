# Utility for Copying Files from an SFTP Server to an S3 Bucket
#
# Copyright 2017 Jonas McCallum.
#
# Open source, MIT license
# http://www.opensource.org/licenses/mit-license.php
"""
Email parser

Author: Jonas McCallum
https://github.com/foobarmus

"""
import re

TOK_SPEC = [('CRUD',    '.+:', ''),
            ('EOL',     '$',   ''),
            ('TO',      '.+',  '(?<=To:)'),
            ('FROM',    '.+',  '(?<=From:)'),
            ('REGION',  '.+',  '(?<=Region:)'),
            ('SUBJECT', '.+',  '(?<=Subject:)'),
            ('BODY',    '.+',  '')]
TOKEN = '{}(?P<{}>{})'
TOKENS = (TOKEN.format(lookbehind, label, expression)
          for label, expression, lookbehind in TOK_SPEC)
RE = re.compile('|'.join(TOKENS), re.MULTILINE)
HEADER_LABELS = ['TO', 'FROM', 'REGION', 'SUBJECT']
IGNORE = ['CRUD', 'EOL']

def tokenize(text, re_, ignore):
    """tokenize an email template"""
    tokens = []
    pos = 0
    match = re_.match(text)
    while pos < len(text):
        typ = match.lastgroup
        if typ in ignore:
            pos = max(match.end(), pos + 1)
        elif typ == 'BODY':
            tok = text[pos:]
            tokens.append((typ, tok))
            break
        else:
            tok = match.group(typ).strip()
            tokens.append((typ, tok))
            pos = match.end()
        match = re_.match(text, pos)
    return tokens

def parse_email(template, **args):
    """populate and parse an email template"""
    with open(template, 'r') as f:
        text = f.read()
    personalized_template = text.format(**args)
    tokens = tokenize(personalized_template, RE, IGNORE)
    header = {k:v.strip() for k, v in tokens
              if k in HEADER_LABELS}
    body = tokens[-1][-1].strip()
    email = {'Destination': {'ToAddresses': [header['TO']]},
             'Message': {'Body': {'Text': {'Charset': 'UTF-8', 'Data': body}},
                         'Subject': {'Charset': 'UTF-8', 'Data': header['SUBJECT']}},
             'Source': header['FROM']}
    region = header['REGION']
    return email, region
