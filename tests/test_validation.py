# This file is part of CycloneDX Python Lib
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) OWASP Foundation. All Rights Reserved.


from itertools import product
from typing import Tuple
from unittest import TestCase

from ddt import data, ddt, named_data, unpack

from cyclonedx.schema import OutputFormat, SchemaVersion
from cyclonedx.validation import make_schemabased_validator
from tests import UNDEFINED_SCHEMA_VERSIONS


@ddt
class TestGetSchemabasedValidator(TestCase):

    @named_data(
        *([f'{of.name} {sv.name}', of, sv]
          for of, sv in product(OutputFormat, SchemaVersion)
          if sv not in UNDEFINED_SCHEMA_VERSIONS.get(of, ()))
    )
    @unpack
    def test_as_expected(self, of: OutputFormat, sv: SchemaVersion) -> None:
        validator = make_schemabased_validator(of, sv)
        self.assertIs(validator.output_format, of)
        self.assertIs(validator.schema_version, sv)

    @data(
        *(('foo', sv, (ValueError, 'Unexpected output_format')) for sv in SchemaVersion),
        *((of, sv, (ValueError, 'Unsupported schema_version'))
          for of in UNDEFINED_SCHEMA_VERSIONS
          for sv in UNDEFINED_SCHEMA_VERSIONS[of])
    )
    @unpack
    def test_fails_on_wrong_args(self, of: OutputFormat, sv: SchemaVersion, raises_regex: Tuple) -> None:
        with self.assertRaisesRegex(*raises_regex):
            make_schemabased_validator(of, sv)
