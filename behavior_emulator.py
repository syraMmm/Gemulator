from character import Character
from event import Event
import utils
from consts import Gender, Trait
import random
import copy


def show_npc_info(npc, traits_visible):
    if traits_visible:
        info = "新增" + npc.info_all()
    else:
        info = "新增" + npc.info()
    print(info)


def init_character(num, traits_visible):
    npc_list = []
    for i in range(num):
        gender = Gender.random()
        npc_list.append(Character(utils.random_name_by_gender(gender), gender))
        npc = copy.deepcopy(npc_list[i])
        show_npc_info(npc, traits_visible)
    return npc_list


def start_emulator(num, traits_visible):
    if num < 2:
        print("人数少于2，无法生成事件")
        return
    npc_list = init_character(num, traits_visible)
    print("输入回车开启事件，按q结束，s显示人物性格，a显示人物信息\r\n")
    c = input()
    while True:
        # time.sleep(1.5)
        if c == "q":
            break
        elif c == "s":
            for n in npc_list:
                cypher = "%s\t当前性格: %s\r\n" % (n.name, n.tag_info())
                print(cypher)
        elif c == "a":
            for n in npc_list:
                show_npc_info(n, traits_visible)
        else:
            first_npc = random.randint(0, num - 1)
            second_npc = random.randint(0, num - 1)
            while first_npc == second_npc:
                second_npc = random.randint(0, num - 1)
            e = Event(npc_list[first_npc], npc_list[second_npc], Trait.random())
            e.info()
        c = input()


if __name__ == '__main__':
    num_npc = int(input("请输入初始化人物个数："))
    con = input("是否显示隐藏属性?(y/n)")
    if con.startswith("y") or con.startswith("Y"):
        show_invisible_traits = True
    else:
        show_invisible_traits = False

    start_emulator(num_npc, show_invisible_traits)

