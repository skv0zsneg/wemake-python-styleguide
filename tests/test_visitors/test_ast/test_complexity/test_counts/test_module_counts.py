import pytest

from wemake_python_styleguide.violations.complexity import (
    TooManyModuleMembersViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.counts import (
    ModuleMembersVisitor,
)

# Multiple module members:

module_with_function_and_class = """
def first(): ...

class Second: ...
"""

module_with_function_and_class_and_method = """
def first(): ...

class Second:
    def method(self): ...
"""

module_with_function_and_async_method = """
def first(): ...

class Second:
    async def method(self): ...
"""

module_with_function_and_classmethod = """
def first(): ...

class Second:
    @classmethod
    def method(cls): ...
"""

module_with_async_function_and_class = """
async def first(): ...

class Second: ...
"""

module_with_methods = """
class First:
    def method(self): ...

class Second:
    def method2(self): ...
"""

module_with_async_methods = """
class First:
    async def method(self): ...

class Second:
    async def method2(self): ...
"""

module_with_classmethods = """
class First:
    @classmethod
    def method(cls): ...

class Second:
    @classmethod
    def method2(cls): ...
"""

module_with_staticmethods = """
class First:
    @staticmethod
    def method(cls): ...

class Second:
    @staticmethod
    def method2(cls): ...
"""

# Single module member:

module_with_single_function = """
def single(): ...
"""

module_with_single_async_function = """
async def single(): ...
"""

module_with_single_class = """
class First:
    @classmethod
    def method(cls): ...

    async def test(self): ...

    def other(self): ...
"""

# regression1779
module_with_overloads = """
@overload
def first(): ...

@typing.overload
def first(): ...

# Only this def counts:
def first(): ...
"""

# Empty:

empty_module = ''


@pytest.mark.parametrize(
    'code',
    [
        empty_module,
        module_with_function_and_class,
        module_with_function_and_class_and_method,
        module_with_function_and_async_method,
        module_with_function_and_classmethod,
        module_with_async_function_and_class,
        module_with_methods,
        module_with_async_methods,
        module_with_staticmethods,
        module_with_classmethods,
        module_with_single_class,
        module_with_overloads,
    ],
)
def test_module_counts_normal(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that classes and functions in a module work well."""
    tree = parse_ast_tree(code)

    visitor = ModuleMembersVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        module_with_function_and_class,
        module_with_function_and_class_and_method,
        module_with_function_and_async_method,
        module_with_function_and_classmethod,
        module_with_async_function_and_class,
        module_with_methods,
        module_with_async_methods,
        module_with_classmethods,
        module_with_staticmethods,
    ],
)
def test_module_counts_violation(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    options,
):
    """Testing that violations are raised when reaching max value."""
    tree = parse_ast_tree(code)

    option_values = options(max_module_members=1)
    visitor = ModuleMembersVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyModuleMembersViolation])
    assert_error_text(visitor, '2', option_values.max_module_members)


@pytest.mark.parametrize(
    'code',
    [
        empty_module,
        module_with_single_function,
        module_with_single_async_function,
        module_with_single_class,
        module_with_overloads,
    ],
)
def test_module_counts_single_member(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Testing that violations are not raised for a single member."""
    tree = parse_ast_tree(code)

    option_values = options(max_module_members=1)
    visitor = ModuleMembersVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
