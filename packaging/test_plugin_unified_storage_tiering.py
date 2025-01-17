import os
import sys
import shutil
import contextlib
import os.path
import unittest

from time import sleep

from ..controller import IrodsController
from ..configuration import IrodsConfig
from .resource_suite import ResourceBase
from . import session
from .. import test
from .. import paths
from .. import lib
from . import ustrings

@contextlib.contextmanager
def storage_tiering_configured_custom(arg=None, sleep_time=1):
    filename = paths.server_config_path()
    with lib.file_backed_up(filename):
        irods_config = IrodsConfig()
        irods_config.server_config['advanced_settings']['delay_server_sleep_time_in_seconds'] = sleep_time

        irods_config.server_config['plugin_configuration']['rule_engines'].insert(0,
            {
                "instance_name" : "irods_rule_engine_plugin-unified_storage_tiering-instance",
                "plugin_name" : "irods_rule_engine_plugin-unified_storage_tiering",
                "plugin_specific_configuration" : {
                    "access_time_attribute" : "irods::custom_access_time",
                    "group_attribute" : "irods::custom_storage_tiering::group",
                    "time_attribute" : "irods::custom_storage_tiering::time",
                    "query_attribute" : "irods::custom_storage_tiering::query",
                    "verification_attribute" : "irods::custom_storage_tiering::verification",
                    "restage_delay_attribute" : "irods::custom_storage_tiering::restage_delay",

                    "default_restage_delay_parameters" : "<PLUSET>1s</PLUSET>",
                    "time_check_string" : "TIME_CHECK_STRING"
                }
            }
        )

        irods_config.commit(irods_config.server_config, irods_config.server_config_path)
        try:
            yield
        finally:
            pass

@contextlib.contextmanager
def storage_tiering_configured(arg=None, sleep_time=1):
    filename = paths.server_config_path()
    with lib.file_backed_up(filename):
        irods_config = IrodsConfig()
        irods_config.server_config['advanced_settings']['delay_server_sleep_time_in_seconds'] = sleep_time

        irods_config.server_config['plugin_configuration']['rule_engines'].insert(0,
            {
                "instance_name": "irods_rule_engine_plugin-unified_storage_tiering-instance",
                "plugin_name": "irods_rule_engine_plugin-unified_storage_tiering",
                "plugin_specific_configuration": {
                }
            }
        )

        irods_config.commit(irods_config.server_config, irods_config.server_config_path)
        try:
            yield
        finally:
            pass

@contextlib.contextmanager
def storage_tiering_configured_with_log(arg=None, sleep_time=1):
    filename = paths.server_config_path()
    with lib.file_backed_up(filename):
        irods_config = IrodsConfig()
        irods_config.server_config['advanced_settings']['delay_server_sleep_time_in_seconds'] = sleep_time

        irods_config.server_config['plugin_configuration']['rule_engines'].insert(0,
            {
                "instance_name": "irods_rule_engine_plugin-unified_storage_tiering-instance",
                "plugin_name": "irods_rule_engine_plugin-unified_storage_tiering",
                "plugin_specific_configuration": {
                    "data_transfer_log_level" : "LOG_NOTICE"
                }
            }
        )

        irods_config.commit(irods_config.server_config, irods_config.server_config_path)

        try:
            yield
        finally:
            pass

@contextlib.contextmanager
def storage_tiering_configured_without_replication(arg=None, sleep_time=1):
    filename = paths.server_config_path()
    with lib.file_backed_up(filename):
        irods_config = IrodsConfig()
        irods_config.server_config['advanced_settings']['delay_server_sleep_time_in_seconds'] = sleep_time

        irods_config.server_config['plugin_configuration']['rule_engines'].insert(0,
            {
                "instance_name": "irods_rule_engine_plugin-unified_storage_tiering-instance",
                "plugin_name": "irods_rule_engine_plugin-unified_storage_tiering",
                "plugin_specific_configuration": {
                }
            }
        )

        irods_config.commit(irods_config.server_config, irods_config.server_config_path)
        try:
            yield
        finally:
            pass

@contextlib.contextmanager
def storage_tiering_configured_without_verification(arg=None, sleep_time=1):
    filename = paths.server_config_path()
    with lib.file_backed_up(filename):
        irods_config = IrodsConfig()
        irods_config.server_config['advanced_settings']['delay_server_sleep_time_in_seconds'] = sleep_time

        irods_config.server_config['plugin_configuration']['rule_engines'].insert(0,
            {
                "instance_name": "irods_rule_engine_plugin-unified_storage_tiering-instance",
                "plugin_name": "irods_rule_engine_plugin-unified_storage_tiering",
                "plugin_specific_configuration": {
                }
            }
        )

        irods_config.commit(irods_config.server_config, irods_config.server_config_path)
        try:
            yield
        finally:
            pass

@contextlib.contextmanager
def storage_tiering_configured_without_access_time(arg=None, sleep_time=1):
    filename = paths.server_config_path()
    with lib.file_backed_up(filename):
        irods_config = IrodsConfig()
        irods_config.server_config['advanced_settings']['delay_server_sleep_time_in_seconds'] = sleep_time

        irods_config.server_config['plugin_configuration']['rule_engines'].insert(0,
            {
                "instance_name": "irods_rule_engine_plugin-unified_storage_tiering-instance",
                "plugin_name": "irods_rule_engine_plugin-unified_storage_tiering",
                "plugin_specific_configuration": {
                }
            }
        )

        irods_config.commit(irods_config.server_config, irods_config.server_config_path)
        try:
            yield
        finally:
            pass

def wait_for_empty_queue(function):
    done = False
    while done == False:
        out, err, rc = lib.execute_command_permissive(['iqstat'])
        if -1 != out.find('No delayed rules pending'):
            function()
            done = True
        else:
            print(out)
            sleep(1)

def delay_assert(function):
    max_iter = 100
    counter = 0
    done = False
    while done == False:
        try:
            out, err, rc = lib.execute_command_permissive(['iqstat'])
            print(out)
            out, err, rc = function()
            print(out)
            print(err)
            print(rc)
        except:
            counter = counter + 1
            if(counter > max_iter):
                assert(False)
            sleep(1)
            continue
        else:
            done = True

def delay_assert_icommand(session, *args, **kwargs):
    max_iter = 100
    counter = 0
    done = False
    while done == False:
        try:
            session.assert_icommand(*args, **kwargs)
        except:
            counter = counter + 1
            if(counter > max_iter):
                assert(False)
            sleep(1)
            continue
        else:
            done = True

def invoke_storage_tiering_rule():
    rep_instance = 'irods_rule_engine_plugin-unified_storage_tiering-instance'
    rule_file_path = '/var/lib/irods/example_unified_tiering_invocation.r'
    with session.make_session_for_existing_admin() as admin_session:
        admin_session.assert_icommand(['irule', '-r', rep_instance, '-F', rule_file_path])


