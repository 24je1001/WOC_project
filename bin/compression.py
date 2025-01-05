#!/usr/bin/env python3

import argparse
import os

def is_binary(file_path):
    """Determine if a file is binary or text."""
    with open(file_path, 'rb') as file:
        chunk = file.read(1024)  # Read a small portion
    return b'\0' in chunk  # Binary files often contain null bytes

def compress_file(input_path, output_path, binary_mode):
    open_mode = 'rb' if binary_mode else 'r'
    write_mode = 'wb' if binary_mode else 'w'

    with open(input_path, open_mode) as f_in, open(output_path, write_mode) as f_out:
        data = f_in.read()
        if not binary_mode:
            data = data.encode()  # Convert text to bytes for uniform processing

        compressed_data = bytearray()
        i = 0
        while i < len(data):
            count = 1
            while i + 1 < len(data) and data[i] == data[i + 1] and count < 255:
                i += 1
                count += 1
            compressed_data.append(data[i])
            compressed_data.append(count)
            i += 1

        f_out.write(compressed_data)

def decompress_file(input_path, output_path, binary_mode):
    open_mode = 'rb' if binary_mode else 'r'
    write_mode = 'wb' if binary_mode else 'w'

    with open(input_path, open_mode) as f_in, open(output_path, write_mode) as f_out:
        data = f_in.read()
        if not binary_mode:
            data = data.encode()  # Convert text to bytes for uniform processing

        decompressed_data = bytearray()
        i = 0
        while i < len(data):
            char = data[i]
            count = data[i + 1]
            decompressed_data.extend([char] * count)
            i += 2

        if not binary_mode:
            decompressed_data = decompressed_data.decode()  # Convert bytes back to text
        f_out.write(decompressed_data)

def main():
    parser = argparse.ArgumentParser(description="Universal File Compression/Decompression Tool")
    parser.add_argument("operation", choices=["compress", "decompress"], help="Choose the operation to perform")
    parser.add_argument("input_path", help="Path to the input file")
    parser.add_argument("output_path", help="Path to the output file")

    args = parser.parse_args()

    if not os.path.exists(args.input_path):
        print(f"Error: File '{args.input_path}' does not exist.")
        return

    binary_mode = is_binary(args.input_path)

    if args.operation == "compress":
        try:
            compress_file(args.input_path, args.output_path, binary_mode)
            print(f"File successfully compressed to {args.output_path}")
        except Exception as e:
            print(f"An error occurred during compression: {e}")

    elif args.operation == "decompress":
        try:
            decompress_file(args.input_path, args.output_path, binary_mode)
            print(f"File successfully decompressed to {args.output_path}")
        except Exception as e:
            print(f"An error occurred during decompression: {e}")

if __name__ == "__main__":
    main()
