from genai_code_file import make_palindrome


class TestCode(object):
    def test_gc(self):
        assert make_palindrome('') == ''
        assert make_palindrome('cat') == 'catac'
        assert make_palindrome('cata') == 'catac'
