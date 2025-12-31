# -*- coding: utf-8 -*-

"""
A converter for transforming text from the legacy IranSystem encoding to Unicode.
This final version uses a rule-based engine to correctly handle the
visual-to-logical conversion, including ZWNJ logic and full character mapping.
"""

# --- Step 1: Data Structures ---

# Visual form constants from IranSystem
FORM_ISOLATED = "isolated"
FORM_INITIAL = "initial"
FORM_MEDIAL = "medial"
FORM_FINAL = "final"
FORM_NEUTRAL = "neutral"

# Unicode joining property constants
JOIN_DUAL = "dual"   # Joins on both sides
JOIN_RIGHT = "right" # Joins only to the previous character
JOIN_NONE = "none"   # Does not join

ZWNJ = '\u200C'

# Dictionary mapping IranSystem bytes to (Unicode Character, Visual Form)
# Based on the table by Roozbeh Pournader (v1.0, 21 Jan 2000)
IRANSYSTEM_MAP = {
    # ASCII and control characters (0x00-0x7F) are neutral
    **{i: (chr(i), FORM_NEUTRAL) for i in range(128)},

    # Persian Numbers and punctuation (0x80-0x8F, 0xFF) are neutral
    0x80: ('\u06F0', FORM_NEUTRAL), 0x81: ('\u06F1', FORM_NEUTRAL), 0x82: ('\u06F2', FORM_NEUTRAL),
    0x83: ('\u06F3', FORM_NEUTRAL), 0x84: ('\u06F4', FORM_NEUTRAL), 0x85: ('\u06F5', FORM_NEUTRAL),
    0x86: ('\u06F6', FORM_NEUTRAL), 0x87: ('\u06F7', FORM_NEUTRAL), 0x88: ('\u06F8', FORM_NEUTRAL),
    0x89: ('\u06F9', FORM_NEUTRAL), 0x8A: ('\u060C', FORM_NEUTRAL), 0x8B: ('\u0640', FORM_INITIAL),
    0x8C: ('\u061F', FORM_NEUTRAL), 0x8F: ('\u0621', FORM_NEUTRAL), 0xFF: ('\u00A0', FORM_NEUTRAL),

    # Letters with their visual forms explicitly defined (0x8D-0xA6, 0xA7-0xAF, 0xE0-0xFE)
    0x8D: ('\u0622', FORM_ISOLATED), 0x90: ('\u0627', FORM_ISOLATED), 0x91: ('\u0627', FORM_FINAL),
    0x8E: ('\u0626', FORM_INITIAL),
    0x92: ('\u0628', FORM_FINAL),   0x93: ('\u0628', FORM_INITIAL),
    0x94: ('\u067E', FORM_FINAL),   0x95: ('\u067E', FORM_INITIAL),
    0x96: ('\u062A', FORM_FINAL),   0x97: ('\u062A', FORM_INITIAL),
    0x98: ('\u062B', FORM_FINAL),   0x99: ('\u062B', FORM_INITIAL),
    0x9A: ('\u062C', FORM_FINAL),   0x9B: ('\u062C', FORM_INITIAL),
    0x9C: ('\u0686', FORM_FINAL),   0x9D: ('\u0686', FORM_INITIAL),
    0x9E: ('\u062D', FORM_FINAL),   0x9F: ('\u062D', FORM_INITIAL),
    0xA0: ('\u062E', FORM_FINAL),   0xA1: ('\u062E', FORM_INITIAL),
    0xA2: ('\u062F', FORM_ISOLATED), 0xA3: ('\u0630', FORM_ISOLATED), 0xA4: ('\u0631', FORM_ISOLATED),
    0xA5: ('\u0632', FORM_ISOLATED), 0xA6: ('\u0698', FORM_ISOLATED),
    0xA7: ('\u0633', FORM_FINAL),   0xA8: ('\u0633', FORM_INITIAL),
    0xA9: ('\u0634', FORM_FINAL),   0xAA: ('\u0634', FORM_INITIAL),
    0xAB: ('\u0635', FORM_FINAL),   0xAC: ('\u0635', FORM_INITIAL),
    0xAD: ('\u0636', FORM_FINAL),   0xAE: ('\u0636', FORM_INITIAL),
    0xAF: ('\u0637', FORM_ISOLATED), 0xE0: ('\u0638', FORM_ISOLATED),
    0xE1: ('\u0639', FORM_ISOLATED),0xE2: ('\u0639', FORM_FINAL),  0xE3: ('\u0639', FORM_MEDIAL),  0xE4: ('\u0639', FORM_INITIAL),
    0xE5: ('\u063A', FORM_ISOLATED),0xE6: ('\u063A', FORM_FINAL),  0xE7: ('\u063A', FORM_MEDIAL),  0xE8: ('\u063A', FORM_INITIAL),
    0xE9: ('\u0641', FORM_FINAL),   0xEA: ('\u0641', FORM_INITIAL),
    0xEB: ('\u0642', FORM_FINAL),   0xEC: ('\u0642', FORM_INITIAL),
    0xED: ('\u06A9', FORM_FINAL),   0xEE: ('\u06A9', FORM_INITIAL),
    0xEF: ('\u06AF', FORM_FINAL),   0xF0: ('\u06AF', FORM_INITIAL),
    0xF1: ('\u0644', FORM_FINAL),   0xF3: ('\u0644', FORM_INITIAL), 0xF2: ('\u0644\u0627', FORM_FINAL),
    0xF4: ('\u0645', FORM_FINAL),   0xF5: ('\u0645', FORM_INITIAL),
    0xF6: ('\u0646', FORM_FINAL),   0xF7: ('\u0646', FORM_INITIAL),
    0xF8: ('\u0648', FORM_ISOLATED),
    0xF9: ('\u0647', FORM_FINAL),   0xFA: ('\u0647', FORM_MEDIAL),  0xFB: ('\u0647', FORM_INITIAL),
    0xFC: ('\u06CC', FORM_FINAL),   0xFD: ('\u06CC', FORM_ISOLATED),0xFE: ('\u06CC', FORM_INITIAL),

    # Box drawing and block characters (0xB0-0xDF) are neutral
    0xB0: ('\u2591', FORM_NEUTRAL), 0xB1: ('\u2592', FORM_NEUTRAL), 0xB2: ('\u2593', FORM_NEUTRAL),
    0xB3: ('\u2502', FORM_NEUTRAL), 0xB4: ('\u2524', FORM_NEUTRAL), 0xB5: ('\u2561', FORM_NEUTRAL),
    0xB6: ('\u2562', FORM_NEUTRAL), 0xB7: ('\u2556', FORM_NEUTRAL), 0xB8: ('\u2555', FORM_NEUTRAL),
    0xB9: ('\u2563', FORM_NEUTRAL), 0xBA: ('\u2551', FORM_NEUTRAL), 0xBB: ('\u2557', FORM_NEUTRAL),
    0xBC: ('\u255D', FORM_NEUTRAL), 0xBD: ('\u255C', FORM_NEUTRAL), 0xBE: ('\u255B', FORM_NEUTRAL),
    0xBF: ('\u2510', FORM_NEUTRAL), 0xC0: ('\u2514', FORM_NEUTRAL), 0xC1: ('\u2534', FORM_NEUTRAL),
    0xC2: ('\u252C', FORM_NEUTRAL), 0xC3: ('\u251C', FORM_NEUTRAL), 0xC4: ('\u2500', FORM_NEUTRAL),
    0xC5: ('\u253C', FORM_NEUTRAL), 0xC6: ('\u255E', FORM_NEUTRAL), 0xC7: ('\u255F', FORM_NEUTRAL),
    0xC8: ('\u255A', FORM_NEUTRAL), 0xC9: ('\u2554', FORM_NEUTRAL), 0xCA: ('\u2569', FORM_NEUTRAL),
    0xCB: ('\u2566', FORM_NEUTRAL), 0xCC: ('\u2560', FORM_NEUTRAL), 0xCD: ('\u2550', FORM_NEUTRAL),
    0xCE: ('\u256C', FORM_NEUTRAL), 0xCF: ('\u2567', FORM_NEUTRAL), 0xD0: ('\u2568', FORM_NEUTRAL),
    0xD1: ('\u2564', FORM_NEUTRAL), 0xD2: ('\u2565', FORM_NEUTRAL), 0xD3: ('\u2559', FORM_NEUTRAL),
    0xD4: ('\u2558', FORM_NEUTRAL), 0xD5: ('\u2552', FORM_NEUTRAL), 0xD6: ('\u2553', FORM_NEUTRAL),
    0xD7: ('\u256B', FORM_NEUTRAL), 0xD8: ('\u256A', FORM_NEUTRAL), 0xD9: ('\u2518', FORM_NEUTRAL),
    0xDA: ('\u250C', FORM_NEUTRAL), 0xDB: ('\u2588', FORM_NEUTRAL), 0xDC: ('\u2584', FORM_NEUTRAL),
    0xDD: ('\u258C', FORM_NEUTRAL), 0xDE: ('\u2590', FORM_NEUTRAL), 0xDF: ('\u2580', FORM_NEUTRAL),
}

