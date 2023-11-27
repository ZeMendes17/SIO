import pkcs11
import PyKCS11

# Attributes are key-value pairs, get all the possible keys
all_attr = list( PyKCS11.CKA.keys() )
#Filter attributes
all_attr = [e for e in all_attr if isinstance(e, int)]
slot = 0  # Define the slot variable
session = pkcs11.openSession(slot)  # Open the session
for obj in session.findObjects():
    # Get object attributes
    attr = session.getAttributeValue(obj, all_attr)
    # Create dictionary with attributes
    attr = dict(zip(map(PyKCS11.CKA.get, all_attr), attr))
    # Print the object label
    print('Label: %s, Class: %d' % (attr['CKA_LABEL'], attr['CKA_CLASS']))
    print('Class: %d means private key, %d means public key, %d means certificate' % (PyKCS11.CKO_PRIVATE_KEY, PyKCS11.CKO_PUBLIC_KEY, PyKCS11.CKO_CERTIFICATE))
