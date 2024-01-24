import json
import yaml
from robot import run
from robot.api import ExecutionResult
import logging

logging.basicConfig(filename='robot_test.log', level=logging.INFO)


class RobotTest:
    def __init__(self, test_file_suite):
        self.test_suite_file = test_file_suite

    def run_tests(self):
        options = {
            'outputdir': '',  # Change to your desired output directory
            'output': 'output.xml',
            'log': 'log.html',
            'report': 'report.html'
        }
        return run(self.test_suite_file, **options)

    def extract_results(self, output):
        result = ExecutionResult('output.xml')
        result.configure(stat_config={'suite_stat_level': 2})
        test_results = []

        for suite in result.suite.suites:
            for test in suite.tests:
                test_case_name = test.name
                test_case_status = test.status
                test_results.append({'Test Case': test_case_name,
                                     'Status': test_case_status})
        return test_results

    def extract_results_as_json(self, output):
        results = self.extract_results(output)
        return results

    def extract_results_as_yaml(self, output):
        results = self.extract_results(output)
        return results

    def write_results_to_json_files(self, output_folder):
        output = self.run_tests()
        json_results = self.extract_results_as_json(output)
        print(json_results)
        for result in json_results:
            test_case_name = result['Test Case']
            file_name = f"{test_case_name}.json"
            file_path = f"{output_folder}/{file_name}"

            with open(file_path, 'w') as json_file:
                json.dump(result, json_file, indent=4)

            logging.info(f"JSON result file created: {file_path}")

    def write_results_to_yaml_files(self, output_folder):
        output = self. run_tests()
        yaml_results = self.extract_results_as_yaml(output)
        for result in yaml_results:
            test_case_name = result['Test Case']
            file_name = f"{test_case_name}.yaml"
            file_path = f"{output_folder}/{file_name}"

            with open(file_path, 'w') as yaml_file:
                yaml.dump(result, yaml_file)

            logging.info(f"YAML result file created: {file_path}")


if __name__ == '__main__':
    test_suite_file = 'vm_monitoring.robot'
    output_folder = 'robot_test_results'
    test_runner = RobotTest(test_suite_file)
    test_runner.write_results_to_json_files(output_folder)
    test_runner.write_results_to_yaml_files(output_folder)
