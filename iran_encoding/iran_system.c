#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include "iran_system.h"

/**
 * Iran System Encoding implementation.
 * Ported and cleaned up for professional use.
 */

/* Character mapping tables */
const unsigned char unicodeNumberStr[]    = {0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0};
const unsigned char iransystemNumberStr[] = {0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0};

const unsigned char unicodeStr[] = {
    0xC2, 0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xCF, 0xD0, 0xD1, 0xD2,
    0x8E, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8, 0xD9, 0xDD, 0xDE, 0x98, 0x90, 0xE1, 0xE3,
    0xE4, 0xE6,
    0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, // Digits script codes
    0x20, 0xA1, 0xC1, 0
};

const unsigned char iransystemUpperStr[] = {
    0x8D, 0x92, 0x94, 0x96, 0x98, 0x9A, 0x9C, 0x9E, 0xA0, 0xA2, 0xA3, 0xA4, 0xA5,
    0xA6, 0xA7, 0xA9, 0xAB, 0xAD, 0xAF, 0xE0, 0xE9, 0xEB, 0xED, 0xEF, 0xF1, 0xF4,
    0xF6, 0xF8,
    0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89,
    0x20, 0x8A, 0x8F, 0
};

const unsigned char iransystemLowerStr[] = {
    0x8D, 0x93, 0x95, 0x97, 0x99, 0x9B, 0x9D, 0x9F, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5,
    0xA6, 0xA8, 0xAA, 0xAC, 0xAE, 0xAF, 0xE0, 0xEA, 0xEC, 0xEE, 0xF0, 0xF3, 0xF5,
    0xF7, 0xF8,
    0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89,
    0x20, 0x8A, 0x8E, 0
};

const unsigned char nextCharStr[] = {
    0xC2, 0xC7, 0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xCF, 0xD0, 0xD1,
    0xD2, 0x8E, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8, 0xD9, 0xDD, 0xDE, 0x98, 0x90, 0xE1,
    0xE3, 0xE4, 0xE6, 0xDA, 0xDB, 0xED, 0xE5, 0xC1, 0
};

const unsigned char prevCharStr[] = {
    0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8,
    0xD9, 0xDA, 0xDB, 0xDD, 0xDE, 0x98, 0x90, 0xE1, 0xE3, 0xE4, 0xE5, 0xED, 0xC1, 0
};

const unsigned char unicodeStrTail[]        = {0xDA, 0xDB, 0xE5, 0xC7, 0xED, 0};
const unsigned char iransystemUpperStrTail[] = {0xE1, 0xE5, 0xF9, 0x90, 0xFD, 0};
const unsigned char iransystemLowerStrTail[] = {
    /*ein*/ 0xE2, 0xE3, 0xE4,
    /*ghein*/ 0xE6, 0xE7, 0xE8,
    /*he*/ 0xFA, 0xFB, 0xFB,
    /*alef*/ 0x91, 0x91, 0x91,
    /*ye*/ 0xFC, 0xFE, 0xFE, 0
};

const unsigned int wideCharStr[] = {
    0x0622, 0x0628, 0x067E, 0x062A, 0x062B, 0x062C, 0x0686, 0x062D, 0x062E, 0x062F,
    0x0630, 0x0631, 0x0632, 0x0698, 0x0633, 0x0634, 0x0635, 0x0636, 0x0637, 0x0638,
    0x0639, 0x063A, 0x0641, 0x0642, 0x06A9, 0x06AF, 0x0644, 0x0645, 0x0646, 0x0648,
    0x0647, 0x06CC, 0x06F0, 0x06F1, 0x06F2, 0x06F3, 0x06F4, 0x06F5, 0x06F6, 0x06F7,
    0x06F8, 0x06F9, 0x0020, 0x060C, 0x0627, 0x0626, 0x064A, 0x0621, 0x0643, 0x02DC,
    0x00C6, 0
};

const unsigned char UTF8Str[] = {
    0xC2, 0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xCF, 0xD0, 0xD1, 0xD2,
    0x8E, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8, 0xD9, 0xDA, 0xDB, 0xDD, 0xDE, 0x98, 0x90,
    0xE1, 0xE3, 0xE4, 0xE6, 0xE5, 0xED,
    0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39,
    0x20, 0xA1, 0xC7, 0xED, 0xED, 0xC1, 0x98, 0x98, 0xC1, 0
};

