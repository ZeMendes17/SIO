# Task: For this exercise, take each user-provided certificate (from the Citizen’s Card, XCA, downloaded,
# etc.) and recreate its validation chain in a list. To make the chain, load the user certificate, a dictionary of
# user-specified intermediate roots, and the roots.
# You should stop when you get a root certificate (i.e., self-signed). The root certificate can be missing from
# that list. That usually means the root certificate is already in your trusted certificates. Otherwise, the chain
# will be untrusted unless you already trust the user or intermediate certificates.
# HINT: Remember that the user and root certificates are loaded into a dictionary with the subject as the key.
# Therefore, it is simple to obtain the issuer of a certificate.

import sys
import cryptography.x509
from trust_anchor_certs import get_trust_anchor_certs

def get_cert_path(cert, trusted_certs):
    """Build the certificate path for a given certificate.
    
    Args:
        cert (cryptography.x509.Certificate): The certificate to build the path for.
        trusted_certs (dict): The trusted certificates.
    
    Returns:
        list: The certificate path.
    """
    cert_path = []
    
    # Add the user certificate to the path
    cert_path.append(cert)
    
    # Get the issuer of the user certificate
    issuer = str(cert.issuer)
    
    # While the issuer is not a root certificate
    while issuer not in trusted_certs and issuer != str(cert.subject):
        # Add the issuer to the path
        cert_path.append(trusted_certs[issuer])
        # Get the issuer of the issuer
        issuer = str(trusted_certs[issuer].issuer)
    
    # Add the root certificate to the path
    cert_path.append(trusted_certs[issuer])
    
    return cert_path

if __name__ == "__main__":
    # Load the cert passed as argument
    if len(sys.argv) != 2:
        print("Usage: python3 build_cert_path.py <cert>")
        sys.exit(1)

    certs = {}

    cert = cryptography.x509.load_pem_x509_certificate(open(sys.argv[1], "rb").read())
    certs[str(cert.subject)] = cert

    # Get the trusted certs
    trusted_certs = get_trust_anchor_certs()
    
    # Build the certificate path
    cert_path = get_cert_path(cert, trusted_certs)
    
    # Print the certificate path
    for cert in cert_path:
        print(cert)