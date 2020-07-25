import subprocess
import traceback
from os import path


def build_java_project(service_workspace):
    try:
        result = subprocess.check_output('mvn clean package', shell=True, cwd=service_workspace)
        if 'Finished' in str(result):
            return path.join(service_workspace, 'target/deploy')
    except Exception:
        print(traceback.format_exc())
