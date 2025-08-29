from iran_encoding import IranSystemEncoder, EncodingError

# Create an encoder instance that will raise an error for unknown characters
# and will not perform visual ordering.
encoder = IranSystemEncoder(
    visual_ordering=False,
    fallback_char=None  # Set to None to raise errors
)

# This will work fine
text_supported = "تست"
encoded_logical = encoder.encode(text_supported)
print(f"'{text_supported}' encoded logically (hex): {encoded_logical.hex()}")

# This will raise an EncodingError because '€' is not in the map
text_unsupported = "این یک تست با کاراکتر نامعتبر است: €"
try:
    encoder.encode(text_unsupported)
except EncodingError as e:
    print(f"\nSuccessfully caught expected error: {e}")


# --- File I/O Example ---
print("\n--- File I/O Example ---")

# Create a sample input file
with open('input.txt', 'w', encoding='utf-8') as f:
    f.write("این یک متن نمونه برای تست فایل است.")

# Create an encoder with a fallback for this example
file_encoder = IranSystemEncoder(fallback_char='?')

# Read from the input file, encode, and write to a binary output file
try:
    with open('input.txt', 'r', encoding='utf-8') as f_in:
        text_from_file = f_in.read()
        print(f"Read from input.txt: '{text_from_file}'")

        encoded_content = file_encoder.encode(text_from_file)
        print(f"Encoded content (hex): {encoded_content.hex()}")

    with open('output.bin', 'wb') as f_out:
        f_out.write(encoded_content)
        print("Encoded content written to output.bin")

    # Verify by reading the binary file and decoding it
    with open('output.bin', 'rb') as f_in_bin:
        binary_data = f_in_bin.read()
        decoded_content = file_encoder.decode(binary_data)
        print(f"Read and decoded from output.bin: '{decoded_content}'")
        assert decoded_content == text_from_file
        print("File I/O roundtrip successful!")

except IranSystemError as e:
    print(f"An error occurred during file processing: {e}")
finally:
    # Clean up the created files
    import os
    if os.path.exists('input.txt'):
        os.remove('input.txt')
    if os.path.exists('output.bin'):
        os.remove('output.bin')
