import json
import os
from pprint import pprint
from typing import List, Dict

from canvasapi import Canvas
from canvasapi.quiz import QuizSubmissionQuestion, QuizSubmission
from environs import Env
from git import Repo

import fibonacci
import contextlib
import pyramid
import hashlib
from io import StringIO
import re


def get_answers(questions: List[QuizSubmissionQuestion]) -> List[Dict]:
    """Creates answers for Canvas quiz questions"""
    # Formulate your answers - see docs for QuizSubmission.answer_submission_questions below
    # It should be a list of dicts, one per q, each with an 'id' and 'answer' field
    # The format of the 'answer' field depends on the question type
    # You are responsible for collating questions with the functions to call - do not hard code
    # raise NotImplementedError()
    # eg {"id": questions[0].id, "answer": {key: some_func(key) for key in questions[0].answer.keys()}}

    for x in questions:

        print(re.findall('id="(\w+)"', x.question_text))



    # pyramid
    mem_file = StringIO()
    with contextlib.redirect_stdout(mem_file):
        pyramid.print_pyramid(10)

    pyramid_hash = hashlib.sha256(mem_file.getvalue().encode()).hexdigest()[:8]

    print(mem_file.getvalue())
    print(pyramid_hash)

    # fibonacci
    fib = fibonacci.optimized_fibonacci(6)
    print(f"fib is {fib}")

    # summable sequence
    new_seq = fibonacci.SummableSequence(5, 7, 11)
    ss = fibonacci.last_8(new_seq(100000))
    print("new_seq(100000)[-8:]:", ss)

    # assemble return
    test_answer = hashlib.sha256("asdfasdfasdfasdf".encode()).hexdigest()
    response_list = []
    response_list.append({"id": 2476703, "answer": {"1": test_answer, "2": test_answer}})
    response_list.append({"id": 2476706, "answer": 4609})

    return response_list



def get_submission_comments(repo: Repo, qsubmission: QuizSubmission) -> Dict:
    """Get some info about this submission"""
    return dict(
        hexsha=repo.head.commit.hexsha[:8],
        submitted_from=repo.remotes.origin.url,
        dt=repo.head.commit.committed_datetime.isoformat(),
        branch=os.environ.get("TRAVIS_BRANCH", None),  # repo.active_branch.name,
        is_dirty=repo.is_dirty(),
        quiz_submission_id=qsubmission.id,
        quiz_attempt=qsubmission.attempt,
        travis_url=os.environ.get("TRAVIS_BUILD_WEB_URL", None),
    )


if __name__ == "__main__":

    repo = Repo(".")

    # Load environment
    env = Env()
    # Load locally.  this needs to come out at some point.
    env.read_env()

    course_id = env.int("CANVAS_COURSE_ID")
    assignment_id = env.int("CANVAS_ASSIGNMENT_ID")
    quiz_id = env.int("CANVAS_QUIZ_ID")
    as_user_id = env.int("CANVAS_AS_USER_ID", 0)  # Optional - for test student

    if as_user_id:
        masquerade = dict(as_user_id=as_user_id)
    else:
        masquerade = {}

    if repo.is_dirty() and not env.bool("ALLOW_DIRTY", False):
        raise RuntimeError(
            "Must submit from a clean working directory - commit your code and rerun"
        )

    # Load canvas objects
    canvas = Canvas(env.str("CANVAS_URL"), env.str("CANVAS_TOKEN"))
    course = canvas.get_course(course_id, **masquerade)
    assignment = course.get_assignment(assignment_id, **masquerade)
    quiz = course.get_quiz(quiz_id, **masquerade)

    # print(f"the quiz is {quiz}")
    # print(f"the quiz id is {quiz.id}")

    # Begin submissions
    url = "https://github.com/csci-e-29/{}/commit/{}".format(
        os.path.basename(repo.working_dir), repo.head.commit.hexsha
    )  # you MUST push to the classroom org, even if CI/CD runs elsewhere (you can push anytime before peer review begins)

    qsubmission = None
    try:
        # Attempt quiz submission first - only submit assignment if successful
        qsubmission = quiz.create_submission(**masquerade)
        questions = qsubmission.get_submission_questions(**masquerade)

        # Get some basic info to help develop
        for q in questions:
            print("{} - {}".format(q.question_name, q.question_text.split("\n", 1)[0]))

            # MC and some q's have 'answers' not 'answer'
            pprint(
                {
                    k: getattr(q, k, None)
                    for k in ["question_type", "id", "answer", "answers"]
                }
            )

            print()

        # Submit your answers
        answers = get_answers(questions)
        pprint(answers)
        responses = qsubmission.answer_submission_questions(
            quiz_questions=answers, **masquerade
        )

    finally:
        if qsubmission is not None:
            completed = qsubmission.complete(**masquerade)

            # Only submit assignment if quiz finished successfully
            submission = assignment.submit(
                dict(
                    submission_type="online_url",
                    url=url,
                ),
                comment=dict(
                    text_comment=json.dumps(get_submission_comments(repo, qsubmission))
                ),
                **masquerade,
            )

    pass