class TestStorageTieringPlugin(ResourceBase, unittest.TestCase):
    def setUp(self):
        super(TestStorageTieringPlugin, self).setUp()
        with session.make_session_for_existing_admin() as admin_session:
            admin_session.assert_icommand('iqdel -a')
            admin_session.assert_icommand('iadmin mkresc ufs0 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs0', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs1 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs1', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs2 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs2', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs3 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs3', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs4 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs4', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs5 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs5', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc rnd0 random', 'STDOUT_SINGLELINE', 'random')
            admin_session.assert_icommand('iadmin mkresc rnd1 random', 'STDOUT_SINGLELINE', 'random')
            admin_session.assert_icommand('iadmin mkresc rnd2 random', 'STDOUT_SINGLELINE', 'random')
            admin_session.assert_icommand('iadmin addchildtoresc rnd0 ufs0')
            admin_session.assert_icommand('iadmin addchildtoresc rnd0 ufs1')
            admin_session.assert_icommand('iadmin addchildtoresc rnd1 ufs2')
            admin_session.assert_icommand('iadmin addchildtoresc rnd1 ufs3')
            admin_session.assert_icommand('iadmin addchildtoresc rnd2 ufs4')
            admin_session.assert_icommand('iadmin addchildtoresc rnd2 ufs5')

            admin_session.assert_icommand('imeta add -R rnd0 irods::storage_tiering::group example_group 0')
            admin_session.assert_icommand('imeta add -R rnd1 irods::storage_tiering::group example_group 1')
            admin_session.assert_icommand('imeta add -R rnd2 irods::storage_tiering::group example_group 2')
            admin_session.assert_icommand('imeta add -R rnd0 irods::storage_tiering::time 5')
            admin_session.assert_icommand('imeta add -R rnd1 irods::storage_tiering::time 15')
            admin_session.assert_icommand('''imeta set -R rnd1 irods::storage_tiering::query "SELECT DATA_NAME, COLL_NAME, USER_NAME, USER_ZONE, DATA_REPL_NUM where RESC_NAME = 'ufs2' || = 'ufs3' and META_DATA_ATTR_NAME = 'irods::access_time' and META_DATA_ATTR_VALUE < 'TIME_CHECK_STRING'"''')
            admin_session.assert_icommand('imeta add -R rnd0 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R rnd0 irods::storage_tiering::maximum_delay_time_in_seconds 2')
            admin_session.assert_icommand('imeta add -R rnd1 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R rnd1 irods::storage_tiering::maximum_delay_time_in_seconds 2')

            admin_session.assert_icommand('ilsresc -l', 'STDOUT_SINGLELINE', 'random')

    def tearDown(self):
        super(TestStorageTieringPlugin, self).tearDown()
        with session.make_session_for_existing_admin() as admin_session:

            admin_session.assert_icommand('iadmin rmchildfromresc rnd0 ufs0')
            admin_session.assert_icommand('iadmin rmchildfromresc rnd0 ufs1')
            admin_session.assert_icommand('iadmin rmchildfromresc rnd1 ufs2')
            admin_session.assert_icommand('iadmin rmchildfromresc rnd1 ufs3')
            admin_session.assert_icommand('iadmin rmchildfromresc rnd2 ufs4')
            admin_session.assert_icommand('iadmin rmchildfromresc rnd2 ufs5')

            admin_session.assert_icommand('iadmin rmresc rnd0')
            admin_session.assert_icommand('iadmin rmresc rnd1')
            admin_session.assert_icommand('iadmin rmresc rnd2')
            admin_session.assert_icommand('iadmin rmresc ufs0')
            admin_session.assert_icommand('iadmin rmresc ufs1')
            admin_session.assert_icommand('iadmin rmresc ufs2')
            admin_session.assert_icommand('iadmin rmresc ufs3')
            admin_session.assert_icommand('iadmin rmresc ufs4')
            admin_session.assert_icommand('iadmin rmresc ufs5')
            admin_session.assert_icommand('iadmin rum')

    def test_put_and_get(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            zone_name = IrodsConfig().client_environment['irods_zone_name']
            with session.make_session_for_existing_admin() as admin_session:
                with session.make_session_for_existing_user('alice', 'apass', lib.get_hostname(), zone_name) as alice_session:
                    filename = "test_put_file"

                    try:
                        lib.create_local_testfile(filename)
                        alice_session.assert_icommand('iput -R rnd0 ' + filename)
                        alice_session.assert_icommand('imeta ls -d ' + filename, 'STDOUT_SINGLELINE', filename)
                        alice_session.assert_icommand('ils -L ' + filename, 'STDOUT_SINGLELINE', filename)
                        sleep(5)

                        # test stage to tier 1
                        invoke_storage_tiering_rule()
                        delay_assert_icommand(alice_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'rnd1')

                        # test stage to tier 2
                        sleep(15)
                        invoke_storage_tiering_rule()
                        delay_assert_icommand(alice_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'rnd2')

                        # test restage to tier 0
                        alice_session.assert_icommand('iget ' + filename + ' - ', 'STDOUT_SINGLELINE', 'TESTFILE')
                        delay_assert_icommand(alice_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'rnd0')

                    finally:
                        alice_session.assert_icommand('irm -f ' + filename)

    def test_put_and_get_with_preserve_replica__92(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            zone_name = IrodsConfig().client_environment['irods_zone_name']
            with session.make_session_for_existing_admin() as admin_session:
                with session.make_session_for_existing_user('alice', 'apass', lib.get_hostname(), zone_name) as alice_session:
                    filename = "test_put_file"

                    try:
                        admin_session.assert_icommand('imeta add -R rnd0 irods::storage_tiering::preserve_replicas true')

                        lib.create_local_testfile(filename)
                        alice_session.assert_icommand('iput -R rnd0 ' + filename)
                        alice_session.assert_icommand('imeta ls -d ' + filename, 'STDOUT_SINGLELINE', filename)
                        alice_session.assert_icommand('ils -L ' + filename, 'STDOUT_SINGLELINE', filename)

                        # wait for object to age out of tier 0
                        sleep(5)

                        # test stage to tier 1
                        invoke_storage_tiering_rule()
                        delay_assert_icommand(alice_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'rnd0')
                        delay_assert_icommand(alice_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'rnd1')

                        # wait for object to age back out of tier 0
                        sleep(5)

                        invoke_storage_tiering_rule()

                        # wait for rule to execute
                        sleep(1)

                        # check for objects to have been queued from tier 0
                        for i in range(50):
                            stdout, _, _ = admin_session.run_icommand('iqstat')
                            self.assertEqual(-1, stdout.find('rnd0'))

                    finally:
                        alice_session.assert_icommand('irm -f ' + filename)
                        admin_session.assert_icommand('imeta rm -R rnd0 irods::storage_tiering::preserve_replicas true')

    def test_put_and_get_with_preserve_replica_restage__125(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            zone_name = IrodsConfig().client_environment['irods_zone_name']
            with session.make_session_for_existing_admin() as admin_session:
                admin_session.assert_icommand('imeta add -R rnd0 irods::storage_tiering::preserve_replicas true')
                with session.make_session_for_existing_user('alice', 'apass', lib.get_hostname(), zone_name) as alice_session:
                    filename = "test_put_file"

                    try:
                        lib.create_local_testfile(filename)
                        alice_session.assert_icommand('iput -R rnd0 ' + filename)
                        alice_session.assert_icommand('imeta ls -d ' + filename, 'STDOUT_SINGLELINE', filename)
                        alice_session.assert_icommand('ils -L ' + filename, 'STDOUT_SINGLELINE', filename)
                        sleep(5)

                        # test stage to tier 1
                        invoke_storage_tiering_rule()
                        delay_assert_icommand(alice_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'rnd1')

                        # test stage to tier 2
                        sleep(15)
                        invoke_storage_tiering_rule()
                        delay_assert_icommand(alice_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'rnd2')

                        # test restage to tier 0
                        alice_session.assert_icommand('iget ' + filename + ' - ', 'STDOUT_SINGLELINE', 'TESTFILE')
                        delay_assert_icommand(alice_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'rnd0')
                        delay_assert_icommand(alice_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'rnd2')

                    finally:
                        alice_session.assert_icommand('irm -f ' + filename)

    def test_single_quote_data_name__127(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            zone_name = IrodsConfig().client_environment['irods_zone_name']
            with session.make_session_for_existing_admin() as admin_session:
                with session.make_session_for_existing_user('alice', 'apass', lib.get_hostname(), zone_name) as alice_session:
                    filename = "test_put_file_with_\'quotes\'"
                    cmd_filename = '\"'+filename+'\"'

                    try:
                        lib.create_local_testfile(filename)
                        alice_session.assert_icommand('iput -R rnd0 ' + cmd_filename)
                        alice_session.assert_icommand('imeta ls -d ' + cmd_filename, 'STDOUT_SINGLELINE', filename)
                        alice_session.assert_icommand('ils -L ' + cmd_filename, 'STDOUT_SINGLELINE', filename)
                        sleep(5)

                        # test stage to tier 1
                        invoke_storage_tiering_rule()
                        delay_assert_icommand(alice_session, 'ils -L ' + cmd_filename, 'STDOUT_SINGLELINE', 'rnd1')

                        # test stage to tier 2
                        sleep(15)
                        invoke_storage_tiering_rule()
                        delay_assert_icommand(alice_session, 'ils -L ' + cmd_filename, 'STDOUT_SINGLELINE', 'rnd2')

                        # test restage to tier 0
                        alice_session.assert_icommand('iget ' + cmd_filename + ' - ', 'STDOUT_SINGLELINE', 'TESTFILE')
                        delay_assert_icommand(alice_session, 'ils -L ' + cmd_filename, 'STDOUT_SINGLELINE', 'rnd0')

                    finally:
                        alice_session.assert_icommand('irm -f ' + cmd_filename)

    def test_storage_tiering_sets_admin_keyword_when_updating_access_time_as_rodsadmin__222(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)

            with session.make_session_for_existing_admin() as admin_session:
                zone_name = IrodsConfig().client_environment['irods_zone_name']

                with session.make_session_for_existing_user('alice', 'apass', lib.get_hostname(), zone_name) as alice_session:
                    resc_name = 'storage_tiering_ufs_222'
                    filename = 'test_file_issue_222'

                    try:
                        lib.create_local_testfile(filename)
                        alice_session.assert_icommand(f'iput -R rnd0 {filename}')
                        alice_session.assert_icommand(f'imeta ls -d {filename}', 'STDOUT_SINGLELINE', filename)
                        alice_session.assert_icommand(f'ils -L {filename}', 'STDOUT_SINGLELINE', filename)
                        sleep(5)

                        # test stage to tier 1.
                        invoke_storage_tiering_rule()
                        delay_assert_icommand(alice_session, f'ils -L {filename}', 'STDOUT_SINGLELINE', 'rnd1')

                        # test stage to tier 2.
                        sleep(15)
                        invoke_storage_tiering_rule()
                        delay_assert_icommand(alice_session, f'ils -L {filename}', 'STDOUT_SINGLELINE', 'rnd2')

                        # capture the access time.
                        _, out, _ = admin_session.assert_icommand(
                            ['iquest', '%s', f"select META_DATA_ATTR_VALUE where DATA_NAME = '{filename}' and META_DATA_ATTR_NAME = 'irods::access_time'"], 'STDOUT')
                        access_time = out.strip()
                        self.assertGreater(len(access_time), 0)

                        # sleeping guarantees the access time will be different following the call to irepl.
                        sleep(2)

                        # show the access time is updated correctly.
                        lib.create_ufs_resource(admin_session, resc_name)
                        admin_session.assert_icommand(f'irepl -M -R {resc_name} {alice_session.home_collection}/{filename}')

                        _, out, _ = admin_session.assert_icommand(
                            ['iquest', '%s', f"select META_DATA_ATTR_VALUE where DATA_NAME = '{filename}' and META_DATA_ATTR_NAME = 'irods::access_time'"], 'STDOUT')
                        new_access_time = out.strip()
                        self.assertGreater(len(new_access_time), 0)

                        # this assertion is the primary focus of the test.
                        self.assertGreater(int(new_access_time), int(access_time))

                    finally:
                        alice_session.assert_icommand(f'irm -f {filename}')
                        admin_session.assert_icommand(f'iadmin rmresc {resc_name}')

class TestStorageTieringPluginMultiGroup(ResourceBase, unittest.TestCase):
    def setUp(self):
        super(TestStorageTieringPluginMultiGroup, self).setUp()
        with session.make_session_for_existing_admin() as admin_session:
            admin_session.assert_icommand('iqdel -a')
            admin_session.assert_icommand('iadmin mkresc ufs0 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs0', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs1 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs1', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs2 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs2', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs3 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs3', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs4 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs4', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs5 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs5', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc rnd0 random', 'STDOUT_SINGLELINE', 'random')
            admin_session.assert_icommand('iadmin mkresc rnd1 random', 'STDOUT_SINGLELINE', 'random')
            admin_session.assert_icommand('iadmin mkresc rnd2 random', 'STDOUT_SINGLELINE', 'random')
            admin_session.assert_icommand('iadmin addchildtoresc rnd0 ufs0')
            admin_session.assert_icommand('iadmin addchildtoresc rnd0 ufs1')
            admin_session.assert_icommand('iadmin addchildtoresc rnd1 ufs2')
            admin_session.assert_icommand('iadmin addchildtoresc rnd1 ufs3')
            admin_session.assert_icommand('iadmin addchildtoresc rnd2 ufs4')
            admin_session.assert_icommand('iadmin addchildtoresc rnd2 ufs5')

            admin_session.assert_icommand('imeta add -R rnd0 irods::storage_tiering::group example_group 0')
            admin_session.assert_icommand('imeta add -R rnd1 irods::storage_tiering::group example_group 1')
            admin_session.assert_icommand('imeta add -R rnd2 irods::storage_tiering::group example_group 2')
            admin_session.assert_icommand('imeta add -R rnd0 irods::storage_tiering::time 5')
            admin_session.assert_icommand('imeta add -R rnd1 irods::storage_tiering::time 15')
            admin_session.assert_icommand('''imeta set -R rnd1 irods::storage_tiering::query "SELECT DATA_NAME, COLL_NAME, USER_NAME, USER_ZONE, DATA_REPL_NUM  where RESC_NAME = 'ufs2' || = 'ufs3' and META_DATA_ATTR_NAME = 'irods::access_time' and META_DATA_ATTR_VALUE < 'TIME_CHECK_STRING'"''')

            admin_session.assert_icommand('iadmin mkresc ufs0g2 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs0g2', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs1g2 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs1g2', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs2g2 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs2g2', 'STDOUT_SINGLELINE', 'unixfilesystem')

            admin_session.assert_icommand('imeta add -R ufs0g2 irods::storage_tiering::group example_group_g2 0')
            admin_session.assert_icommand('imeta add -R ufs1g2 irods::storage_tiering::group example_group_g2 1')
            admin_session.assert_icommand('imeta add -R ufs2g2 irods::storage_tiering::group example_group_g2 2')

            admin_session.assert_icommand('imeta add -R ufs0g2 irods::storage_tiering::time 5')
            admin_session.assert_icommand('imeta add -R ufs1g2 irods::storage_tiering::time 15')

            admin_session.assert_icommand('''imeta set -R ufs1g2 irods::storage_tiering::query "SELECT DATA_NAME, COLL_NAME, USER_NAME, USER_ZONE, DATA_REPL_NUM where RESC_NAME = 'ufs1g2' and META_DATA_ATTR_NAME = 'irods::access_time' and META_DATA_ATTR_VALUE < 'TIME_CHECK_STRING'"''')
            admin_session.assert_icommand('imeta add -R rnd0 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R rnd0 irods::storage_tiering::maximum_delay_time_in_seconds 2')
            admin_session.assert_icommand('imeta add -R rnd1 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R rnd1 irods::storage_tiering::maximum_delay_time_in_seconds 2')

    def tearDown(self):
        super(TestStorageTieringPluginMultiGroup, self).tearDown()
        with session.make_session_for_existing_admin() as admin_session:

            admin_session.assert_icommand('iadmin rmchildfromresc rnd0 ufs0')
            admin_session.assert_icommand('iadmin rmchildfromresc rnd0 ufs1')
            admin_session.assert_icommand('iadmin rmchildfromresc rnd1 ufs2')
            admin_session.assert_icommand('iadmin rmchildfromresc rnd1 ufs3')
            admin_session.assert_icommand('iadmin rmchildfromresc rnd2 ufs4')
            admin_session.assert_icommand('iadmin rmchildfromresc rnd2 ufs5')

            admin_session.assert_icommand('iadmin rmresc rnd0')
            admin_session.assert_icommand('iadmin rmresc rnd1')
            admin_session.assert_icommand('iadmin rmresc rnd2')
            admin_session.assert_icommand('iadmin rmresc ufs0')
            admin_session.assert_icommand('iadmin rmresc ufs1')
            admin_session.assert_icommand('iadmin rmresc ufs2')
            admin_session.assert_icommand('iadmin rmresc ufs3')
            admin_session.assert_icommand('iadmin rmresc ufs4')
            admin_session.assert_icommand('iadmin rmresc ufs5')

            admin_session.assert_icommand('iadmin rmresc ufs0g2')
            admin_session.assert_icommand('iadmin rmresc ufs1g2')
            admin_session.assert_icommand('iadmin rmresc ufs2g2')

            admin_session.assert_icommand('iadmin rum')

    def test_put_and_get(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:
                print("yep")
                admin_session.assert_icommand('ils -L ', 'STDOUT_SINGLELINE', 'rods')

                filename = 'test_put_file'

                filenameg2 = 'test_put_fileg2'

                try:
                    lib.create_local_testfile(filename)
                    lib.create_local_testfile(filenameg2)

                    admin_session.assert_icommand('iput -R rnd0 ' + filename)
                    admin_session.assert_icommand('imeta ls -d ' + filename, 'STDOUT_SINGLELINE', filename)
                    admin_session.assert_icommand('ils -L ' + filename, 'STDOUT_SINGLELINE', filename)

                    admin_session.assert_icommand('iput -R ufs0g2 ' + filenameg2)
                    admin_session.assert_icommand('imeta ls -d ' + filenameg2, 'STDOUT_SINGLELINE', filenameg2)
                    admin_session.assert_icommand('ils -L ' + filenameg2, 'STDOUT_SINGLELINE', filenameg2)

                    # test stage to tier 1
                    sleep(5)
                    invoke_storage_tiering_rule()
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'rnd1')
                    delay_assert_icommand(admin_session, 'ils -L ' + filenameg2, 'STDOUT_SINGLELINE', 'ufs1g2')

                    # test stage to tier 2
                    sleep(15)
                    invoke_storage_tiering_rule()
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'rnd2')
                    delay_assert_icommand(admin_session, 'ils -L ' + filenameg2, 'STDOUT_SINGLELINE', 'ufs2g2')

                    # test restage to tier 0
                    admin_session.assert_icommand('iget ' + filename + ' - ', 'STDOUT_SINGLELINE', 'TESTFILE')
                    admin_session.assert_icommand('iget ' + filenameg2 + ' - ', 'STDOUT_SINGLELINE', 'TESTFILE')
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'rnd0')
                    delay_assert_icommand(admin_session, 'ils -L ' + filenameg2, 'STDOUT_SINGLELINE', 'ufs0g2')

                finally:
                    admin_session.assert_icommand('irm -f ' + filename)
                    admin_session.assert_icommand('irm -f ' + filenameg2)

class TestStorageTieringPluginCustomMetadata(ResourceBase, unittest.TestCase):
    def setUp(self):
        super(TestStorageTieringPluginCustomMetadata, self).setUp()
        with session.make_session_for_existing_admin() as admin_session:
            admin_session.assert_icommand('iqdel -a')
            admin_session.assert_icommand('iadmin mkresc ufs0 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs0', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs1 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs1', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs2 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs2', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs3 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs3', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs4 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs4', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs5 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs5', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc rnd0 random', 'STDOUT_SINGLELINE', 'random')
            admin_session.assert_icommand('iadmin mkresc rnd1 random', 'STDOUT_SINGLELINE', 'random')
            admin_session.assert_icommand('iadmin mkresc rnd2 random', 'STDOUT_SINGLELINE', 'random')
            admin_session.assert_icommand('iadmin addchildtoresc rnd0 ufs0')
            admin_session.assert_icommand('iadmin addchildtoresc rnd0 ufs1')
            admin_session.assert_icommand('iadmin addchildtoresc rnd1 ufs2')
            admin_session.assert_icommand('iadmin addchildtoresc rnd1 ufs3')
            admin_session.assert_icommand('iadmin addchildtoresc rnd2 ufs4')
            admin_session.assert_icommand('iadmin addchildtoresc rnd2 ufs5')

            admin_session.assert_icommand('imeta add -R rnd0 irods::custom_storage_tiering::group example_group 0')
            admin_session.assert_icommand('imeta add -R rnd1 irods::custom_storage_tiering::group example_group 1')
            admin_session.assert_icommand('imeta add -R rnd2 irods::custom_storage_tiering::group example_group 2')
            admin_session.assert_icommand('imeta add -R rnd0 irods::custom_storage_tiering::time 5')
            admin_session.assert_icommand('imeta add -R rnd1 irods::custom_storage_tiering::time 15')
            admin_session.assert_icommand('''imeta set -R rnd1 irods::custom_storage_tiering::query "SELECT DATA_NAME, COLL_NAME, USER_NAME, USER_ZONE, DATA_REPL_NUM where RESC_NAME = 'ufs2' || = 'ufs3' and META_DATA_ATTR_NAME = 'irods::custom_access_time' and META_DATA_ATTR_VALUE < 'TIME_CHECK_STRING'"''')
            admin_session.assert_icommand('imeta add -R rnd0 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R rnd0 irods::storage_tiering::maximum_delay_time_in_seconds 2')
            admin_session.assert_icommand('imeta add -R rnd1 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R rnd1 irods::storage_tiering::maximum_delay_time_in_seconds 2')

    def tearDown(self):
        super(TestStorageTieringPluginCustomMetadata, self).tearDown()
        with session.make_session_for_existing_admin() as admin_session:

            admin_session.assert_icommand('iadmin rmchildfromresc rnd0 ufs0')
            admin_session.assert_icommand('iadmin rmchildfromresc rnd0 ufs1')
            admin_session.assert_icommand('iadmin rmchildfromresc rnd1 ufs2')
            admin_session.assert_icommand('iadmin rmchildfromresc rnd1 ufs3')
            admin_session.assert_icommand('iadmin rmchildfromresc rnd2 ufs4')
            admin_session.assert_icommand('iadmin rmchildfromresc rnd2 ufs5')

            admin_session.assert_icommand('iadmin rmresc rnd0')
            admin_session.assert_icommand('iadmin rmresc rnd1')
            admin_session.assert_icommand('iadmin rmresc rnd2')
            admin_session.assert_icommand('iadmin rmresc ufs0')
            admin_session.assert_icommand('iadmin rmresc ufs1')
            admin_session.assert_icommand('iadmin rmresc ufs2')
            admin_session.assert_icommand('iadmin rmresc ufs3')
            admin_session.assert_icommand('iadmin rmresc ufs4')
            admin_session.assert_icommand('iadmin rmresc ufs5')
            admin_session.assert_icommand('iadmin rum')


    def test_put_and_get(self):
        with storage_tiering_configured_custom():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:
                filename = 'test_put_file'

                try:
                    lib.create_local_testfile(filename)
                    admin_session.assert_icommand('iput -R rnd0 ' + filename)
                    admin_session.assert_icommand('imeta ls -d ' + filename, 'STDOUT_SINGLELINE', filename)
                    admin_session.assert_icommand('ils -L ' + filename, 'STDOUT_SINGLELINE', filename)

                    # test stage to tier 1
                    sleep(5)
                    invoke_storage_tiering_rule()
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'rnd1')

                    # test stage to tier 2
                    sleep(15)
                    invoke_storage_tiering_rule()
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'rnd2')

                    # test restage to tier 0
                    admin_session.assert_icommand('iget ' + filename + ' - ', 'STDOUT_SINGLELINE', 'TESTFILE')
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'rnd0')

                finally:
                    admin_session.assert_icommand('irm -f ' + filename)

