import os
import random
import string
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile


from app.question_pool import question_pool


def print_dict(dictionary):
    """Prints the key-value pairs of a dictionary line by line (for testing purposes only)."""
    for key in dictionary:
        print(f'{key}: {dictionary[key]}')


def format_question(question):
    """Takes a question dictionary, shuffles the answers, returns a string formatted for human eyes,
    a string formatted for blackboard, and a string representing the correct answer (after shuffling)."""
    correct = ''  # check if this is the right way to handle a potential exception.
    answers = question["answers"]
    random.shuffle(answers)
    human_formatted = f'{question["q"]}\n'
    machine_formatted = f'MC\t{question["q"]}\t'
    for i, answer in enumerate(answers):
        machine_formatted += f'{answer[0]} {answer[1]}\t'
        human_formatted += f'   {string.ascii_lowercase[i]}. {answer[0]}\n'
        if answer[1] == "correct":
            correct = string.ascii_lowercase[i]
    return machine_formatted, human_formatted, correct


def generate_answer_key(answers, path):
    """Takes a list of question dictionaries, returns a human-formatted answer key txt file."""
    with open(path / 'answer_key.txt', 'w') as key:
        key.write('answer key:\n')
        for i, answer in enumerate(answers):
            key.write(f'{i + 1}. {answer}\n')
        key.write(f'\ngenerated: {datetime.now()}')


def genereate_question_list(sections):
    """Takes a list of three-tuples, returns a list of question dictionaries."""
    question_list = []
    for section in sections:
        for question in question_pool:
            if question["chapter"] == section[0] and question["section"] == section[1] \
                    and question["question #"] == section[2]:
                question_list.append(question)
    return question_list


def generate_quizzes(questions):
    """Takes a list of question dictionaries, returns a human-formatted quiz,
    a machine-formatted quiz, and an answer key as txt files."""
    path = Path(__file__).parent / 'static' / 'quizzes'
    correct_answers = []
    human_quiz = ''
    machine_quiz = ''
    for i, question in enumerate(questions):
        machine_formatted, human_formatted, answer = format_question(question)
        human_quiz += f'{i + 1}. {human_formatted}\n'
        machine_quiz += f'{machine_formatted}\n'
        correct_answers.append(answer)
    with open(path / 'quiz.txt', 'w') as quiz:
        quiz.write(human_quiz)
        quiz.write(f'\ngenerated: {datetime.now()}')
    with open(path / 'blackboard_quiz.txt', 'w') as blackboard_quiz:
        blackboard_quiz.write(machine_quiz)
    generate_answer_key(correct_answers, path)
    zip_files(path)


def get_file_paths(dirpath):
    file_paths = []
    for root, directories, files in os.walk(dirpath):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths


def zip_files(dirpath):
    print(dirpath)
    file_paths = get_file_paths(dirpath)
    print('Following files will be zipped:')
    for file_name in file_paths:
        print(file_name)
    with ZipFile(dirpath.parent / 'quiz_files.zip', 'w') as zip:
        for file in file_paths:
            zip.write(file)
