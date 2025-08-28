import unittest
import json
from iran_encoding import encode, decode

class TestCorpus(unittest.TestCase):

    def test_hamshahri_corpus(self):
        """
        Tests the encoding and decoding of sentences from the Hamshahri corpus.
        """
        with open("tests/corpus.json", "r", encoding="utf-8") as f:
            corpus = json.load(f)

        for article in corpus:
            for field in ["title", "summary"]:
                text = article.get(field)
                if text:
                    with self.subTest(text=text):
                        import unicodedata
                        encoded = encode(text)
                        decoded = decode(encoded)

                        # Normalize both strings to handle character variations
                        # and remove ZWNJ for a valid comparison.
                        normalized_original = unicodedata.normalize('NFKC', text).replace('\u200c', '')
                        normalized_decoded = unicodedata.normalize('NFKC', decoded).replace('\u200c', '')

                        self.assertEqual(normalized_original, normalized_decoded)

if __name__ == "__main__":
    unittest.main()
