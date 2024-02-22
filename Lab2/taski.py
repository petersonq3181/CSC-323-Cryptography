def pad(p, block):
    padding = block - (len(p) % block)
    if padding == 0:
        padding = block
    return p + bytes([padding] * padding)

def unpad(padded, block):
    if len(padded) % block != 0:
        raise ValueError("incorrect padded message length")

    padding = padded[-1]

    if padding < 1 or padding > block:
        raise ValueError("incorrect padding size")

    for byte in padded[-padding:]:
        if byte != padding:
            raise ValueError("incorrect padding bytes")

    return padded[:-padding]

block_size = 16
message = b"Hello, Worlddd"

padded = pad(message, block_size)
print("Padded message:", padded)

unpadded = unpad(padded, block_size)
print("Unpadded message:", unpadded)
