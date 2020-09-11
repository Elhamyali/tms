import tempfile
import unittest
import sys
import os
import shutil
sys.path.append('src')
import project_localizer


EXAMPLE_FILE = 'example.po'
GOLDEN_EXAMPLE_IN = 'golden_in.po'
GOLDEN_EXAMPLE_OUT = 'golden_out.po'
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
TARGET_LANGUAGE_ISO_LIST = ['es', 'fr']


class TestPoLocalizer(unittest.TestCase):

    # Temporary directories & files to read/write during testing
    temp_root_dir = None
    temp_in_dir = None
    temp_out_dir = None

    @classmethod
    def setUpClass(cls):

        # Make a temporary root directory and in/out subdirectories to hold the test resources in
        cls.temp_root_dir = tempfile.mkdtemp()
        cls.temp_in_dir = os.path.join(cls.temp_root_dir, 'in')
        cls.temp_out_dir = os.path.join(cls.temp_root_dir, 'out')

        if not os.path.exists(cls.temp_in_dir):
            os.makedirs(cls.temp_in_dir)

        if not os.path.exists(cls.temp_out_dir):
            os.makedirs(cls.temp_out_dir)

        # Get the path for the golden in example file
        golden_in_filepath = os.path.join(RESOURCES_DIR, GOLDEN_EXAMPLE_IN)

        # Create subdirectories for each target language
        # and add a copy of the golden in example file in each
        for lang in TARGET_LANGUAGE_ISO_LIST:
            lang_subdir = os.path.join(cls.temp_in_dir, lang)
            if not os.path.exists(lang_subdir):
                os.makedirs(lang_subdir)

            # Copy the golden in example file into the lang_subdir
            lang_subdir_example_path = os.path.join(lang_subdir, EXAMPLE_FILE)
            shutil.copyfile(golden_in_filepath, lang_subdir_example_path)

    @classmethod
    def tearDownClass(cls):
        # Remove temporary root directory and its subdirectories & files
        shutil.rmtree(cls.temp_root_dir)

    def test_localize_project(self):
        """
        localize_project
            expected in: input_dir, output_dir, translation_api, google_key_path
            expected out: localization subdirs created in output_dir
        """

        # Call localize_project with the test input and output directories
        project_localizer.localize_project(self.temp_in_dir, self.temp_out_dir, translation_api='caps')

        # TEST: Check that all localization subdirectories are created in the output dir
        for lang in TARGET_LANGUAGE_ISO_LIST:
            lang_subdir = os.path.join(self.temp_out_dir, lang)
            self.assertTrue(os.path.exists(lang_subdir))

    def test_create_output_localized_subdir(self):
        """
        create_output_localized_subdir
            expected in: output_dir, target_lang_iso
            expected out: subdir for target_lang_iso created in output_dir
        """
        # Language subdir and path for testing
        lang = TARGET_LANGUAGE_ISO_LIST[0]
        lang_subdir = os.path.join(self.temp_out_dir, lang)

        # Call create_output_localized_subdir
        project_localizer.create_output_localized_subdir(self.temp_out_dir, lang)

        # TEST: Ensure that lang_subdir is created
        self.assertTrue(os.path.exists(lang_subdir))

    def test_validate_args_invalid_in(self):
        """
        validate_args
            expected_in: input_dir, output_dir
            expected_out: Error for invalid input_dir
        """

        input_dir_invalid = ""

        # TEST: Error is raised if the input_dir is invalid
        with self.assertRaises(project_localizer.InvalidArgumentError):
            project_localizer.validate_args(input_dir_invalid, self.temp_out_dir)

    def test_validate_args_invalid_out(self):
        """
        validate_args
            expected_in: input_dir, output_dir
            expected_out: Error for invalid output_dir
        """
        output_dir_invalid = ""

        # TEST: Error is raised if the output_dir is invalid
        with self.assertRaises(project_localizer.InvalidArgumentError):
            project_localizer.validate_args(self.temp_in_dir, output_dir_invalid)


if __name__ == '__main__':
    unittest.main()