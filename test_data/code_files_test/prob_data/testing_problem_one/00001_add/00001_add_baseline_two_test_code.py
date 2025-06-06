from gen_ai_code_file import add
import pytest
import random

class TestCode(object):

    def test_add(self):
        assert add(2, 3) == 5
        assert add(5, 7) == 12
        assert add(7, 5) == 12
