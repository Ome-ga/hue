# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()
from builtins import range
import logging

from datetime import datetime, timedelta
from prometheus_client import Gauge

from desktop.lib.metrics import global_registry
from desktop.models import Document2

LOG = logging.getLogger(__name__)


def num_of_queries():
  try:
    count = Document2.objects.filter(type__istartswith='query-', is_history=True, last_modified__gt=datetime.now() - timedelta(minutes=10)).count()
  except:
    LOG.exception('Could not get num_of_queries')
    count = 0
  return count

global_registry().gauge_callback(
    name='queries.number',
    callback=num_of_queries,
    label='number of queries',
    description='Number of queries were executed in last 10 minutes',
    numerator='users',
)

prometheus_queries_numbers = Gauge('hue_queries_numbers', 'Hue - numbers of queries')
prometheus_queries_numbers.set_function(num_of_queries)