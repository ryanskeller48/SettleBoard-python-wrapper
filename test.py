from settleboard import Settleboard
import logging
import json
import os

def main():

    sb = Settleboard(os.environ['settle_auth'])

    print (sb.get_user_id("cnevz"))
    print (sb.get_last_user_match("cnevz"))
    #print (sb.create_match("Keller", 10, "Keller2", 9, "cnevz", 8))

if __name__ == "__main__":
    main()