class TestStorageTieringPluginMinimumRestage(ResourceBase, unittest.TestCase):
    def setUp(self):
        super(TestStorageTieringPluginMinimumRestage, self).setUp()
        with session.make_session_for_existing_admin() as admin_session:
            admin_session.assert_icommand('iqdel -a')
            admin_session.assert_icommand('iadmin mkresc ufs0 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs0', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs1 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs1', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs2 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs2', 'STDOUT_SINGLELINE', 'unixfilesystem')

            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::group example_group 0')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::group example_group 1')
            admin_session.assert_icommand('imeta add -R ufs2 irods::storage_tiering::group example_group 2')
            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::time 5')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::time 15')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::minimum_restage_tier true')
            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::maximum_delay_time_in_seconds 2')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::maximum_delay_time_in_seconds 2')

    def tearDown(self):
        super(TestStorageTieringPluginMinimumRestage, self).tearDown()
        with session.make_session_for_existing_admin() as admin_session:

            admin_session.assert_icommand('iadmin rmresc ufs0')
            admin_session.assert_icommand('iadmin rmresc ufs1')
            admin_session.assert_icommand('iadmin rmresc ufs2')
            admin_session.assert_icommand('iadmin rum')

    def test_put_and_get(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:
                filename = 'test_put_file'

                try:
                    lib.create_local_testfile(filename)
                    admin_session.assert_icommand('iput -R ufs0 ' + filename)
                    admin_session.assert_icommand('ils -L ', 'STDOUT_SINGLELINE', 'rods')
                    sleep(5)
                    invoke_storage_tiering_rule()
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'ufs1')

                    sleep(15)
                    invoke_storage_tiering_rule()
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'ufs2')

                    # test restage to tier 1
                    admin_session.assert_icommand('iget ' + filename + ' - ', 'STDOUT_SINGLELINE', 'TESTFILE')
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'ufs1')

                finally:
                    admin_session.assert_icommand('irm -f ' + filename)

