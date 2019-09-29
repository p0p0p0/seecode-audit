# coding: utf-8

CONFIG_ENGINE_CACHE = (
    60 * 60 * 24 * 1024,  # TIMEOUT
    "config:engine",
    "config:engine:all",
    "config:engine:customize",
)

CONFIG_LANG_CACHE = (
    60 * 60 * 24 * 1024,  # TIMEOUT
    "conf:language",
    "conf:language:all",
)

CONFIG_NODE_CACHE = (
    60 * 60 * 24 * 1024,  # TIMEOUT
    "conf:node",
    "conf:node:service",
)

CONFIG_TEMPLATE_CACHE = (
    (0, 60 * 60 * 24 * 1024),  # TIMEOUT
    (1, "config_engine"),
)

ISSUE_CACHE = (
    60 * 60 * 24 * 1024,  # TIMEOUT
    "issue",
    "issue:whitelist",
)

# 项目
PROJECT_GROUP_CACHE = (
    60 * 60 * 24 * 1024, # TIMEOUT
    "project:group",
    "project:gitlab_group",
    "project:group_top20",
)

PROJECT_MEMBER_CACHE = (
    60 * 60 * 24 * 1024, # TIMEOUT
    "project:member",
    "project:member:gitlab",
)


PROJECT_INFO_CACHE = (
    60 * 60 * 24 * 1024,  # TIMEOUT
    "project:info",
    "project:info:gitlab",
    "project:info:top50",
)


PROJECT_APP_CACHE = (
    60 * 60 * 24 * 1024,  # TIMEOUT
    "project:app",  # 1
    "project:app:dependent",  # 2
    "project:app:statistics",  # 3
    "project:app:risk",  # 4
)

PROJECT_REPO_CACHE = (
    60 * 60 * 24 * 1024,  # TIMEOUT
    "project:repo",
)

# 扫描
SCAN_CACHE = (
    60 * 60 * 24 * 1024,  # TIMEOUT
    "scan:group",  # 1
    "scan:group:all",  # 2
    "scan:task",  # 3
    "scan:result",  # 4
    "scan:group:default",  # 5
)

SCAN_PROFILE_CACHE = (
    60 * 60 * 24 * 1024,  # TIMEOUT
    "scan:profile",
    "scan:profile:engine",
    "scan:profile:engine:rule",
    "scan:profile:engine:plugin",
    "scan:profile:all",
)

# 系统设置
SYSTEM_CACHE = (
    60 * 60 * 24 * 1024,  # TIMEOUT 0
    "sys:config",  # 1
    "sys:periodic",  # 2
    "sys:permissions",  # 3
    "sys:sched",  # 4
    "sys:service",  # 5
    "sys:service:key",  # 6
    "sys:syslogs:key",  # 7
    "sys:widget",  # 8
    "sys:widget:scm",  # 9
    "sys:widget:alarm",  # 10
    "sys:dept",  # 11
    "sys:employee",  # 12
)

TACTIC_CACHE = (
    60 * 60 * 24 * 1024,  # TIMEOUT
    "tactic",  # 1
    "tactic:tags",  # 2
)


VULN_CACHE = (
    60 * 60 * 24 * 1024,  # TIMEOUT
    "vuln",
    "vuln:cve",
    "vuln:cate",
    "vuln:cate:all",
    "vuln:origin:all",
)

UPGRADE_CACHE = (
    60 * 60 * 24 * 1024,  # TIMEOUT
    "ui",
    "client",
    "upgrade",
)

DASHBOARD = (
    60 * 15,  # TIMEOUT
    "dashboard:total",
    "dashboard:scan",
    "dashboard:project",
    "dashboard:bu",
    "dashboard:tactic",
    "dashboard:alarm",
)

