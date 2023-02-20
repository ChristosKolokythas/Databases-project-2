# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import settings
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db


def connection():
    ''' User this function to create your connections '''
    con = db.connect(
        settings.mysql_host,
        settings.mysql_user,
        settings.mysql_passwd,
        settings.mysql_schema)

    return con

def extract_ngrams(input, n):

    input = input.split(' ')
    output = []
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])
    return output

def classify_review(reviewid):

    con = connection()
    cur = con.cursor()

    #feching data from db
    cur.execute("SELECT b.name FROM reviews r, business b WHERE r.review_id=%s AND r.business_id = b.business_id", (reviewid))
    name = cur.fetchall()
    cur.execute("SELECT text FROM reviews WHERE review_id=%s", (reviewid))
    text = cur.fetchall()
    cur.execute("SELECT word FROM posterms")
    posterms = cur.fetchall()
    cur.execute("SELECT word FROM negterms")
    negterms = cur.fetchall()
    txt =  ' '.join(text[0])
    threegram = extract_ngrams(txt, 3)
    twogram = extract_ngrams(txt, 2)
    onegram = extract_ngrams(txt, 1)

    posneg = []
    counter = 0

    for i in threegram:
        istr =  ' '.join(i)

        for j in posterms:
            jstr = ' '.join(j)

            if istr == jstr :
                counter = counter + 3
                posneg.append(j)

        for k in negterms:
            kstr = ' '.join(k)

            if istr == kstr :
                counter = counter - 3
                posneg.append(k)

    bigrams = []
    for i in posneg:
        istr= ' '.join(i)
        bigrams.append(extract_ngrams(istr,2))
    print(bigrams[0])

    for i in twogram:
        istr =  ' '.join(i)

        for j in posterms:
            jstr = ' '.join(j)

            if istr == jstr :
                testforif = 0
                for a in bigrams:
                    for b in a:
                        bstr = ' '.join(b)
                        if bstr == jstr:
                            testforif = 1
                if testforif == 0:
                    counter = counter + 2
                    posneg.append(j)

        for k in negterms:
            kstr = ' '.join(k)

            if istr == kstr:
                testforif = 0
                for a in bigrams:
                    for b in a:
                        bstr = ' '.join(b)
                        if bstr == kstr:
                            testforif = 1
                if testforif == 0:
                    counter = counter - 2
                    posneg.append(k)


    unirams = []
    for i in posneg:
        istr= ' '.join(i)
        bigrams.append(extract_ngrams(istr,1))
    print(bigrams)

    for i in onegram:
        istr =  ' '.join(i)

        for j in posterms:
            jstr = ' '.join(j)

            if istr == jstr :
                testforif = 0
                for a in bigrams:
                    for b in a:
                        bstr = ' '.join(b)
                        if bstr == jstr:
                            testforif = 1
                if testforif == 0:
                    counter = counter + 1
                    posneg.append(j)

        for k in negterms:
            kstr = ' '.join(k)

            if istr == kstr :
                if istr == kstr :
                    testforif = 0
                for a in bigrams:
                    for b in a:
                        bstr = ' '.join(b)
                        if bstr == kstr:
                            testforif = 1
                if testforif == 0:
                    counter = counter - 1
                    posneg.append(k)

    if counter > 0:
        print("the review is good")
    else:
        print("the review is bad")

    print (text)


    return [name,text]





def updatezipcode(business_id,zipcode):

    con=connection()
    cur = con.cursor()

    cur.execute("SELECT name FROM business WHERE business_id = %s", (business_id))
    name = cur.fetchall()

    if not name:
        error = "ERROR"
        return error

    zc = int(zipcode)
    cur.execute("UPDATE business SET zip_code = %s WHERE business_id = %s", (zc,business_id))
    result = "ok"

    return result

def selectTopNbusinesses(category_id,n):

    con=connection()
    cur=con.cursor()

    i = int(n)
    cur.execute("SELECT b.name, count(r.review_id) FROM reviews r, reviews_pos_neg rpn, business b, business_category bc, category c WHERE r.business_id = b.business_id AND r.review_id=rpn.review_id AND b.business_id=bc.business_id AND bc.category_id=c.category_id AND category = %s AND rpn.positive = 1 GROUP BY b.name order by count(r.review_id) DESC ", (category_id))
    temp = cur.fetchmany(i)
    return temp

def traceUserInfuence(userId,depth):
    # Create a new connection
    con=connection()
    cur=con.cursor()

    dp = int(depth)
    dp = dp - 1
    i = 1
    fofr = [] #friends of friends

    cur.execute("select u.user_id from friends f, user u, reviews r, user u1, reviews r1 WHERE f.user_id = u1.user_id and f.friend_id=u.user_id and r.user_id = u.user_id and u1.user_id = %s and u1.user_id=r1.user_id  and r1.date < r.date  and r1.business_id = r.business_id GROUP BY u.user_id", (userId) )
    friends = cur.fetchall()
    fofr.append(friends)

    for i in range(dp):
        for j in fofr[i-1]:
            cur.execute("select u.user_id from friends f, user u, reviews r, user u1, reviews r1 WHERE f.user_id = u1.user_id and f.friend_id=u.user_id and r.user_id = u.user_id and u1.user_id = %s and u1.user_id=r1.user_id  and r1.date < r.date  and r1.business_id = r.business_id GROUP BY u.user_id", (j) )
            temp = cur.fetchall()
            fofr.append(temp)

    return fofr
