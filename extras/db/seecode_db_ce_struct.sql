/*
 Version: 1.0.0
 Author: MyKings
 Date: 18/09/2019 18:25:53
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for authtoken_token
-- ----------------------------
DROP TABLE IF EXISTS `authtoken_token`;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for django_celery_beat_clockedschedule
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_clockedschedule`;
CREATE TABLE `django_celery_beat_clockedschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clocked_time` datetime(6) NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for django_celery_beat_crontabschedule
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_crontabschedule`;
CREATE TABLE `django_celery_beat_crontabschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `minute` varchar(240) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hour` varchar(96) COLLATE utf8mb4_unicode_ci NOT NULL,
  `day_of_week` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `day_of_month` varchar(124) COLLATE utf8mb4_unicode_ci NOT NULL,
  `month_of_year` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `timezone` varchar(63) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for django_celery_beat_intervalschedule
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_intervalschedule`;
CREATE TABLE `django_celery_beat_intervalschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `every` int(11) NOT NULL,
  `period` varchar(24) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for django_celery_beat_periodictask
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_periodictask`;
CREATE TABLE `django_celery_beat_periodictask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `task` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `args` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `kwargs` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `queue` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `exchange` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `routing_key` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) DEFAULT NULL,
  `total_run_count` int(10) unsigned NOT NULL,
  `date_changed` datetime(6) NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `crontab_id` int(11) DEFAULT NULL,
  `interval_id` int(11) DEFAULT NULL,
  `solar_id` int(11) DEFAULT NULL,
  `one_off` tinyint(1) NOT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `priority` int(10) unsigned DEFAULT NULL,
  `headers` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `clocked_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` (`crontab_id`),
  KEY `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` (`interval_id`),
  KEY `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` (`solar_id`),
  KEY `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` (`clocked_id`),
  CONSTRAINT `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` FOREIGN KEY (`clocked_id`) REFERENCES `django_celery_beat_clockedschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` FOREIGN KEY (`crontab_id`) REFERENCES `django_celery_beat_crontabschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` FOREIGN KEY (`interval_id`) REFERENCES `django_celery_beat_intervalschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` FOREIGN KEY (`solar_id`) REFERENCES `django_celery_beat_solarschedule` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for django_celery_beat_periodictasks
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_periodictasks`;
CREATE TABLE `django_celery_beat_periodictasks` (
  `ident` smallint(6) NOT NULL,
  `last_update` datetime(6) NOT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for django_celery_beat_solarschedule
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_solarschedule`;
CREATE TABLE `django_celery_beat_solarschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event` varchar(24) COLLATE utf8mb4_unicode_ci NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq` (`event`,`latitude`,`longitude`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for r_app_group
-- ----------------------------
DROP TABLE IF EXISTS `r_app_group`;
CREATE TABLE `r_app_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskgroupinfo_id` int(11) NOT NULL,
  `applicationinfo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `r_app_group_taskgroupinfo_id_applicationinfo_id_44977d21_uniq` (`taskgroupinfo_id`,`applicationinfo_id`),
  KEY `r_app_group_applicationinfo_id_0ab27674_fk_sca_application_id` (`applicationinfo_id`),
  CONSTRAINT `r_app_group_applicationinfo_id_0ab27674_fk_sca_application_id` FOREIGN KEY (`applicationinfo_id`) REFERENCES `sca_application` (`id`),
  CONSTRAINT `r_app_group_taskgroupinfo_id_5fab0109_fk_sca_scan_task_group_id` FOREIGN KEY (`taskgroupinfo_id`) REFERENCES `sca_scan_task_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for r_group_member
-- ----------------------------
DROP TABLE IF EXISTS `r_group_member`;
CREATE TABLE `r_group_member` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `groupinfo_id` int(11) NOT NULL,
  `memberinfo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `r_group_member_groupinfo_id_memberinfo_id_69779b85_uniq` (`groupinfo_id`,`memberinfo_id`),
  KEY `r_group_member_memberinfo_id_69426101_fk_sca_gitlab_member_id` (`memberinfo_id`),
  CONSTRAINT `r_group_member_groupinfo_id_a8f71611_fk_sca_gitlab_group_id` FOREIGN KEY (`groupinfo_id`) REFERENCES `sca_gitlab_group` (`id`),
  CONSTRAINT `r_group_member_memberinfo_id_69426101_fk_sca_gitlab_member_id` FOREIGN KEY (`memberinfo_id`) REFERENCES `sca_gitlab_member` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for r_profile_engine
-- ----------------------------
DROP TABLE IF EXISTS `r_profile_engine`;
CREATE TABLE `r_profile_engine` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `scanprofileinfo_id` int(11) NOT NULL,
  `engineinfo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `r_profile_engine_scanprofileinfo_id_engineinfo_id_5a93b954_uniq` (`scanprofileinfo_id`,`engineinfo_id`),
  KEY `r_profile_engine_engineinfo_id_c2be478e_fk_sca_engine_id` (`engineinfo_id`),
  CONSTRAINT `r_profile_engine_engineinfo_id_c2be478e_fk_sca_engine_id` FOREIGN KEY (`engineinfo_id`) REFERENCES `sca_engine` (`id`),
  CONSTRAINT `r_profile_engine_scanprofileinfo_id_b7865664_fk_sca_scan_` FOREIGN KEY (`scanprofileinfo_id`) REFERENCES `sca_scan_profile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for r_profile_tactic
-- ----------------------------
DROP TABLE IF EXISTS `r_profile_tactic`;
CREATE TABLE `r_profile_tactic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `scanprofileinfo_id` int(11) NOT NULL,
  `tacticinfo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `r_profile_tactic_scanprofileinfo_id_tacticinfo_id_8d7e05c7_uniq` (`scanprofileinfo_id`,`tacticinfo_id`),
  KEY `r_profile_tactic_tacticinfo_id_8ecbb767_fk_sca_tactic_id` (`tacticinfo_id`),
  CONSTRAINT `r_profile_tactic_scanprofileinfo_id_37becfec_fk_sca_scan_` FOREIGN KEY (`scanprofileinfo_id`) REFERENCES `sca_scan_profile` (`id`),
  CONSTRAINT `r_profile_tactic_tacticinfo_id_8ecbb767_fk_sca_tactic_id` FOREIGN KEY (`tacticinfo_id`) REFERENCES `sca_tactic` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for r_project_member
-- ----------------------------
DROP TABLE IF EXISTS `r_project_member`;
CREATE TABLE `r_project_member` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `projectinfo_id` int(11) NOT NULL,
  `memberinfo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `r_project_member_projectinfo_id_memberinfo_id_b296a164_uniq` (`projectinfo_id`,`memberinfo_id`),
  KEY `r_project_member_memberinfo_id_b9fc0455_fk_sca_gitlab_member_id` (`memberinfo_id`),
  CONSTRAINT `r_project_member_memberinfo_id_b9fc0455_fk_sca_gitlab_member_id` FOREIGN KEY (`memberinfo_id`) REFERENCES `sca_gitlab_member` (`id`),
  CONSTRAINT `r_project_member_projectinfo_id_a567d78e_fk_sca_gitla` FOREIGN KEY (`projectinfo_id`) REFERENCES `sca_gitlab_project` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for r_tactic_tag
-- ----------------------------
DROP TABLE IF EXISTS `r_tactic_tag`;
CREATE TABLE `r_tactic_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tacticinfo_id` int(11) NOT NULL,
  `taginfo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `r_tactic_tag_tacticinfo_id_taginfo_id_6f5b1cba_uniq` (`tacticinfo_id`,`taginfo_id`),
  KEY `r_tactic_tag_taginfo_id_da0f5aaf_fk_sca_common_tag_id` (`taginfo_id`),
  CONSTRAINT `r_tactic_tag_tacticinfo_id_013a9eac_fk_sca_tactic_id` FOREIGN KEY (`tacticinfo_id`) REFERENCES `sca_tactic` (`id`),
  CONSTRAINT `r_tactic_tag_taginfo_id_da0f5aaf_fk_sca_common_tag_id` FOREIGN KEY (`taginfo_id`) REFERENCES `sca_common_tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for r_vuln_tag
-- ----------------------------
DROP TABLE IF EXISTS `r_vuln_tag`;
CREATE TABLE `r_vuln_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vulninfo_id` int(11) NOT NULL,
  `taginfo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `r_vuln_tag_vulninfo_id_taginfo_id_7c5790ba_uniq` (`vulninfo_id`,`taginfo_id`),
  KEY `r_vuln_tag_taginfo_id_545e0c7a_fk_sca_common_tag_id` (`taginfo_id`),
  CONSTRAINT `r_vuln_tag_taginfo_id_545e0c7a_fk_sca_common_tag_id` FOREIGN KEY (`taginfo_id`) REFERENCES `sca_common_tag` (`id`),
  CONSTRAINT `r_vuln_tag_vulninfo_id_300ff9a5_fk_sca_vuln_info_id` FOREIGN KEY (`vulninfo_id`) REFERENCES `sca_vuln_info` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_application
-- ----------------------------
DROP TABLE IF EXISTS `sca_application`;
CREATE TABLE `sca_application` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `module_name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `app_name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `version` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `code_total` int(11) NOT NULL,
  `size` int(11) DEFAULT NULL,
  `report_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ignore_count` int(11) NOT NULL,
  `critical` int(11) NOT NULL,
  `high` int(11) NOT NULL,
  `medium` int(11) NOT NULL,
  `low` int(11) NOT NULL,
  `info` int(11) NOT NULL,
  `risk_scope` double NOT NULL,
  `status` smallint(6) NOT NULL,
  `is_archive` tinyint(1) NOT NULL,
  `last_scan_time` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `lang_id` int(11) DEFAULT NULL,
  `project_id` int(11) NOT NULL,
  `repo_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sca_application_module_name_ad2d5707_uniq` (`module_name`),
  KEY `sca_application_lang_id_67c3c297_fk_sca_conf_language_id` (`lang_id`),
  KEY `sca_application_project_id_20ffa1a9_fk_sca_gitlab_project_id` (`project_id`),
  KEY `sca_application_repo_id_836fc36e_fk_sca_gitlab_repository_id` (`repo_id`),
  CONSTRAINT `sca_application_lang_id_67c3c297_fk_sca_conf_language_id` FOREIGN KEY (`lang_id`) REFERENCES `sca_conf_language` (`id`),
  CONSTRAINT `sca_application_project_id_20ffa1a9_fk_sca_gitlab_project_id` FOREIGN KEY (`project_id`) REFERENCES `sca_gitlab_project` (`id`),
  CONSTRAINT `sca_application_repo_id_836fc36e_fk_sca_gitlab_repository_id` FOREIGN KEY (`repo_id`) REFERENCES `sca_gitlab_repository` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_application_dependent
-- ----------------------------
DROP TABLE IF EXISTS `sca_application_dependent`;
CREATE TABLE `sca_application_dependent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `file_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `full_path` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `group_id` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `artifact_id` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `version` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `new_version` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_archive` tinyint(1) NOT NULL,
  `language` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `app_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_application_dependent_app_id_cd050cbb_fk_sca_application_id` (`app_id`),
  CONSTRAINT `sca_application_dependent_app_id_cd050cbb_fk_sca_application_id` FOREIGN KEY (`app_id`) REFERENCES `sca_application` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_application_statistics
-- ----------------------------
DROP TABLE IF EXISTS `sca_application_statistics`;
CREATE TABLE `sca_application_statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `language` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `files` int(11) DEFAULT NULL,
  `blank` int(11) DEFAULT NULL,
  `comment` int(11) DEFAULT NULL,
  `code` int(11) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `app_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_application_statistics_app_id_b4d5b463_fk_sca_application_id` (`app_id`),
  CONSTRAINT `sca_application_statistics_app_id_b4d5b463_fk_sca_application_id` FOREIGN KEY (`app_id`) REFERENCES `sca_application` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_common_config
-- ----------------------------
DROP TABLE IF EXISTS `sca_common_config`;
CREATE TABLE `sca_common_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `site` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_common_sched
-- ----------------------------
DROP TABLE IF EXISTS `sca_common_sched`;
CREATE TABLE `sca_common_sched` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` smallint(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `crontab_id` int(11) DEFAULT NULL,
  `interval_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_common_sched_crontab_id_e7bf56e0_fk_django_ce` (`crontab_id`),
  KEY `sca_common_sched_interval_id_33bccb45_fk_django_ce` (`interval_id`),
  CONSTRAINT `sca_common_sched_crontab_id_e7bf56e0_fk_django_ce` FOREIGN KEY (`crontab_id`) REFERENCES `django_celery_beat_crontabschedule` (`id`),
  CONSTRAINT `sca_common_sched_interval_id_33bccb45_fk_django_ce` FOREIGN KEY (`interval_id`) REFERENCES `django_celery_beat_intervalschedule` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_common_syslog
-- ----------------------------
DROP TABLE IF EXISTS `sca_common_syslog`;
CREATE TABLE `sca_common_syslog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `stack_trace` longtext COLLATE utf8mb4_unicode_ci,
  `object_id` int(11) DEFAULT NULL,
  `ipv4` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` smallint(6) NOT NULL,
  `level` smallint(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `module_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_common_syslog_module_id_07524ba6_fk_django_content_type_id` (`module_id`),
  CONSTRAINT `sca_common_syslog_module_id_07524ba6_fk_django_content_type_id` FOREIGN KEY (`module_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_common_tag
-- ----------------------------
DROP TABLE IF EXISTS `sca_common_tag`;
CREATE TABLE `sca_common_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_common_tag_parent_id_31bc1752_fk_sca_common_tag_id` (`parent_id`),
  CONSTRAINT `sca_common_tag_parent_id_31bc1752_fk_sca_common_tag_id` FOREIGN KEY (`parent_id`) REFERENCES `sca_common_tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_conf_language
-- ----------------------------
DROP TABLE IF EXISTS `sca_conf_language`;
CREATE TABLE `sca_conf_language` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `suffix` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `key` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_engine
-- ----------------------------
DROP TABLE IF EXISTS `sca_engine`;
CREATE TABLE `sca_engine` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `module_name` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `enable` tinyint(1) NOT NULL,
  `url` longtext COLLATE utf8mb4_unicode_ci,
  `is_customize` tinyint(1) NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `whitelist_count` int(11) NOT NULL,
  `blacklist_count` int(11) NOT NULL,
  `config` longtext COLLATE utf8mb4_unicode_ci,
  `revision` double NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_gitlab_group
-- ----------------------------
DROP TABLE IF EXISTS `sca_gitlab_group`;
CREATE TABLE `sca_gitlab_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `git_id` int(11) DEFAULT NULL,
  `name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `path` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `web_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `full_name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `full_path` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `visibility_level` int(11) NOT NULL,
  `type` smallint(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `department_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_gitlab_group_department_id_076bbe2b_fk_sca_common_dept_id` (`department_id`),
  KEY `sca_gitlab_group_user_id_8a54961e_fk_auth_user_id` (`user_id`),
  CONSTRAINT `sca_gitlab_group_department_id_076bbe2b_fk_sca_common_dept_id` FOREIGN KEY (`department_id`) REFERENCES `sca_common_dept` (`id`),
  CONSTRAINT `sca_gitlab_group_user_id_8a54961e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_gitlab_group_member_permission
-- ----------------------------
DROP TABLE IF EXISTS `sca_gitlab_group_member_permission`;
CREATE TABLE `sca_gitlab_group_member_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `access_level` int(11) DEFAULT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `group_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_gitlab_group_mem_group_id_cd8451c2_fk_sca_gitla` (`group_id`),
  KEY `sca_gitlab_group_mem_member_id_7e2611f1_fk_sca_gitla` (`member_id`),
  CONSTRAINT `sca_gitlab_group_mem_group_id_cd8451c2_fk_sca_gitla` FOREIGN KEY (`group_id`) REFERENCES `sca_gitlab_group` (`id`),
  CONSTRAINT `sca_gitlab_group_mem_member_id_7e2611f1_fk_sca_gitla` FOREIGN KEY (`member_id`) REFERENCES `sca_gitlab_member` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_gitlab_member
-- ----------------------------
DROP TABLE IF EXISTS `sca_gitlab_member`;
CREATE TABLE `sca_gitlab_member` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `git_id` int(11) NOT NULL,
  `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `state` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `web_url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gitlab_created_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `employee_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `git_id` (`git_id`),
  KEY `sca_gitlab_member_employee_id_d44cd9fc_fk_sca_common_employee_id` (`employee_id`),
  CONSTRAINT `sca_gitlab_member_employee_id_d44cd9fc_fk_sca_common_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `sca_common_employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_gitlab_project
-- ----------------------------
DROP TABLE IF EXISTS `sca_gitlab_project`;
CREATE TABLE `sca_gitlab_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `git_id` int(11) DEFAULT NULL,
  `git_created_at` datetime(6) DEFAULT NULL,
  `git_last_activity_at` datetime(6) DEFAULT NULL,
  `ssh_url_to_repo` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `http_url_to_repo` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `web_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `default_branch` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `path` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `file_hash` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `file_size` int(11) DEFAULT NULL,
  `file_origin_name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `path_with_namespace` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `creator_id` int(11) DEFAULT NULL,
  `description` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `star_count` int(11) NOT NULL,
  `forks_count` int(11) NOT NULL,
  `open_issues_count` int(11) NOT NULL,
  `visibility_level` int(11) NOT NULL,
  `issues_enabled` tinyint(1) NOT NULL,
  `type` smallint(6) NOT NULL,
  `is_new` tinyint(1) NOT NULL,
  `is_archive` tinyint(1) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `group_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_gitlab_project_group_id_d921b318_fk_sca_gitlab_group_id` (`group_id`),
  KEY `sca_gitlab_project_user_id_39ed1042_fk_auth_user_id` (`user_id`),
  CONSTRAINT `sca_gitlab_project_group_id_d921b318_fk_sca_gitlab_group_id` FOREIGN KEY (`group_id`) REFERENCES `sca_gitlab_group` (`id`),
  CONSTRAINT `sca_gitlab_project_user_id_39ed1042_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_gitlab_project_history
-- ----------------------------
DROP TABLE IF EXISTS `sca_gitlab_project_history`;
CREATE TABLE `sca_gitlab_project_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` smallint(6) NOT NULL,
  `title` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_first` tinyint(1) NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `project_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_gitlab_project_h_project_id_896ef092_fk_sca_gitla` (`project_id`),
  KEY `sca_gitlab_project_history_user_id_279f8fdd_fk_auth_user_id` (`user_id`),
  CONSTRAINT `sca_gitlab_project_h_project_id_896ef092_fk_sca_gitla` FOREIGN KEY (`project_id`) REFERENCES `sca_gitlab_project` (`id`),
  CONSTRAINT `sca_gitlab_project_history_user_id_279f8fdd_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_gitlab_project_member_permission
-- ----------------------------
DROP TABLE IF EXISTS `sca_gitlab_project_member_permission`;
CREATE TABLE `sca_gitlab_project_member_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `access_level` int(11) DEFAULT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `member_id` int(11) NOT NULL,
  `project_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_gitlab_project_m_member_id_68f44647_fk_sca_gitla` (`member_id`),
  KEY `sca_gitlab_project_m_project_id_454f5ba5_fk_sca_gitla` (`project_id`),
  CONSTRAINT `sca_gitlab_project_m_member_id_68f44647_fk_sca_gitla` FOREIGN KEY (`member_id`) REFERENCES `sca_gitlab_member` (`id`),
  CONSTRAINT `sca_gitlab_project_m_project_id_454f5ba5_fk_sca_gitla` FOREIGN KEY (`project_id`) REFERENCES `sca_gitlab_project` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_gitlab_repository
-- ----------------------------
DROP TABLE IF EXISTS `sca_gitlab_repository`;
CREATE TABLE `sca_gitlab_repository` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `merged` tinyint(1) NOT NULL,
  `protected` tinyint(1) NOT NULL,
  `developers_can_push` tinyint(1) NOT NULL,
  `developers_can_merge` tinyint(1) NOT NULL,
  `last_commit_id` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_short_id` varchar(8) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_author_email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_author_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `committed_date` datetime(6) DEFAULT NULL,
  `type` smallint(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `project_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_gitlab_repositor_project_id_dd1bc197_fk_sca_gitla` (`project_id`),
  CONSTRAINT `sca_gitlab_repositor_project_id_dd1bc197_fk_sca_gitla` FOREIGN KEY (`project_id`) REFERENCES `sca_gitlab_project` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_issue
-- ----------------------------
DROP TABLE IF EXISTS `sca_issue`;
CREATE TABLE `sca_issue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `file_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `report_detail_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_commit_author` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_commit_author_email` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_commit` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `risk_scope` double NOT NULL,
  `start_line` int(11) NOT NULL,
  `end_line` int(11) NOT NULL,
  `code_segment` longtext COLLATE utf8mb4_unicode_ci,
  `evidence_content` longtext COLLATE utf8mb4_unicode_ci,
  `is_false_positive` tinyint(1) NOT NULL,
  `whitelist_rule_id` int(11) DEFAULT NULL,
  `is_whitelist` tinyint(1) NOT NULL,
  `status` smallint(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `app_id` int(11) NOT NULL,
  `tactic_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sca_issue_app_id_tactic_id_file_name_start_line_71a67cc0_uniq` (`app_id`,`tactic_id`,`file_name`,`start_line`),
  KEY `sca_issue_tactic_id_484ba42a_fk_sca_tactic_id` (`tactic_id`),
  CONSTRAINT `sca_issue_app_id_687f15e0_fk_sca_application_id` FOREIGN KEY (`app_id`) REFERENCES `sca_application` (`id`),
  CONSTRAINT `sca_issue_tactic_id_484ba42a_fk_sca_tactic_id` FOREIGN KEY (`tactic_id`) REFERENCES `sca_tactic` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_issue_flow
-- ----------------------------
DROP TABLE IF EXISTS `sca_issue_flow`;
CREATE TABLE `sca_issue_flow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `behavior` smallint(6) NOT NULL,
  `status` smallint(6) NOT NULL,
  `url` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comment` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `issue_id` int(11) NOT NULL,
  `member_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_issue_flow_issue_id_27b4a97c_fk_sca_issue_id` (`issue_id`),
  KEY `sca_issue_flow_member_id_baaea706_fk_sca_gitlab_member_id` (`member_id`),
  KEY `sca_issue_flow_user_id_0d4f927c_fk_auth_user_id` (`user_id`),
  CONSTRAINT `sca_issue_flow_issue_id_27b4a97c_fk_sca_issue_id` FOREIGN KEY (`issue_id`) REFERENCES `sca_issue` (`id`),
  CONSTRAINT `sca_issue_flow_member_id_baaea706_fk_sca_gitlab_member_id` FOREIGN KEY (`member_id`) REFERENCES `sca_gitlab_member` (`id`),
  CONSTRAINT `sca_issue_flow_user_id_0d4f927c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_issue_whitelist
-- ----------------------------
DROP TABLE IF EXISTS `sca_issue_whitelist`;
CREATE TABLE `sca_issue_whitelist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `issue_id` int(11) NOT NULL,
  `operator_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_issue_whitelist_issue_id_550070e5_fk_sca_issue_id` (`issue_id`),
  KEY `sca_issue_whitelist_operator_id_dd2b5784_fk_auth_user_id` (`operator_id`),
  CONSTRAINT `sca_issue_whitelist_issue_id_550070e5_fk_sca_issue_id` FOREIGN KEY (`issue_id`) REFERENCES `sca_issue` (`id`),
  CONSTRAINT `sca_issue_whitelist_operator_id_dd2b5784_fk_auth_user_id` FOREIGN KEY (`operator_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_node_host
-- ----------------------------
DROP TABLE IF EXISTS `sca_node_host`;
CREATE TABLE `sca_node_host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_role_ui` tinyint(1) NOT NULL,
  `is_role_client` tinyint(1) NOT NULL,
  `hostname` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ipv4` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ipv6` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ui_version` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `client_version` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_node_host_service
-- ----------------------------
DROP TABLE IF EXISTS `sca_node_host_service`;
CREATE TABLE `sca_node_host_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ppid` int(11) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  `status` smallint(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `host_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_node_host_service_host_id_0b1be4b0_fk_sca_node_host_id` (`host_id`),
  KEY `sca_node_host_service_service_id_b5d03ccd_fk_sca_node_service_id` (`service_id`),
  CONSTRAINT `sca_node_host_service_host_id_0b1be4b0_fk_sca_node_host_id` FOREIGN KEY (`host_id`) REFERENCES `sca_node_host` (`id`),
  CONSTRAINT `sca_node_host_service_service_id_b5d03ccd_fk_sca_node_service_id` FOREIGN KEY (`service_id`) REFERENCES `sca_node_service` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_node_service
-- ----------------------------
DROP TABLE IF EXISTS `sca_node_service`;
CREATE TABLE `sca_node_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `key` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` smallint(6) NOT NULL,
  `process_keyword` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_scan_profile
-- ----------------------------
DROP TABLE IF EXISTS `sca_scan_profile`;
CREATE TABLE `sca_scan_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `exclude_dir` longtext COLLATE utf8mb4_unicode_ci,
  `exclude_ext` longtext COLLATE utf8mb4_unicode_ci,
  `exclude_file` longtext COLLATE utf8mb4_unicode_ci,
  `exclude_java_package` longtext COLLATE utf8mb4_unicode_ci,
  `config` longtext COLLATE utf8mb4_unicode_ci,
  `enable_commit_issue` tinyint(1) NOT NULL,
  `enable_auto_ignore` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `task_timeout` int(11) NOT NULL,
  `revision` double NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `host_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_scan_profile_host_id_00a805ef_fk_sca_node_host_id` (`host_id`),
  CONSTRAINT `sca_scan_profile_host_id_00a805ef_fk_sca_node_host_id` FOREIGN KEY (`host_id`) REFERENCES `sca_node_host` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_scan_task
-- ----------------------------
DROP TABLE IF EXISTS `sca_scan_task`;
CREATE TABLE `sca_scan_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `executor_ip` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `end_time` datetime(6) DEFAULT NULL,
  `status` smallint(6) NOT NULL,
  `scan_way` smallint(6) NOT NULL,
  `log_file` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `error_title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `error_reason` longtext COLLATE utf8mb4_unicode_ci,
  `config` longtext COLLATE utf8mb4_unicode_ci,
  `hash` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_force_scan` tinyint(1) NOT NULL,
  `version` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `template_name` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `template_version` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `critical` int(11) NOT NULL,
  `high` int(11) NOT NULL,
  `medium` int(11) NOT NULL,
  `low` int(11) NOT NULL,
  `info` int(11) NOT NULL,
  `dir_result_path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `file_result_path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `engines_result` longtext COLLATE utf8mb4_unicode_ci,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `app_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_scan_task_app_id_7e44f5df_fk_sca_application_id` (`app_id`),
  KEY `sca_scan_task_group_id_87a0791c_fk_sca_scan_task_group_id` (`group_id`),
  CONSTRAINT `sca_scan_task_app_id_7e44f5df_fk_sca_application_id` FOREIGN KEY (`app_id`) REFERENCES `sca_application` (`id`),
  CONSTRAINT `sca_scan_task_group_id_87a0791c_fk_sca_scan_task_group_id` FOREIGN KEY (`group_id`) REFERENCES `sca_scan_task_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_scan_task_group
-- ----------------------------
DROP TABLE IF EXISTS `sca_scan_task_group`;
CREATE TABLE `sca_scan_task_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `branch` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `args` longtext COLLATE utf8mb4_unicode_ci,
  `is_default` tinyint(1) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `periodic_id` int(11) DEFAULT NULL,
  `profile_id` int(11) NOT NULL,
  `sched_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_scan_task_group_periodic_id_0d6d0299_fk_django_ce` (`periodic_id`),
  KEY `sca_scan_task_group_profile_id_5b2f1505_fk_sca_scan_profile_id` (`profile_id`),
  KEY `sca_scan_task_group_sched_id_7b3a0195_fk_sca_common_sched_id` (`sched_id`),
  CONSTRAINT `sca_scan_task_group_periodic_id_0d6d0299_fk_django_ce` FOREIGN KEY (`periodic_id`) REFERENCES `django_celery_beat_periodictask` (`id`),
  CONSTRAINT `sca_scan_task_group_profile_id_5b2f1505_fk_sca_scan_profile_id` FOREIGN KEY (`profile_id`) REFERENCES `sca_scan_profile` (`id`),
  CONSTRAINT `sca_scan_task_group_sched_id_7b3a0195_fk_sca_common_sched_id` FOREIGN KEY (`sched_id`) REFERENCES `sca_common_sched` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_scan_task_history
-- ----------------------------
DROP TABLE IF EXISTS `sca_scan_task_history`;
CREATE TABLE `sca_scan_task_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` smallint(6) NOT NULL,
  `level` smallint(6) NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `task_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_scan_task_history_task_id_627f6560_fk_sca_scan_task_id` (`task_id`),
  CONSTRAINT `sca_scan_task_history_task_id_627f6560_fk_sca_scan_task_id` FOREIGN KEY (`task_id`) REFERENCES `sca_scan_task` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_tactic
-- ----------------------------
DROP TABLE IF EXISTS `sca_tactic`;
CREATE TABLE `sca_tactic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `revision` double NOT NULL,
  `key` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `solution` longtext COLLATE utf8mb4_unicode_ci,
  `type` smallint(6) NOT NULL,
  `risk` smallint(6) NOT NULL,
  `risk_scope` double NOT NULL,
  `nature_type` smallint(6) NOT NULL,
  `attribution_type` smallint(6) NOT NULL,
  `rule_match_type` smallint(6) NOT NULL,
  `rule_value` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rule_regex` longtext COLLATE utf8mb4_unicode_ci,
  `component_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rule_regex_flag` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `plugin_name` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `plugin_module_name` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `plugin_content` longtext COLLATE utf8mb4_unicode_ci,
  `scm_conf` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `alarm_conf` longtext COLLATE utf8mb4_unicode_ci,
  `alarm_title` longtext COLLATE utf8mb4_unicode_ci,
  `is_active` tinyint(1) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `engine_id` int(11) NOT NULL,
  `lang_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `vuln_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `sca_tactic_engine_id_5836bfc1_fk_sca_engine_id` (`engine_id`),
  KEY `sca_tactic_lang_id_f10eab1a_fk_sca_conf_language_id` (`lang_id`),
  KEY `sca_tactic_user_id_556d5518_fk_auth_user_id` (`user_id`),
  KEY `sca_tactic_vuln_id_abd3d1a9_fk_sca_vuln_info_id` (`vuln_id`),
  CONSTRAINT `sca_tactic_engine_id_5836bfc1_fk_sca_engine_id` FOREIGN KEY (`engine_id`) REFERENCES `sca_engine` (`id`),
  CONSTRAINT `sca_tactic_lang_id_f10eab1a_fk_sca_conf_language_id` FOREIGN KEY (`lang_id`) REFERENCES `sca_conf_language` (`id`),
  CONSTRAINT `sca_tactic_user_id_556d5518_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `sca_tactic_vuln_id_abd3d1a9_fk_sca_vuln_info_id` FOREIGN KEY (`vuln_id`) REFERENCES `sca_vuln_info` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_upgrade_changelog
-- ----------------------------
DROP TABLE IF EXISTS `sca_upgrade_changelog`;
CREATE TABLE `sca_upgrade_changelog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_archive` tinyint(1) NOT NULL,
  `action` smallint(6) NOT NULL,
  `module` smallint(6) NOT NULL,
  `version` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_upgrade_package
-- ----------------------------
DROP TABLE IF EXISTS `sca_upgrade_package`;
CREATE TABLE `sca_upgrade_package` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `version` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `changelog` longtext COLLATE utf8mb4_unicode_ci,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_archive` tinyint(1) NOT NULL,
  `role` smallint(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_upgrade_version
-- ----------------------------
DROP TABLE IF EXISTS `sca_upgrade_version`;
CREATE TABLE `sca_upgrade_version` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `major` int(11) NOT NULL,
  `minor` int(11) NOT NULL,
  `revision` int(11) NOT NULL,
  `role` smallint(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_vuln_category
-- ----------------------------
DROP TABLE IF EXISTS `sca_vuln_category`;
CREATE TABLE `sca_vuln_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tag` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `key` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_vuln_category_parent_id_141656a6_fk_sca_vuln_category_id` (`parent_id`),
  CONSTRAINT `sca_vuln_category_parent_id_141656a6_fk_sca_vuln_category_id` FOREIGN KEY (`parent_id`) REFERENCES `sca_vuln_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for sca_vuln_info
-- ----------------------------
DROP TABLE IF EXISTS `sca_vuln_info`;
CREATE TABLE `sca_vuln_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `solution` longtext COLLATE utf8mb4_unicode_ci,
  `reference` longtext COLLATE utf8mb4_unicode_ci,
  `risk` smallint(6) NOT NULL,
  `hit` int(11) NOT NULL,
  `impact_version` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cnnvd` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cnvd` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cve` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bugtraq` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `find_time` date DEFAULT NULL,
  `update_time` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `cate_id` int(11) NOT NULL,
  `origin_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sca_vuln_info_cate_id_abc060f7_fk_sca_vuln_category_id` (`cate_id`),
  KEY `sca_vuln_info_origin_id_62c91521_fk_sca_common_tag_id` (`origin_id`),
  CONSTRAINT `sca_vuln_info_cate_id_abc060f7_fk_sca_vuln_category_id` FOREIGN KEY (`cate_id`) REFERENCES `sca_vuln_category` (`id`),
  CONSTRAINT `sca_vuln_info_origin_id_62c91521_fk_sca_common_tag_id` FOREIGN KEY (`origin_id`) REFERENCES `sca_common_tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