class TestStorageTieringPluginPreserveReplica(ResourceBase, unittest.TestCase):
    def setUp(self):
        super(TestStorageTieringPluginPreserveReplica, self).setUp()
        with session.make_session_for_existing_admin() as admin_session:
            admin_session.assert_icommand('iqdel -a')
            admin_session.assert_icommand('iadmin mkresc ufs0 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs0', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs1 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs1', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs2 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs2', 'STDOUT_SINGLELINE', 'unixfilesystem')

            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::group example_group 0')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::group example_group 1')
            admin_session.assert_icommand('imeta add -R ufs2 irods::storage_tiering::group example_group 2')

            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::time 5')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::time 15')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::minimum_restage_tier true')

            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::preserve_replicas true')
            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::maximum_delay_time_in_seconds 2')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::maximum_delay_time_in_seconds 2')

    def tearDown(self):
        super(TestStorageTieringPluginPreserveReplica, self).tearDown()
        with session.make_session_for_existing_admin() as admin_session:

            admin_session.assert_icommand('iadmin rmresc ufs0')
            admin_session.assert_icommand('iadmin rmresc ufs1')
            admin_session.assert_icommand('iadmin rmresc ufs2')
            admin_session.assert_icommand('iadmin rum')

    def test_put(self):
        with storage_tiering_configured_with_log():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:
                filename = 'test_put_file'

                try:
                    lib.create_local_testfile(filename)
                    admin_session.assert_icommand('iput -R ufs0 ' + filename)
                    admin_session.assert_icommand('ils -L ', 'STDOUT_SINGLELINE', 'rods')

                    # stage to tier 1, look for both replicas
                    sleep(6)
                    invoke_storage_tiering_rule()
                    admin_session.assert_icommand('iqstat', 'STDOUT_SINGLELINE', 'irods_policy_storage_tiering')

                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'ufs0')
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'ufs1')

                    sleep(15)
                    # stage to tier 2, look for replica in tier 0 and tier 2
                    invoke_storage_tiering_rule()
                    admin_session.assert_icommand('iqstat', 'STDOUT_SINGLELINE', 'irods_policy_storage_tiering')

                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'ufs0')
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'ufs2')

                finally:
                    admin_session.assert_icommand('irm -f ' + filename)

    def test_preserve_replicas_works_with_restage_when_replicas_exist_in_multiple_tiers__issue_232(self):
        with storage_tiering_configured_with_log():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:
                filename = 'test_put_file'

                try:
                    # make sure replicas stored on tier 2 are preserved
                    admin_session.assert_icommand('imeta add -R ufs2 irods::storage_tiering::preserve_replicas true')

                    # create test file and upload it
                    lib.create_local_testfile(filename)
                    admin_session.assert_icommand('iput -R ufs0 ' + filename)
                    admin_session.assert_icommand('ils -L ', 'STDOUT_SINGLELINE', 'rods')

                    # stage to tier 1, look for both replicas
                    sleep(6)
                    invoke_storage_tiering_rule()
                    admin_session.assert_icommand('iqstat', 'STDOUT_SINGLELINE', 'irods_policy_storage_tiering')

                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', '0 ufs0')
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', '1 ufs1')

                    sleep(15)
                    # stage to tier 2, look for replica in tier 0 and tier 2
                    invoke_storage_tiering_rule()
                    admin_session.assert_icommand('iqstat', 'STDOUT_SINGLELINE', 'irods_policy_storage_tiering')

                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', '0 ufs0')
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', '2 ufs2')

                    # test restage to tier 1 using replica from tier 0, look for replica in all tiers afterwards
                    admin_session.assert_icommand('iget -R ufs0 ' + filename + ' - ', 'STDOUT_SINGLELINE', 'TESTFILE')

                    sleep(15)
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', '0 ufs0')
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', '3 ufs1')
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', '2 ufs2')


                finally:
                    admin_session.assert_icommand('irm -f ' + filename)

    def test_preserve_replicas_works_with_restage_when_replica_only_exists_in_last_tier__issue_233(self):
        with storage_tiering_configured_with_log():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:
                filename = 'test_put_file'

                try:
                    # make sure replicas stored on tier 1 are preserved and the minimum_restage_tier is not set
                    admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::preserve_replicas true')
                    admin_session.assert_icommand('imeta rm  -R ufs1 irods::storage_tiering::minimum_restage_tier true')

                    # make sure tier 2 does not get involved
                    admin_session.assert_icommand('imeta rm -R ufs2 irods::storage_tiering::group example_group 2')

                    # create test file and upload it
                    lib.create_local_testfile(filename)
                    admin_session.assert_icommand('iput -R ufs0 ' + filename)
                    admin_session.assert_icommand('ils -L ', 'STDOUT_SINGLELINE', 'rods')

                    # stage to tier 1, look for both replicas
                    sleep(6)
                    invoke_storage_tiering_rule()
                    admin_session.assert_icommand('iqstat', 'STDOUT_SINGLELINE', 'irods_policy_storage_tiering')

                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', '0 ufs0')
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', '1 ufs1')

                    # remove the object in tier 0
                    admin_session.assert_icommand('itrim -N1 -n0 ' + filename, 'STDOUT_SINGLELINE', 'Number of files trimmed = 1' )

                    # test restage to tier 0, look for replica in tier 0 and tier 1
                    admin_session.assert_icommand('iget ' + filename + ' - ', 'STDOUT_SINGLELINE', 'TESTFILE')

                    sleep(15)
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', '2 ufs0')
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', '1 ufs1')


                finally:
                    admin_session.assert_icommand('irm -f ' + filename)


