from urllib.parse import unquote


def infinite_sequence():
    num = 0
    while num != 10:
        yield num
        num += 1
        yield num
        num += 1


generator = infinite_sequence()


url = unquote(r'https://www.tcharter.ir//tickets/search/0/%D9%85%D8%B4%D9%87%D8%AF-%D8%AA%D9%87%D8%B1%D8%A7')
print(url)
