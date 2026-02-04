#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "iran_system.h"

static const int UNICODE_STR[] = {
    0xC2, 0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xCF, 0xD0, 0xD1, 0xD2,
    0x8E, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8, 0xD9, 0xDD, 0xDE, 0x98, 0x90, 0xE1, 0xE3,
    0xE4, 0xE6, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x20,
    0xA1, 0xC1
};

static const int IRANSYSTEM_UPPER_STR[] = {
    0x8D, 0x92, 0x94, 0x96, 0x98, 0x9A, 0x9C, 0x9E, 0xA0, 0xA2, 0xA3, 0xA4, 0xA5,
    0xA6, 0xA7, 0xA9, 0xAB, 0xAD, 0xAF, 0xE0, 0xE9, 0xEB, 0xED, 0xEF, 0xF1, 0xF4,
    0xF6, 0xF8, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x20,
    0x8A, 0x8F
};

static const int IRANSYSTEM_LOWER_STR[] = {
    0x8D, 0x93, 0x95, 0x97, 0x99, 0x9B, 0x9D, 0x9F, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5,
    0xA6, 0xA8, 0xAA, 0xAC, 0xAE, 0xAF, 0xE0, 0xEA, 0xEC, 0xEE, 0xF0, 0xF3, 0xF5,
    0xF7, 0xF8, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x20,
    0x8A, 0x8E
};

static const int NEXT_CHAR_STR[] = {
    0xC2, 0xC7, 0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xCF, 0xD0, 0xD1,
    0xD2, 0x8E, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8, 0xD9, 0xDD, 0xDE, 0x98, 0x90, 0xE1,
    0xE3, 0xE4, 0xE6, 0xDA, 0xDB, 0xED, 0xE5, 0xC1
};

static const int PREV_CHAR_STR[] = {
    0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8,
    0xD9, 0xDA, 0xDB, 0xDD, 0xDE, 0x98, 0x90, 0xE1, 0xE3, 0xE4, 0xE5, 0xED, 0xC1
};

static const unsigned int WIDE_CHAR_STR[] = {
    0x0622, 0x0628, 0x067E, 0x062A, 0x062B, 0x062C, 0x0686, 0x062D, 0x062E, 0x062F,
    0x0630, 0x0631, 0x0632, 0x0698, 0x0633, 0x0634, 0x0635, 0x0636, 0x0637, 0x0638,
    0x0639, 0x063A, 0x0641, 0x0642, 0x06A9, 0x06AF, 0x0644, 0x0645, 0x0646, 0x0648,
    0x0647, 0x06CC, 0x06F0, 0x06F1, 0x06F2, 0x06F3, 0x06F4, 0x06F5, 0x06F6, 0x06F7,
    0x06F8, 0x06F9, 0x0020, 0x060C, 0x0627, 0x0626, 0x064A, 0x0621, 0x0643, 0x02DC,

    0x00C6
};

static const int UTF8_STR[] = {
    0xC2, 0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xCF, 0xD0, 0xD1, 0xD2,
    0x8E, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8, 0xD9, 0xDA, 0xDB, 0xDD, 0xDE, 0x98, 0x90,
    0xE1, 0xE3, 0xE4, 0xE6, 0xE5, 0xED, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86,
    0x87, 0x88, 0x89, 0x20, 0xA1, 0xC7, 0xED, 0xED, 0xC1, 0x98, 0x98, 0xC1
};

static int find_pos(int b, const int *area, int size) {
    for (int i = 0; i < size; i++) if (area[i] == b) return i;
    return -1;
}

static unsigned int utf8_to_unicode(const char **ptr) {
    unsigned char c = **ptr;
    if (c < 128) { (*ptr)++; return c; }
    if ((c & 0xE0) == 0xC0) { unsigned int res = ((c & 0x1F) << 6) | ((*ptr)[1] & 0x3F); (*ptr) += 2; return res; }
    if ((c & 0xF0) == 0xE0) { unsigned int res = ((c & 0x0F) << 12) | (((*ptr)[1] & 0x3F) << 6) | ((*ptr)[2] & 0x3F); (*ptr) += 3; return res; }
    (*ptr)++; return '?';
}

