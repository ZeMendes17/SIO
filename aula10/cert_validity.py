import cryptography.x509
import datetime
import sys

def get_cert_validity(cert):
    """Get the validity of a certificate.

    Args:
        cert (cryptography.x509.Certificate): The certificate to check.

    Returns:
        str: The validity of the certificate.
    """
    now = datetime.datetime.now()
    if cert.not_valid_before < now < cert.not_valid_after:
        return True
    else:
        return False
    
if __name__ == "__main__":
    # Load the cert passed as argument
    if len(sys.argv) != 2:
        print("Usage: python3 cert_validity.py <cert>")
        sys.exit(1)

    certs = {}

    cert = cryptography.x509.load_pem_x509_certificate(open(sys.argv[1], "rb").read())
    certs[str(cert.subject)] = cert

    if get_cert_validity(cert):
        print("Certificate is valid")
    else:
        print("Certificate is not valid")