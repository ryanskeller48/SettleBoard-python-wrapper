# SettleBoard-python-wrapper
Python wrapper for SettleBoard API (https://github.com/nevillco/Settleboard-API)

To run:

`$ python3 run.py [--option] <arg0> <arg1>`

Options:
  -h, --help            show this help message and exit
  --create_match=CREATE_MATCH
                        Add match to database. i.e. --create_match user1(str)
                        score1(int) user2 score2 user3 score3 OR
                        --create_match user1(str) score1(int) user2 score2
                        user3 score3 user4 score4
  --get_users=GET_USERS
                        Return all users in database i.e. --get_users=True
  --get_user_id=GET_USER_ID
                        Return database user id for user displayName i.e.
                        --get_user_id cnevz
  --has_user=HAS_USER   Check if user exists i.e. --has_user cnevz
  --user_last_match=USER_LAST_MATCH
                        Return user's last match i.e. --user_last_match cnevz
  --get_leaderboard=GET_LEADERBOARD
                        Return SettleBoard leaderboard i.e.
                        --get_leaderboard=True
  --create_user=CREATE_USER
                        Create new user i.e. --create_user <username>
                        <password>
