import unittest

from osc.core import makeurl
from osc.core import UrlQueryArray
from osc.core import parseRevisionOption
from osc.oscerr import OscInvalidRevision


class TestParseRevisionOption(unittest.TestCase):
    def test_empty(self):
        expected = None, None
        actual = parseRevisionOption("")
        self.assertEqual(expected, actual)

    def test_colon(self):
        expected = None, None
        actual = parseRevisionOption(":")
        # your revision ':' will be ignored
        self.assertEqual(expected, actual)

    def test_invalid_multiple_colons(self):
        self.assertRaises(OscInvalidRevision, parseRevisionOption, ":::::")

    def test_one_number(self):
        expected = ("1", None)
        actual = parseRevisionOption("1")
        self.assertEqual(expected, actual)

    def test_two_numbers(self):
        expected = ("1", "2")
        actual = parseRevisionOption("1:2")
        self.assertEqual(expected, actual)

    def test_invalid_multiple_numbers(self):
        self.assertRaises(OscInvalidRevision, parseRevisionOption, "1:2:3:4:5")

    def test_one_hash(self):
        expected = "c4ca4238a0b923820dcc509a6f75849b", None
        actual = parseRevisionOption("c4ca4238a0b923820dcc509a6f75849b")
        self.assertEqual(expected, actual)

    def test_two_hashes(self):
        expected = ("d41d8cd98f00b204e9800998ecf8427e", "c4ca4238a0b923820dcc509a6f75849b")
        actual = parseRevisionOption("d41d8cd98f00b204e9800998ecf8427e:c4ca4238a0b923820dcc509a6f75849b")
        self.assertEqual(expected, actual)

    def test_invalid_multiple_hashes(self):
        rev = "d41d8cd98f00b204e9800998ecf8427e:c4ca4238a0b923820dcc509a6f75849b:c81e728d9d4c2f636f067f89cc14862c"
        self.assertRaises(OscInvalidRevision, parseRevisionOption, rev)


class TestMakeurl(unittest.TestCase):
    def test_basic(self):
        url = makeurl("https://example.com/api/v1", ["path", "to", "resource"], {"k1": "v1", "k2": ["v2", "v3"]})
        self.assertEqual(url, "https://example.com/api/v1/path/to/resource?k1=v1&k2=v2&k2=v3")

    def test_array(self):
        url = makeurl("https://example.com/api/v1", ["path", "to", "resource"], {"k1": "v1", "k2": UrlQueryArray(["v2", "v3"])})
        self.assertEqual(url, "https://example.com/api/v1/path/to/resource?k1=v1&k2%5B%5D=v2&k2%5B%5D=v3")

    def test_query_none(self):
        url = makeurl("https://example.com/api/v1", [], {"none": None})
        self.assertEqual(url, "https://example.com/api/v1")

    def test_query_empty_list(self):
        url = makeurl("https://example.com/api/v1", [], {"empty_list": []})
        self.assertEqual(url, "https://example.com/api/v1")

    def test_query_int(self):
        url = makeurl("https://example.com/api/v1", [], {"int": 1})
        self.assertEqual(url, "https://example.com/api/v1?int=1")

    def test_query_bool(self):
        url = makeurl("https://example.com/api/v1", [], {"bool": True})
        self.assertEqual(url, "https://example.com/api/v1?bool=1")

        url = makeurl("https://example.com/api/v1", [], {"bool": False})
        self.assertEqual(url, "https://example.com/api/v1?bool=0")

    def test_quote_path(self):
        mapping = (
            # (character, expected encoded character)
            (" ", "%20"),
            ("!", "%21"),
            ('"', "%22"),
            ("#", "%23"),
            ("$", "%24"),
            ("%", "%25"),
            ("&", "%26"),
            ("'", "%27"),
            ("(", "%28"),
            (")", "%29"),
            ("*", "%2A"),
            ("+", "%2B"),
            (",", "%2C"),
            ("/", "/"),
            (":", ":"),  # %3A
            (";", "%3B"),
            ("=", "%3D"),
            ("?", "%3F"),
            ("@", "%40"),
            ("[", "%5B"),
            ("]", "%5D"),
        )

        for char, encoded_char in mapping:
            url = makeurl("https://example.com/api/v1", [f"PREFIX_{char}_SUFFIX"])
            self.assertEqual(url, f"https://example.com/api/v1/PREFIX_{encoded_char}_SUFFIX")

    def test_quote_query(self):
        mapping = (
            # (character, expected encoded character)
            (" ", "+"),
            ("!", "%21"),
            ('"', "%22"),
            ("#", "%23"),
            ("$", "%24"),
            ("%", "%25"),
            ("&", "%26"),
            ("'", "%27"),
            ("(", "%28"),
            (")", "%29"),
            ("*", "%2A"),
            ("+", "%2B"),
            (",", "%2C"),
            ("/", "%2F"),
            (":", "%3A"),
            (";", "%3B"),
            ("=", "%3D"),
            ("?", "%3F"),
            ("@", "%40"),
            ("[", "%5B"),
            ("]", "%5D"),
        )

        for char, encoded_char in mapping:
            url = makeurl("https://example.com/api/v1", [], {char: char})
            self.assertEqual(url, f"https://example.com/api/v1?{encoded_char}={encoded_char}")


if __name__ == "__main__":
    unittest.main()
