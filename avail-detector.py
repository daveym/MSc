from luminol.anomaly_detector import AnomalyDetector
from time import gmtime, strftime
from datetime import datetime
import time, datetime
import sqlite3
import schedule

ALGORITH_NAME = "exp_avg_detector"
THRESHOLD = 2.0
INTERVAL = "10"
LIMIT = "10"

def job():
    print("Run start: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # Connect to either the normal, anomaly or combined database. Note for SQLlite, the detect types
    # line converts from SQLlite datatypes(typically text) to Python native datatypes
    conn = sqlite3.connect('../hl7-combined.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor() 

    # Group messages into X second intervals
    cur.execute(
            "select messages.MSGTYPE, datetime((strftime('%s', messages.QueueTime) /" +  INTERVAL + ") * " 
            + INTERVAL + ", 'unixepoch') interval, count(*)  count from messages"
            " where msgtype = 'ADT_A31' group by interval order by interval desc limit " + LIMIT )

    rows = cur.fetchall()
    data = {}

    if len(rows)> 0:

        for row in rows:
            # Luminol library requires a 2 column unix timestamp + count
            obsTimestamp = time.mktime(datetime.datetime.strptime(row["interval"], "%Y-%m-%d %H:%M:%S").timetuple())
            data[obsTimestamp] = row["count"]

        print data
        # DETECTOR TYPE - see https://github.com/linkedin/luminol/tree/master/src/luminol/algorithms/anomaly_detector_algorithms
        detector = AnomalyDetector(data, algorithm_name=ALGORITH_NAME, score_threshold=THRESHOLD)
  
        score = detector.get_all_scores()
        anom_score = []

        for (timestamp, value) in score.iteritems():
            t_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

            anom_score.append([t_str, value])

        print "----- ALL SCORES ----- "
        for score in anom_score:
            print(score)
        
        anomalies = detector.get_anomalies()
        
        for (value) in anomalies:
            print "       match: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(value.exact_timestamp)), 
            value.anomaly_score

            if value.anomaly_score >= int(THRESHOLD) and anomalies.count > int(LIMIT):
                print "ANOMALY DETECTED - NOTIFYING ADMINISTRATOR / CALLING WEBSERVICE ETC"
                quit()

        print("Run End: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")

schedule.every(int(INTERVAL)).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)