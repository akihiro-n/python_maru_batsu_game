from dataclasses import field
from enum import Enum, IntEnum
from math import dist
from pickle import NONE
from random import random
from time import sleep
import time
from turtle import position
import random

class NotEnabledFieldError(Exception):
    def __str__(self) -> str:
        return ("既に置かれてるフィールドです")


class FieldType(Enum):
    FIELD_MARU = "○"
    FIELD_BATSU = "×"
    FIELD_NONE = ""


class Winner(Enum):
    YOU = "あなたの勝ち"
    CPU = "CPUの勝ち"
    UNKNOWN = ""
    DRAW = "引き分け"


class Player(Enum):
    YOU = 0
    CPU = 1


game_field_state: dict = {
    0: FieldType.FIELD_NONE,
    1: FieldType.FIELD_NONE,
    2: FieldType.FIELD_NONE,
    3: FieldType.FIELD_NONE,
    4: FieldType.FIELD_NONE,
    5: FieldType.FIELD_NONE,
    6: FieldType.FIELD_NONE,
    7: FieldType.FIELD_NONE,
    8: FieldType.FIELD_NONE,
}

winners_pattern: list[list[int]] = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [3, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


def draw_current_game_field(state: dict) -> str:
    screen = ""

    for index in state:
        item = state.get(index)
        required_new_line = (index + 1) % 3 == 0  # 3列ごとに改行

        field_value: str
        if item == FieldType.FIELD_NONE:
            field_value = str(index)
        else:
            field_value = item.value

        if required_new_line:
            screen += field_value + "\n"
        else:
            screen += field_value + " "

    return screen


def is_empty_filed(position: int) -> bool:
    return game_field_state.get(position) == FieldType.FIELD_NONE


def put_field(position: int, current: Player, state: dist) -> NONE:
    if current == Player.YOU:
        state[position] = FieldType.FIELD_MARU
    else:
        state[position] = FieldType.FIELD_BATSU


def input_cpu() -> int:
    return random.randrange(8)


def input_next_player(current: Player, message: str) -> int:
    if current == Player.YOU:
        return input(message)
    else:
        return input_cpu()


def get_next_player(current: Player) -> Player:
    if current == Player.YOU:
        return Player.CPU
    return Player.YOU


def game_start() -> NONE:
    current_player = Player.YOU
    while True:
        winner = get_winner()
        if winner == Winner.UNKNOWN:
            current_player = get_next_player(current=current_player)
            play_next_step(current_player=current_player)
            continue
        else:
            print(draw_current_game_field(state=game_field_state))
            print("結果" + str(winner.value))
            break


def play_next_step(current_player: Player) -> NONE:
    print(draw_current_game_field(state=game_field_state))
    input_position: int

    if current_player == Player.CPU:
        print("CPUが次の手を考えています")
        time.sleep(1)

    input_position_text = input_next_player(current_player, "あなたのターンです")

    while True:
        try:
            input_position = int(input_position_text)
            if input_position >= 0 and input_position <= 9:
                if is_empty_filed(input_position):
                    put_field(input_position, current_player, game_field_state)
                    break
                else:
                    raise NotEnabledFieldError()
            else:
                raise ValueError()
        except ValueError:
            input_position_text = input_next_player(
                current_player, "1から９の数字で入力して")
        except NotEnabledFieldError:
            input_position_text = input_next_player(
                current_player, "既に置かれてるフィールドです")


def none_enabled_field() -> bool:
    for index in game_field_state:
        state = game_field_state.get(index)
        if state == FieldType.FIELD_NONE:
            return False
    return True


def get_winner() -> Winner:
    for row in winners_pattern:
        field_types = list(
            map(lambda number: game_field_state.get(number),  row))
        you_win = len(
            list(filter(lambda type: type == FieldType.FIELD_MARU, field_types))) == len(row)
        cpu_win = len(
            list(filter(lambda type: type == FieldType.FIELD_BATSU, field_types))) == len(row)
        draw = none_enabled_field()
        if you_win:
            return Winner.YOU
        elif cpu_win:
            return Winner.CPU
       
    if none_enabled_field():
        return Winner.DRAW
    else:
        return Winner.UNKNOWN


game_start()
