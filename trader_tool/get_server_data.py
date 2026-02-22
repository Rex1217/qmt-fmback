import paramiko
class get_server_data:
    def __init__(self,hostname='120.78.132.143',port=22,username='root',password='LiXG135790'):
        '''
        hostname 服务器ip
        port端口
        username使用名称
        password密码
        '''
        self.hostname=hostname
        self.port=port
        self.username=username
        self.password=password
        self.client=''
    
    def connect(self):
        '''
        # 创建SSH客户端
        '''
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password,timeout=30)
        self.client=client
        return client

