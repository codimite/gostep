from git import Repo

from gostep.consts import TEMPLATE_REPO
from gostep.consts import TEMPLATE_BRANCH


def clone_template(service, runtime, target_dir):
    template = service + '/' + runtime
    Repo.clone(TEMPLATE_REPO, )
