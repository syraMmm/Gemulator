import random
import uuid
from consts import *


class Character:
    # traits
    visible_traits = ["容貌", "体质", "家世", "能力", "名望", "学识", "武力"]
    invisible_traits = ["道德", "底线", "善良", "心性", "阅历", "天赋"]

    # behaviors
    behaviors = ["救人", "害人", "容易被害"]

    def __init__(self, name, gender):
        self.id = uuid.uuid1()

        # 基本属性初始化
        self.name = name
        self.gender: Gender = gender
        self.preference: Preference = Preference.random()
        self.job: Job = Job.random()
        self.age = random.randint(0, 80)

        # 人物属性初始化
        self.traits_value = [0] * (len(self.invisible_traits) + len(self.visible_traits))
        for i in range(len(self.visible_traits) + len(self.invisible_traits)):
            self.traits_value[i] = random.randint(1, 100)

        # 人物个性判定
        self.behaviors_value = [True, True, True]
        self.refresh_behavior()

        # 未实装属性
        self.intimacy = 0  # 好感
        self.love = {}  # 钟情人物与钟情好感度
        self.log = {}    # log 存储人物历史进度

    def info_all(self):
        return "角色信息：\r\n" \
               "姓名：%s\t性别：%s\t性格：%s\r\n" \
               "职业：%s\t喜好：%s\r\n" \
               "%s\r\n" \
               "隐藏属性：\r\n" \
               "%s\r\n" \
               "%s\r\n" \
               % (self.name, self.gender.value, self.tag_info(),
                  self.job.value, self.preference.value,
                  self._visible_traits_info(), self._tag_detail_info(), self._invisible_traits_info())

    def info(self):
        return "角色信息：\r\n" \
               "姓名：%s\t性别：%s\t性格：%s\r\n" \
               "职业：%s\t喜好：%s\r\n" \
               "%s\r\n" % (self.name, self.gender.value, self.tag_info(),
                           self.job.value, self.preference.value, self._visible_traits_info())

    def _visible_traits_info(self):
        result = ""
        for i in range(len(self.visible_traits)):
            result += "%s: %02d\r\n" % (self.visible_traits[i], self.traits_value[i])
        return result

    def _invisible_traits_info(self):
        result = ""
        for i in range(len(self.invisible_traits)):
            result += "%s: %02d\r\n" % (self.invisible_traits[i], self.traits_value[i + len(self.visible_traits)])
        return result

    def _tag_detail_info(self):
        behavior_prefix = "不"
        result = ""
        for i in range(len(self.behaviors)):
            if not self.behaviors_value[i]:
                result += behavior_prefix + self.behaviors[i]
            else:
                result += self.behaviors[i]
        return result

    def tag_info(self):
        if self.behaviors_value[Behavior.SAVE.value]:
            if self.behaviors_value[Behavior.HARM.value]:
                if self.behaviors_value[Behavior.HARMED.value]:
                    return "性情中人"
                else:
                    return "城府颇深"
            else:
                if self.behaviors_value[Behavior.HARMED.value]:
                    return "乐善好施"
                else:
                    return "谨小慎微"
        else:
            if self.behaviors_value[Behavior.HARM.value]:
                if self.behaviors_value[Behavior.HARMED.value]:
                    return "桀骜不驯"
                else:
                    return "阴险狡诈"
            else:
                if self.behaviors_value[Behavior.HARMED.value]:
                    return "清冷孤傲"
                else:
                    return "圆滑世故"

    def refresh_behavior(self):
        if self.traits_value[Trait.EXPERIENCE.value] * random.randint(1, 3) / 120 >= 1:
            self.behaviors_value[Behavior.HARMED.value] = False
        else:
            self.behaviors_value[Behavior.HARMED.value] = True
        if self.traits_value[Trait.KINDNESS.value] > 60:
            self.behaviors_value[Behavior.SAVE.value] = True
        else:
            self.behaviors_value[Behavior.SAVE.value] = False
        if self.traits_value[Trait.MORALITY.value] > 60:
            self.behaviors_value[Behavior.HARM.value] = True
        else:
            self.behaviors_value[Behavior.HARM.value] = False

    def inc_trait(self, trait: Trait):
        inc_value = random.randint(1, 5)
        self.traits_value[trait.value] += inc_value
        return inc_value

    def dec_trait(self, trait: Trait):
        dec_value = random.randint(1, 5)
        self.traits_value[trait.value] -= dec_value
        return 0-dec_value

    def will_save(self):
        return self.behaviors_value[Behavior.SAVE.value]

    def will_harm(self):
        return self.behaviors_value[Behavior.HARM.value]

    def will_be_harmed(self):
        return self.behaviors_value[Behavior.HARMED.value]

    def trait_info(self, trait: Trait):
        if trait.value <= len(self.visible_traits) - 1:
            return self.visible_traits[trait.value]
        else:
            return self.invisible_traits[trait.value - len(self.visible_traits)]
