from nose.tools import assert_raises
from cli.branch import validate_branch, BranchValidationException


def test_valid_branch():
    assert validate_branch('B1,E1')


def test_invalid_branch():
    with assert_raises(BranchValidationException):
        validate_branch('B1')

