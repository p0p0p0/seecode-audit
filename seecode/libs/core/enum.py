# coding: utf-8

RISK_TYPE = (
    (1, u"严重"),  # BLOCKER, critical
    (2, u"高危"),  # BLOCKER, high
    (3, u"中危"),  # CRITICAL, medium
    (4, u"低危"),  # MAJOR, low
    (5, u"信息"),  # BLOCKER, info
)

SCAN_STATUS = (
    (1, u"扫描失败"),
    (2, u"等待调度"),
    (3, u"初始化扫描"),
    (4, u"分析组件"),
    (5, u"开始扫描"),
    (6, u"扫描完成"),
)

SCAN_WAY = (
    (1, u"手动"),
    (2, u"API 接口"),
)


EVENT_STATUS = (
    (1, u"待处理"),
    (2, u"已忽略"),
    (3, u"已处理"),
)


PROJECT_STATUS = (
    (1, u"未扫描"),
    (2, u"已扫描"),
    (3, u"扫描失败"),
    (4, u"分支为空"),
)

PROJECT_TYPE = (
    (1, u"线上"),
    (2, u"线下"),
)

REPOSITORY_TYPE = (
    (1, u"Branch"),
    (2, u"Tag"),
)

APP_TYPE = (
    (1, u"GitLab"),
    (2, u"自定义"),
)

ISSUE_STATUS = (
    (1, u"待修复"),
    (2, u"已忽略"),
    (3, u"已修复"),
    (4, u"已确认"),
    (5, u"不修复"),
    # (6, u"重新打开"),
)

BEHAVIOR_TYPE = (
    (1, u"系统"),
    (2, u"人工"),
)


TACTIC_RULE_TYPE = (
    (1, u"正则表达式"),
    (2, u"字符串"),
)

TACTIC_MATCH_TYPE = (
    (1, u"目录名称"),
    (2, u"文件名称"),
    (3, u"文件内容"),
    (4, u"依赖组件"),
)

TACTIC_TYPE = (
    (1, u"Bug"),
    (2, u"Code Smell"),
    (3, u"Vulnerability"),
)

COMPONENT_MATCH_TYPE = (
    (1, u"POM 文件 groupId"),
    # (2, u"POM 文件 groupId + 组件名称"),
    (3, u"组件名称"),
)

SONAR_SEVERITY = (
    (1, u"Blocker"),  # 最高等级，阻碍的
    (2, u"Critical"),  # 高等级，极为严重的
    (3, u"Major"),  # 较高等级，主要的；默认级别。
    (4, u"Minor"),  # 较低等级
    (5, u"Info"),  # 低等级
)

NATURE_TYPE = (
    (1, u"白名单"),
    (2, u"黑名单"),
    (3, u"其他"),
)

ATTRIBUTE_TYPE = (
    (1, u"规则"),
    (2, u"插件"),
    (3, u"其他"),
)

SYSLOG_TYPE = (
    (1, u"系统"),
    (2, u"应用"),
)

SYSLOG_LEVEL = (
    (1, u"严重"),
    (2, u"错误"),
    (3, u"警告"),
    (4, u"信息"),
    (5, u"调试"),
    (6, u"通知"),
)

RSS_TYPE = (
    (1, u"RSS"),
    (2, u"CVE"),
    (3, u"CNNVD"),
)

PATCH_ALARM_TYPE = (
    (1, u"未设置"),
    (2, u"待提醒"),
    (3, u"已提醒"),
)

SCHED_TYPE = (
    (2, u"CRON表达式"),
)

WIDGET_TYPE = (
    (1, u"SCM 配置"),
    (2, u"告警配置"),
)


TASK_GROUP_TYPE = (
    (1, u"扫描单个项目"),
    (2, u"扫描单个项目组"),
    (3, u"扫描所有项目"),
)

SERVICE_STATUS_TYPE = (
    (1, u"运行"),
    (2, u"停止"),
    (3, u"未知"),

)

NODE_ROLE_TYPE = (
    (1, u"UI"),
    (2, u"Client"),
)

CHANGELOG_ACTION_TYPE = (
    (1, u"添加"),
    (2, u"删除"),
    (3, u"修改"),
)

