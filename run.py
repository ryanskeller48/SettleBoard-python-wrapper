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

        # first see if the user has at least provided 6 input arguments (3 scores, 3 names)
        try:
            p1 = str(sys.argv[2])
            s1 = sys.argv[3]
            p2 = str(sys.argv[4])
            s2 = sys.argv[5]
            p3 = str(sys.argv[6])
            s3 = sys.argv[7]

            # make sure scores are integers and > 2 and < 11
            tick = 1
            winners = 0
            scores = [s1, s2, s3]
            for score in scores:
                try:
                    score = int(score)
                    if score < 2:
                        print(f"Score {tick} must be >= 2! You entered: {score}")
                        sys.exit(1)
                    elif score > 11:
                        print(f"Score {tick} must be <= 11! You entered: {score}")
                        sys.exit(1)
                    elif score >= 10:
                        winners += 1
                except ValueError:
                    print(f"Score {tick} must be an integer! You entered: {score}")
                    sys.exit(1)
                tick += 1

            try: # 4 man game if this succeeds
                p4 = str(sys.argv[8])
                s4 = sys.argv[9]
                
                # make sure score 4 is an integer and > 2 and < 11
                try:
                    score = int(score)
                    if score < 2:
                        print(f"Score 4 must be >= 2! You entered: {score}")
                        sys.exit(1)
                    elif score > 11:
                        print(f"Score 4 must be <= 11! You entered: {score}")
                        sys.exit(1)
                    elif score >= 10:
                        winners += 1
                    
                    # verify there is exactly one winning (>10) score
                    if winners < 1:
                        print ("No winning score!")
                        sys.exit(1)
                    elif winners > 1:
                        print ("Too many winning scores!")
                        sys.exit(1)

                except ValueError:
                    print(f"Score 4 must be an integer! You entered: {score}")
                    sys.exit(1)

                # try to make game
                response = sb.create_match(p1, int(s1), p2, int(s2), p3, int(s3), p4=p4, s4=int(s4))

                if response is not None: # 200 good query
                    print (response)
                else:
                    # one of the names was bad, scores already checked
                    for name in [p1, p2, p3, p4]:
                        if not sb.has_user(name):
                            print (f"User {name} does not exist!")

            except IndexError: # 3 man game since there were less than 8 arguments

                # verify there is exactly one winning (>10) score
                if winners < 1:
                    print ("No winning score!")
                    sys.exit(1)
                elif winners > 1:
                    print ("Too many winning scores!")
                    sys.exit(1)

                # try to make game
                response = sb.create_match(p1, int(s1), p2, int(s2), p3, int(s3))

                if response is not None: # 200 good query
                    print (response)
                else:
                    # one of the names was bad, scores already checked
                    for name in [p1, p2, p3]:
                        if not sb.has_user(name):
                            print (f"User {name} does not exist!")

        except IndexError: # incorrect number of input arguments
            print ("Bad number of arguments! Need 6 or 8. See --help")

    elif options.get_users == "True":
        response = sb.get_users()
        print (response)

    elif options.get_user_id:
        try:
            name = str(sys.argv[2])
            response = sb.get_user_id(name)
            print (response)
        except IndexError: # no name provided
            print ("Provide a name!")

    elif options.has_user:
        try:
            name = str(sys.argv[2])
            response = sb.has_user(name)
            print (response)
        except IndexError: # no name provided
            print ("Provide a name!")

    elif options.user_last_match:
        try:
            name = str(sys.argv[2])
            response = sb.get_last_user_match(name)
            print (response)
        except IndexError: # no name provided
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
        except IndexError: # have 1 or 0 input arguments, need 2
            print ("Provide a name and password!")

    else: # no option provided
        print ("Provide an action!")

if __name__ == "__main__":
    main()
