import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_question_starts_with_no_choices():
    question = Question(title='q1')
    assert len(question.choices) == 0

def test_add_correct_choice():
    question = Question(title='q1')
    choice = question.add_choice('resposta certa', True)
    assert choice.is_correct

def test_add_multiple_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', False)
    question.add_choice('c', True)
    assert len(question.choices) == 3

def test_choice_ids_are_sequential():
    question = Question(title='q1')
    c1 = question.add_choice('a', False)
    c2 = question.add_choice('b', False)
    assert c2.id == c1.id + 1

def test_remove_choice_by_id():
    question = Question(title='q1')
    question.add_choice('a', False)
    choice = question.add_choice('b', False)
    question.remove_choice_by_id(choice.id)
    assert len(question.choices) == 1

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', False)
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_set_correct_choices():
    question = Question(title='q1')
    c1 = question.add_choice('a', False)
    question.add_choice('b', False)
    question.set_correct_choices([c1.id])
    assert question.choices[0].is_correct
    assert not question.choices[1].is_correct

def test_correct_selected_choices_returns_right_ids():
    question = Question(title='q1')
    c1 = question.add_choice('certa', True)
    c2 = question.add_choice('errada', False)
    result = question.correct_selected_choices([c1.id])
    assert c1.id in result
    assert c2.id not in result

def test_exceed_max_selections_raises_exception():
    question = Question(title='q1', max_selections=1)
    c1 = question.add_choice('a', True)
    c2 = question.add_choice('b', True)
    with pytest.raises(Exception):
        question.correct_selected_choices([c1.id, c2.id])

def test_invalid_points_raises_exception():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_choice_with_empty_text_raises_exception():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('', False)

def test_remove_invalid_choice_id_raises_exception():
    question = Question(title='q1')
    question.add_choice('a', False)
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)