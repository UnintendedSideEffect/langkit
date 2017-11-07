from __future__ import absolute_import, division, print_function

from os import path

from langkit.diagnostics import Diagnostics, DiagnosticError
from langkit.dsl import ASTNode, abstract
from langkit.parsers import Grammar


Diagnostics.set_lang_source_dir(path.abspath(__file__))


@abstract
class FooNode(ASTNode):
    pass


class ExampleNode(FooNode):
    pass


grammar = Grammar('main_rule')
grammar.add_rules(
    sec_rule=ExampleNode('example'),
)

try:
    grammar.add_rules(
        sec_rule=ExampleNode('example'),
        main_rule=ExampleNode(grammar.sec_rule)
    )
except DiagnosticError:
    # Diagnostics are supposed to be printed on standard output, no need to do
    # anything else.
    pass

print('Done')
