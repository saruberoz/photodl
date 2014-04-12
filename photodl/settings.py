#! /usr/bin/env python

# External Imports
import lya
import os

__author__ = 'kyle.walker@zefr.com'


def get_connection_string(settings, psycopg2_format=False):
    """
    Given a dictionary of current settings, form the database connection
    string.
    """

    engine = settings.get('engine', 'mysql')

    user = settings['user']
    password = settings['passwd']
    host = settings['host']
    database = settings['db']
    port = settings['port']

    # MySQL needs extra params
    extra_params = ''
    if engine == "mysql":
        extra_params += "?charset=utf8&use_unicode=1"

    if psycopg2_format:
        if port:
            db_uri = ("host='{0}' dbname='{1}' user='{2}' "
                      "password='{3}' port='{4}'"
                      .format(host, database, user, password, port))
        else:
            db_uri = ("host='{0}' dbname='{1}' "
                      "user='{2}' password='{3}'".
                      format(host, database, user, password))
    elif port:
        db_uri = ('{0}://{1}:{2}@{3}:{4}/{5}{6}'.
                  format(engine, user, password,
                         host, port, database, extra_params))
    else:
        db_uri = ('{0}://{1}:{2}@{3}/{4}{5}'.
                  format(engine, user, password, host, database, extra_params))
    return db_uri


def get_config(root_dir, environment, default_env='photodl'):
    config = lya.AttrDict.from_yaml('{}/defaults.yml'.format(root_dir))
    if environment != default_env:
        # Copy the default settings to requested configuration
        config[environment] = config[default_env]
    try:
        config.update_yaml('{}/settings.yml'.format(root_dir))
    except IOError:
        # Note: Values can also be setup using environment variables.
        pass

    def get_env_vars(prefix, config):
        for key, val in config.iteritems():
            if isinstance(val, dict):
                get_env_vars("{}_{}".format(prefix, key), config[key])
            else:
                new_val = os.environ.get("{}_{}".format(prefix.upper(),
                                                        key.upper()), None)
                if new_val is not None:
                    config[key] = new_val

    get_env_vars(default_env, config[environment])

    # Create DB Connection Strings.
    for cur_db in config[environment].get('databases', []):
        try:
            config[environment].databases[cur_db].conn_string = \
                get_connection_string(config[environment].databases[cur_db])
        except AttributeError:
            print "Error {} is not a valid database entry".format(cur_db)

    return config[environment]
