import oci
from base64 import b64encode  
import json
from json import dumps

STREAM_NAME='enhanced_stream' #in your compartment
STREAM_OCID='ocid1.stream.oc1.ap-tokyo-1.amaaaaaavsea7yiaijzsy76jk5mtoollwrdrwur32mgc34ou4mrz2juduzlq'
MESSAGE_ENDPOINT='https://cell-1.streaming.ap-tokyo-1.oci.oraclecloud.com'
  
def produce_messages(json_str, client, stream_ocid):
  message_list = []
  encoded_value =b64encode(json_str.encode()).decode()
  message_list.append(oci.streaming.models.PutMessagesDetailsEntry(value = encoded_value))  
  messages = oci.streaming.models.PutMessagesDetails(messages=message_list)
  put_message_result = client.put_messages(stream_ocid, messages)
  
  return put_message_result

with open('../data/enhanced_livelabs.json', 'r') as file:
    livelabs = json.load(file)

print("Total Data Size:", len(livelabs))

config = oci.config.from_file()
stream_client = oci.streaming.StreamClient(config, service_endpoint=MESSAGE_ENDPOINT)

for livelab in livelabs:
    result = produce_messages(json.dumps(livelab), stream_client, STREAM_OCID)

    for entry in result.data.entries:
        if entry.error:
            print("Error ({}) : {}".format(entry.error, entry.error_message))
        else:
            print("Published message to partition {} , offset {}, livelab_id {}".format(entry.partition, entry.offset, livelab["id"]))


print()
print("===================")
print("Task(Sedning MSG to The enhanced_stream) completed....")
print("===================")