# Dictionary of Unicode joining properties for relevant characters
UNICODE_JOIN_PROPS = {
    'ب': JOIN_DUAL, 'پ': JOIN_DUAL, 'ت': JOIN_DUAL, 'ث': JOIN_DUAL, 'ج': JOIN_DUAL,
    'چ': JOIN_DUAL, 'ح': JOIN_DUAL, 'خ': JOIN_DUAL, 'س': JOIN_DUAL, 'ش': JOIN_DUAL,
    'ص': JOIN_DUAL, 'ض': JOIN_DUAL, 'ع': JOIN_DUAL, 'غ': JOIN_DUAL, 'ف': JOIN_DUAL,
    'ق': JOIN_DUAL, 'ک': JOIN_DUAL, 'گ': JOIN_DUAL, 'ل': JOIN_DUAL, 'م': JOIN_DUAL,
    'ن': JOIN_DUAL, 'ه': JOIN_DUAL, 'ی': JOIN_DUAL, 'ئ': JOIN_DUAL,
    'ا': JOIN_RIGHT, 'آ': JOIN_RIGHT, 'د': JOIN_RIGHT, 'ذ': JOIN_RIGHT, 'ر': JOIN_RIGHT,
    'ز': JOIN_RIGHT, 'ژ': JOIN_RIGHT, 'و': JOIN_RIGHT, 'لا': JOIN_RIGHT, 'ط': JOIN_RIGHT,
    'ظ': JOIN_RIGHT,
}

