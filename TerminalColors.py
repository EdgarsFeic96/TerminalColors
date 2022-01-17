from sys import argv

CODE = "\033[38;2;{};{};{}m"
BLOCK = "\U00002588"
RESET = "\033[0m"
HEX = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F")

def intToHex(val: int) -> str:
    '''Returns the hexadecimal value of an integer.'''
    return HEX[val // 16] + HEX[(val%16)*16 if (val%16 < 0) else val%16]

def rgbToHex(R:int, G:int, B:int) -> str:
    '''Converts an RGB value to Hexadecimal and return a string with the format #FFFFFF.'''
    return "#" + intToHex(R) + intToHex(G) + intToHex(B)

def hexToInt(hexV: str) -> int:
    '''Returns the integer value of an hexadecimal value.'''
    return (HEX.index(hexV[0]) * 16) + (HEX.index(hexV[1]))

def hexToRgb(hexV: str) -> tuple:
    '''Converts an Hexadecimal value to an tuple of (R, G, B) values.'''
    return (hexToInt(hexV[:2]), hexToInt(hexV[2:4]), hexToInt(hexV[4:6]))

def getColorName(Hex: str) -> str:
    '''Tries to get the HTML color name, but if it doesn't exists, returns a 
    message "Not avaiable".'''

    try:
        with open("./colors.csv", "r", encoding="utf-8") as colors:
            while True:
                row = colors.readline().split(",")[:-2]

                if row == []:
                    break

                if row[2].strip("#").upper() == Hex.strip("#"):
                    return(row[1].replace("\"", ""))

            return "Not Available"

    except FileNotFoundError:
        return "File not available"

def getColorByName(htmlName: str) -> str:
    '''Tries to get the HTML color in Hexadecimal by its name,
    but if it doesn't exists, returns a message "Not avaiable"'''
    try:
        with open("./colors.csv", "r", encoding="utf-8") as colors:
            while True:
                row = colors.readline().split(",")[:-2]

                if row == []:
                    break

                if row[1].replace("\"", "").lower() == htmlName.lower():
                    return row[2].strip("#").upper()

            return "Color not Available"
    except FileNotFoundError:
        return "File not available"

def printColorInfo(R, G, B) -> None:
    '''Prints the color info in RGB, HEX, and, if it is on the
    HTML color list, also print its name'''
    R = int(R)
    G = int(G)
    B = int(B)

    if R > 255 or G > 255 or B > 255:
        print("RGB values must be in range of 0 - 255")
        return

    hexadecimal = rgbToHex(R, G, B)
    print(f"{CODE.format(R, G, B)}{BLOCK*10}{RESET}")
    print(f"{CODE.format(R, G, B)}{BLOCK*10}{RESET} HTML | {getColorName(hexadecimal)}")
    print(f"{CODE.format(R, G, B)}{BLOCK*10}{RESET} RGB  | ({R}, {G}, {B})")
    print(f"{CODE.format(R, G, B)}{BLOCK*10}{RESET} HEX  | {hexadecimal}")
    print(f"{CODE.format(R, G, B)}{BLOCK*10}{RESET}")

if __name__ == "__main__":
    if "--rgb" in argv:
        printColorInfo(*argv[2:5])
        
    if "--hex" in argv:
        hexColor = argv[2].upper()
        if len(hexColor) != 6:
            print(f"Hexadecimal value not valid.")

        for i in hexColor:
            if i not in HEX:
                print("Hexadecimal value not valid.")
                exit()

        printColorInfo(*hexToRgb(hexColor))

    if "--html" in argv:
        hexColor = getColorByName(argv[2])
        if len(hexColor) != 6:
            print(f"{hexColor} on file")
        else:
            printColorInfo(*hexToRgb(hexColor))

    if "--help" in argv:
        print("""Terminal Colors
        Usage:
        --rgb <R> <G> <B>
          Prints the color by getting it from its RGB value,
          the values must be in the range of 0-255

        --hex <HEX>
          Prints the color by getting it from its hexadecimal value,
          this must be given without the # character

        --html <Name>
          Tries to find the color by its name in the colors file.
          It uses a CSV list by codebrainz (Thank You!):
          https://github.com/codebrainz/color-names.git
          """)

    if len(argv) <= 1:
        print("Required arguments missing, see --help for info.")

