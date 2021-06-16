#!/usr/bin/env python3
from flashcards_model import Flashcard, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def listen_option():
    allowed_opts = ('1', '2', '3')
    option = input('')
    if option in allowed_opts:
        return option
    else:
        print(f'{option} is not an option')
        return False


def main_menu():
    print('1. Add flashcards\n'
          '2. Practice flashcards\n'
          '3. Exit')


def update_menu(item: Flashcard):
    while True:
        option = input('press "d" to delete the flashcard:\n'
                       'press "e" to edit the flashcard:')
        if option in ('d', 'e'):
            break
        else:
            print(f'{option} is no an option')
    if option == 'e':
        print(f'current question: {item.question}')
        new_question = input(f'please write a new question:')
        if new_question:
            item.question = new_question
            session.commit()

        print(f'current answer: {item.answer}')
        new_answer = input(f'please write a new answer:')
        if new_answer:
            item.answer = new_answer
            session.commit()
    else:
        session.delete(item)
        session.commit()


def box_handler(item: Flashcard):
    while True:
        option = input('press "y" if your answer is correct:\n'
                       'press "n" if your answer is wrong:')
        if option in ('y', 'n'):
            break
        else:
            print(f'{option} is no an option')

    if option == 'y':
        item.box_number += 1
        if item.box_number > 3:
            session.delete(item)
            session.commit()
    else:
        item.box_number = 1


def practice_flashcards():
    num_session = 1
    items = tuple(session.query(Flashcard).filter(Flashcard.box_number<=num_session))
    if not items:
        print('There is no flashcard to practice!')
    else:
        for i in range(len(items)):
            print(f'Question: {items[i].question}')
            while True:
                option = input('press "y" to see the answer:\n'
                               'press "n" to skip:\n'
                               'press "u" to update:')
                if option in ('y', 'n', 'u'):
                    break
                else:
                    print(f'{option} is not an option')

            if option == 'y':
                print(f'Answer: {items[i].answer}')
                box_handler(items[i])
                continue
            elif option == 'n':
                box_handler(items[i])
                continue
            else:
                update_menu(items[i])

        num_session += 1


def add_flashcards():
    while True:
        print('1. Add a new flashcard\n'
              '2. Exit')
        option = listen_option()
        if not option:
            # back to the sub menu if the option was incorrect
            continue
        if option == '1':
            while True:
                question = input('Question:')
                if question != '':
                    break
            while True:
                answer = input('Answer:')
                if answer != '':
                    break
            # add new flashcard record to the db
            new_flashcard = Flashcard(question=question, answer=answer, box_number=1)
            session.add(new_flashcard)
            session.commit()
            # back to the sub menu
            continue
        else:
            # exit to the main menu
            return


def main():
    running = True
    while running:
        main_menu()
        option = listen_option()
        if option:
            if option == '1':
                add_flashcards()
            elif option == '2':
                practice_flashcards()
            else:
                running = False

    print('Bye!')


if __name__ == '__main__':
    main()
