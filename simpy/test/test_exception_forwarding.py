"""
Tests for forwarding exceptions from child to parent processes.

"""
import pytest

import simpy


def test_error_forwarding(env):
    """Exceptions are forwarded from child to parent processes if there
    are any.

    """
    def child(env):
        raise ValueError('Onoes!')
        yield env.hold(1)

    def parent(env):
        try:
            yield env.start(child(env))
            pytest.fail('We should not have gotten here ...')
        except ValueError as err:
            assert err.args[0] == 'Onoes!'

    env.start(parent(env))
    simpy.simulate(env)


def test_no_parent_process(env):
    """Exceptions should be normally raised if there are no processes
    waiting for the one that raises something.

    """
    def child(env):
        raise ValueError('Onoes!')
        yield env.hold(1)

    def parent(env):
        try:
            env.start(child(env))
            yield env.hold(1)
        except:
            pytest.fail('There should be no error.')

    env.start(parent(env))
    pytest.raises(ValueError, simpy.simulate, env)