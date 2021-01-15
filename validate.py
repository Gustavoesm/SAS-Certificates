#!/usr/bin/env python3

# CONSTANTS
MSG_WRONG_ARGS = "\nIncorrect arguments.\n\nPlease use the following format: ./validate path_to_file path_to_certificate"

import sys, base64, datetime

# check for incorrect versions of package
import pkg_resources
pkg_resources.require("cryptography>3.0")

from cryptography.x509 import load_der_x509_certificate # imports certificate loader

# removes own command syntax from sys argv list
del sys.argv[0]

# checks for incorrect number of args
if (len(sys.argv) != 2):
    print(MSG_WRONG_ARGS)
    sys.exit()

# gets file address from args
fileaddr = str(sys.argv[0])
certaddr = str(sys.argv[1])


# tries to open a file given the address and saves it's contents for later use
try:
    file = open(fileaddr)

    # data extraction
    content = file.readlines() # saves all lines in a list
    filename = content[1][4::] # extracts the name substring
    signer = content[4][10::] # extracts the signer name
    doc = content[7] # extracts the encoded document
    signature = content[10] # extracts the encoded signature certificate
except IOError:
    print("\nError: File not accessible.\n")
    file.close()
    sys.exit()
finally:
    file.close()

# checks for existent certificate header
if not(content[0] == "-----BEGIN DOCSIGNED-----\n"):
    print("\nDocument not signed.\n")
    sys.exit()

# tries to open the certificate given the address and saves it's contents for later use
try:
    file = open(certaddr, 'rb')
    certificate = load_der_x509_certificate(file.read())
except IOError:
    print("\nError: Certificate not accessible.\n")
    file.close()
    sys.exit()
finally:
    file.close()

# Decoding b64 section
doc = base64.b64decode(doc.encode('utf-8')) # parses to byte format before encoding
signature = base64.b64decode(signature.encode('utf-8')) # parses to byte format before encoding

# gets current timestamp from system
today = datetime.datetime.now()
# sets valid time range for certificate
validRange = [certificate.not_valid_before, certificate.not_valid_after]

# checks document certificate ingrity and if within valid date
if (signature == certificate.signature and validRange[0] < today < validRange[1]):
    print("\nDocumento íntegro e assinado por "+signer[0:-1]+".\n")
else:
    print("\nDocumento com integridade corrompida.")

# document file creation section
file = open("output/"+filename, 'w+b')
file.write(doc)
file.close()
