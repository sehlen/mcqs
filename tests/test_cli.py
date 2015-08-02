import pytest, os
from click.testing import CliRunner
from mcqs import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.main, ['-n2', 'examples/test-exam.tex'])
    assert result.exit_code == 0
    assert not result.exception
    fn1 = 'examples/test-exam-1.tex'
    f1 = open(fn1, 'r')
    fn1 = os.path.abspath(f1.name)
    f1.close()
    os.remove(fn1)
    fn2 = 'examples/test-exam-2.tex'
    f2 = open(fn2, 'r')
    fn2 = os.path.abspath(f2.name)
    f2.close()
    os.remove(fn2)


## def test_cli_with_option(runner):
##     result = runner.invoke(cli.main, ['--as-cowboy'])
##     assert not result.exception
##     assert result.exit_code == 0
##     assert result.output.strip() == 'Howdy, world.'


## def test_cli_with_arg(runner):
##     result = runner.invoke(cli.main, ['Stephan'])
##     assert result.exit_code == 0
##     assert not result.exception
##     assert result.output.strip() == 'Hello, Stephan.'