# --- Step 2: Rule-Based Conversion Function ---

def convert_iransystem_to_unicode(iransystem_bytes):
    if not iransystem_bytes:
        return ""

    result = []
    i = 0
    while i < len(iransystem_bytes):
        char, form = IRANSYSTEM_MAP.get(iransystem_bytes[i], ('?', FORM_NEUTRAL))
        result.append(char)

        if i + 1 < len(iransystem_bytes):
            current_join_prop = UNICODE_JOIN_PROPS.get(char, JOIN_NONE)

            next_char, next_form = IRANSYSTEM_MAP.get(iransystem_bytes[i+1], ('?', FORM_NEUTRAL))
            next_join_prop = UNICODE_JOIN_PROPS.get(next_char, JOIN_NONE)

            # THE FINAL RULE:
            # Insert a ZWNJ if the current character was explicitly non-joining
            # in IranSystem (final/isolated form), but its Unicode nature
            # is to join, and the next character's Unicode nature is to join back.
            if (form == FORM_FINAL or form == FORM_ISOLATED) and \
               (current_join_prop == JOIN_DUAL) and \
               (next_join_prop == JOIN_DUAL):
                 result.append(ZWNJ)
        i += 1

    return "".join(result)

# --- Step 3: Final Tests ---

if __name__ == '__main__':
    test_cases = [
        {"name": "Basic word 'سلام'", "bytes": bytes([0xA8, 0xF3, 0x91, 0xF4]), "expected": "سلام"},
        {"name": "Word with right-joining 'برنامه'", "bytes": bytes([0x93,0xA4,0xF7,0x91,0xF5,0xF9]), "expected": "برنامه"},
        {"name": "Key ZWNJ case 'خانه‌ها'", "bytes": bytes([0xA1, 0x91, 0xF7, 0xF9, 0xFB, 0x91]), "expected": "خانه‌ها"},
        {"name": "Ezafe construct 'خانه‌ی'", "bytes": bytes([0xA1, 0x91, 0xF7, 0xF9, 0xFE]), "expected": "خانه‌ی"},
        {"name": "Numbers do not join '۱۲۳'", "bytes": bytes([0x81,0x82,0x83]), "expected": "۱۲۳"},
        {"name": "Ligature 'طلا'", "bytes": bytes([0xAF, 0xF2]), "expected": "طلا"},
        {"name": "Box drawing '┌─┐'", "bytes": bytes([0xDA, 0xC4, 0xBF]), "expected": "┌─┐"},
    ]

    for test in test_cases:
        print(f"--- Test Case: {test['name']} ---")
        converted_text = convert_iransystem_to_unicode(test['bytes'])
        print(f"Bytes:     {test['bytes'].hex(' ').upper()}")
        print(f"Converted: '{converted_text}'")
        print(f"Expected:  '{test['expected']}'")
        try:
            assert converted_text == test['expected']
            print("Result:    PASSED!")
        except AssertionError:
            print(f"Result:    FAILED!")
        print("-" * 20)
