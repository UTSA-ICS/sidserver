# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sqlalchemy

from sidserver.common.sql import migration_helpers


def list_constraints(migrate_engine):
    meta = sqlalchemy.MetaData()
    meta.bind = migrate_engine
    assignment_table = sqlalchemy.Table('assignment', meta, autoload=True)
    role_table = sqlalchemy.Table('role', meta, autoload=True)

    constraints = [{'table': assignment_table,
                    'fk_column': 'role_id',
                    'ref_column': role_table.c.id}]
    return constraints


def upgrade(migrate_engine):
    # SQLite does not support constraints, and querying the constraints
    # raises an exception
    if migrate_engine.name == 'sqlite':
        return
    migration_helpers.remove_constraints(list_constraints(migrate_engine))
