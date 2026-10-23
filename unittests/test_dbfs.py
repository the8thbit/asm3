
import unittest
from unittests import base

import asm3.dbfs
import asm3.utils

class TestDBFS(unittest.TestCase):

    def setUp(self):
        asm3.dbfs.put_string_filepath(base.get_dbo(), "/reports/nopic.jpg", b"fake_jpg_image_data")

    def tearDown(self):
        asm3.dbfs.delete_filepath(base.get_dbo(), "/reports/nopic.jpg")

    def test_create_path(self):
        asm3.dbfs.create_path(base.get_dbo(), "/", "test")
        asm3.dbfs.delete_path(base.get_dbo(), "test")
        asm3.dbfs.delete(base.get_dbo(), "test")
        asm3.dbfs.delete_filepath(base.get_dbo(), "/test")

    def test_get_string_filepath(self):
        self.assertNotEqual(0, len(asm3.dbfs.get_string_filepath(base.get_dbo(), "/reports/nopic.jpg")))

    def test_get_string(self):
        self.assertNotEqual(0, len(asm3.dbfs.get_string(base.get_dbo(), "nopic.jpg", "/reports")))

    def test_put_string_filepath(self):
        content = b"123test"
        asm3.dbfs.put_string_filepath(base.get_dbo(), "/reports/test.txt", content)
        self.assertEqual(content, asm3.dbfs.get_string_filepath(base.get_dbo(), "/reports/test.txt"))
        asm3.dbfs.delete_filepath(base.get_dbo(), "/reports/test.txt")

    def test_file_exists(self):
        content = b"123test"
        asm3.dbfs.put_string_filepath(base.get_dbo(), "/reports/test.txt", content)
        self.assertTrue(asm3.dbfs.file_exists(base.get_dbo(), "test.txt"))

    def test_list_contents(self):
        self.assertNotEqual(0, len(asm3.dbfs.list_contents(base.get_dbo(), "/reports")))

    def test_get_document_repository(self):
        asm3.dbfs.get_document_repository(base.get_dbo())

    def test_upload_document_repository(self):
        asm3.dbfs.upload_document_repository(base.get_dbo(), "", "testdr.txt", b"content")
        self.assertEqual(b"content", asm3.dbfs.get_string_filepath(base.get_dbo(), "/document_repository/testdr.txt"))

    def test_rename_document_repository(self):
        asm3.dbfs.upload_document_repository(base.get_dbo(), "", "testrename.txt", b"content")
        asm3.dbfs.rename_document_repository(base.get_dbo(), "/document_repository", "testrename.txt", "testrenamed.txt")
        self.assertEqual(b"content", asm3.dbfs.get_string_filepath(base.get_dbo(), "/document_repository/testrenamed.txt"))
        asm3.dbfs.delete_filepath(base.get_dbo(), "/document_repository/testrenamed.txt")

    def test_move_document_repository(self):
        asm3.dbfs.upload_document_repository(base.get_dbo(), "", "testmove.txt", b"content")
        asm3.dbfs.rename_document_repository(base.get_dbo(), "/document_repository", "testmove.txt", "training/testmoved.txt")
        self.assertFalse(asm3.dbfs.file_exists(base.get_dbo(), "testmove.txt", "/document_repository"))
        self.assertEqual(b"content", asm3.dbfs.get_string_filepath(base.get_dbo(), "/document_repository/training/testmoved.txt"))
        asm3.dbfs.delete_filepath(base.get_dbo(), "/document_repository/training/testmoved.txt")

    def test_move_document_repository_to_root(self):
        asm3.dbfs.upload_document_repository(base.get_dbo(), "training", "testroot.txt", b"content")
        asm3.dbfs.rename_document_repository(base.get_dbo(), "/document_repository/training", "testroot.txt", "/document_repository/testrootmoved.txt")
        self.assertFalse(asm3.dbfs.file_exists(base.get_dbo(), "testroot.txt", "/document_repository/training"))
        self.assertEqual(b"content", asm3.dbfs.get_string_filepath(base.get_dbo(), "/document_repository/testrootmoved.txt"))
        asm3.dbfs.delete_filepath(base.get_dbo(), "/document_repository/testrootmoved.txt")

    def test_move_document_repository_existing_destination(self):
        asm3.dbfs.upload_document_repository(base.get_dbo(), "", "testsource.txt", b"source")
        asm3.dbfs.upload_document_repository(base.get_dbo(), "training", "testdestination.txt", b"destination")
        with self.assertRaises(asm3.utils.ASMValidationError):
            asm3.dbfs.rename_document_repository(base.get_dbo(), "/document_repository", "testsource.txt", "training/testdestination.txt")
        self.assertEqual(b"source", asm3.dbfs.get_string_filepath(base.get_dbo(), "/document_repository/testsource.txt"))
        self.assertEqual(b"destination", asm3.dbfs.get_string_filepath(base.get_dbo(), "/document_repository/training/testdestination.txt"))
        asm3.dbfs.delete_filepath(base.get_dbo(), "/document_repository/testsource.txt")
        asm3.dbfs.delete_filepath(base.get_dbo(), "/document_repository/training/testdestination.txt")

    def test_rename_document_repository_outside_path(self):
        with self.assertRaises(asm3.utils.ASMValidationError):
            asm3.dbfs.rename_document_repository(base.get_dbo(), "/reports", "nopic.jpg", "renamed.jpg")
        with self.assertRaises(asm3.utils.ASMValidationError):
            asm3.dbfs.rename_document_repository(base.get_dbo(), "/document_repositoryx", "nopic.jpg", "renamed.jpg")
        asm3.dbfs.upload_document_repository(base.get_dbo(), "", "testescape.txt", b"content")
        with self.assertRaises(asm3.utils.ASMValidationError):
            asm3.dbfs.rename_document_repository(base.get_dbo(), "/document_repository", "testescape.txt", "../reports/escaped.txt")
        self.assertEqual(b"content", asm3.dbfs.get_string_filepath(base.get_dbo(), "/document_repository/testescape.txt"))
        asm3.dbfs.delete_filepath(base.get_dbo(), "/document_repository/testescape.txt")
        self.assertNotEqual(0, len(asm3.dbfs.get_string_filepath(base.get_dbo(), "/reports/nopic.jpg")))

    def test_get_report_images(self):
        self.assertNotEqual(0, len(asm3.dbfs.get_report_images(base.get_dbo())))

    def test_delete_orphaned_media(self):
        asm3.dbfs.delete_orphaned_media(base.get_dbo())

    def test_switch_storage(self):
        asm3.dbfs.switch_storage(base.get_dbo())


