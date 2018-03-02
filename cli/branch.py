class BranchValidationException(Exception):
    pass


def is_branch_empty(branch):
    if branch:
        return True
    else:
        raise BranchValidationException('Branch is empty')


def is_branch_full(branch):
    if len(branch.split(',')) > 1:
        return True
    else:
        raise BranchValidationException('Branch does not have any relationship')


def is_branch_have_dupes(branch):
    branch_list = branch.split(',')
    branch_set = set(branch_list)
    if len(branch_list) == len(branch_set):
        return True
    else:
        raise BranchValidationException('Branch contains dupes')


def validate_branch(branch):
    validators = [
        is_branch_empty,
        is_branch_full,
        is_branch_have_dupes
    ]
    try:
        if all([validator for validator in validators if validator(branch)]):
            branch = branch.split(',')
            return branch[0], branch[1:]
    except BranchValidationException as e:
        raise e
