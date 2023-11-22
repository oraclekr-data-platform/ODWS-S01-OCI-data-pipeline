import oci
from base64 import b64encode  
import json
from json import dumps

STREAM_NAME='crawled_stream'
STREAM_OCID='<<#RES#INFO#01>>'
MESSAGE_ENDPOINT='<<#RES#INFO#02>>'
  
def produce_messages(json_str, client, stream_ocid):
  message_list = []
  encoded_value =b64encode(json_str.encode()).decode()
  message_list.append(oci.streaming.models.PutMessagesDetailsEntry(value = encoded_value))  
  messages = oci.streaming.models.PutMessagesDetails(messages=message_list)
  put_message_result = client.put_messages(stream_ocid, messages)
  
  return put_message_result

def generating_data():
    with open('../../data/crawled_livelabs.json', 'r') as file:
        crawled_messages = json.load(file)

    config = oci.config.from_file()
    stream_client = oci.streaming.StreamClient(config, service_endpoint=MESSAGE_ENDPOINT)

    print("Total Data Size:", len(crawled_messages))

    for msg in crawled_messages:
        result = produce_messages(json.dumps(msg), stream_client, STREAM_OCID)

        for entry in result.data.entries:
            if entry.error:
                print("Error ({}) : {}".format(entry.error, entry.error_message))
            else:
                print("Published message to partition {} , offset {}, livelab_id {}".format(entry.partition, entry.offset, msg["id"]))

    print("Total Data Size:", len(crawled_messages))

if __name__ == "__main__":
    generating_data()

    print()
    print("===================")
    print("Task(Sedning MSG to The enhanced_stream) completed....")
    print("===================")
