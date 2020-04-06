from settleboard import Settleboard
import logging
import json
import os
import sys
from optparse import OptionParser

CREATE_HELP = "Add match to database. i.e. --create_match user1(str) score1(int) user2 score2 user3 score3 OR " + \
              "--create_match user1(str) score1(int) user2 score2 user3 score3 user4 score4"
USER_ID_HELP = "Return database user id for user displayName i.e. --get_user_id cnevz"
HAS_USER_HELP = "Check if user exists i.e. --has_user cnevz"
CREATE_USER_HELP = "Create new user i.e. --create_user <username> <password>"

def main():

    # make Settleboard object
    sb = Settleboard(os.environ['settle_auth'])

    # set up command line options
    usage = """usage: interact with SettleBoard API -- POST matches, GET users, etc."""

    parser = OptionParser(usage)
    parser.add_option("--create_match", action="store", dest="create_match", default=None, help=CREATE_HELP)
    parser.add_option("--get_users", action="store", dest="get_users", default=None,
                       help="Return all users in database i.e. --get_users=True")
    parser.add_option("--get_user_id", action="store", dest="get_user_id", default=None, help=USER_ID_HELP)
    parser.add_option("--has_user", action="store", dest="has_user", default=None, help=HAS_USER_HELP)
    parser.add_option("--user_last_match", action="store", dest="user_last_match", default=None,
                       help="Return user's last match i.e. --user_last_match cnevz")
    parser.add_option("--get_leaderboard", action="store", dest="get_leaderboard", default=None,
                       help="Return SettleBoard leaderboard i.e. --get_leaderboard=True")
    parser.add_option("--create_user", action="store", dest="create_user", default=None, help=CREATE_USER_HELP)

    # read command line input
    (options, _) = parser.parse_args()

    # execute desired user action

    if options.create_match:
        try:
            p1 = str(sys.argv[2])
            s1 = int(sys.argv[3])
            p2 = str(sys.argv[4])
            s2 = int(sys.argv[5])
            p3 = str(sys.argv[6])
            s3 = int(sys.argv[7])
            
            # TODO: catch bad input types (e.g. score>11 or score<2) and return verbose error message
            try: # 4 man game
                p4 = str(sys.argv[8])
                s4 = int(sys.argv[9])
                response = sb.create_match(p1, s1, p2, s2, p3, s3, p4=p4, s4=s4)
                print (response)
            except: # 3 man game
                response = sb.create_match(p1, s1, p2, s2, p3, s3)
                print (response)
        except:
            print ("Not enough arguments! Need 6 or 8")

    elif options.get_users == "True":
        response = sb.get_users()
        print (response)

    elif options.get_user_id:
        try:
            name = str(sys.argv[2])
            response = sb.get_user_id(name)
            print (response)
        except:
            # TODO: add better input checking for this and below similar conditionals
            print ("Provide a name!")

    elif options.has_user:
        try:
            name = str(sys.argv[2])
            response = sb.has_user(name)
            print (response)
        except:
            print ("Provide a name!")

    elif options.user_last_match:
        try:
            name = str(sys.argv[2])
            response = sb.get_last_user_match(name)
            print (response)
        except:
            print ("Provide a name!")

    elif options.get_leaderboard == "True":
        response = sb.get_leaderboard()
        print (response)

    elif options.create_user:
        try:
            name = str(sys.argv[2])
            password = str(sys.argv[3])
            response = sb.make_user(name, password)
            print (response)
        except:
            # TODO: add better input checking
            print ("Provide a name and password!")

    else: # no option provided
        print ("Provide an action!")

if __name__ == "__main__":
    main()
