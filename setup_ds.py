import read_config
import subprocess


class SetupDS(object):
    """
    Class setup DS with configuration values provided in globals.cfg
    """
    conf_file = 'globals.cfg'

    def __init__(self):
        self.obj_conf = read_config.ReadConfig(self.conf_file)
        self.conf_dict = self.obj_conf.get_param_in_section('DS')
        self.set_attributs()

    def set_attributs(self):
        self.hostname = self.conf_dict('HOST_NAME')
        self.user = self.conf_dict('D_USER')
        self.group = self.conf_dict('D_GROUP')
        self.ds_port = self.conf_dict('DS_PORT')
        self.as_port = self.conf_dict('AS_PORT')
        self.ip = self.conf_dict('IP')
        self.root_dn = "cn =" + self.conf_dict('DN')
        self.root_pwd = self.conf_dict('DNPWD')
        a = self.hostname.split('.')
        self.suffix = "dc = " + a[1] + ", dc =" + a[2]

    def set_setup_ds_commnad(self):
        self.setup_ds_cmd = ["setup-ds.pl --silent \\"]
        self.setup_ds_cmd.append("General.FullMachineName =" + self.hostname + " \\")
        self.setup_ds_cmd.append("General.SuiteSpotUserID =" + self.user + " \\")
        self.setup_ds_cmd.append("General.SuiteSpotUserID =" + self.user + " \\")
        self.setup_ds_cmd.append("General.SuiteSpotGroup =" + self.group + " \\")
        self.setup_ds_cmd.append("slapd.ServerPort =" + self.ds_port + " \\")
        self.setup_ds_cmd.append("slapd.ServerIdentifier = ca \\")
        self.setup_ds_cmd.append("slapd.Suffix =" + self.suffix +" \\")
        self.setup_ds_cmd.append(self.root_dn + " \\")
        self.setup_ds_cmd.append("slapd.RootDNPwd = " + self.root_pwd)

        print(self.setup_ds_cmd)
        
        self.ds_service_enable_cmd = "systemctl enable dirsrv.target"
        self.ds_service_start_cmd = "systemctl start dirsrv.target"

    def setup_ds(self):
        self.set_setup_ds_commnad()
        with open('logfile', "w") as outfile:
            subprocess.call(self.setup_ds_cmd, stdout=outfile)
            subprocess.call(self.ds_service_enable_cmd.split(' '), stdout=outfile)
            subprocess.call(self.ds_service_start_cmd.split(' '), stdout=outfile)
