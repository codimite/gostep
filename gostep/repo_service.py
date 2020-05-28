import traceback
from svn import remote

from gostep.consts import TEMPLATE_REPO


def clone_template(service, runtime, target_dir):
    """
        Observe serverless template and returns the directory path.

                Parameters:
                        service (string): root directory of the repo
                        runtime (string): sublevel directory of the repo
                        target_dir (string): download target

                Returns:
                        template_dir (str): path of downloaded template
    """
    try:
        template = TEMPLATE_REPO%(service, runtime)
        print("Getting %s template for %s..."%(service, runtime))
        svn_client = remote.RemoteClient(template)
        svn_client.checkout(target_dir)
        print("Successfully fetched template")
        return ''.join([target_dir, '/', service, '/', runtime])
    except Exception:
        print(traceback.format_exc())
