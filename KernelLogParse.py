import operator

def main():
    f = open('kernellogs', "r")
    list1 = []
    for line in f:
        if line.startswith('-') and '[' in line:
            out = line.split('[')[1].split(']')[0]
            if not (out.startswith('2') or (out.startswith('bug'))):
                list1.append(out)
    prefix_count = cust_dict(list1)
    prefix_count_sort = sorted(prefix_count.items(), key=operator.itemgetter(1), reverse=True)
    prefixes = list(prefix_count)

    print("Your options are:", [k for k, v in prefix_count_sort])
    choice = str(input("Pick prefixes split by ,'s: "))
    choices = choice.split(',')
    strip_choices = [c.strip() for c in choices]

    for a in strip_choices:
        if a not in prefixes:
            print("Invalid choice")
            return

    f.seek(0)
    o = open("output.txt", "w+")
    for line in f:
        for choice in strip_choices:
            starts = "- [" + choice + "]"
            if line.startswith(starts):
                print(line)
                o.writelines(line)
    return


def cust_dict(lst):
    dict = {}
    for item in lst:
        if item not in dict:
            dict[item] = 1
        else:
            dict[item] += 1
    return dict
main()