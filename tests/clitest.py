from nose.tools import assert_raises
from cli.branch import (
    validate_branch,
    BranchValidationException,
    is_branch_empty,
    is_branch_full,
    is_branch_have_dupes
)

valid_branch = 'B1,E1'
invalid_branch = 'B1'


def test_valid_branch():
    assert validate_branch(valid_branch)


def test_invalid_branch_for_empty():
    with assert_raises(BranchValidationException):
        validate_branch('')


def test_invalid_branch_for_full():
    with assert_raises(BranchValidationException):
        validate_branch(invalid_branch)


def test_invalid_branch_for_dupes():
    with assert_raises(BranchValidationException):
        validate_branch(','.join([invalid_branch, invalid_branch]))


def test_is_branch_empty():
    assert is_branch_empty(valid_branch)


def test_is_branch_full():
    assert is_branch_full(valid_branch)


def test_is_branch_have_dupes():
    assert is_branch_have_dupes(valid_branch)


def test_is_branch_empty_raises():
    with assert_raises(BranchValidationException):
        is_branch_empty('')


def test_is_branch_full_raises():
    with assert_raises(BranchValidationException):
        is_branch_full(invalid_branch)


def test_is_branch_dupes_raises():
    with assert_raises(BranchValidationException):
        is_branch_have_dupes(','.join([invalid_branch, invalid_branch]))


def test_is_branch_doesnt_have_dupes():
    with assert_raises(BranchValidationException):
        is_branch_have_dupes(invalid_branch*2)
