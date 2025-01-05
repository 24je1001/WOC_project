#!/usr/bin/env python3

import argparse
from PIL import Image

def hide_message_in_image(image_path, output_path, message):
    # Open the image
    image = Image.open(image_path)
    image = image.convert('RGB')  # Ensure the image is in RGB format
    pixels = image.load()

    # Convert the message to binary
    message_binary = ''.join(format(ord(char), '08b') for char in message)
    message_binary += '00000000'  # Add a null character to mark the end of the message

    width, height = image.size
    pixel_count = 0
    binary_index = 0

    for y in range(height):
        for x in range(width):
            if pixel_count % 7 == 0 and binary_index < len(message_binary):
                r, g, b = pixels[x, y]

                # Modify the least significant bit of the red channel to store the message bit
                new_r = (r & ~1) | int(message_binary[binary_index])
                pixels[x, y] = (new_r, g, b)
                binary_index += 1

            pixel_count += 1

    # Save the modified image
    image.save(output_path)
    print(f"Message hidden in {output_path}")

def extract_message_from_image(image_path):
    # Open the image
    image = Image.open(image_path)
    image = image.convert('RGB')  # Ensure the image is in RGB format
    pixels = image.load()

    width, height = image.size
    pixel_count = 0
    message_binary = ''

    for y in range(height):
        for x in range(width):
            if pixel_count % 7 == 0:
                r, g, b = pixels[x, y]

                # Extract the least significant bit of the red channel
                message_binary += str(r & 1)

            pixel_count += 1

    # Convert the binary message to text
    message = ''
    for i in range(0, len(message_binary), 8):
        byte = message_binary[i:i + 8]
        if byte == '00000000':  # Stop at the null character
            break
        message += chr(int(byte, 2))

    return message

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Steganography Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for hiding a message
    hide_parser = subparsers.add_parser("hide", help="Hide a message in an image")
    hide_parser.add_argument("input", help="Path to the input image")
    hide_parser.add_argument("output", help="Path to save the output image")
    hide_parser.add_argument("message", help="Message to hide")

    # Subparser for extracting a message
    extract_parser = subparsers.add_parser("extract", help="Extract a message from an image")
    extract_parser.add_argument("input", help="Path to the image to extract the message from")

    args = parser.parse_args()

    if args.command == "hide":
        hide_message_in_image(args.input, args.output, args.message)
    elif args.command == "extract":
        extracted_message = extract_message_from_image(args.input)
        print(f"Extracted Message: {extracted_message}")
