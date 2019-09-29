# coding: utf-8
from __future__ import unicode_literals

from seecode.apps.project.models.item import ProjectHistoryInfo
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.units import close_old_connections


def create_pro_history_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """

    project_obj = kwargs.get('project_obj', None)
    htype = kwargs.get('type', 1)
    user = kwargs.get('user', None)
    title = kwargs.get('title', None)
    is_first = kwargs.get('is_first', False)
    description = kwargs.get('description', None)

    if not description:
        raise ParameterIsEmptyException(u'Project description cannot be empty!')

    if len(title) > 128:
        title = title[:128]

    close_old_connections()

    his = ProjectHistoryInfo(
        project=project_obj,
        type=htype,
        user=user,
        title=title,
        is_first=is_first,
        description=description
    )
    his.save()
    return his
