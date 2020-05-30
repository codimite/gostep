import traceback

from svn import remote

from gostep.consts import TEMPLATE_REPO


def clone_template(kind, environment, target_dir):
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
        template = TEMPLATE_REPO % (kind, environment)
        print("Getting %s template for %s..." % (kind, environment))
        svn_client = remote.RemoteClient(template)
        svn_client.checkout(target_dir)
        print("Successfully fetched template")
        return ''.join([target_dir, '/', kind, '/', environment])
    except Exception:
        print(traceback.format_exc())
