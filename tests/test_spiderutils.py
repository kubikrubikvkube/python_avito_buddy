from datetime import datetime
from unittest import TestCase

from avito_russia.avito_russia.avito_russia_utils import gen_random_string, last_stamp


class TestSpiderUtils(TestCase):

    def test_gen_random_string(self):
        rnd_str = gen_random_string(44)
        assert rnd_str is not None
        assert len(rnd_str) == 44

    def test_last_timestamp(self):
        tmstp = last_stamp()
        assert tmstp is not None
        assert datetime.fromtimestamp(tmstp) < datetime.now()