unsigned char reverseAlphaNumericFlag = 1;

/* Helper functions */
int FindPos(unsigned char inByte, const unsigned char *areaString) {
    unsigned int byteCount;
    for (byteCount = 0; areaString[byteCount] != 0; byteCount++) {
        if (areaString[byteCount] == inByte) return byteCount;
    }
    return -1;
}

int FindPos16(unsigned int inByte, const unsigned int *areaString) {
    unsigned int wideLen = 0;
    while (areaString[wideLen]) {
        if (areaString[wideLen] == inByte) return wideLen;
        wideLen++;
    }
    return -1;
}

void IransystemToUpper(unsigned char *inString, unsigned char *outString) {
    unsigned int byteCount;
    unsigned int len = strlen((char*)inString);
    int posIndex;
    for (byteCount = 0; byteCount < len; byteCount++) {
        posIndex = FindPos(inString[byteCount], iransystemLowerStr);
        if (posIndex < 0) {
            posIndex = FindPos(inString[byteCount], iransystemLowerStrTail);
            outString[byteCount] = (posIndex < 0) ? inString[byteCount] : iransystemUpperStrTail[posIndex / 3];
        } else {
            outString[byteCount] = iransystemUpperStr[posIndex];
        }
    }
    outString[len] = 0;
}

void ReverseVisualRTL(unsigned char *inString, unsigned char *outString) {
    unsigned int i, j;
    int start = -1;
    unsigned int len = strlen((char*)inString);
    unsigned char reversed[2048];

    if (len >= 2048) len = 2047;

    // Step 1: Global Reverse
    for (i = 0; i < len; i++) {
        reversed[i] = inString[len - 1 - i];
    }
    reversed[len] = 0;

    strcpy((char*)outString, (char*)reversed);

    // Step 2: Un-reverse LTR chunks (ASCII > 0x20 or Persian digits 0x80-0x89)
    for (i = 0; i <= len; i++) {
        unsigned char current = (i < len) ? reversed[i] : 0x00;
        int is_ltr = (current != 0x00) && ((current > 0x20 && current < 0x80) || (current >= 0x80 && current <= 0x89));

        if (is_ltr) {
            if (start == -1) start = i;
        } else {
            if (start != -1) {
                int chunkLen = i - start;
                for (j = 0; j < (unsigned int)chunkLen; j++) {
                    outString[start + j] = reversed[i - 1 - j];
                }
                start = -1;
            }
        }
    }
    outString[len] = 0;
}

void IransystemToUnicode(unsigned char *inString, unsigned char *outString) {
    unsigned int byteCount;
    unsigned int len = strlen((char*)inString);
    int posIndex;
    unsigned char logical[2048];

    if (len >= 2048) len = 2047;

    // Step 1: Reverse Global RTL back to logical order
    ReverseVisualRTL(inString, logical);

    // Step 2: Convert to Unicode
    for (byteCount = 0; byteCount < len; byteCount++) {
        posIndex = FindPos(logical[byteCount], iransystemUpperStr);
        if (posIndex < 0) {
            posIndex = FindPos(logical[byteCount], iransystemUpperStrTail);
            outString[byteCount] = (posIndex < 0) ? logical[byteCount] : unicodeStrTail[posIndex];
        } else {
            outString[byteCount] = unicodeStr[posIndex];
        }
    }
    outString[len] = 0;
}

void Reverse(unsigned char *inString, unsigned char *outString) {
    unsigned int byteCount;
    unsigned int len = strlen((char*)inString);
    if (!len) {
        outString[0] = 0;
        return;
    }
    for (byteCount = 0; byteCount < len; byteCount++) {
        outString[len - byteCount - 1] = inString[byteCount];
    }
    outString[len] = 0;
}

