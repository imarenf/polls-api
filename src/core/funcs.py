from exceptions import UnknownQuestionId, IncorrectQuestionId


def get_poll_data(data):
    poll_data = {
        'title': data['title'],
        'context': data['context'],
        'end_date': data.get('end_date', default='')
    }
    return poll_data


def validate_question_key(key):
    if not key.startswith('question_'):
        raise IncorrectQuestionId


def get_questions_data(data, poll):
    questions_data = []
    for key, text in data.items():
        validate_question_key(key)
        questions_data.append({'poll': poll,
                               'question_text': text})
    return questions_data


def get_pk(key):
    if key.startswith('answer_'):
        return int(key[7:])
    else:
        raise UnknownQuestionId


def get_answers_data(view, data, current_user):
    answers_data = [{'question': view.get_question_by_pk(get_pk(key)),
                     'answer_text': text, 'user': current_user}
                    for key, text in data.items()]
    return answers_data

