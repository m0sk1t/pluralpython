import re


boss_pattern = '(B\d+){1}?'
employee_pattern = '(E\d+)'
allowed_symbols_pattern = '[EB\d,]+'


class BranchValidationException(Exception):
    pass


def is_branch_have_allowed_symbols(branch):
    if re.match(allowed_symbols_pattern, branch):
        return True
    else:
        raise BranchValidationException('Branch string contains not allowed symbols')


def is_branch_have_boss(branch):
    if re.match(boss_pattern, branch):
        return True
    else:
        raise BranchValidationException('Branch does not have a boss')


def is_branch_have_single_boss(branch):
    if len(re.findall(boss_pattern, branch)) == 1:
        return True
    else:
        raise BranchValidationException('Branch have many bosses')


def is_branch_have_employees(branch):
    employees = branch.split(',')[1:]
    if len(employees) and all([re.match(employee_pattern, employee) for employee in employees]):
        return True
    else:
        raise BranchValidationException('Branch does not contains employees')


def is_branch_have_dupes(branch):
    branch_list = branch.split(',')
    branch_set = set(branch_list)
    if len(branch_list) == len(branch_set):
        return True
    else:
        raise BranchValidationException('Branch contains dupes')


def validate_branch(branch):
    validators = [
        is_branch_have_allowed_symbols,
        is_branch_have_boss,
        is_branch_have_single_boss,
        is_branch_have_employees,
        is_branch_have_dupes
    ]
    try:
        if all([validator for validator in validators if validator(branch)]):
            branch = branch.split(',')
            return branch[0], ','.join(branch[1:])
    except BranchValidationException as e:
        raise e
