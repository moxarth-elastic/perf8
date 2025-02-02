#
# Licensed to Elasticsearch B.V. under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Elasticsearch B.V. licenses this file to you under
# the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import importlib
import sys
from copy import copy
import runpy
import pathlib


def get_plugin_klass(fqn):
    module_name, klass_name = fqn.split(":")
    module = importlib.import_module(module_name)
    return getattr(module, klass_name)


_PLUGINS = []


def register_plugin(klass):
    _PLUGINS.append(klass)


def get_registered_plugins():
    # this import will load all internal plugins modules
    # so they have a chance to register them selves
    from perf8 import plugins  # NOQA

    return _PLUGINS


def get_code(script):
    with open(script, mode="rb") as f:
        return compile(f.read(), "__main__", "exec", dont_inherit=True)


def run_script(script_file, script_args):
    saved = copy(sys.argv[:])
    sys.path[0] = str(pathlib.Path(script_file).resolve().parent.absolute())
    sys.argv[:] = [script_file, *script_args]
    try:
        runpy.run_path(script_file, run_name="__main__")
    except SystemExit:
        pass

    sys.argv[:] = saved
