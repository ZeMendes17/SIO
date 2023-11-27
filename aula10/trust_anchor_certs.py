import os
import cryptography.x509
from cert_validity import get_cert_validity

def get_trust_anchor_certs():
    """Reads all system-trusted certificates into a
    dictionary of trusted certificates, with the
    subject as the key.
    Scan for all certificates in /etc/ssl/certs
    """
    trusted_certs = {}
    with os.scandir("/etc/ssl/certs") as it:
        for entry in it:
            if entry.is_file():
                cert = cryptography.x509.load_pem_x509_certificate(open(entry.path, "rb").read())
                if get_cert_validity(cert):
                    trusted_certs[str(cert.subject)] = cert
    return trusted_certs

if __name__ == "__main__":
    certs = get_trust_anchor_certs()
    
    for cert in certs:
        print(cert)