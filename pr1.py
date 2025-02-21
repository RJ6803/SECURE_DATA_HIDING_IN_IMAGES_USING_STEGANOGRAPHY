import cv2
import os

def xor_encrypt(text, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))

# Read the image
img_path = input("Enter image path: ")
img = cv2.imread(img_path)

if img is None:
    print("Error: Could not load image.")
    exit()

msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

# Encrypt message with XOR
encrypted_msg = xor_encrypt(msg, password)

# Convert the message length to fit inside the image
height, width, _ = img.shape
max_chars = (height * width * 3) - 10  # Use all 3 channels, reserve 10 bytes for length

if len(encrypted_msg) > max_chars:
    print("Error: Message is too long for the selected image.")
    exit()

# Store message length in the first 10 bytes across all 3 channels
msg_length = len(encrypted_msg)
for i in range(10):
    channel = i % 3  # Cycle through B, G, R
    pixel_index = i // 3  # Spread across the first few pixels
    img[0, pixel_index, channel] = (msg_length >> (i * 8)) & 0xFF

# Encrypt message into image (use all channels)
index = 0
for i in range(height):
    for j in range(10 if i == 0 else 0, width):  # Skip first 10 pixels in first row
        for k in range(3):  # Use all three channels
            if index < len(encrypted_msg):
                img[i, j, k] = ord(encrypted_msg[index]) & 0xFF  # Ensure value stays in range
                index += 1
            else:
                break

# Save as PNG to avoid corruption
output_path = "encryptedImage.png"
cv2.imwrite(output_path, img)
print(f"Encryption complete. Image saved as '{output_path}'.")
