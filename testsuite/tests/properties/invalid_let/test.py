from __future__ import absolute_import, division, print_function

from langkit.dsl import ASTNode
from langkit.expressions import Literal, Property, Let
from langkit.parsers import Grammar

from utils import emit_and_print_errors


def run(name, expr):
    """
    Emit and print the errors we get for the below grammar with "expr" as
    a property in ExampleNode.
    """

    global Compound, Expression, FooNode, NullNode, Number

    print('== {} =='.format(name))

    class FooNode(ASTNode):
        pass

    class BarNode(FooNode):
        prop = Property(expr, public=True)

    grammar = Grammar('main_rule')
    grammar.add_rules(
        main_rule=BarNode('example'),
    )
    emit_and_print_errors(grammar)
    print('')


run("Correct code", lambda: Let(lambda a=Literal(1): a))
run("Missing var value", lambda: Let(lambda a: a))
run("Invalid args", lambda: Let(lambda a=Literal(1), *b, **c: a))

print('Done')
