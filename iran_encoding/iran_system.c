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
    0xE4, 0xE6, 0x80, 0x8A, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x20,
    0xA1, 0xC1, 0
};

const unsigned char iransystemUpperStr[] = {
    0x8D, 0x92, 0x94, 0x96, 0x98, 0x9A, 0x9C, 0x9E, 0xA0, 0xA2, 0xA3, 0xA4, 0xA5,
    0xA6, 0xA7, 0xA9, 0xAB, 0xAD, 0xAF, 0xE0, 0xE9, 0xEB, 0xED, 0xEF, 0xF1, 0xF4,
    0xF6, 0xF8, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x20,
    0x8A, 0x8F, 0
};

const unsigned char iransystemLowerStr[] = {
    0x8D, 0x93, 0x95, 0x97, 0x99, 0x9B, 0x9D, 0x9F, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5,
    0xA6, 0xA8, 0xAA, 0xAC, 0xAE, 0xAF, 0xE0, 0xEA, 0xEC, 0xEE, 0xF0, 0xF3, 0xF5,
    0xF7, 0xF8, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x20,
    0x8A, 0x8E, 0
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
    0x0647, 0x06CC, 0x0660, 0x0661, 0x0662, 0x0663, 0x0664, 0x0665, 0x0666, 0x0667,
    0x0668, 0x0669, 0x0020, 0x060C, 0x0627, 0x0626, 0x064A, 0x0621, 0x0643, 0x02DC,
    0x00C6, 0
};

const unsigned char UTF8Str[] = {
    0xC2, 0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xCF, 0xD0, 0xD1, 0xD2,
    0x8E, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8, 0xD9, 0xDA, 0xDB, 0xDD, 0xDE, 0x98, 0x90,
    0xE1, 0xE3, 0xE4, 0xE6, 0xE5, 0xED, 0x80, 0x8A, 0x82, 0x83, 0x84, 0x85, 0x86,
    0x87, 0x88, 0x89, 0x20, 0xA1, 0xC7, 0xED, 0xED, 0xC1, 0x98, 0x98, 0xC1, 0
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

void ReverseIransystem(unsigned char *inString, unsigned char *outString) {
    unsigned int byteCount, numberCount;
    unsigned int numberPosition = 0;
    unsigned int len = strlen((char*)inString);

    for (byteCount = 0; byteCount <= len; byteCount++) {
        unsigned char current = (byteCount < len) ? inString[byteCount] : 0x20; // Space as end marker

        if (current < 80) {
            if ((byteCount - numberPosition) > 1) {
                for (numberCount = numberPosition; numberCount < byteCount; numberCount++) {
                    outString[numberCount] = inString[byteCount - (numberCount - numberPosition) - 1];
                }
            }
            numberPosition = byteCount + 1;
            if (byteCount < len) {
                outString[byteCount] = inString[byteCount];
            }
        }
    }
    outString[len] = 0;
}

void IransystemToUnicode(unsigned char *inString, unsigned char *outString) {
    unsigned int byteCount;
    unsigned int len = strlen((char*)inString);
    int posIndex;
    for (byteCount = 0; byteCount < len; byteCount++) {
        posIndex = FindPos(inString[byteCount], iransystemUpperStr);
        if (posIndex < 0) {
            posIndex = FindPos(inString[byteCount], iransystemUpperStrTail);
            outString[byteCount] = (posIndex < 0) ? inString[byteCount] : unicodeStrTail[posIndex];
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

void ReverseAlphaNumeric(unsigned char *inString, unsigned char *outString) {
    unsigned int byteCount, numberCount;
    unsigned int numberPosition = 0;
    unsigned int len = strlen((char*)inString);

    for (byteCount = 0; byteCount <= len; byteCount++) {
        unsigned char current = (byteCount < len) ? inString[byteCount] : 0xFF;

        if (current > 0x7E || current < 0x20) {
            if ((byteCount - numberPosition) > 1) {
                for (numberCount = numberPosition; numberCount < byteCount; numberCount++) {
                    outString[numberCount] = inString[byteCount - (numberCount - numberPosition) - 1];
                }
            }
            numberPosition = byteCount + 1;
        }
        if (byteCount < len) {
            outString[byteCount] = inString[byteCount];
        }
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
    unsigned int byteCount;
    unsigned int len;
    int posIndex;

    len = strlen((char*)unicodeString);

    if (reverseAlphaNumericFlag) {
        ReverseAlphaNumeric(unicodeString, iransystemString);
    } else {
        strcpy((char*)iransystemString, (char*)unicodeString);
    }

    len = strlen((char*)iransystemString);
    for (byteCount = 0; byteCount < len; byteCount++) {
        prevByte = (byteCount > 0) ? iransystemString[byteCount - 1] : 0;
        nextByte = (byteCount < (len - 1)) ? iransystemString[byteCount + 1] : 0;

        posIndex = FindPos(iransystemString[byteCount], unicodeStr);
        if (posIndex >= 0) {
            if (FindPos(nextByte, nextCharStr) >= 0) {
                iransystemString[byteCount] = iransystemLowerStr[posIndex];
            } else {
                iransystemString[byteCount] = iransystemUpperStr[posIndex];
            }
        } else {
            switch (iransystemString[byteCount]) {
                case 218: // ein
                    if (FindPos(nextByte, nextCharStr) >= 0) {
                        if (FindPos(prevByte, prevCharStr) >= 0) iransystemString[byteCount] = 227;
                        else iransystemString[byteCount] = 228;
                    } else {
                        if (FindPos(prevByte, prevCharStr) >= 0) iransystemString[byteCount] = 226;
                        else iransystemString[byteCount] = 225;
                    }
                    break;
                case 219: // ghein
                    if (FindPos(nextByte, nextCharStr) >= 0) {
                        if (FindPos(prevByte, prevCharStr) >= 0) iransystemString[byteCount] = 231;
                        else iransystemString[byteCount] = 232;
                    } else {
                        if (FindPos(prevByte, prevCharStr) >= 0) iransystemString[byteCount] = 230;
                        else iransystemString[byteCount] = 229;
                    }
                    break;
                case 229: // he
                    if (FindPos(nextByte, nextCharStr) >= 0) {
                        if (FindPos(prevByte, prevCharStr) >= 0) iransystemString[byteCount] = 250;
                        else iransystemString[byteCount] = 251;
                    } else {
                        iransystemString[byteCount] = 249;
                    }
                    break;
                case 199: // alef
                    if (FindPos(prevByte, prevCharStr) >= 0) iransystemString[byteCount] = 145;
                    else iransystemString[byteCount] = 144;
                    break;
                case 237: // ye
                    if (FindPos(nextByte, nextCharStr) >= 0) iransystemString[byteCount] = 254;
                    else {
                        if (FindPos(prevByte, prevCharStr) >= 0) iransystemString[byteCount] = 252;
                        else iransystemString[byteCount] = 253;
                    }
                    break;
            }
        }
    }
    iransystemString[len] = 0;
}
