from nose.tools import assert_raises
from cli.branch import (
    validate_branch,
    BranchValidationException,
    is_branch_have_boss,
    is_branch_have_dupes,
    is_branch_have_employees,
    is_branch_have_single_boss,
    is_branch_have_disallowed_symbols,
)

valid_branch = 'B1,E1,E2,E3'
invalid_branch = 'E1,E2,E3'


def test_valid_branch():
    assert validate_branch(valid_branch)


def test_invalid_branch():
    with assert_raises(BranchValidationException):
        validate_branch('B1')


def test_is_branch_have_not_disallowed_symbols():
    assert is_branch_have_disallowed_symbols(valid_branch)


def test_is_branch_have_boss():
    assert is_branch_have_boss(valid_branch)


def test_is_branch_have_single_boss():
    assert is_branch_have_single_boss(valid_branch)


def test_is_branch_have_employees():
    assert is_branch_have_employees(valid_branch)


def test_is_branch_have_dupes():
    assert is_branch_have_dupes(valid_branch)


def test_is_branch_have_disallowed_symbols():
    with assert_raises(BranchValidationException):
        is_branch_have_disallowed_symbols('@sD' + valid_branch)


def test_is_branch_doesnt_have_boss():
    with assert_raises(BranchValidationException):
        is_branch_have_boss(invalid_branch)


def test_is_branch_doesnt_have_single_boss():
    with assert_raises(BranchValidationException):
        is_branch_have_single_boss('B1,B2' + invalid_branch)


def test_is_branch_doesnt_have_employees():
    with assert_raises(BranchValidationException):
        is_branch_have_employees('B1,')


def test_is_branch_doesnt_have_dupes():
    with assert_raises(BranchValidationException):
        is_branch_have_dupes(invalid_branch*2)
