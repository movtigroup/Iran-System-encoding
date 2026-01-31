#ifndef IRAN_SYSTEM_H
#define IRAN_SYSTEM_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Converts a UTF-8 string to Iran System visual encoding.
 * @param utf8_in Pointer to the input UTF-8 string.
 * @param out Pointer to the output buffer for Iran System bytes.
 * @param out_len Pointer to store the resulting length.
 * @param reverse Whether to apply visual RTL ordering.
 */
void unicode_to_iransystem(const char *utf8_in, unsigned char *out, int *out_len, int reverse);

/**
 * Converts Iran System visual bytes back to a UTF-8 string.
 * @param in Pointer to the input Iran System bytes.
 * @param len Length of the input bytes.
 * @param utf8_out Pointer to the output buffer for the UTF-8 string.
 */
void iransystem_to_unicode(const unsigned char *in, int len, char *utf8_out);

#ifdef __cplusplus
}
#endif

#endif
