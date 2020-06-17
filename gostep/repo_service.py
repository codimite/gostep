import traceback

from svn import remote

from gostep.consts import TEMPLATE_REPO


def clone_template(environment, target_dir):
    """
        Observe serverless template and returns the directory path.

            Parameters:
                kind (string): root directory of the repo
                environment (string): sublevel directory of the repo
                target_dir (string): download target

            Returns:
                template_dir (str): path of downloaded template
    """
    try:
        template = ''.join([TEMPLATE_REPO, '/function/', environment])
        print("Getting %s template..." % environment)
        svn_client = remote.RemoteClient(template)
        print(target_dir)
        svn_client.checkout(target_dir)
        print("Successfully fetched template")
        return target_dir
    except Exception:
        print(traceback.format_exc())
