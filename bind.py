import numpy as np
from PIL import Image

def read_secret(secret_file):
    with open(secret_file, 'rb') as file:
        return file.read()

def import_image(img_file):
    return np.array(Image.open(img_file))

def find_capacity(img, secret):
    img_size = img.size
    secret_size = len(secret)
    return img_size, secret_size

def encode_capacity(img, secret_size):
    # Encode the size of the secret file into the first few pixels of the image
    # Example implementation: replace the LSB of each pixel's R channel
    for i in range(secret_size.bit_length()):
        img[i] = (img[i] & 0xFE) | ((secret_size >> i) & 1)

def encode_secret(img, secret):
    # Encode the secret file into the image
    # Example implementation: replace the LSB of each pixel's G channel
    for i, byte in enumerate(secret):
        for j in range(8):
            img[i * 8 + j] = (img[i * 8 + j] & 0xFE) | ((byte >> j) & 1)

def encode(img_file, secret_file):
    # Read the secret file
    secret = read_secret(secret_file)

    # Read the image
    img = import_image(img_file)

    # Find the size of the secret file and the capacity of the image
    img_size, secret_size = find_capacity(img, secret)

    # Check if the secret file is too large for the image
    if secret_size >= img_size:
        print('Secret file is too large for this image. Please use a larger image.')
        return None
    else:
        # Prompt the user to proceed
        if input("Proceed? (y/n): ").lower() != 'y':
            return None

        # Save dimensions of the image then flatten it
        img_dim = img.shape
        img = img.flatten()

        # Encode length to image
        encode_capacity(img, secret_size)

        # Encode secret file to image
        encode_secret(img, secret)

        # Reshape the image back to 3D
        img = img.reshape(img_dim)

        # Save the image
        stego_image = Image.fromarray(img)
        stego_image.save('stego_image.png')
        print('Done. "stego_image.png" should be in your directory.')

# Example usage
encode("secret.png", "Malware.py")