CHANGELOG_MODULE_TYPE = (
    (1, u"扫描引擎"),
    (2, u"策略规则"),
    (3, u"扫描模板"),
)


HTTP_METHOD = (
    (1, u"GET"),
    (2, u"PUT"),
    (3, u"POST"),
)


EMPLOYEE_STATUS = (
    (1, u"离职"),
    (2, u"在职"),
)


GENDER_TYPE = (
    (1, u"女"),
    (2, u"男"),
    (3, u"未知"),
)


SONAR_PROJECT_PROPERTIES = """sonar.projectKey={{project_key}}
sonar.projectName={{project_name}}
sonar.projectVersion=1.0
sonar.sources=.
sonar.sourceEncoding=UTF-8
sonar.exclusions=**/node_modules/**/*.*,
sonar.host.url={{sonar_host}}
sonar.login={{sonar_login}}
sonar.java.binaries=."""


class LOG_LEVEL:

    CRITICAL = 1
    ERROR = 2
    WARN = 3
    INFO = 4
    DEBUG = 5
    NOTIFICATION = 6


class log_type:

    SYS = 1
    APP = 2


class action:

    ADD = 1
    DEL = 2
    UPDATE = 3


class changelog_module:
    SCANNER_ENGINE = 1
    SCAN_TACTIC = 2
    SCAN_TEMPLATE = 3


class task_type:
    SINGLE = 1
    MULTIPLE = 2
    GROUPS = 3


class behavior_type:
    SYS = 1
    HUMAN = 2

ICON_TYPE = (
    (1, u"fa fa-info bg-olive"),
    (2, u"fa fa-comments bg-yellow"),
    (3, u"fa fa-user bg-aqua"),
    (4, u"fa fa-clock-o bg-gray"),
    (5, u"fa fa-envelope bg-blue"),
    (6, u"fa fa-video-camera bg-maroon"),
    (7, u"fa fa-camera bg-purple"),
    (8, u"fa fa-tags bg-fuchsia"),
    (9, u"fa fa-code-fork bg-teal"),
    (10, u"fa fa-database bg-purple"),
    (11, u"fa fa-fw fa-users bg-lime-active"),
)

class icon_type:
    INFO = 1
    MESSAGE = 2
    USER = 3
    TIME = 4
    MAIL = 5
    VIDEO = 6
    CAMERA = 7
    TAGS = 8
    CODE_FORK = 9
    DATABASE = 10
    ORGANIZATION = 11

MONTH_TYPE = (
    (3, u"3个月内"),
    (6, u"6个月内"),
    (9, u"9个月内"),
    (12, u"12个月内"),
    (24, u"24个月内"),
)


BASIC_SCOPE = {
        'vulnerability': {
            'basic': 300.0,
            '1': {
                'scope': 0.4,
                'min': 75.0,
                'max': 100.0,
            },
            '2': {
                'scope': 0.3,
                'min': 50.0,
                'max': 75.0,
            },
            '3': {
                'scope': 0.2,
                'min': 25.0,
                'max': 50.0,
            },
            '4': {
                'scope': 0.1,
                'min': 0.0,
                'max': 25.0,
            },
        },
        'bug': {
            'basic': 200.0,
            '1': {
                'scope': 0.4,
                'min': 75.0,
                'max': 100.0,
            },
            '2': {
                'scope': 0.3,
                'min': 50.0,
                'max': 75.0,
            },
            '3': {
                'scope': 0.2,
                'min': 25.0,
                'max': 50.0,
            },
            '4': {
                'scope': 0.1,
                'min': 0.0,
                'max': 25.0,
            },
        },
        'code smell': {
            'basic': 100.0,
            '1': {
                'scope': 0.1,
                'min': 0.0,
                'max': 25.0,
            },
            '2': {
                'scope': 0.2,
                'min': 25,
                'max': 50,
            },
            '3': {
                'scope': 0.3,
                'min': 50.0,
                'max': 75.0,
            },
            '4': {
                'scope': 0.4,
                'min': 75.0,
                'max': 100.0,
            },
        }
    }