import cv2

def xor_decrypt(text, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))

# Read the encrypted image
img_path = input("Enter image path: ")
img = cv2.imread(img_path)

if img is None:
    print("Error: Could not load encrypted image.")
    exit()

# User input passcode
password = input("Enter passcode for decryption: ")

height, width, _ = img.shape

# Read message length from the first 10 bytes (spread across B, G, R channels)
msg_length = 0
for i in range(10):
    channel = i % 3  # Cycle through B, G, R
    pixel_index = i // 3  # Spread across the first few pixels
    msg_length |= (img[0, pixel_index, channel] << (i * 8))  # Read from correct channel

# Extract encrypted message from the image
encrypted_message = []
index = 0
for i in range(height):
    for j in range(10 if i == 0 else 0, width):  # Skip first 10 pixels in the first row
        for k in range(3):  # Read from all channels
            if index < msg_length:
                encrypted_message.append(chr(img[i, j, k]))  # Read ASCII value
                index += 1
            else:
                break

# Convert list to string
encrypted_message = ''.join(encrypted_message)

# Decrypt the message using XOR
decrypted_message = xor_decrypt(encrypted_message, password)

print("Decrypted message:", decrypted_message)
