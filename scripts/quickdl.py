import requests
import argparse

baseUrl = "https://raw.githubusercontent.com/Arcticons-Team/Arcticons/main/icons/white/"

parser = argparse.ArgumentParser()
parser.add_argument("SRC_FILENAME", type=str, help="Source filename without .svg")
parser.add_argument("DST_FILENAME", type=str, nargs ='?', help="Destination filename (optional)")
args = parser.parse_args()


def downloadIcon(srcUrl, dstUrl):
    response = requests.get(srcUrl)
    with open(dstUrl, mode="wb") as file:
        file.write(response.content)
    return

def main():
    srcUrl = baseUrl + args.SRC_FILENAME + ".svg"
    dstUrl = args.SRC_FILENAME + ".svg"
    if args.DST_FILENAME is not None:
        dstUrl = args.DST_FILENAME + ".svg"
    downloadIcon(srcUrl,dstUrl)

if __name__ == "__main__":
    main()
