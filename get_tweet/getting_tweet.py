# coding: utf-8
import sys
import twitter
import time

CONSUMER_KEY = ["GG96kwKXN2f6k5eS7El1eWyyF", "yMWZIZD1IRhG0uArXI9rFtidS", "8KX29dsia1CNLQxOau4F4Cp9r",
                "q3NSI9a1fFyrQ4nxeiTCJj86z", "2CG1IF96MzkX6qvXTapt1PPgH", "9LeuS0m1Wb4cAK8yKXSnEZbJo"]
CONSUMER_SECRET = ["XDNMc0XIlZAcuxDNyPfB5N32xrizNEgiUgYrdEhPYNcFDTj2sz", "9R5yZp0E2kFk7is5cEmz0AWTJDFxnemjvRV8xvldfor6DGGw3F", "8aJ15OIyyx2HW2YxH17qnTgHcEOJpVf5CxS6p6eNipWUclq3zs",
                  "UtXmj1nUu0IxYoqyZoxFVF65IXFnVQfGi912wdf9cGuJ3dFGBJ", "42p1J9U2gFkbiY3rVhrb9U1Jmcxv7NCv4YpC75PQdlY17tB9w6", "QKV7l4LM3N2WpEejr7A9N8vY34MYCdCoErEXkMsX3ZzxVMZCgh"]
ACCESS_TOKEN_KEY = ["2506162753-F7HKMVe4nP32R4qDYydN3tDiDBxXLPPlVuQPk0n", "2506162753-ScOg7Dpr7fORxD70LV4vVaTb8CVXgSiTSpV80w8", "2506162753-MKRoWKUgQIsq5knSGkSRTdFSdWaY5LGYzU5DVJA",
                  "95452081-IDJfkc8DjKWdTC1r0OAkQSJ3jZLRvWv2pkKcvKXzI", "95452081-7T9xnvK4HEUbPrjDinbiQFsqPjDCtofmfO0fThXRh", "95452081-IqohAf6gB7MT13dclg7EkaTMrahfeTcyEhg7sJ7ga"]
ACCESS_TOKEN_SECRET = ["tlJpcDn4UNiciFsE6XSeQYKR1PKhQMwip6r6UhJ1pUFPL", "eyIjkO9nx2obRH9JYDnXvhQ5nt2B5zFh4PJRYI56khi1B", "F5xfxHKrQl6NvUsSCFLQP5jOvTkaMAF8yulCm54S9Ntwf",
                  "neNDR1nLqujIajJXd0pSJAVraYwyzNwgnrhPwWbxBzXu2", "6pW8xkHNppv45UyDXA0xYwbhBFsX9KmIzWPe1uxdYIfkO", "jlLkP7nhrUX3pzDQDWtAAtPiH7X1Pc95mgY1EoHxpWEAx"]

def getting_tweet(search_str):
  j = 0
  check = 0
  check2 = 0
  api = twitter.Api(consumer_key=CONSUMER_KEY[0],
                  consumer_secret=CONSUMER_SECRET[0],
                  access_token_key=ACCESS_TOKEN_KEY[0],
                  access_token_secret=ACCESS_TOKEN_SECRET[0])
  with open(search_str, 'w') as f:
    while(True):
      try:
        tweets = api.GetSearch(term=search_str, count=200)
        check = 0
        break
      except:
        j += 1
        check += 1
        if check == 6:
          print ("-")
          time.sleep(60)
          check = 0
        if j ==6:
          j=0
        api = twitter.Api(consumer_key=CONSUMER_KEY[j],
                  consumer_secret=CONSUMER_SECRET[j],
                  access_token_key=ACCESS_TOKEN_KEY[j],
                  access_token_secret=ACCESS_TOKEN_SECRET[j])
    i = 0
    for tweet in tweets:
      f.write(str(tweet) + "\n")
      i += 1
      check = 0
    maxid = tweets[len(tweets)-1].id
    print i
    while(True):
      try:
        tweets = api.GetSearch(term=search_str, count=200, max_id=maxid)
        if len(tweets) == 1:
          check2 += 1
          if check2 >= 10:
            return i
        else:
          check2 = 0
        for tweet in tweets:
          f.write(str(tweet) + "\n")
          i += 1
          check = 0
          if i>=20000:
            return i
        maxid = tweets[len(tweets)-1].id
        check = 0
        print i
      except:
        j += 1
        check += 1
        if check >= 6:
          print ("-")
          time.sleep(60)
          check = 0
        if j >=6:
          j=0
        api = twitter.Api(consumer_key=CONSUMER_KEY[j],
                  consumer_secret=CONSUMER_SECRET[j],
                  access_token_key=ACCESS_TOKEN_KEY[j],
                  access_token_secret=ACCESS_TOKEN_SECRET[j])
        print "change api, no:" + str(j)
        if i>=20000:
          return i


    # for tweet in tweets:
    #   f.write(str(tweet) + "\n")

  return i


if __name__ == "__main__":
  with open('./../dict/100.txt', mode = 'r') as fh:
  # ファイルを一行ずつ処理
    for search_str in fh:
      search_str = search_str.rstrip()
      print search_str
      getting_tweet(search_str)
