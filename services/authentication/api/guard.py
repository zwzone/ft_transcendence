import hmac, base64, struct, hashlib, time, array

def truncate(hmac_sha1):
    """
    truncate represents the function that converts an HMAc-SHA-1
    value into an hotp value as defined in Section 5.3.

    http://tools.ietf.org/html/rfc4226#section-5.3

    """
    offset = int(hmac_sha1[-1], 16)
    binary = int(hmac_sha1[(offset * 2):((offset * 2) + 8)], 16) & 0x7fffffff
    return str(binary)

def _long_to_byte_array(long_num):
    """
    helper function to convert a long number into a byte array
    """
    byte_array = array.array('B')
    for _ in reversed(range(0, 8)):
        byte_array.insert(0, long_num & 0xff)
        long_num >>= 8
    return byte_array

def hotp(k, c, digits=6):
    """
    hotp accepts key k and counter c
    optional digits parameter can control the response length

    returns the OATH integer code with {digits} length
    """
    c_bytes = _long_to_byte_array(c)
    hmac_sha1 = hmac.new(key=k, msg=c_bytes, digestmod=hashlib.sha1).hexdigest()
    return truncate(hmac_sha1)[-digits:]

def totp(k, digits=6, window=30):
    """
    totp is a time-based variant of hotp.
    It accepts only key k, since the counter is derived from the current time
    optional digits parameter can control the response length
    optional window parameter controls the time window in seconds

    returns the OATH integer code with {digits} length
    """
    c = int(time.time() / window)
    return hotp(base64.b32decode(k), c, digits=digits)
