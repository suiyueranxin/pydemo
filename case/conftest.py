import pytest


@pytest.fixture(scope='class', autouse=False)
def fix_class():
    print('fix_class')


@pytest.fixture(scope='function', autouse=False)
def fix_function(request):
    print('fix_function')


@pytest.fixture(scope='function', params=[1, 2, 3])
def p_data(request):
    return request.param

