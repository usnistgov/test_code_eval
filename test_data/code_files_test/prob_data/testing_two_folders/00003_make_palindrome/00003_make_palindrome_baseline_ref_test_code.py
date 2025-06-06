from gen_ai_code_file import make_palindrome


class TestCode(object):
    def test_gc(self):
        assert make_palindrome('') == ''
        assert make_palindrome('x') == 'x'
        assert make_palindrome('xyz') == 'xyzyx'
        assert make_palindrome('xyx') == 'xyx'
        assert make_palindrome('jerry') == 'jerryrrej'
