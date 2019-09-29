
========================
依赖服务
========================


1. SonarQube
========================

* 使用 Docker 搭建

地址 https://github.com/chrismissonbrit/sonarqube，拉取镜像

.. code-block:: console

  $ docker pull chrismisson/sonarqube


创建容器，成功后访问 URL ``http://本机IP:9000``，默认账号： ``admin/admin``

.. code-block:: console

  $ docker run -d --name sonarqube -p 0.0.0.0:9000:9000 docker.io/chrismisson/sonarqube


-----


2. vsftpd
========================


2.1 安装
----------------


* **安装 vsftpd、db4：**

.. code-block:: console

  $ sudo yum install -y vsftpd db4


* **FTP服务模式**

  - PORT（主动）模式，模式模式只要开启服务器的 21 和 20 端口
  - PASV（被动）模式，模式需要开启服务器大于 1024 所有 tcp 端口和 21 端口。

PS: 这里我们使用 PASV 的模式


2.2 配置
----------------

* **目录规划**

  - FTP 存储位置：/data/vsftpd/
  - 日志文件：/var/log/xferlog
  - 配置文件：/etc/vsftpd/vsftpd.conf
  - 账号配置：/etc/vsftpd/virtusers

* **配置设置**

创建一个虚拟宿主用户：

.. code-block:: console
	
	$ useradd virtualhost -s /sbin/nologin

编辑 /etc/vsftpd/vsftpd.conf 文件：

.. code-block:: bash

	# 不允许匿名访问
	anonymous_enable=NO

	# 允许本地用户
	local_enable=YES
	write_enable=YES

	# 设置本地用户的文件掩码
	local_umask=022

	# 不允许匿名上传、写入
	anon_upload_enable=NO
	anon_mkdir_write_enable=NO

	# 日志文件
	xferlog_enable=YES
	xferlog_file=/var/log/xferlog
	xferlog_std_format=YES

	# 开启被动模式
	connect_from_port_20=NO
	pasv_enable=YES
	pasv_min_port=50000
	pasv_max_port=60000
	chown_uploads=YES

	#设定支持异步传输功能。
	async_abor_enable=YES
	ftpd_banner=Welcome to blah FTP service.
	chroot_local_user=NO
	chroot_list_enable=YES
	chroot_list_file=/etc/vsftpd/chroot_list
	ls_recurse_enable=NO
	listen=YES

	# 关于虚拟用户的重要配置
	pam_service_name=vsftpd
	userlist_enable=YES
	tcp_wrappers=YES
	guest_enable=YES
	guest_username=virtualhost
	virtual_use_local_privs=YES
	user_config_dir=/etc/vsftpd/virtualconf
	allow_writeable_chroot=YES

创建日志文件与账户目录：

.. code-block:: console
	
	$ touch /var/log/vsftpd.log
	$ chown virtualhost.virtualhost /var/log/vsftpd.log
	$ mkdir /etc/vsftpd/virtualconf

创建虚拟用户，内容格式为一行账号一行密码，如下：

.. code-block:: console
	
	$ vim /etc/vsftpd/virtusers
	seecode
	P@ssw0rd!

生成虚拟用户数据文件:

.. code-block:: console

	$ db_load -T -t hash -f /etc/vsftpd/virtusers /etc/vsftpd/virtusers.db

配置 vsftp 的 PAM 验证，非 64 位操作系统请使用 /lib/security/pam_userdb.so ：

.. code-block:: console

	$ vim /etc/pam.d/vsftpd
	auth    sufficient      /lib64/security/pam_userdb.so     db=/etc/vsftpd/virtusers
	account sufficient      /lib64/security/pam_userdb.so     db=/etc/vsftpd/virtusers

配置 FTP 用户:

.. code-block:: console

	$ mkdir /data/vsftpd/seecode/
	$ vim /etc/vsftpd/virtualconf/seecode

	local_root=/data/vsftpd/seecode
	anonymous_enable=NO
	write_enable=YES
	local_umask=022
	anon_upload_enable=NO
	anon_mkdir_write_enable=NO
	idle_session_timeout=3000
	data_connection_timeout=90
	max_clients=1000
	max_per_ip=100
	local_max_rate=25000

* **启动服务**

.. code-block:: console

	$ systemctl start vsftpd.service

