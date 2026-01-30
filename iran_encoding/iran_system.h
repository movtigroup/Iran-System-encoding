#ifndef IRAN_SYSTEM_H
#define IRAN_SYSTEM_H

// Function declarations matching the C implementation
void UnicodeToIransystem(unsigned char *unicodeString, unsigned char *iransystemString);
void UnicodeNumberToIransystem(unsigned char *unicodeString, unsigned char *iransystemString);
void IransystemToUnicode(unsigned char *inString, unsigned char *outString);
void IransystemToUpper(unsigned char *inString, unsigned char *outString);
void Reverse(unsigned char *inString, unsigned char *outString);
void ReverseAlphaNumeric(unsigned char *inString, unsigned char *outString);
void ReverseIransystem(unsigned char *inString, unsigned char *outString);
unsigned char UnicodeToPersianScript(unsigned int unicodeChar);

#endif
