import read_config
import subprocess
import pexpect


class SetupCA(object):
    """
    Class provides utility to setup root CA and other CA services (sign / verify cert)

    """
    conf_file = 'globals.cfg'

    def __init__(self):
        self.obj_conf = read_config.ReadConfig(self.conf_file)
        self.conf_dict = self.obj_conf.get_param_in_section('CA')
        self.set_attributs()

    def set_attributs(self):
        self.ca_database = self.conf_dict('CA_DATABASE_REPO')
        self.hostname = self.conf_dict('HOST_NAME')
        self.cert_key_type = self.conf_dict('CERT_KEY_TYPE')
        self.cert_key_len = self.conf_dict('CERT_KEY_LEN')
        self.cert_mac_algo = self.conf_dict('CERT_MAC_ALGO')
        self.cert_name = self.conf_dict('CERTNAME')
        self.ca_profile = self.conf_dict('CA_PROFILE')
        self.ds_password = self.conf_dict('DS_PASSWORD')
        self.req_id = 0
        self.seed = self.conf_dict('SEED')

    def set_setup_ca_commnad(self):
        self.setup_ca_cmd = "pkispawn -v -f ca.cfg -s CA"
        self.ca_service_enable_cmd = "systemctl status pki-tomcatd@pki-tomcat.service"
        self.ca_service_start_cmd = "systemctl start pki-tomcatd@pki-tomcat.service"
        self.ca_csr_gen_cmd = "certutil -R  -d" + self.ca_database + \
                        " -c " + self.ds_password + " -k " + self.cert_key_type + \
                        " -g " + self.cert_key_len + " -Z " + self.cert_mac_algo + \
                        " -s " + "\"CN=" + self.hostname +",O=EXAMPLE\" --keyUsage critical," \
                                                          "dataEncipherment,keyEncipherment," \
                                                          "digitalSignature  --extKeyUsage " \
                                                          "serverAuth " +\
                        " -o " + self.cert_name + ".csr.der"
        self.ca_csr_gen_2_cmd = "openssl req -inform der -in " + self.cert_name+ ".csr.der -out " + self.cert_name + ".csr"
        self.cer_req_cmd = "pki ca-cert-request-submit --profile " + self.ca_profile + " --csr-file " + self.cert_name + ".csr"
        self.approave_req_cmd = "pki -d " + self.ca_database + " -c " + self.ds_password + \
                                " -n caadmin   ca-cert-request-review " + self.req_id + " -action approve"
        self.download_cert_cmd = "pki ca-cert-show " + self.req_id + "--output " + self.cert_name + ".crt"

    def setup_ca(self):
        self.set_setup_ca_commnad()
        with open('logfile', "w") as outfile:
            subprocess.call(self.setup_ds_cmd, stdout=outfile)
            subprocess.call(self.ds_service_enable_cmd.split(' '), stdout=outfile)
            subprocess.call(self.ds_service_start_cmd.split(' '), stdout=outfile)

    def request_cert(self):
        child = pexpect.spawn(self.ca_csr_gen_cmd)
        child.expect("Enter Password or Pin for \"NSS Certificate DB\":")
        child.sendline("Secret.123")
        child.expect("Continue typing untill the progress meter is full:")
        child.sendline(self.seed)
        child.expect("Generating Key.")
        child.sendline(self.ca_csr_gen_2_cmd)
        child.sendline(self.cer_req_cmd)
        child.expect("Submitted certificate request")

    def approve_cert_request(self):
        child = pexpect.spawn(self.approave_req_cmd)
        child.expect("Operation Result: success")

    def download_cert(self):
        child = pexpect.spawn(self.download_cert_cmd)
        child.expect("Status: VALID")
