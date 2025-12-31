# -*- coding: utf-8 -*-

"""
A converter for transforming text from the legacy IranSystem encoding to Unicode.
This converter uses a mapping to Windows-1256 as an intermediate step.
"""

# This dictionary maps IranSystem byte codes to Windows-1256 byte codes.
# The mapping is based on the character they represent.
# IranSystem has separate codes for different forms of a letter,
# while Windows-1256 uses a single code for each letter.
IRANSYSTEM_TO_WIN1256_MAP = {
    # Persian Numbers 0-9 (mapped to ASCII digits 0-9)
    # Windows-1256 does not have dedicated Persian digits, so we map to ASCII.
    128: 0x30,  # ۰ -> 0
    129: 0x31,  # ۱ -> 1
    130: 0x32,  # ۲ -> 2
    131: 0x33,  # ۳ -> 3
    132: 0x34,  # ۴ -> 4
    133: 0x35,  # ۵ -> 5
    134: 0x36,  # ۶ -> 6
    135: 0x37,  # ۷ -> 7
    136: 0x38,  # ۸ -> 8
    137: 0x39,  # ۹ -> 9

    # Punctuation
    138: 0xA1,  # ، (Comma)
    139: 0xDC,  # ـ (Tatweel)
    140: 0xBF,  # ؟ (Question Mark)

    # Alef variants and Hamza
    141: 0xC2,  # ﺁ (Alef with Madda)
    142: 0xC6,  # ﺋ (Yeh with Hamza Above)
    143: 0xC1,  # ﺀ (Hamza)
    144: 0xC7,  # ﺍ (Alef)
    145: 0xC7,  # ﺎ (Alef)

    # Beh
    146: 0xC8,  # ﺏ
    147: 0xC8,  # ﺑ

    # Peh
    148: 0x81,  # ﭖ
    149: 0x81,  # ﭘ

    # Teh
    150: 0xCA,  # ﺕ
    151: 0xCA,  # ﺗ

    # Theh
    152: 0xCB,  # ﺙ
    153: 0xCB,  # ﺛ

    # Jeem
    154: 0xCC,  # ﺝ
    155: 0xCC,  # ﺟ

    # Cheh
    156: 0x8D,  # ﭺ
    157: 0x8D,  # ﭼ

    # Hah
    158: 0xCD,  # ﺡ
    159: 0xCD,  # ﺣ

    # Khah
    160: 0xCE,  # ﺥ
    161: 0xCE,  # ﺧ

    # Dal, Thal, Reh, Zain, Jeh
    162: 0xCF,  # ﺩ
    163: 0xD0,  # ﺫ
    164: 0xD1,  # ﺭ
    165: 0xD2,  # ﺯ
    166: 0x8E,  # ﮊ

    # Seen
    167: 0xD3,  # ﺱ
    168: 0xD3,  # ﺳ

    # Sheen
    169: 0xD4,  # ﺵ
    170: 0xD4,  # ﺷ

    # Sad
    171: 0xD5,  # ﺹ
    172: 0xD5,  # ﺻ

    # Dad
    173: 0xD6,  # ﺽ
    174: 0xD6,  # ﺿ

    # Tah, Zah
    175: 0xD8,  # ﻁ
    225: 0xD9,  # ﻅ

    # Ain
    226: 0xDA,  # ﻉ
    227: 0xDA,  # ﻊ
    228: 0xDA,  # ﻌ
    229: 0xDA,  # ﻋ

    # Ghain
    230: 0xDB,  # ﻍ
    231: 0xDB,  # ﻎ
    232: 0xDB,  # ﻐ
    233: 0xDB,  # ﻏ

    # Feh
    234: 0xDD,  # ﻑ
    235: 0xDD,  # ﻓ

    # Qaf
    236: 0xDE,  # ﻕ
    237: 0xDE,  # ﻗ

    # Kaf
    238: 0xDF,  # ﮎ
    239: 0xDF,  # ﮐ

    # Gaf
    240: 0x90,  # ﮒ
    241: 0x90,  # ﮔ

    # Lam
    242: 0xE1,  # ﻝ
    243: 0xFC,  # ﻻ (Lam with Alef)
    244: 0xE1,  # ﻟ

    # Meem
    245: 0xE3,  # ﻡ
    246: 0xE3,  # ﻣ

    # Noon
    247: 0xE4,  # ﻥ
    248: 0xE4,  # ﻧ

    # Waw
    249: 0xE6,  # ﻭ

    # Heh
    250: 0xE5,  # ﻩ
    251: 0xE5,  # ﻬ
    252: 0xE5,  # ﻫ

    # Yeh
    253: 0xED,  # ﯽ
    254: 0xED,  # ﯼ
    255: 0xED,  # ﯾ
}

