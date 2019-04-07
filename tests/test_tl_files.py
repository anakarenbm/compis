import unittest  # Reference: https://docs.python.org/2/library/unittest.html
from parser.parser import parser, yacc, quad_helper, error_helper

TESTING_PREFIX = "our_tests/"


def aux_tl_file(file_name, expected_number_of_errors):
    try:
        f = open(file_name, "r")
        data = f.read()
        f.close()
        yacc.parse(data, tracking=True)
        number_of_errors = error_helper.error_cont
        error_helper.reset()
        return number_of_errors
    except EOFError:
        print("EOFError")


class OurTestCase(unittest.TestCase):
    def test_0_0_pass_estatutos_secuenciales(self):
        file_name = TESTING_PREFIX + "0_0_pass_estatutos_secuenciales.tl"
        expected_errors = 0
        result = aux_tl_file(file_name, expected_errors)
        print(f"\nTESTING: {file_name}\n")
        self.assertEqual(result, expected_errors)

    def test_0_1_pass_estatutos_secuenciales(self):
        file_name = TESTING_PREFIX + "0_1_pass_estatutos_secuenciales.tl"
        expected_errors = 0
        result = aux_tl_file(file_name, expected_errors)
        print(f"\nTESTING: {file_name}\n")
        self.assertEqual(result, expected_errors)

    def test_1_0_fail_estatutos_secuenciales(self):
        file_name = TESTING_PREFIX + "1_0_fail_estatutos_secuenciales.tl"
        expected_errors = 1
        result = aux_tl_file(file_name, expected_errors)
        print(f"\nTESTING: {file_name}\n")
        self.assertEqual(result, expected_errors)

    def test_2_0_pass_estatutos_secuenciales(self):
        file_name = TESTING_PREFIX + "2_0_pass_estatutos_secuenciales.tl"
        expected_errors = 0
        result = aux_tl_file(file_name, expected_errors)
        print(f"\nTESTING: {file_name}\n")
        self.assertEqual(result, expected_errors)

    def test_2_1_pass_estatutos_secuenciales_rel(self):
        file_name = TESTING_PREFIX + "2_1_pass_estatutos_secuenciales_rel.tl"
        expected_errors = 0
        result = aux_tl_file(file_name, expected_errors)
        print(f"\nTESTING: {file_name}\n")
        self.assertEqual(result, expected_errors)

    def test_2_2_pass_estatutos_secuenciales_eval(self):
        file_name = TESTING_PREFIX + "2_2_pass_estatutos_secuenciales_eval.tl"
        expected_errors = 0
        result = aux_tl_file(file_name, expected_errors)
        print(f"\nTESTING: {file_name}\n")
        self.assertEqual(result, expected_errors)

    def test_3_0_pass_estatutos_condicionales_if(self):
        file_name = TESTING_PREFIX + "3_0_pass_estatutos_condicionales_if.tl"
        expected_errors = 0
        result = aux_tl_file(file_name, expected_errors)
        print(f"\nTESTING: {file_name}\n")
        self.assertEqual(result, expected_errors)

    def test_5_2_fail_returning_function_no_args(self):
        file_name = TESTING_PREFIX + "5_2_fail_returning_function_no_args.tl"
        expected_errors = 1
        result = aux_tl_file(file_name, expected_errors)
        print(f"\nTESTING: {file_name}\n")
        self.assertEqual(result, expected_errors)

    def test_5_4_fail_call_non_existing_function(self):
        file_name = TESTING_PREFIX + "5_4_fail_call_non_existing_function.tl"
        expected_errors = 1
        result = aux_tl_file(file_name, expected_errors)
        print(f"\nTESTING: {file_name}\n")
        self.assertEqual(result, expected_errors)
    def test_8_1_fail_gorritos_html(self):
        file_name = TESTING_PREFIX + "8_1_fail_gorritos_html.tl"
        expected_errors = 2
        result = aux_tl_file(file_name, expected_errors)
        print(f"\nTESTING: {file_name}\n")
        self.assertEqual(result, expected_errors)

    def test_8_6_pass_func_call_html(self):
        file_name = TESTING_PREFIX + "8_6_pass_func_call_html.tl"
        expected_errors = 0
        result = aux_tl_file(file_name, expected_errors)
        print(f"\nTESTING: {file_name}\n")
        self.assertEqual(result, expected_errors)

    def test_8_7_fail_eval_outside_tag_html(self):

        with self.assertRaises(SystemExit) as cm:
            file_name = TESTING_PREFIX + "8_7_fail_eval_outside_tag_html.tl"
            print(f"\nTESTING: {file_name}\n")
            # expected_errors: None, since error_helper cannot help here (program should exit)
            expected_errors = None

            # No result expected since program should exit (1)
            # result = aux_tl_file(file_name, expected_errors)
            aux_tl_file(file_name, expected_errors)
        expected_exit_code = 1
        self.assertEqual(cm.exception.code, expected_exit_code)

    def test_8_8_fail_do_loop_outside_tag_html(self):
        with self.assertRaises(SystemExit) as cm:
            file_name = TESTING_PREFIX + "8_8_fail_do_loop_outside_tag_html.tl"
            print(f"\nTESTING: {file_name}\n")
            # expected_errors: None, since error_helper cannot help here (program should exit)
            expected_errors = None

            # No result expected since program should exit (1)
            # result = aux_tl_file(file_name, expected_errors)
            aux_tl_file(file_name, expected_errors)
        expected_exit_code = 1
        self.assertEqual(cm.exception.code, expected_exit_code)

    def test_8_9_fail_loop_outside_tag_html(self):
        with self.assertRaises(SystemExit) as cm:
            file_name = TESTING_PREFIX + "8_9_fail_loop_outside_tag_html.tl"
            print(f"\nTESTING: {file_name}\n")
            # expected_errors: None, since error_helper cannot help here (program should exit)
            expected_errors = None

            # No result expected since program should exit (1)
            # result = aux_tl_file(file_name, expected_errors)
            aux_tl_file(file_name, expected_errors)
        expected_exit_code = 1
        self.assertEqual(cm.exception.code, expected_exit_code)
