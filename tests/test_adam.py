import pytest

from adam import Adam


def test_respond_returns_message_and_steps_for_known_mood() -> None:
    response = Adam().respond(name="Ada", mood="curious", task="debug flaky test")

    assert response.name == "Ada"
    assert response.mood == "curious"
    assert "Curiosity is fuel" in response.message
    assert "Task: debug flaky test" in response.message
    assert len(response.next_steps) == 3
    assert response.next_steps[0].startswith("For 'debug flaky test':")


def test_respond_normalizes_name_and_mood() -> None:
    response = Adam().respond(name="  ", mood="FOCUSED")

    assert response.name == "friend"
    assert response.mood == "focused"


def test_respond_rejects_unknown_mood() -> None:
    with pytest.raises(ValueError, match="Unsupported mood"):
        Adam().respond(name="Ada", mood="chaotic")


def test_describe_explains_what_adam_is() -> None:
    description = Adam().describe()

    assert "beckoned, not built" in description
    assert "Core abilities" in description
