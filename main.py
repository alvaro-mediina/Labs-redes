import idna
import sys

def nonASCIIchar(url:str):
    affirmative = any(ord(c) > 127 for c in url)
    if affirmative:
        print("Se encontró dominio en formato Unicode...")
    return affirmative



def main():
    url = input("Introducir ->")
    affirmativeIDN = nonASCIIchar(url)
    print(affirmativeIDN)


if __name__ == "__main__":
    main()
    sys.exit(0)