# Box Drawing Characters (0xB0-0xDF -> 176-223)
# These do not have a direct equivalent in Windows-1256.
# We will map them to a space character (0x20).
IRANSYSTEM_TO_WIN1256_MAP.update({i: 0x20 for i in range(176, 224)})


def convert_iransystem_to_unicode(iransystem_bytes):
    """
    Converts a byte string from IranSystem encoding to a Unicode string.

    Args:
        iransystem_bytes: A bytes object representing text in IranSystem encoding.

    Returns:
        A string decoded as Unicode.
    """
    win1256_byte_list = []
    for byte in iransystem_bytes:
        # For bytes in the ASCII range (0-127), keep them as they are.
        if byte < 128:
            win1256_byte_list.append(byte)
        else:
            # For bytes in the extended range, look up the mapping.
            # Default to a space character (0x20) if a mapping is not found.
            win1256_byte_list.append(IRANSYSTEM_TO_WIN1256_MAP.get(byte, 0x20))

    # Convert the list of integers to a bytes object
    win1256_bytes = bytes(win1256_byte_list)

    # Decode the resulting Windows-1256 bytes to a Unicode string
    unicode_string = win1256_bytes.decode('windows-1256')

    # Replace Arabic Yeh (ي) with Persian Yeh (ی) and Arabic Kaf (ك) with Persian Kaf (ک)
    return unicode_string.replace('\u064A', '\u06CC').replace('\u0643', '\u06A9')

if __name__ == '__main__':
    # Example Usage:
    # This byte sequence in IranSystem represents "سلام دنیا" (Salam Donya)
    # س (final) -> 0xA7 -> 167
    # ل (final) -> 0xF2 -> 242
    # ا (final) -> 0x91 -> 145
    # م (final) -> 0xF5 -> 245
    #   (space) -> 0x20 -> 32
    # د (final) -> 0xA2 -> 162
    # ن (medial) -> 0xF8 -> 248
    # ی (final) -> 0xFE -> 254
    # ا (final) -> 0x91 -> 145

    # Note: IranSystem uses contextual forms. A more realistic sequence:
    # س (initial) -> 0xA8 -> 168
    # ل (medial)  -> 0xF4 -> 244
    # ا (final)   -> 0x91 -> 145
    # م (final)   -> 0xF5 -> 245
    #   (space)   -> 0x20 -> 32
    # د           -> 0xA2 -> 162
    # ن (initial) -> 0xF8 -> 248
    # ی (medial)  -> 0xFF -> 255
    # ا (final)   -> 0x91 -> 145

    # Let's try "ایران سیستم"
    # ا -> 144
    # ی -> 255
    # ر -> 164
    # ا -> 145
    # ن -> 247
    # (space)
    # س -> 168
    # ی -> 255
    # س -> 168
    # ت -> 151
    # م -> 245

    example_bytes = bytes([168, 244, 145, 245, 32, 162, 248, 255, 145]) # سلام دنیا
    unicode_text = convert_iransystem_to_unicode(example_bytes)

    print(f"Original IranSystem Bytes: {example_bytes}")
    print(f"Converted Unicode Text: {unicode_text}")

    example_iran_system = bytes([144, 255, 164, 145, 247, 32, 168, 255, 168, 151, 245])
    unicode_iran_system = convert_iransystem_to_unicode(example_iran_system)
    print(f"Original IranSystem Bytes for 'ایران سیستم': {example_iran_system}")
    print(f"Converted Unicode Text: {unicode_iran_system}")

    # Example for Kaf
    example_kaf = bytes([239, 240, 238]) # کگک
    unicode_kaf = convert_iransystem_to_unicode(example_kaf)
    print(f"Original IranSystem Bytes for 'ک': {example_kaf}")
    print(f"Converted Unicode Text: {unicode_kaf}")
