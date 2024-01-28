import hmac, base64, struct, hashlib, time, array


def truncate(hmac_sha1):
    offset = int(hmac_sha1[-1], 16)
    binary = int(hmac_sha1[(offset * 2):((offset * 2) + 8)], 16) & 0x7fffffff
    return str(binary)


def long_to_byte_array(long_num):
    byte_array = array.array('B')
    for _ in reversed(range(0, 8)):
        byte_array.insert(0, long_num & 0xff)
        long_num >>= 8
    return byte_array


def hotp(k, c, digits=6):
    c_bytes = long_to_byte_array(c)
    hmac_sha1 = hmac.new(key=k, msg=c_bytes, digestmod=hashlib.sha1).hexdigest()
    return truncate(hmac_sha1)[-digits:]


def totp(secret_key, digits=6, time_window=30):
    current_time_window = int(time.time() / time_window)
    return hotp(base64.b32decode(secret_key), current_time_window, digits=digits)


def hotp_secret(player_id: str, secret_key: str) -> str:
    combined_key = player_id.encode('utf-8') + secret_key.encode('utf-8')
    hashed_key = hashlib.sha256(combined_key).digest()
    return base64.b32encode(hashed_key).decode('utf-8')
