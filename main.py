# Иммитация игры Scrabble
from random import sample

# Исходный словарь с буквами
dict_alfas = {"а": 8, "б": 2, "в": 4, "г": 2, "д": 4, "е": 8, "ё": 1, "ж": 1, "з": 2, "и": 5, "й": 1, "к": 4, "л": 4,
              "м": 3, "н": 5, "о": 10, "п": 4, "р": 5, "с": 5, "т": 5, "у": 4, "ф": 1, "х": 1, "ц": 1, "ч": 1, "ш": 1,
              "щ": 1, "ъ": 1, "ы": 2, "ь": 2, "э": 1, "ю": 1, "я": 2}


def list_words():
    """
    Функция считывает из файла слова и возвращает кортеж из допустимых слов
    """
    with open('ru_word.txt', encoding='utf-8') as file:
        words = tuple(map(str.strip, file.readlines()))
        return words


def choice_letters(n: int):
    """
    Функция возвращает случайный список из n букв из словаря dict_alfas и уменьшает количество букв в словаре
    """
    let_string = ''.join([k * v for k, v in dict_alfas.items()])
    letters = sample(let_string, n)
    for letter in letters:
        dict_alfas[letter] -= 1
    return letters


def welcome():
    """
    Функция выводит приветствие и запрашивает имена игроков, возвращает словарь игроков, в котором по номеру игрока
    список с его именем, очками (0) и пустым списком под буквы)
    """
    print('Привет.\nМы начинаем играть в Scrabble')
    name_1 = input('Как зовут первого игрока? <<< ').lower().strip().capitalize()
    name_2 = input('Как зовут второго игрока? <<< ').lower().strip().capitalize()
    return {1: [name_1, 0, []], 2: [name_2, 0, []]}


def chek_word(number):
    """
    Функция принимает на вход номер игрока, получает ответ игрока и проверяет валидность слова, что слово
    составлено из букв игрока и отсутствие его в списке использованных слов, если слово уже было или не верно
    использованы буквы предлагает повторить ход, возвращает валидное слово или False, если игрок ввел неверное слово.
    Также возвращает флаг остановки игры, если пользователь ввел stop или стоп.
    """
    while True:
        word = input('<<< ').lower().strip()
        if word == 'stop' or word == 'стоп':
            return 'stop'
        if word in used_words:
            print('Такое слово уже было, найдите другое')
            continue
        elif word in valid_words:
            chek_list = user_list[number][2].copy()
            for letter in word:
                if letter in chek_list:
                    chek_list.remove(letter)
                else:
                    print('Вы использовали букву, которой у вас не было, попробуйте еще раз')
                    break
            else:
                used_words.append(word)
                return word
            continue
        return False


def game():
    """
    Функция основного цикла игры.
    """
    is_game = True  # флаг продолжения игры
    player = 1  # текущий номер игрока
    score = {2: 2, 3: 3, 4: 6, 5: 7, 6: 8, 7: 10, 8: 11}  # словарь с баллами для длины слова
    while is_game:
        letters = ', '.join(user_list[player][2])
        print(f'Ходит {user_list[player][0]}. Твои буквы "{letters}"')
        user_answer = chek_word(player)
        if user_answer and user_answer != 'stop':
            for letter in user_answer:
                user_list[player][2].remove(letter)
            points = score[len(user_answer)]
            new_letters = choice_letters(len(user_answer))
            new_letters_str = ', '.join(new_letters)
            print(f'Такое слово есть\n{user_list[player][0]} получает {points} баллов\n'
                  f'Добавляю буквы "{new_letters_str}"')
            user_list[player][2].extend(new_letters)
            user_list[player][1] += points
        elif user_answer is False:
            new_letter = choice_letters(1)
            new_letter_str = ', '.join(new_letter)
            print(f'Такого слова нет\n{user_list[player][0]} не получает очков\n'
                  f'Добавляю буквы "{new_letter_str}"')
            user_list[player][2].extend(new_letter)
        else:
            is_game = False
        player = 2 if player == 1 else 1


def get_winner():
    """
    Функция выявляет победителя или ничью, выводит счет
    """
    if user_list[1][1] > user_list[2][1]:
        winner = 1
    elif user_list[1][1] < user_list[2][1]:
        winner = 2
    else:
        winner = 3
    if winner == 3:
        print('Ничья')
        print(f'Счет {user_list[1][1]} : {user_list[2][1]}')
    else:
        print(f'Выигрывает {user_list[winner][0]}')
        other = 1 if winner == 2 else 2
        print(f'Счет {user_list[winner][1]} : {user_list[other][1]}')


if __name__ == '__main__':
    used_words = []  # Список использованных игроками слов
    user_list = welcome()  # словарь игроков по номеру игрока
    valid_words = list_words()  # список всех допустимых слов
    for i in range(1, 3):
        user_list[i][2] = choice_letters(7)
    print(f'{user_list[1][0]} vs {user_list[2][0]} раздаю случайные буквы')
    for i in range(1, 3):
        letters = ', '.join(user_list[i][2])
        print(f'{user_list[i][0]} - буквы "{letters}"\n')
    game()
    get_winner()
