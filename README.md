<!--This README is auto-generated from `docs/README.md`. Do not edit this file directly.-->

[![Build Status](https://travis-ci.org/ickc/csv2table.svg?branch=master)](https://travis-ci.org/ickc/csv2table) [![GitHub Releases](https://img.shields.io/github/tag/ickc/csv2table.svg?label=github+release)](https://github.com/ickc/csv2table/releases) [![PyPI version](https://img.shields.io/pypi/v/csv2table.svg)](https://pypi.python.org/pypi/csv2table/) [![Development Status](https://img.shields.io/pypi/status/csv2table.svg)](https://pypi.python.org/pypi/csv2table/) [![Python version](https://img.shields.io/pypi/pyversions/csv2table.svg)](https://pypi.python.org/pypi/csv2table/) <!-- [![Downloads](https://img.shields.io/pypi/dm/csv2table.svg)](https://pypi.python.org/pypi/csv2table/) --> ![License](https://img.shields.io/pypi/l/csv2table.svg) [![Coveralls](https://img.shields.io/coveralls/ickc/csv2table.svg)](https://coveralls.io/github/ickc/csv2table) <!-- [![Scrutinizer](https://img.shields.io/scrutinizer/g/ickc/csv2table.svg)](https://scrutinizer-ci.com/g/ickc/csv2table/) -->

A simple cli that uses terminaltables to convert CSV into table in plain text. For example, the resulted table is a valid pandoc grid\_table. Kramdown uses this syntax as well. If the CSV cell contains markdown element, it will be contained in the grid table output as is.