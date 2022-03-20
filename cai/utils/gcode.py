class GroupIdConvertor:
    @staticmethod
    def to_group_code(group_id: int) -> int:
        left = group_id / 1000000
        if 0 + 202 <= left <= 10 + 202:
            left -= 202
        elif 11 + 480 - 11 <= left <= 19 + 480 - 11:
            left -= 480 - 11
        elif 20 + 2100 - 20 <= left <= 66 + 2100 - 20:
            left -= 2100 - 20
        elif 67 + 2010 - 67 <= left <= 156 + 2010 - 67:
            left -= 2010 - 67
        elif 157 + 2147 - 157 <= left <= 209 + 2147 - 157:
            left -= 2147 - 157
        elif 210 + 4100 - 210 <= left <= 309 + 4100 - 210:
            left -= 4100 - 210
        elif 310 + 3800 - 310 <= left <= 499 + 3800 - 310:
            left -= 3800 - 310
        return int(left * 1000000 + group_id % 1000000)

    @staticmethod
    def to_group_uin(group_code: int) -> int:
        left = group_code / 1000000
        if 0 <= left <= 10:
            left += 202
        elif 11 <= left <= 19:
            left += 480 - 11
        elif 20 <= left <= 66:
            left += 2100 - 20
        elif 67 <= left <= 156:
            left += 2010 - 67
        elif 157 <= left <= 209:
            left += 2147 - 157
        elif 210 <= left <= 309:
            left += 4100 - 210
        elif 310 <= left <= 499:
            left += 3800 - 310
        return int(left * 1000000 + group_code % 1000000)