void unicode_to_iransystem(const char *utf8_in, unsigned char *out, int *out_len, int reverse) {
    int len = 0; const char *p = utf8_in; unsigned int script[1024];
    while (*p && len < 1024) {
        unsigned int u = utf8_to_unicode(&p);
        if (u >= 0x06F0 && u <= 0x06F9) script[len++] = 0xB0 + (u - 0x06F0);
        else { int found = 0; for (int i = 0; i < 51; i++) if (WIDE_CHAR_STR[i] == u) { script[len++] = (unsigned int)UTF8_STR[i]; found = 1; break; } if (!found) script[len++] = (u < 256) ? (unsigned int)u : '?'; }
    }
    for (int i = 0; i < len; i++) {
        int prev = (i > 0) ? (int)script[i-1] : 0; int next = (i < len - 1) ? (int)script[i+1] : 0; int cur = (int)script[i];
        if (cur >= 0xB0 && cur <= 0xB9) out[i] = 0x80 + (cur - 0xB0);
        else {
            int pos = find_pos(cur, UNICODE_STR, 41);
            if (pos >= 0) out[i] = (find_pos(next, NEXT_CHAR_STR, 34) >= 0) ? IRANSYSTEM_LOWER_STR[pos] : IRANSYSTEM_UPPER_STR[pos];
            else {
                if (cur == 218) { if (find_pos(next, NEXT_CHAR_STR, 34) >= 0) out[i] = (find_pos(prev, PREV_CHAR_STR, 26) >= 0) ? 227 : 228; else out[i] = (find_pos(prev, PREV_CHAR_STR, 26) >= 0) ? 226 : 225; }
                else if (cur == 219) { if (find_pos(next, NEXT_CHAR_STR, 34) >= 0) out[i] = (find_pos(prev, PREV_CHAR_STR, 26) >= 0) ? 231 : 232; else out[i] = (find_pos(prev, PREV_CHAR_STR, 26) >= 0) ? 230 : 229; }
                else if (cur == 229) { if (find_pos(next, NEXT_CHAR_STR, 34) >= 0) out[i] = (find_pos(prev, PREV_CHAR_STR, 26) >= 0) ? 250 : 251; else out[i] = 249; }
                else if (cur == 199) out[i] = (find_pos(prev, PREV_CHAR_STR, 26) >= 0) ? 145 : 144;
                else if (cur == 237) { if (find_pos(next, NEXT_CHAR_STR, 34) >= 0) out[i] = 254; else out[i] = (find_pos(prev, PREV_CHAR_STR, 26) >= 0) ? 252 : 253; }
                else out[i] = (unsigned char)cur;
            }
        }
    }
    if (reverse) {
        for (int i = 0; i < len / 2; i++) { unsigned char tmp = out[i]; out[i] = out[len - 1 - i]; out[len - 1 - i] = tmp; }
        int start = -1;
        for (int i = 0; i <= len; i++) {
            unsigned char c = (i < len) ? out[i] : 0;
            if (c >= 0x21 && c <= 0x7E) { if (start == -1) start = i; }
            else { if (start != -1) { for (int j = 0; j < (i - start) / 2; j++) { unsigned char tmp = out[start + j]; out[start + j] = out[i - 1 - j]; out[i - 1 - j] = tmp; } start = -1; } }
    outString[len] = 0;
}

void ReverseAlphaNumeric(unsigned char *inString, unsigned char *outString) {
    unsigned int byteCount, numberCount;
    unsigned int numberPosition = 0;
    unsigned int len = strlen((char*)inString);

    for (byteCount = 0; byteCount <= len; byteCount++) {
        unsigned char current = (byteCount < len) ? inString[byteCount] : 0xFF;

        // Trigger reversal on Persian letters or special markers
        int is_trigger = (current > 0x8C && current != 0xFF) || current < 0x20 || current == 0x8E || current == 0x8F;
        if (is_trigger || byteCount == len) {
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

void IransystemToUnicode(unsigned char *inString, unsigned char *outString) {
    unsigned int byteCount;
    unsigned int len = strlen((char*)inString);
    int posIndex;
    unsigned char reversed[2048];
    unsigned char logical[2048];

    if (len >= 2048) len = 2047;

    // Step 1: Reverse whole string to handle visual RTL input
    for (byteCount = 0; byteCount < len; byteCount++) {
        reversed[byteCount] = inString[len - 1 - byteCount];
    }
    reversed[len] = 0;

    // Step 2: Fix chunks of English/numbers
    ReverseAlphaNumeric(reversed, logical);

    // Step 3: Convert to Unicode
    for (byteCount = 0; byteCount < len; byteCount++) {
        posIndex = FindPos(logical[byteCount], iransystemUpperStr);
        if (posIndex < 0) {
            posIndex = FindPos(logical[byteCount], iransystemUpperStrTail);
            outString[byteCount] = (posIndex < 0) ? logical[byteCount] : unicodeStrTail[posIndex];
        } else {
            outString[byteCount] = unicodeStr[posIndex];
        }
    }
    for (int i = 0; i < len; i++) if (out[i] >= '0' && out[i] <= '9') out[i] = 0x80 + (out[i] - '0');
    *out_len = len;
}

void iransystem_to_unicode(const unsigned char *in, int len, char *utf8_out) {
    unsigned char rev[1024]; for (int i = 0; i < len; i++) rev[i] = in[len - 1 - i];
    int start = -1;
    for (int i = 0; i <= len; i++) {
        unsigned char c = (i < len) ? rev[i] : 0;
        if ((c >= 0x21 && c <= 0x7E) || (c >= 0x80 && c <= 0x89)) { if (start == -1) start = i; }
        else { if (start != -1) { for (int j = 0; j < (i - start) / 2; j++) { unsigned char tmp = rev[start + j]; rev[start + j] = rev[i - 1 - j]; rev[i - 1 - j] = tmp; } start = -1; } }
    }
    char *out_p = utf8_out;
    for (int i = 0; i < len; i++) {
        unsigned char b = rev[i];
        if (b >= 0x80 && b <= 0x89) { unsigned int u = 0x06F0 + (b - 0x80); *out_p++ = (char)(0xE0 | (u >> 12)); *out_p++ = (char)(0x80 | ((u >> 6) & 0x3F)); *out_p++ = (char)(0x80 | (u & 0x3F)); continue; }
        int pos = find_pos(b, IRANSYSTEM_LOWER_STR, 41); if (pos < 0) pos = find_pos(b, IRANSYSTEM_UPPER_STR, 41);
        int script_b = (pos >= 0) ? UNICODE_STR[pos] : b;
        if (b >= 0xF9 && b <= 0xFB) script_b = 229; else if (b == 0xFD || b == 0xFC || b == 0xFE) script_b = 237; else if (b == 0x90 || b == 0x91) script_b = 199;
        unsigned int u = '?'; for (int j = 0; j < 51; j++) if (UTF8_STR[j] == script_b) { u = WIDE_CHAR_STR[j]; break; }
        if (u == '?') u = (script_b < 256) ? script_b : '?';
        if (u < 128) *out_p++ = (char)u; else if (u < 2048) { *out_p++ = (char)(0xC0 | (u >> 6)); *out_p++ = (char)(0x80 | (u & 0x3F)); } else { *out_p++ = (char)(0xE0 | (u >> 12)); *out_p++ = (char)(0x80 | ((u >> 6) & 0x3F)); *out_p++ = (char)(0x80 | (u & 0x3F)); }
    }
    *out_p = '\0';
}