void UnicodeNumberToIransystem(unsigned char *unicodeString, unsigned char *iransystemString) {
    unsigned int byteCount;
    unsigned int len = strlen((char*)unicodeString);
    int posIndex;
    if (!len) {
        iransystemString[0] = 0;
        return;
    }
    for (byteCount = 0; byteCount < len; byteCount++) {
        iransystemString[byteCount] = unicodeString[byteCount];
        posIndex = FindPos(iransystemString[byteCount], unicodeNumberStr);
        if (posIndex >= 0) {
            iransystemString[byteCount] = iransystemNumberStr[posIndex];
        }
    }
    iransystemString[len] = 0;
}

unsigned char UnicodeToPersianScript(unsigned int unicodeChar) {
    int posIndex = FindPos16(unicodeChar, wideCharStr);
    if (posIndex >= 0) {
        return UTF8Str[posIndex];
    } else {
        return (unsigned char)(unicodeChar < 256 ? unicodeChar : '?');
    }
}

void UnicodeToIransystem(unsigned char *unicodeString, unsigned char *iransystemString) {
    unsigned char prevByte, nextByte;
    unsigned int i;
    unsigned int len;
    int posIndex;
    unsigned char intermediate[2048];

    len = strlen((char*)unicodeString);
    if (len >= 2048) len = 2047;

    // Step 1: Reshape in logical order
    for (i = 0; i < len; i++) {
        prevByte = (i > 0) ? unicodeString[i - 1] : 0;
        nextByte = (i < (len - 1)) ? unicodeString[i + 1] : 0;

        posIndex = FindPos(unicodeString[i], unicodeStr);

        // Collision Check: Only treat as letter if not a digit code (0x30-0x39)
        if (posIndex >= 0 && !(unicodeString[i] >= 0x30 && unicodeString[i] <= 0x39)) {
            if (FindPos(nextByte, nextCharStr) >= 0) {
                intermediate[i] = iransystemLowerStr[posIndex];
            } else {
                intermediate[i] = iransystemUpperStr[posIndex];
            }
        } else {
            intermediate[i] = unicodeString[i];
            switch (unicodeString[i]) {
                case 218: // ein
                    if (FindPos(nextByte, nextCharStr) >= 0) {
                        if (FindPos(prevByte, prevCharStr) >= 0) intermediate[i] = 227;
                        else intermediate[i] = 228;
                    } else {
                        if (FindPos(prevByte, prevCharStr) >= 0) intermediate[i] = 226;
                        else intermediate[i] = 225;
                    }
                    break;
                case 219: // ghein
                    if (FindPos(nextByte, nextCharStr) >= 0) {
                        if (FindPos(prevByte, prevCharStr) >= 0) intermediate[i] = 231;
                        else intermediate[i] = 232;
                    } else {
                        if (FindPos(prevByte, prevCharStr) >= 0) intermediate[i] = 230;
                        else intermediate[i] = 229;
                    }
                    break;
                case 229: // he
                    if (FindPos(nextByte, nextCharStr) >= 0) {
                        if (FindPos(prevByte, prevCharStr) >= 0) intermediate[i] = 250;
                        else intermediate[i] = 251;
                    } else {
                        intermediate[i] = 249;
                    }
                    break;
                case 199: // alef
                    if (FindPos(prevByte, prevCharStr) >= 0) intermediate[i] = 145;
                    else intermediate[i] = 144;
                    break;
                case 237: // ye
                    if (FindPos(nextByte, nextCharStr) >= 0) intermediate[i] = 254;
                    else {
                        if (FindPos(prevByte, prevCharStr) >= 0) intermediate[i] = 252;
                        else intermediate[i] = 253;
                    }
                    break;
                default:
                    // Handle numbers: convert ASCII digits to Iran System digits
                    if (unicodeString[i] >= '0' && unicodeString[i] <= '9') {
                        posIndex = FindPos(unicodeString[i], unicodeNumberStr);
                        if (posIndex >= 0) intermediate[i] = iransystemNumberStr[posIndex];
                    }
                    break;
            }
        }
    }
    intermediate[len] = 0;

    // Step 2: Perform Global RTL reversal if requested
    if (reverseAlphaNumericFlag) {
        ReverseVisualRTL(intermediate, iransystemString);
    } else {
        strcpy((char*)iransystemString, (char*)intermediate);
    }
}
