import unittest
from unittest import TestCase
import drivecasa
import os
import tempfile
from drivecasa import default_test_ouput_dir


class TestDefaultCasaInterface(TestCase):
    """
    Ensure that the method of shelling out to CASA is working as expected.
    """
    def shortDescription(self):
        return None

    @classmethod
    def setUpClass(cls):
        casa_dir = os.environ.get('CASA_DIR',
                                  drivecasa.default_casa_dir)
        cls.casa = drivecasa.Casapy(casa_dir, echo_to_stdout=False)

    def test_script_file(self):
        script = 'tasklist()\n'
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile_path = tmpfile.name
            tmpfile.write(script)
        out, errors = self.casa.run_script_from_file(tmpfile_path)
#         for l in out:
#             print l
        self.assertNotEqual(len(out), 0)
        self.assertEqual(len(errors), 0)
        os.remove(tmpfile_path)

    def test_basic_command(self):
        script = ['tasklist()']
        out, errors = self.casa.run_script(script)
#         for l in out:
#             print l
        self.assertNotEqual(len(out), 0)
        self.assertEqual(len(errors), 0)

    def test_error_exception(self):
        script = ['importuvfits("dummy_in.fits", "dummy_out.ms")']
        with self.assertRaises(RuntimeError):
            out, errors = self.casa.run_script(script)

    def test_error_reporting(self):
        script = ['importuvfits("dummy_in.fits", "dummy_out.ms")']
        out, errors = self.casa.run_script(script, raise_on_severe=False)
        self.assertEqual(len(errors), 1)


#         print "Errors:", errors
#     def test_logged_to_stdout_only(self):
#         stdout, stderr, errors = run_script(self.script, casa_dir=self.casa_dir,
#                    log2term=True,
#                    casa_logfile=False,
#                    return_stdout=True)
#         self.assertNotEqual(len(stdout), 0)
#         self.assertEqual(len(stderr), 0)
#         self.assertEqual(len(errors), 0)
#         print "Stdout:"
#         print stdout
#         print "Stderr:"
#         print stderr
