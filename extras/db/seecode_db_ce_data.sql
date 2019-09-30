
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Records of auth_group
-- ----------------------------
BEGIN;

INSERT INTO `auth_group` VALUES (1, '超级管理员');
INSERT INTO `auth_group` VALUES (2, '普通账户');


INSERT INTO `django_content_type` VALUES (1, 'scan', 'issueinfo');
INSERT INTO `django_content_type` VALUES (2, 'node', 'hostinfo');
INSERT INTO `django_content_type` VALUES (3, 'node', 'upgradepackageinfo');
INSERT INTO `django_content_type` VALUES (4, 'project', 'applicationinfo');
INSERT INTO `django_content_type` VALUES (5, 'project', 'dependentinfo');
INSERT INTO `django_content_type` VALUES (6, 'project', 'groupinfo');
INSERT INTO `django_content_type` VALUES (7, 'project', 'memberinfo');
INSERT INTO `django_content_type` VALUES (8, 'project', 'projectinfo');
INSERT INTO `django_content_type` VALUES (9, 'scan', 'scanprofileinfo');
INSERT INTO `django_content_type` VALUES (10, 'scan', 'taskgroupinfo');
INSERT INTO `django_content_type` VALUES (11, 'scan', 'taskinfo');
INSERT INTO `django_content_type` VALUES (12, 'system', 'configinfo');
INSERT INTO `django_content_type` VALUES (15, 'system', 'languageinfo');
INSERT INTO `django_content_type` VALUES (17, 'tactic', 'engineinfo');
INSERT INTO `django_content_type` VALUES (18, 'tactic', 'tacticinfo');
INSERT INTO `django_content_type` VALUES (19, 'tactic', 'vulncategoryinfo');
INSERT INTO `django_content_type` VALUES (20, 'tactic', 'vulninfo');
INSERT INTO `django_content_type` VALUES (21, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (22, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (23, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (24, 'system', 'schedinfo');
INSERT INTO `django_content_type` VALUES (25, 'system', 'sysloginfo');


-- INSERT INTO `auth_permission` VALUES (1, '添加风险问题', 1, 'add_issueinfo');
INSERT INTO `auth_permission` VALUES (2, '编辑风险问题', 1, 'change_issueinfo');
INSERT INTO `auth_permission` VALUES (3, '删除风险问题', 1, 'delete_issueinfo');
INSERT INTO `auth_permission` VALUES (4, '查看风险问题', 1, 'view_issueinfo');


-- INSERT INTO `auth_permission` VALUES (5, '添加节点', 2, 'add_hostinfo');
-- INSERT INTO `auth_permission` VALUES (6, '编辑节点', 2, 'change_hostinfo');
-- INSERT INTO `auth_permission` VALUES (7, '删除节点', 2, 'delete_hostinfo');
INSERT INTO `auth_permission` VALUES (8, '查看节点', 2, 'view_hostinfo');


INSERT INTO `auth_permission` VALUES (9, '添加升级包', 3, 'add_upgradepackageinfo');
INSERT INTO `auth_permission` VALUES (10, '编辑升级包', 3, 'change_upgradepackageinfo');
INSERT INTO `auth_permission` VALUES (11, '删除升级包', 3, 'delete_upgradepackageinfo');
INSERT INTO `auth_permission` VALUES (12, '查看升级包', 3, 'view_upgradepackageinfo');


INSERT INTO `auth_permission` VALUES (13, '添加应用', 4, 'add_applicationinfo');
INSERT INTO `auth_permission` VALUES (14, '编辑应用', 4, 'change_applicationinfo');
INSERT INTO `auth_permission` VALUES (15, '删除应用', 4, 'delete_applicationinfo');
INSERT INTO `auth_permission` VALUES (16, '查看应用', 4, 'view_applicationinfo');


-- INSERT INTO `auth_permission` VALUES (17, '添加依赖', 5, 'add_dependentinfo');
-- INSERT INTO `auth_permission` VALUES (18, '编辑依赖', 5, 'change_dependentinfo');
INSERT INTO `auth_permission` VALUES (19, '删除依赖', 5, 'delete_dependentinfo');
INSERT INTO `auth_permission` VALUES (20, '查看依赖', 5, 'view_dependentinfo');


INSERT INTO `auth_permission` VALUES (21, '添加项目组', 6, 'add_groupinfo');
INSERT INTO `auth_permission` VALUES (22, '编辑项目组', 6, 'change_groupinfo');
INSERT INTO `auth_permission` VALUES (23, '删除项目组', 6, 'delete_groupinfo');
INSERT INTO `auth_permission` VALUES (24, '查看项目组', 6, 'view_groupinfo');


-- INSERT INTO `auth_permission` VALUES (24, '添加项目成员', 7, 'add_memberinfo');
-- INSERT INTO `auth_permission` VALUES (25, '编辑项目成员', 7, 'change_memberinfo');
-- INSERT INTO `auth_permission` VALUES (26, '删除项目成员', 7, 'delete_memberinfo');
INSERT INTO `auth_permission` VALUES (27, '查看项目成员', 7, 'view_memberinfo');


INSERT INTO `auth_permission` VALUES (28, '添加项目', 8, 'add_projectinfo');
INSERT INTO `auth_permission` VALUES (29, '编辑项目', 8, 'change_projectinfo');
INSERT INTO `auth_permission` VALUES (30, '删除项目', 8, 'delete_projectinfo');
INSERT INTO `auth_permission` VALUES (31, '查看项目', 8, 'view_projectinfo');


INSERT INTO `auth_permission` VALUES (32, '添加扫描模板', 9, 'add_scanprofileinfo');
INSERT INTO `auth_permission` VALUES (33, '编辑扫描模板', 9, 'change_scanprofileinfo');
INSERT INTO `auth_permission` VALUES (34, '删除扫描模板', 9, 'delete_scanprofileinfo');
INSERT INTO `auth_permission` VALUES (35, '查看扫描模板', 9, 'view_scanprofileinfo');


INSERT INTO `auth_permission` VALUES (36, '添加扫描分组', 10, 'add_taskgroupinfo');
INSERT INTO `auth_permission` VALUES (37, '编辑扫描分组', 10, 'change_taskgroupinfo');
INSERT INTO `auth_permission` VALUES (38, '删除扫描分组', 10, 'delete_taskgroupinfo');
INSERT INTO `auth_permission` VALUES (39, '查看扫描分组', 10, 'view_taskgroupinfo');


INSERT INTO `auth_permission` VALUES (40, '添加扫描', 11, 'add_taskinfo');
INSERT INTO `auth_permission` VALUES (41, '编辑扫描', 11, 'change_taskinfo');
INSERT INTO `auth_permission` VALUES (42, '删除扫描', 11, 'delete_taskinfo');
INSERT INTO `auth_permission` VALUES (43, '查看扫描', 11, 'view_taskinfo');


-- INSERT INTO `auth_permission` VALUES (44, '添加系统设置', 12, 'add_configinfo');
INSERT INTO `auth_permission` VALUES (45, '编辑系统设置', 12, 'change_configinfo');
-- INSERT INTO `auth_permission` VALUES (46, '删除系统设置', 12, 'delete_configinfo');
INSERT INTO `auth_permission` VALUES (47, '查看系统设置', 12, 'view_configinfo');


INSERT INTO `auth_permission` VALUES (56, '添加开发语言', 15, 'add_languageinfo');
INSERT INTO `auth_permission` VALUES (57, '编辑开发语言', 15, 'change_languageinfo');
INSERT INTO `auth_permission` VALUES (58, '删除开发语言', 15, 'delete_languageinfo');
INSERT INTO `auth_permission` VALUES (59, '查看开发语言', 15, 'view_languageinfo');


INSERT INTO `auth_permission` VALUES (64, '添加扫描引擎', 17, 'add_engineinfo');
INSERT INTO `auth_permission` VALUES (65, '编辑扫描引擎', 17, 'change_engineinfo');
INSERT INTO `auth_permission` VALUES (66, '删除扫描引擎', 17, 'delete_engineinfo');
INSERT INTO `auth_permission` VALUES (67, '查看扫描引擎', 17, 'view_engineinfo');


INSERT INTO `auth_permission` VALUES (68, '添加扫描策略', 18, 'add_tacticinfo');
INSERT INTO `auth_permission` VALUES (69, '编辑扫描策略', 18, 'change_tacticinfo');
INSERT INTO `auth_permission` VALUES (70, '删除扫描策略', 18, 'delete_tacticinfo');
INSERT INTO `auth_permission` VALUES (71, '查看扫描策略', 18, 'view_tacticinfo');

INSERT INTO `auth_permission` VALUES (72, '添加漏洞类型', 19, 'add_vulncategoryinfo');
INSERT INTO `auth_permission` VALUES (73, '编辑漏洞类型', 19, 'change_vulncategoryinfo');
INSERT INTO `auth_permission` VALUES (74, '删除漏洞类型', 19, 'delete_vulncategoryinfo');
INSERT INTO `auth_permission` VALUES (75, '查看漏洞类型', 19, 'view_vulncategoryinfo');


INSERT INTO `auth_permission` VALUES (76, '添加漏洞', 20, 'add_vulninfo');
INSERT INTO `auth_permission` VALUES (77, '编辑漏洞', 20, 'change_vulninfo');
INSERT INTO `auth_permission` VALUES (78, '删除漏洞', 20, 'delete_vulninfo');
INSERT INTO `auth_permission` VALUES (79, '查看漏洞', 20, 'view_vulninfo');


INSERT INTO `auth_permission` VALUES (80, '添加账户组', 21, 'add_group');
INSERT INTO `auth_permission` VALUES (81, '编辑账户组', 21, 'change_group');
INSERT INTO `auth_permission` VALUES (82, '删除账户组', 21, 'delete_group');
INSERT INTO `auth_permission` VALUES (83, '查看账户组', 21, 'view_group');

INSERT INTO `auth_permission` VALUES (84, '添加权限', 22, 'add_permission');
INSERT INTO `auth_permission` VALUES (85, '编辑权限', 22, 'change_permission');
INSERT INTO `auth_permission` VALUES (86, '删除权限', 22, 'delete_permission');
INSERT INTO `auth_permission` VALUES (87, '查看权限', 22, 'view_permission');

INSERT INTO `auth_permission` VALUES (88, '添加账号', 23, 'add_user');
INSERT INTO `auth_permission` VALUES (89, '编辑账号', 23, 'change_user');
INSERT INTO `auth_permission` VALUES (90, '删除账号', 23, 'delete_user');
INSERT INTO `auth_permission` VALUES (91, '查看账号', 23, 'view_user');

INSERT INTO `auth_permission` VALUES (92, '编辑调度', 24, 'change_schedinfo');
INSERT INTO `auth_permission` VALUES (93, '查看调度', 24, 'view_schedinfo');

INSERT INTO `auth_permission` VALUES (94, '删除日志', 25, 'delete_sysloginfo');
INSERT INTO `auth_permission` VALUES (95, '查看日志', 25, 'view_sysloginfo');

COMMIT;

-- ----------------------------
-- Records of sca_common_config
-- ----------------------------
BEGIN;
INSERT INTO `sca_common_config` VALUES (1, 'http://127.0.0.1:8080', '{}', '2019-09-20 16:39:24.000000');
COMMIT;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
BEGIN;
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$150000$Vn0s7QktPTpX$H21Q7rFfbkBOjKdcrdt/G0A3XZuUUBB0AEY3bYk/8MM=', '2019-09-16 10:32:05.094651', 1, 'root', '', '', 'root@seecode.org', 1, 1, '2019-03-25 07:23:50.960702');
COMMIT;

-- ----------------------------
-- Records of sca_vuln_category
-- ----------------------------
BEGIN;
INSERT INTO `sca_vuln_category` VALUES (1, '本地文件包含', 'LFI', 'local file include', '2019-03-26 14:32:52.454839', 5);
INSERT INTO `sca_vuln_category` VALUES (2, '代码执行', 'RCE', 'remote code/command execute', '2019-03-27 09:41:15.000000', 5);
INSERT INTO `sca_vuln_category` VALUES (3, '跨站脚本', NULL, 'XSS', '2019-03-27 09:41:29.000000', 5);
INSERT INTO `sca_vuln_category` VALUES (4, '移动安全', NULL, NULL, '2019-06-21 01:09:10.429918', NULL);
INSERT INTO `sca_vuln_category` VALUES (5, 'Web安全', 'Web', NULL, '2019-06-21 01:09:18.955213', NULL);
INSERT INTO `sca_vuln_category` VALUES (9, '已知组件漏洞', '', 'Known Vulnerabilities', '2019-07-12 07:43:59.483799', NULL);
COMMIT;

-- ----------------------------
-- Records of django_celery_beat_crontabschedule
-- ----------------------------
BEGIN;
INSERT INTO `django_celery_beat_crontabschedule` VALUES (2, '0', '*/6', '*', '*', '*', 'Asia/Shanghai');
INSERT INTO `django_celery_beat_crontabschedule` VALUES (3, '*/1', '*', '*', '*', '*', 'Asia/Shanghai');
INSERT INTO `django_celery_beat_crontabschedule` VALUES (4, '*/10', '*', '*', '*', '*', 'Asia/Shanghai');
INSERT INTO `django_celery_beat_crontabschedule` VALUES (5, '0', '4', '*', '*', '*', 'Asia/Shanghai');
COMMIT;

-- ----------------------------
-- Records of django_celery_beat_periodictask
-- ----------------------------
BEGIN;
INSERT INTO `django_celery_beat_periodictask` VALUES (4, 'GitLab 项目同步服务', 'seecode.services.gitlab_sync.start', '[]', '{}', 'gitlab', NULL, NULL, NULL, 1, '2019-09-05 04:00:00.016596', 0, '2019-09-05 04:01:55.680815', ' ', 1, NULL, NULL, 0, NULL, NULL, '{}', NULL);

COMMIT;

-- ----------------------------
-- Records of sca_conf_language
-- ----------------------------
BEGIN;
INSERT INTO `sca_conf_language` VALUES (2, 'Java', '.java', 'java', '2019-03-30 16:34:17.797543');
INSERT INTO `sca_conf_language` VALUES (3, 'JavaScript', '.js', 'js', '2019-03-30 16:34:31.820691');
INSERT INTO `sca_conf_language` VALUES (4, 'C#', '.cs', 'cs', '2019-03-30 16:34:48.065087');
INSERT INTO `sca_conf_language` VALUES (5, 'Vuejs Component', '.vue', 'vue', '2019-03-30 16:35:00.058448');
INSERT INTO `sca_conf_language` VALUES (6, 'Python', '.py', 'py', '2019-03-30 16:35:10.813441');
INSERT INTO `sca_conf_language` VALUES (7, 'Freemarker Templ', NULL, 'freemarker-template', '2019-03-30 16:35:23.243209');
INSERT INTO `sca_conf_language` VALUES (8, 'C/C++ Header', '.h,.c,.cpp', 'c/c++', '2019-03-30 16:35:37.067373');
INSERT INTO `sca_conf_language` VALUES (9, 'Go', '.go', 'go', '2019-03-30 16:35:49.491326');
INSERT INTO `sca_conf_language` VALUES (10, 'TypeScript', NULL, 'ts', '2019-03-30 16:36:00.866308');
INSERT INTO `sca_conf_language` VALUES (11, 'Lua', '.lua', 'lua', '2019-03-30 16:36:10.737551');
INSERT INTO `sca_conf_language` VALUES (12, 'CSS', '.css,.less,.scss,.styl', 'css', '2019-03-30 16:36:21.702359');
INSERT INTO `sca_conf_language` VALUES (13, 'Dockerfile', NULL, 'dockerfile', '2019-03-30 16:36:33.391224');
INSERT INTO `sca_conf_language` VALUES (14, 'HTML', '.html,.htm,pthml', 'html', '2019-03-30 16:36:45.660964');
INSERT INTO `sca_conf_language` VALUES (15, 'Markdown', '.md', 'md', '2019-03-30 16:36:58.590530');
INSERT INTO `sca_conf_language` VALUES (16, 'YAML', '.yml', 'yaml', '2019-03-30 16:37:07.373914');
INSERT INTO `sca_conf_language` VALUES (17, 'JSX', NULL, 'jsx', '2019-03-30 16:37:18.384585');
INSERT INTO `sca_conf_language` VALUES (18, 'Objective C', '.m', 'objc', '2019-03-30 16:37:28.534165');
INSERT INTO `sca_conf_language` VALUES (19, 'XML', '.xml', 'xml', '2019-03-30 16:37:40.031281');
INSERT INTO `sca_conf_language` VALUES (20, 'Flex', NULL, 'flex', '2019-04-02 13:32:00.000000');
INSERT INTO `sca_conf_language` VALUES (21, 'Groovy', NULL, 'grvy', '2019-04-02 13:32:28.000000');
INSERT INTO `sca_conf_language` VALUES (22, 'PHP', '.php,.php3,.php4,.php5', 'php', '2019-04-02 13:33:14.000000');
INSERT INTO `sca_conf_language` VALUES (23, 'Web', NULL, 'web', '2019-04-02 13:34:36.000000');
INSERT INTO `sca_conf_language` VALUES (24, 'Scale', '.sbt,.scale', 'scale', '2019-05-23 18:13:57.000000');
INSERT INTO `sca_conf_language` VALUES (25, 'SHELL', '.sh', 'shell', '2019-05-23 18:14:22.000000');
INSERT INTO `sca_conf_language` VALUES (26, 'BAT', '.bat', 'bat', '2019-05-23 18:14:44.000000');
INSERT INTO `sca_conf_language` VALUES (27, 'SQL', '.sql', 'sql', '2019-05-23 18:15:44.000000');
INSERT INTO `sca_conf_language` VALUES (28, 'Kotlin', '.kt', 'kotlin', '2019-05-23 18:17:43.000000');
INSERT INTO `sca_conf_language` VALUES (29, 'Neutral', NULL, 'neutral', '2019-07-16 13:57:46.000000');
INSERT INTO `sca_conf_language` VALUES (30, 'Ruby', '.rb', 'ruby', '2019-07-16 13:58:34.000000');
INSERT INTO `sca_conf_language` VALUES (31, 'Swift', NULL, 'swift', '2019-07-16 13:59:31.000000');
INSERT INTO `sca_conf_language` VALUES (32, 'Scala', '.scala', 'scala', '2019-07-16 06:17:23.271212');
COMMIT;

-- ----------------------------
-- Records of sca_engine
-- ----------------------------
BEGIN;
INSERT INTO `sca_engine` VALUES (1, 'SonarScanner', 'seecode_scanner.lib.engines.sonarscanner', 1, NULL, 0,
'SonarQube扫描引擎', '{\'API_TOKEN\': \'TOKEN******************\', \'API_DOMAIN\': \'http://sonar7.seecode-audit.com\', \'SONAR_SCANNER_PATH\': \'/usr/bin/sonar-scanner\'}', 2.6, '2019-08-26 01:36:28.238513', '2019-04-09 19:01:00.000000', 0, 3362);
INSERT INTO `sca_engine` VALUES (2, 'RuleScanner', 'seecode_scanner.lib.engines.rulescanner', 1, NULL, 1, '自定义规则的扫描引擎', '{}', 1.5, '2019-08-07 08:57:54.156295', '2019-04-09 19:01:53.000000', 0, 5);
INSERT INTO `sca_engine` VALUES (3, 'PluginScanner', 'seecode_scanner.lib.engines.pluginscanner', 1, NULL, 1, '自定义插件的扫描引擎', '{}', 1.5, '2019-08-08 11:04:53.336821', '2019-04-09 19:02:47.000000', 1, 0);
COMMIT;

-- ----------------------------
-- Records of sca_scan_profile
-- ----------------------------
BEGIN;
INSERT INTO `sca_scan_profile` VALUES (1, 'default', '默认扫描模板，只包含规则引擎与插件引擎。', '.git/,bin/,node_modules/,assets/,static/', '.jpg,.jpeg,.png,.bmp,.gif,.ico,.cur,.eot,.otf,.svg,.ttf,.woff,.html,.htm,.css,.less,.scss,.styl,.min.js,.po,.mp3,.mp4,.swf,.exe,.sh,.dll,.so,.bat,.jar,.swp,.crt,.pdf,.doc,.docx,.csv,.md,.properties,.zip,.bak,.tar,.rar,.tar.gz,.rar,.7z,.iso,.db,.spf,.iml,.manifest,.psd,.as,.log,.template,.tpl', '', '', '{\'seecode_scanner.lib.engines.sonarscanner\': {\'ENGINE_TIMEOUT\': 1200, \'HTTP_TIMEOUT\': 10, \'HTTP_TIMEOUT_RETRY\': 3, \'HTTP_FAILED_RETRY\': 3, \'SONAR_PROJECT_PROPERTIES\': \'sonar.projectKey={{project_key}}\\nsonar.projectName={{project_name}}\\nsonar.projectVersion=1.0\\nsonar.sources=.\\nsonar.sourceEncoding=UTF-8\\nsonar.exclusions=**/node_modules/**/*.*,\\nsonar.host.url={{sonar_host}}\\nsonar.login={{sonar_login}}\\nsonar.java.binaries=.\'}, \'seecode_scanner.lib.engines.rulescanner\': {\'ENGINE_TIMEOUT\': 1200}, \'seecode_scanner.lib.engines.pluginscanner\': {\'ENGINE_TIMEOUT\': 1200}}', 0, 0, 0, '2019-03-27 11:01:49.843330', NULL, 1.0, '2019-08-15 06:36:48.138276', 0, 0, 7200);
INSERT INTO `sca_scan_profile` VALUES (6, 'normal', '包含所有扫描引擎的扫描策略。', '.git/,bin/,node_modules/,assets/,static/', '.jpg,.jpeg,.png,.bmp,.gif,.ico,.cur,.eot,.otf,.svg,.ttf,.woff,.html,.htm,.css,.less,.scss,.styl,.min.js,.po,.mp3,.mp4,.swf,.exe,.sh,.dll,.so,.bat,.jar,.swp,.crt,.pdf,.doc,.docx,.csv,.md,.properties,.zip,.bak,.tar,.rar,.tar.gz,.rar,.7z,.iso,.db,.spf,.iml,.manifest,.psd,.as,.log,.template,.tpl', '', '', '{\'seecode_scanner.lib.engines.sonarscanner\': {\'ENGINE_TIMEOUT\': \'1200\', \'HTTP_TIMEOUT\': \'10\', \'HTTP_TIMEOUT_RETRY\': \'3\', \'HTTP_FAILED_RETRY\': \'3\', \'SONAR_PROJECT_PROPERTIES\': \'sonar.projectKey={{project_key}}\\r\\nsonar.projectName={{project_name}}\\r\\nsonar.projectVersion=1.0\\r\\nsonar.sources=.\\r\\nsonar.sourceEncoding=UTF-8\\r\\nsonar.exclusions=**/node_modules/**/*.*,\\r\\nsonar.host.url={{sonar_host}}\\r\\nsonar.login={{sonar_login}}\\r\\nsonar.java.binaries=.\'}, \'seecode_scanner.lib.engines.rulescanner\': {\'ENGINE_TIMEOUT\': 1200}, \'seecode_scanner.lib.engines.pluginscanner\': {\'ENGINE_TIMEOUT\': 1200}}', 0, 0, 0, '2019-06-21 08:37:18.150207', NULL, 1.0, '2019-08-15 07:06:27.825014', 0, 0,
7200);
INSERT INTO `sca_scan_profile` VALUES (9, 'component_scan', '组件漏洞扫描模板，只基于规则引擎。', '.git/,bin/,node_modules/,assets/,static/', '.jpg,.jpeg,.png,.bmp,.gif,.ico,.cur,.eot,.otf,.svg,.ttf,.woff,.html,.htm,.css,.less,.scss,.styl,.min.js,.po,.mp3,.mp4,.swf,.exe,.sh,.dll,.so,.bat,.jar,.swp,.crt,.pdf,.doc,.docx,.csv,.md,.properties,.zip,.bak,.tar,.rar,.tar.gz,.rar,.7z,.iso,.db,.spf,.iml,.manifest,.psd,.as,.log,.template,.tpl', '', '', '{\'seecode_scanner.lib.engines.sonarscanner\': {\'ENGINE_TIMEOUT\': 1200, \'HTTP_TIMEOUT\': 10, \'HTTP_TIMEOUT_RETRY\': 3, \'HTTP_FAILED_RETRY\': 3, \'SONAR_PROJECT_PROPERTIES\': \'sonar.projectKey={{project_key}}\\nsonar.projectName={{project_name}}\\nsonar.projectVersion=1.0\\nsonar.sources=.\\nsonar.sourceEncoding=UTF-8\\nsonar.exclusions=**/node_modules/**/*.*,\\nsonar.host.url={{sonar_host}}\\nsonar.login={{sonar_login}}\\nsonar.java.binaries=.\'}, \'seecode_scanner.lib.engines.rulescanner\': {\'ENGINE_TIMEOUT\': 1200}, \'seecode_scanner.lib.engines.pluginscanner\': {\'ENGINE_TIMEOUT\': 1200}}', 0, 0, 0, '2019-06-26 07:41:15.968243', NULL, 1.0, '2019-08-26 09:04:49.477578', NULL, NULL, 7200);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