class TestStorageTieringPluginObjectLimit(ResourceBase, unittest.TestCase):
    def setUp(self):
        super(TestStorageTieringPluginObjectLimit, self).setUp()
        with session.make_session_for_existing_admin() as admin_session:
            admin_session.assert_icommand('iqdel -a')
            admin_session.assert_icommand('iadmin mkresc ufs0 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs0', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs1 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs1', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs2 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs2', 'STDOUT_SINGLELINE', 'unixfilesystem')

            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::group example_group 0')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::group example_group 1')
            admin_session.assert_icommand('imeta add -R ufs2 irods::storage_tiering::group example_group 2')

            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::time 5')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::time 15')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::minimum_restage_tier true')
            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::maximum_delay_time_in_seconds 2')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::maximum_delay_time_in_seconds 2')

            self.filename  = 'test_put_file'
            self.filename2 = 'test_put_file2'

    def tearDown(self):
        super(TestStorageTieringPluginObjectLimit, self).tearDown()
        with session.make_session_for_existing_admin() as admin_session:

            admin_session.assert_icommand('iadmin rmresc ufs0')
            admin_session.assert_icommand('iadmin rmresc ufs1')
            admin_session.assert_icommand('iadmin rmresc ufs2')
            admin_session.assert_icommand('iadmin rum')

    def test_put_and_get_limit_1(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:
                try:
                    admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::object_limit 1')

                    lib.create_local_testfile(self.filename)

                    admin_session.assert_icommand('iput -R ufs0 ' + self.filename)
                    admin_session.assert_icommand('iput -R ufs0 ' + self.filename + " " + self.filename2)
                    admin_session.assert_icommand('ils -L ', 'STDOUT_SINGLELINE', 'rods')

                    # stage to tier 1, look for both replicas (only one should move)
                    sleep(5)
                    invoke_storage_tiering_rule()
                    admin_session.assert_icommand('iqstat', 'STDOUT_SINGLELINE', 'irods_policy_storage_tiering')
                    delay_assert_icommand(admin_session, 'ils -L ' + self.filename2, 'STDOUT_SINGLELINE', 'ufs0')
                    delay_assert_icommand(admin_session, 'ils -L ' + self.filename, 'STDOUT_SINGLELINE', 'ufs1')

                finally:
                    admin_session.assert_icommand('irm -f ' + self.filename)
                    admin_session.assert_icommand('irm -f ' + self.filename2)

    def test_put_and_get_no_limit_zero(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:
                try:
                    admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::object_limit 0')

                    lib.create_local_testfile(self.filename)

                    admin_session.assert_icommand('iput -R ufs0 ' + self.filename)
                    admin_session.assert_icommand('iput -R ufs0 ' + self.filename + " " + self.filename2)
                    admin_session.assert_icommand('ils -L ', 'STDOUT_SINGLELINE', 'rods')

                    # stage to tier 1, everything should move
                    sleep(5)
                    invoke_storage_tiering_rule()
                    admin_session.assert_icommand('iqstat', 'STDOUT_SINGLELINE', 'irods_policy_storage_tiering')
                    delay_assert_icommand(admin_session, 'ils -L ' + self.filename, 'STDOUT_SINGLELINE', 'ufs1')
                    delay_assert_icommand(admin_session, 'ils -L ' + self.filename2, 'STDOUT_SINGLELINE', 'ufs1')

                finally:
                    admin_session.assert_icommand('irm -f ' + self.filename)
                    admin_session.assert_icommand('irm -f ' + self.filename2)

    def test_put_and_get_no_limit_default(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:
                try:
                    lib.create_local_testfile(self.filename)
                    admin_session.assert_icommand('iput -R ufs0 ' + self.filename)
                    admin_session.assert_icommand('iput -R ufs0 ' + self.filename + " " + self.filename2)
                    admin_session.assert_icommand('ils -L ', 'STDOUT_SINGLELINE', 'rods')

                    # stage to tier 1, everything should move
                    sleep(5)
                    invoke_storage_tiering_rule()
                    admin_session.assert_icommand('iqstat', 'STDOUT_SINGLELINE', 'irods_policy_storage_tiering')
                    delay_assert_icommand(admin_session, 'ils -L ' + self.filename, 'STDOUT_SINGLELINE', 'ufs1')
                    delay_assert_icommand(admin_session, 'ils -L ' + self.filename2, 'STDOUT_SINGLELINE', 'ufs1')

                finally:
                    admin_session.assert_icommand('irm -f ' + self.filename)
                    admin_session.assert_icommand('irm -f ' + self.filename2)

#   class TestStorageTieringPluginLogMigration(ResourceBase, unittest.TestCase):
#       def setUp(self):
#           super(TestStorageTieringPluginLogMigration, self).setUp()
#           with session.make_session_for_existing_admin() as admin_session:
#               admin_session.assert_icommand('iqdel -a')
#               admin_session.assert_icommand('iadmin mkresc ufs0 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs0', 'STDOUT_SINGLELINE', 'unixfilesystem')
#               admin_session.assert_icommand('iadmin mkresc ufs1 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs1', 'STDOUT_SINGLELINE', 'unixfilesystem')
#
#               admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::group example_group 0')
#               admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::group example_group 1')
#
#               admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::time 5')
#               admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::minimum_delay_time_in_seconds 1')
#               admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::maximum_delay_time_in_seconds 2')
#
#               self.max_sql_rows = 256
#
#       def tearDown(self):
#           super(TestStorageTieringPluginLogMigration, self).tearDown()
#           with session.make_session_for_existing_admin() as admin_session:
#               admin_session.assert_icommand('iadmin rmresc ufs0')
#               admin_session.assert_icommand('iadmin rmresc ufs1')
#               admin_session.assert_icommand('iadmin rum')
#
#       def test_put_and_get(self):
#           with storage_tiering_configured_with_log():
#               with session.make_session_for_existing_admin() as admin_session:
#
#                       initial_log_size = lib.get_file_size_by_path(paths.server_log_path())
#
#                       filename = 'test_put_file'
#                       admin_session.assert_icommand('iput -R ufs0 ' + filename)
#                       admin_session.assert_icommand('imeta ls -d ' + filename, 'STDOUT_SINGLELINE', filename)
#                       admin_session.assert_icommand('ils -L ' + filename, 'STDOUT_SINGLELINE', filename)
#
#                       # test stage to tier 1
#                       sleep(5)
#                       invoke_storage_tiering_rule()
#                       sleep(60)
#
#                       admin_session.assert_icommand('ils -L ' + filename, 'STDOUT_SINGLELINE', 'ufs1')
#                       admin_session.assert_icommand('irm -f ' + filename)
#
#                       log_count = lib.count_occurrences_of_string_in_log(paths.server_log_path(), 'irods::storage_tiering migrating', start_index=initial_log_size)
#                       self.assertTrue(1 == log_count, msg='log_count:{}'.format(log_count))

class TestStorageTieringMultipleQueries(ResourceBase, unittest.TestCase):
    def setUp(self):
        super(TestStorageTieringMultipleQueries, self).setUp()
        with session.make_session_for_existing_admin() as admin_session:
            admin_session.assert_icommand('iqdel -a')
            admin_session.assert_icommand('''iadmin asq "select distinct R_DATA_MAIN.data_name, R_COLL_MAIN.coll_name, R_DATA_MAIN.data_owner_name, R_DATA_MAIN.data_owner_zone, R_DATA_MAIN.data_repl_num from R_DATA_MAIN, R_COLL_MAIN, R_RESC_MAIN, R_OBJT_METAMAP r_data_metamap, R_META_MAIN r_data_meta_main where R_RESC_MAIN.resc_name = 'ufs0' AND r_data_meta_main.meta_attr_name = 'archive_object' AND r_data_meta_main.meta_attr_value = 'yes' AND R_COLL_MAIN.coll_id = R_DATA_MAIN.coll_id AND R_RESC_MAIN.resc_id = R_DATA_MAIN.resc_id AND R_DATA_MAIN.data_id = r_data_metamap.object_id AND r_data_metamap.meta_id = r_data_meta_main.meta_id order by R_COLL_MAIN.coll_name, R_DATA_MAIN.data_name" archive_query''')

            admin_session.assert_icommand('iadmin mkresc ufs0 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs0', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs1 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs1', 'STDOUT_SINGLELINE', 'unixfilesystem')

            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::group example_group 0')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::group example_group 1')

            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::time 15')

            admin_session.assert_icommand('''imeta add -R ufs0 irods::storage_tiering::query "SELECT DATA_NAME, COLL_NAME, USER_NAME, USER_ZONE, DATA_REPL_NUM where RESC_NAME = 'ufs0' and META_DATA_ATTR_NAME = 'irods::access_time' and META_DATA_ATTR_VALUE < 'TIME_CHECK_STRING'"''')
            admin_session.assert_icommand('''imeta add -R ufs0 irods::storage_tiering::query archive_query specific''')
            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::maximum_delay_time_in_seconds 2')


    def tearDown(self):
        super(TestStorageTieringMultipleQueries, self).tearDown()
        with session.make_session_for_existing_admin() as admin_session:

            admin_session.assert_icommand('iadmin rmresc ufs0')
            admin_session.assert_icommand('iadmin rmresc ufs1')
            admin_session.assert_icommand('iadmin rum')
            admin_session.assert_icommand('iadmin rsq archive_query')

    def test_put_and_get(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:

                filename  = 'test_put_file'
                filename2 = 'test_put_file2'
                filepath  = lib.create_local_testfile(filename)

                try:
                    admin_session.assert_icommand('iput -R ufs0 ' + filename)
                    admin_session.assert_icommand('imeta add -d ' + filename + ' archive_object yes')
                    admin_session.assert_icommand('imeta ls -d ' + filename, 'STDOUT_SINGLELINE', 'irods::access_time')

                    admin_session.assert_icommand('iput -R ufs0 ' + filename + ' ' + filename2)
                    admin_session.assert_icommand('imeta ls -d ' + filename2, 'STDOUT_SINGLELINE', 'irods::access_time')

                    # test stage to tier 1
                    invoke_storage_tiering_rule()
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'ufs1')
                    delay_assert_icommand(admin_session, 'ils -L ' + filename2, 'STDOUT_SINGLELINE', 'ufs0')

                    sleep(15)
                    invoke_storage_tiering_rule()
                    delay_assert_icommand(admin_session, 'ils -L ' + filename2, 'STDOUT_SINGLELINE', 'ufs1')

                finally:
                    admin_session.assert_icommand('irm -f ' + filename)
                    admin_session.assert_icommand('irm -f ' + filename2)

class TestStorageTieringPluginRegistration(ResourceBase, unittest.TestCase):
    def setUp(self):
        super(TestStorageTieringPluginRegistration, self).setUp()
        with session.make_session_for_existing_admin() as admin_session:
            admin_session.assert_icommand('iqdel -a')
            admin_session.assert_icommand('iadmin mkresc ufs0 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs0', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs1 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs1', 'STDOUT_SINGLELINE', 'unixfilesystem')

            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::group example_group 0')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::group example_group 1')

            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::time 5')
            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::maximum_delay_time_in_seconds 2')


    def tearDown(self):
        super(TestStorageTieringPluginRegistration, self).tearDown()
        with session.make_session_for_existing_admin() as admin_session:
            admin_session.assert_icommand('iadmin rmresc ufs0')
            admin_session.assert_icommand('iadmin rmresc ufs1')
            admin_session.assert_icommand('iadmin rum')

    def test_file_registration(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:
                filename  = 'test_put_file'
                filepath  = lib.create_local_testfile(filename)
                ipwd, _, _ = admin_session.run_icommand('ipwd')
                ipwd = ipwd.rstrip()
                dest_path = ipwd + '/' + filename

                try:
                    admin_session.assert_icommand('ipwd', 'STDOUT_SINGLELINE', 'rods')
                    admin_session.assert_icommand('ireg -R ufs0 ' + filepath + ' ' + dest_path)
                    admin_session.assert_icommand('imeta ls -d ' + filename, 'STDOUT_SINGLELINE', filename)
                    admin_session.assert_icommand('ils -L ' + filename, 'STDOUT_SINGLELINE', filename)

                    # test stage to tier 1
                    sleep(5)
                    invoke_storage_tiering_rule()
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'ufs1')

                finally:
                    admin_session.assert_icommand('irm -f ' + filename)

    def test_directory_registration(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:
                local_dir_name = '/tmp/test_directory_registration_dir'
                shutil.rmtree(local_dir_name, ignore_errors=True)
                local_tree = lib.make_deep_local_tmp_dir(local_dir_name, 3, 10, 5)

                dest_path = '/tempZone/home/rods/reg_coll'

                try:
                    admin_session.assert_icommand('ireg -r -R ufs0 ' + local_dir_name + ' ' + dest_path)
                    admin_session.assert_icommand('ils -rL ' + dest_path, 'STDOUT_SINGLELINE', dest_path)

                    # test stage to tier 1
                    sleep(5)
                    invoke_storage_tiering_rule()
                    delay_assert_icommand(admin_session, 'ils -L ' + dest_path, 'STDOUT_SINGLELINE', 'ufs1')

                finally:
                    delay_assert_icommand(admin_session, 'iqdel -a')

                    admin_session.assert_icommand('irm -rf ' + dest_path)


class TestStorageTieringContinueInxMigration(ResourceBase, unittest.TestCase):
    def setUp(self):
        super(TestStorageTieringContinueInxMigration, self).setUp()
        with session.make_session_for_existing_admin() as admin_session:
            admin_session.assert_icommand('iqdel -a')
            admin_session.assert_icommand('iadmin mkresc ufs0 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs0', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs1 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs1', 'STDOUT_SINGLELINE', 'unixfilesystem')

            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::group example_group 0')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::group example_group 1')

            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::time 5')

            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::maximum_delay_time_in_seconds 2')

            self.max_sql_rows = 256

    def tearDown(self):
        super(TestStorageTieringContinueInxMigration, self).tearDown()
        with session.make_session_for_existing_admin() as admin_session:
            admin_session.assert_icommand('iadmin rmresc ufs0')
            admin_session.assert_icommand('iadmin rmresc ufs1')
            admin_session.assert_icommand('iadmin rum')

    def test_put_gt_max_sql_rows(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:
                # Put enough objects to force continueInx when iterating over violating objects (above MAX_SQL_ROWS)
                file_count = self.max_sql_rows + 1
                dirname = 'test_put_gt_max_sql_rows'

                try:
                    shutil.rmtree(dirname, ignore_errors=True)
                    lib.make_large_local_tmp_dir(dirname, file_count, 1)
                    admin_session.assert_icommand(['iput', '-R', 'ufs0', '-r', dirname], 'STDOUT_SINGLELINE', ustrings.recurse_ok_string())

                    # stage to tier 1, everything should have been tiered out
                    sleep(5)
                    invoke_storage_tiering_rule()
                    sleep(5)
                    delay_assert_icommand(admin_session, ['ils', '-l', dirname], 'STDOUT_SINGLELINE', 'ufs1')
                    delay_assert_icommand(admin_session, ['ils', '-l', dirname], 'STDOUT_SINGLELINE', 'ufs0')
                    # Wait for the queue to be emptied and ensure that everything has tiered out from ufs0
                    wait_for_empty_queue(lambda: admin_session.assert_icommand_fail(['ils', '-l', dirname], 'STDOUT', 'ufs0'))

                finally:
                    delay_assert_icommand(admin_session, 'iqdel -a')

                    # cleanup
                    admin_session.assert_icommand(['irm', '-f', '-r', dirname])
                    shutil.rmtree(dirname, ignore_errors=True)

    def test_put_max_sql_rows(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:
                # Put exactly MAX_SQL_ROWS objects (boundary test)
                file_count = self.max_sql_rows
                dirname = 'test_put_max_sql_rows'

                try:
                    shutil.rmtree(dirname, ignore_errors=True)
                    lib.make_large_local_tmp_dir(dirname, file_count, 1)
                    admin_session.assert_icommand(['iput', '-R', 'ufs0', '-r', dirname], 'STDOUT_SINGLELINE', ustrings.recurse_ok_string())

                    # stage to tier 1, everything should have been tiered out
                    sleep(5)
                    invoke_storage_tiering_rule()
                    sleep(5)
                    delay_assert_icommand(admin_session, ['ils', '-l', dirname], 'STDOUT_SINGLELINE', 'ufs1')
                    delay_assert_icommand(admin_session, ['ils', '-l', dirname], 'STDOUT_SINGLELINE', 'ufs0')
                    # Wait for the queue to be emptied and ensure that everything has tiered out from ufs0
                    wait_for_empty_queue(lambda: admin_session.assert_icommand_fail(['ils', '-l', dirname], 'STDOUT', 'ufs0'))

                finally:
                    delay_assert_icommand(admin_session, 'iqdel -a')

                    # cleanup
                    admin_session.assert_icommand(['irm', '-f', '-r', dirname])
                    shutil.rmtree(dirname, ignore_errors=True)

    def test_put_object_limit_lt(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:
                # Put enough objects to force continueInx and set object_limit to one less than that (above MAX_SQL_ROWS)
                file_count = self.max_sql_rows + 2
                admin_session.assert_icommand(['imeta', 'add', '-R', 'ufs0', 'irods::storage_tiering::object_limit', str(file_count - 1)])
                dirname = 'test_put_object_limit_lt'

                try:
                    shutil.rmtree(dirname, ignore_errors=True)
                    last_item_path = os.path.join(dirname, 'junk0' + str(file_count - 1))
                    next_to_last_item_path = os.path.join(dirname, 'junk0' + str(file_count - 2))
                    lib.make_large_local_tmp_dir(dirname, file_count, 1)
                    admin_session.assert_icommand(['iput', '-R', 'ufs0', '-r', dirname], 'STDOUT_SINGLELINE', ustrings.recurse_ok_string())

                    # stage to tier 1, only the last item should not have been tiered out
                    sleep(5)
                    invoke_storage_tiering_rule()
                    sleep(5)
                    delay_assert_icommand(admin_session, ['ils', '-l', dirname], 'STDOUT_SINGLELINE', 'ufs0')
                    delay_assert_icommand(admin_session, ['ils', '-l', dirname], 'STDOUT_SINGLELINE', 'ufs1')
                    # Wait for the queue to be emptied and ensure that everything has tiered out from ufs0 except for 1
                    wait_for_empty_queue(lambda: admin_session.assert_icommand(['ils', '-l', dirname], 'STDOUT', 'ufs0'))
                    # Ensure that exactly 1 item did not tier out
                    _, out, _ = admin_session.assert_icommand(['ils', '-l', dirname], 'STDOUT_SINGLELINE', 'ufs0')
                    self.assertEqual(file_count - 1, out.count('ufs1'))
                    self.assertEqual(1, out.count('ufs0'))

                finally:
                    delay_assert_icommand(admin_session, 'iqdel -a')

                    # cleanup
                    admin_session.assert_icommand(['irm', '-f', '-r', dirname])
                    shutil.rmtree(dirname, ignore_errors=True)

    def test_put_multi_fetch_page(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:
                # Put enough objects to force results paging more than once
                file_count = (self.max_sql_rows * 2) + 1
                dirname = 'test_put_multi_fetch_page'

                try:
                    shutil.rmtree(dirname, ignore_errors=True)
                    lib.make_large_local_tmp_dir(dirname, file_count, 1)
                    admin_session.assert_icommand(['iput', '-R', 'ufs0', '-r', dirname], 'STDOUT_SINGLELINE', ustrings.recurse_ok_string())

                    # stage to tier 1, everything should have been tiered out
                    sleep(5)
                    invoke_storage_tiering_rule()
                    delay_assert_icommand(admin_session, ['ils', '-l', dirname], 'STDOUT_SINGLELINE', 'ufs1')
                    delay_assert(lambda: admin_session.assert_icommand_fail(['ils', '-l', dirname], 'STDOUT_SINGLELINE', 'ufs0'))

                finally:
                    delay_assert_icommand(admin_session, 'iqdel -a')

                    # cleanup
                    admin_session.assert_icommand('irm -r ' + dirname)
                    shutil.rmtree(dirname, ignore_errors=True)

class TestStorageTieringPluginMultiGroupRestage(ResourceBase, unittest.TestCase):
    def setUp(self):
        super(TestStorageTieringPluginMultiGroupRestage, self).setUp()
        with session.make_session_for_existing_admin() as admin_session:
            admin_session.assert_icommand('iqdel -a')
            admin_session.assert_icommand('iadmin mkresc ufs0 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs0', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs1 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs1', 'STDOUT_SINGLELINE', 'unixfilesystem')
            admin_session.assert_icommand('iadmin mkresc ufs2 unixfilesystem '+test.settings.HOSTNAME_1 +':/tmp/irods/ufs2', 'STDOUT_SINGLELINE', 'unixfilesystem')

            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::group example_group 0')
            admin_session.assert_icommand('imeta add -R ufs2 irods::storage_tiering::group example_group 1')

            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::group example_group2 0')
            admin_session.assert_icommand('imeta add -R ufs2 irods::storage_tiering::group example_group2 1')

            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::time 5')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::time 5')
            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R ufs0 irods::storage_tiering::maximum_delay_time_in_seconds 2')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::minimum_delay_time_in_seconds 1')
            admin_session.assert_icommand('imeta add -R ufs1 irods::storage_tiering::maximum_delay_time_in_seconds 2')


    def tearDown(self):
        super(TestStorageTieringPluginMultiGroupRestage, self).tearDown()
        with session.make_session_for_existing_admin() as admin_session:

            admin_session.assert_icommand('iadmin rmresc ufs0')
            admin_session.assert_icommand('iadmin rmresc ufs1')
            admin_session.assert_icommand('iadmin rmresc ufs2')
            admin_session.assert_icommand('iadmin rum')

    def test_put_and_get(self):
        with storage_tiering_configured():
            IrodsController().restart(test_mode=True)
            with session.make_session_for_existing_admin() as admin_session:

                try:
                    filename = 'test_put_file'
                    filepath  = lib.create_local_testfile(filename)
                    admin_session.assert_icommand('iput -R ufs0 ' + filename)
                    admin_session.assert_icommand('ils -L ', 'STDOUT_SINGLELINE', 'rods')
                    sleep(5)
                    invoke_storage_tiering_rule()
                    delay_assert_icommand(admin_session, ['ils', '-l', filename], 'STDOUT_SINGLELINE', 'ufs2')
                    admin_session.assert_icommand('imeta ls -d '+filename, 'STDOUT_SINGLELINE', '--')

                    # test restage to tier 0
                    admin_session.assert_icommand('iget ' + filename + ' - ', 'STDOUT_SINGLELINE', 'TESTFILE')
                    delay_assert_icommand(admin_session, 'ils -L ' + filename, 'STDOUT_SINGLELINE', 'ufs0')
                finally:
                    admin_session.assert_icommand('irm -f ' + filename)




