import os
import unittest
import uuid
from Infrastructure.SessionManager import SessionManager

os.environ["APPROVALS_TEXT_DIFF_TOOL"] = "C:\\Program Files\\TortoiseSVN\\bin\\TortoiseMerge.exe"


class FakeUuidGenerator(object):
    def __init__(self, static_uuid):
        self.static_uuid = static_uuid

    def uuid1(self):
        return uuid.UUID(self.static_uuid)


class TestsSessionManager(unittest.TestCase):
    def test_creating_session(self):
        file_name = '00010203-0405-0607-0809-0a0b0c0d0e0f'
        try:
            os.remove(os.path.dirname(os.path.realpath(__file__)) + "\\Sessions\\" + file_name)
        except OSError:
            pass
        fake_uuid_generator = FakeUuidGenerator('{%s}' % file_name)
        session_manager = SessionManager(fake_uuid_generator)
        session_manager.create_session()
        self.assertEqual(session_manager.get_active_sessions(), [file_name])

    def test_clear_sessions(self):

        file_name = '00010203-0405-0607-0809-0a0b0c0d0e0f'
        try:
            os.remove(os.path.dirname(os.path.realpath(__file__)) + "\\Sessions\\" + file_name)
        except OSError:
            pass
        fake_uuid_generator = FakeUuidGenerator('{%s}' % file_name)
        session_manager = SessionManager(fake_uuid_generator)
        session_manager.create_session()
        session_manager.clear_sessions()
        self.assertEqual(session_manager.get_active_sessions(), [])


if __name__ == '__main__':
    unittest.main()
