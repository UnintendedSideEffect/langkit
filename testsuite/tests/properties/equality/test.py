"""
Check that the DSL equality operator tests for equivalence, not pointer
equality.
"""

from __future__ import absolute_import, division, print_function

from langkit.dsl import ASTNode, EnumNode, Field, Struct, UserField, T
from langkit.envs import EnvSpec, add_env, add_to_env
from langkit.expressions import New, Self, langkit_property
from langkit.parsers import Grammar, List, Opt, Tok

from lexer_example import Token
from utils import build_and_run


class EnvStruct(Struct):
    env = UserField(type=T.LexicalEnvType)


class FooNode(ASTNode):

    @langkit_property()
    def env_struct():
        return New(EnvStruct, env=Self.children_env.env_orphan)

    @langkit_property()
    def env_array():
        return Self.children_env.env_orphan.singleton


class HasPlus(EnumNode):
    qualifier = True


class Decl(FooNode):
    has_plus = Field()
    name = Field()
    items = Field()

    env_spec = EnvSpec(
        add_to_env(mappings=New(T.env_assoc, key=Self.name.symbol, val=Self)),
        add_env(),
    )

    @langkit_property(public=True, return_type=T.BoolType)
    def test_env(other=T.FooNode.entity):
        return Self.children_env.env_orphan == other.children_env.env_orphan

    @langkit_property(public=True, return_type=T.BoolType)
    def test_struct(other=T.FooNode.entity):
        return Self.env_struct == other.env_struct

    @langkit_property(public=True, return_type=T.BoolType)
    def test_array(other=T.FooNode.entity):
        return Self.env_array == other.env_array


class Ref(FooNode):
    name = Field()


fg = Grammar('main_rule')
fg.add_rules(
    main_rule=List(fg.decl),
    decl=Decl(Opt('+').as_bool(HasPlus),
              Tok(Token.Identifier, keep=True),
              '(', fg.ref_list, ')'),
    ref_list=List(fg.ref, empty_valid=True),
    ref=Ref(Tok(Token.Identifier, keep=True)),
)
build_and_run(fg, 'main.py')
print('Done')
