from tweets_data_collector import count_tweets, search_tweets, parse_search_category
import os
from datetime import datetime as dt
from dateutil.tz import gettz
from matplotlib import pyplot as plt
import japanize_matplotlib
import numpy as np

def search_per_category(file_path):
    designations, relates = parse_search_category(file_path)
    result_img_path = os.path.join("results", "{}.png".format(designations[0]))
    
    ys = []
    x = np.array([])
    count_relate_dict = dict()
    for relate in relates:
        counts_per_relates = None
        for name in designations:
            query = '{name} {relate} -is:retweet lang:ja'.format(name=name, relate=relate)
            json_data = count_tweets(query)
            print(query)
            x_utc = [dt.strptime(json_data[i]["end"], '%Y-%m-%dT%H:%M:%S.%fZ') for i in range(len(json_data))]
            x = np.array([datetime_utc.astimezone(gettz("Asia/Tokyo")) for datetime_utc in x_utc])
            y = np.array([json_data[i]["tweet_count"] for i in range(len(json_data))])
            ys.append(y)
            
            if counts_per_relates is None:
                counts_per_relates = np.zeros(x.size)
            counts_per_relates += y
            
            # get tweets
            search_datetime = x_utc[np.argmax(y)]

            #tweetの中身表示したいときは適用、触るな危険
            #if max(y) > 0:
            #    json_data = search_tweets(query, search_datetime)
            #    for i in range(len(json_data)):
            #        print(json_data[i]["text"])
                
        count_relate_dict[relate] = counts_per_relates
    
    # FIXME:xが漏れてるのでそこの記述は考え直した方がいい
    for key in count_relate_dict:
        plt.plot(x, count_relate_dict[key], label=key)
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()
    plt.tight_layout()
    plt.savefig(result_img_path)
    plt.close()

def main():
    file_path = "search_category"
    files = os.listdir(file_path)
    json_files = [os.path.join(file_path, f) for f in files if ".json" in f]
    for jf in json_files:
        search_per_category(jf)
    
if __name__ == "__main__":
    main()
