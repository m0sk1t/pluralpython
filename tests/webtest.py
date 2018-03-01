from web.web import employees_for_add


def test_employee_wo_difference():
    assert employees_for_add('E1,E2', 'E1,E2') == ''


def test_employee_with_difference():
    assert employees_for_add('E1,E2', 'E1,E2,E3') == 'E3'

