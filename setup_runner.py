# This file is a sample executer file to show usage of classes
# for setup of DS and CA.


import setup_ds
import ca_utils

obj_setupds = setup_ds.SetupDS()
obj_setupds.setup_ds()

obj_setupca = ca_utils.SetupCA()
obj_setupca.setup_ca()

# To execute following methods SAN support has to be added to the defined CA profile
obj_setupca.request_cert()
obj_setupca.approve_cert_request()
obj_setupca.download_cert()

