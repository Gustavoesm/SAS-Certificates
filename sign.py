#!/usr/bin/env python3

# CONSTANTS
MSG_WRONG_ARGS = "\nIncorrect arguments.\n\nPlease use the following format: ./sign \"name\" path_to_file path_to_certificate password\n"

# for handling args, b64 encoding/decoding
import sys, base64

# check for incorrect versions of package
import pkg_resources
pkg_resources.require("cryptography>3.0")

from cryptography.hazmat.primitives.serialization import pkcs12 # imports filetype pkcs12 loader
from cryptography.x509 import load_pem_x509_certificate # imports certificate loader

# removes own command syntax from sys argv list
del sys.argv[0]

# checks for incorrect number of args
if (len(sys.argv) != 4):
    print(MSG_WRONG_ARGS)
    sys.exit()

# gets name, file adress, file path and password from args
name = str(sys.argv[0])
fileaddr = sys.argv[1]
p12path = sys.argv[2]
passwd = sys.argv[3]

# tries to open a file given the name and saves it's contents for later use
try:
    file = open(fileaddr, 'rb')
    content = file.read()
except IOError:
    print("\nError: File not accessible.\n")
    file.close()
    sys.exit()
finally:
    file.close()

# checks for existent certificate header
if (content[0:25] == "-----BEGIN DOCSIGNED-----"):
    print("\nDocument already signed.\n")
    sys.exit()

# gets filename from filepath
filename = fileaddr.split('/')[-1]


# tries to open and encode p12 certificate
try:
    passwd = passwd.encode('utf-8') # parses password to byte format
    file = open(p12path, 'rb')

    # loads certificate data using password with cryptography pkcs12 load function
    certificate = pkcs12.load_key_and_certificates(file.read(), passwd)[1]

    # gets commonName from certificate subject array (it's always the last one)
    for attribute in certificate.subject:
        CN = attribute.value

except IOError:
    print("\nError: File not accessible or wrong password.\n")
    file.close()
    sys.exit()
finally:
    file.close()

# header creation
header = "-----BEGIN DOCSIGNED-----\n"
header += "doc:"+filename+'\n'
header += "alg:RSA\nhash:SHA1\nassinante:"+CN+"\n\n-----BEGIN DOC-----\n"

# encodes file content in b64
content = base64.b64encode(content)

# encodes certificate content in b64
certificate = base64.b64encode(certificate.signature)

# appends header to the beggining of the file
content = header + content.decode('utf-8') + "\n-----END DOC-----\n"

# adds signature and mounts final document body
content += "-----BEGIN SIGNATURE-----\n"+certificate.decode('latin-1')+"\n-----END SIGNATURE-----\n-----END DOCSIGNED-----\n"

# creates a file and writes it's contents
file = open("output/"+name+".txt", 'w+')
file.write(content)
file.close()
