import random
import time


class TicTacToe:
    """
    Класс игры 'Обратные крестики-нолики'
    """
    # у нас размер 10 на 10,
    # не будем дописывать доп. переменную для количества столбцов
    COUNT_ROWS_OR_COLUMNS = 10

    COUNT_INPUT_FOR_LOST = 5
    SEPARATE_LINE = f'{"-" * 40}'

    # больше данного индекса нет смысла проверять количество Х/О по вертикали,
    # а также диагонали ниже
    MAX_VERTICAL_AND_DIAG_IDX = 60

    MIN_LEFT_DIAG_IDX = 5
    MIN_EX_RIGHT_DIAG_IDX = 6
    MAX_EX_RIGHT_DIAG_IDX = 9

    # шаг индекса для диагонали вправо вниз
    STEP_DIAG_RIGHT = 11

    # шаг индекса для диагонали влево вниз
    STEP_DIAG_LEFT = 9

    # количество клеток
    COUNT_CELLS = COUNT_ROWS_OR_COLUMNS ** 2

    table = list(range(1, COUNT_CELLS + 1))

    def __init__(self, player_token):
        self.PLAYER_TOKEN = player_token
        if player_token == 'X':
            self.COMP_TOKEN = 'O'
        else:
            self.COMP_TOKEN = 'X'

    def draw_table(self):
        """
        Отрисовывает игровую таблицу
        """
        for i in range(self.COUNT_ROWS_OR_COLUMNS):
            row = f'{self.SEPARATE_LINE}\n'
            for j in range(self.COUNT_ROWS_OR_COLUMNS):
                num_table = self.table[j + i * self.COUNT_ROWS_OR_COLUMNS]
                row += f'| {num_table}'
                if i == 0 or isinstance(num_table, str):
                    row += ' '
                elif num_table == self.table[-1]:
                    row += f'\n{self.SEPARATE_LINE}'

            print(row)

    def take_input(self):
        """
        Пользовательский ход
        """
        valid = False
        while not valid:
            player_answer = input("Куда поставим " + self.PLAYER_TOKEN + "? ")
            try:
                player_answer = int(player_answer)
            except ValueError:
                print("Некорректный ввод. Вы уверены, что ввели число?")
                continue
            if 1 <= player_answer <= 100:
                if str(self.table[player_answer - 1]) not in "XO":
                    self.insert_element(
                        position=player_answer,
                        token=self.PLAYER_TOKEN,
                    )
                    valid = True
                else:
                    print("Эта клеточка уже занята")
            else:
                print(
                    "Некорректный ввод. "
                    "Введите число от 1 до 100 чтобы походить."
                )

    def insert_element(self, position, token):
        """
        Вставляет элемент на позицию
        """
        self.table[position - 1] = token

    def make_move(self):
        """
        Ход компьютера
        """
        # алгоритм пока простой - рандомно генерируется позиция,
        # проверяется ход на проигрыш с этой позицией,
        # если ход проигрышный, генерируется другой,
        # до тех пор, пока не найдется
        # не проигрышная позиция
        # либо пока не останется других вариантов

        # генерируем список из пустых клеток
        empty_cells = [i for i in self.table if isinstance(i, int)]

        # эту позицию будем проверять после вставки
        position = self.set_random_position(
            empty_cells=empty_cells,
        )

        # будем возвращать эту переменную в False в случае,
        # если не проигрышный ход был найден до того,
        # как осталась 1 свободная клетка
        need_check = True

        # если у нас осталась 1 пустая клетка, то проверять не будем
        while len(empty_cells) > 1:
            # если после вставки элемента на эту позицию мы проигрываем,
            # то ищем другую позицию
            if self.check_lost(token=self.COMP_TOKEN):
                # сначала из empty_cells удалим нашу невыигрышную позицию
                empty_cells.remove(position)

                # также нужно убрать наш проигрышный ход
                self.insert_element(
                    position=position,
                    token=position,
                )

                # после чего достанем рандомно другую позицию,
                # вставим её и на след. итерации будем её проверять
                position = self.set_random_position(
                    empty_cells=empty_cells,
                )
            else:
                # если мы нашли не проигрышную позицию
                # до окончания количества свободных клеток (более 1),
                # то последующая проверка на проигрыш не нужна
                need_check = False
                break
        return need_check

    def set_random_position(self, empty_cells):
        """
        Находит рандомно позицию и вставляет элемент на эту позицию
        """
        position = random.choice(empty_cells)
        self.insert_element(
            position=position,
            token=self.COMP_TOKEN
        )

        return position

    def check_lost(self, token):
        """
        Проверка на проигрыш
        """
        # алгоритм проверки - идем последовательно по таблице,
        # если элемент в этой таблице Х или О,
        # то начинаем проверять горизонталь
        # и вертикаль на проигрыш (совпадение 5 элементов),
        # и диагонали вниз влево и вправо
        for i in range(len(self.table)):
            if self.table[i] == token:

                # по горизонтали есть смысл
                # проверять только для чисел 1-6, 11-16 и т.п
                if i % self.COUNT_ROWS_OR_COLUMNS <= (
                        self.COUNT_ROWS_OR_COLUMNS - self.COUNT_INPUT_FOR_LOST
                ):
                    # проверяем по горизонтали
                    if self.check_sequence(
                            start=i + 1,  # начинаем проверять со след элемента
                            stop=i + self.COUNT_INPUT_FOR_LOST,
                            step=1,
                            token=token,
                    ):
                        return True

                # по вертикали нет смысла проверять
                # для индекса больше 60
                if i < self.MAX_VERTICAL_AND_DIAG_IDX:
                    # проверяем по вертикали
                    if self.check_sequence(
                            start=i + self.COUNT_ROWS_OR_COLUMNS,
                            stop=i + self.COUNT_ROWS_OR_COLUMNS * self.COUNT_INPUT_FOR_LOST,  # noqa
                            step=self.COUNT_ROWS_OR_COLUMNS,
                            token=token,
                    ):
                        return True

                # по диагонали вправо вниз также нет смысла проверять
                # для индекса больше 60,
                # и для индекса в пределах от 6 до 9
                if (
                        i < self.MIN_EX_RIGHT_DIAG_IDX or i > self.MAX_EX_RIGHT_DIAG_IDX  # noqa
                ) and i < self.MAX_VERTICAL_AND_DIAG_IDX:
                    if self.check_sequence(
                            start=i+self.STEP_DIAG_RIGHT,
                            stop=self.COUNT_CELLS,
                            step=self.STEP_DIAG_RIGHT,
                            token=token,
                    ):
                        return True

                # по диагонали влево вниз нет смысла проверять
                # для индекса менее 5 и более 60
                if self.MIN_LEFT_DIAG_IDX < i < self.MAX_VERTICAL_AND_DIAG_IDX:
                    if self.check_sequence(
                            start=i+self.STEP_DIAG_LEFT,
                            stop=self.COUNT_CELLS,
                            step=self.STEP_DIAG_LEFT,
                            token=token,
                    ):
                        return True

        return False

    def check_sequence(self, start, stop, step, token):
        """
        Проверяет вертикаль/горизонталь/диагональ на проигрыш
        """
        count = 1
        for j in range(start, stop, step):
            if self.table[j] == token:
                count += 1
            else:
                break

        if self.check_count(
                count=count,
        ):
            return True

    def check_count(self, count):
        """
        Сравнивает количество элементов
        количеству, соотв. проигрышному
        """
        if count >= self.COUNT_INPUT_FOR_LOST:
            # проиграл
            return True
        return False

    @staticmethod
    def print_sep():
        """
        Печатает перенос строки
        """
        print(sep='\n')

    def run(self):
        """
        Запуск игрового процесса
        """
        if self.PLAYER_TOKEN == 'X':
            # крестики ходят первыми
            count = 0
            diff = 0
        else:
            count = 1
            diff = 1

        # после хода этим элементом,
        # будем проверять этот элемент на проигрыш
        check_token = None

        while True:
            #  игра длится, пока кто-то не проиграл,
            #  или пока все клетки не заполнены
            self.print_sep()
            self.draw_table()
            if count % 2 == 0:
                # нужна ли проверка на проигрыш
                # ход пользователя будем проверять
                need_check = True

                self.take_input()
                check_token = self.PLAYER_TOKEN
            else:
                # пусть пользователь считает,
                # что компьютеру нужно время на подумать
                time.sleep(1)

                # если переменная в False, значит,
                # проверка на проигрыш не нужна - в методе хода компьютера
                # уже была выполнена проверка, и ход не проигрышный
                need_check = self.make_move()
                check_token = self.COMP_TOKEN
            count += 1
            if count >= self.COUNT_INPUT_FOR_LOST + diff and need_check:
                if self.check_lost(
                        token=check_token,
                ):
                    # отрисуем напоследок таблицу
                    self.print_sep()
                    self.draw_table()

                    if check_token == self.PLAYER_TOKEN:
                        msg = 'Вы проиграли'
                    else:
                        msg = 'Вы выиграли'

                    print(f'Game over. {msg}')
                    break

            if count == self.COUNT_CELLS + diff:
                print('Ничья')
                break


if __name__ == '__main__':

    while True:
        player_token = str(
            input(
                'Приветствуем вас в игре "Обратные крестики-нолики". '
                'Пожалуйста, выберите, каким элементом '
                'будете ходить (X или O, ввод латиницей):'
            )
        ).upper()

        if player_token in 'XO':
            TicTacToe(
                player_token=player_token,
            ).run()
            break
        else:
            print('Нужно ввести X или O')
