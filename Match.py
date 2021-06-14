#! /usr/bin/env python3
import sys, msvcrt, ctypes, re

class Match:
    def __init__(self, raw):
        self.rawString = raw

        self.regex = re.compile(r'( - )(\w)(\w*)(\w)')
        self.repl = r' \2*\4'

    def sub(self):
        result = self.regex.sub(lambda m: ' ' + m.group(2) + '*' * len(m.group(3)) + m.group(4), self.rawString)

        print('\nLambda 運算式：\n"' + result + '"')

    def run(self):
        print('比對模式： "{}"'.format(self.regex.pattern))
        print('\n輸入字串：\n"{}"'.format(self.rawString))

        print('\n取代模式： "{}"'.format(self.repl))
        result = self.regex.sub(self.repl, self.rawString)

        print('\n結果字串：\n"{}"'.format(result))

        print('\n反向參考：')

        i = 0
        prev = None
        result = []

        for m in self.regex.finditer(self.rawString):
            i += 1
            print(r'{}{}. \3 "{}"'.format(('\n' if i > 1 else ''), i, m.expand(r'\3')))
            line = ''

            if not prev:
                line = self.rawString[:m.start()]
                print('    "{}"'.format(line))
            else:
                line = self.rawString[prev:m.start()]
                print('    "{}"'.format(line))

            result.append(line)
            print('    "{}"'.format(m.string[m.start():m.end()]))
            print('    m = {}'.format(m.groups()))

            for g in range(len(m.groups()) + 1):
                if g == 1:
                    result.append(' ')
                    print("    m[{}]: '{}' 取代為 ' '".format(g, m[g]))
                elif g == 3:
                    result.append('*' * len(m[g]))
                elif g > 0:
                    result.append(m[g])
                    print("    m[{}]: '{}'".format(g, m[g]))

            prev = m.end()

        if prev and prev < len(self.rawString):
            result.append(self.rawString[prev:])

        print('\n重組反向參考：\n"{}"'.format(''.join(result)))
        print('\n比對結果組：\n' + '\n'.join([str(x) for x in self.regex.findall(self.rawString)]))

if __name__ == '__main__':
    ctypes.windll.kernel32.SetConsoleTitleW(sys.implementation.name + ' ' + sys.version)

    m = Match('The Nobel Prizes were awarded, in - Physics, - Chemistry, - Physiology or Medicine, - Literature and - Peace.')
    m.run()
    m.sub()

    print('請按任意鍵繼續 . . . ', end='', flush=True)
    msvcrt.getch()
