import io
import json
import logging
import json 
import gzip
import oci
import base64

#import pandas as pd
#import pyarrow as pa
#import pyarrow.parquet as pq

from fdk import response



def handler(ctx, data: io.BytesIO = None):
    try:
        cfg = ctx.Config()
        bucket_name= cfg["bucket_name"]
    except Exception:
        logging.getLogger().error('Missing function parameters: bucket_name')
        raise

    signer = oci.auth.signers.get_resource_principals_signer()
    client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    namespace = client.get_namespace().data

    try:
        body = json.loads(data.getvalue())
        data = body['data']
        object_name = data['resourceName']
        src_bucket_name = data['additionalDetails']['bucketName']
        namespace = data['additionalDetails']['namespace']
        logging.getLogger().info('Namespace: {}.'.format(namespace))
        logging.getLogger().info('Object Name: {}.'.format(object_name))
        logging.getLogger().info('Bucket Name: {}.'.format(src_bucket_name))

    except (Exception, ValueError) as ex:
        logging.getLogger().error('error parsing Parquet payload: ' + str(ex))

    object = client.get_object(namespace, src_bucket_name, object_name)
    gz_file = object.data.content
    file_content = gzip.decompress(gz_file)
    
    # Convert the bytes to a string
    file_content = file_content.decode("utf-8")

    json_array=[]

    for msg in file_content.splitlines():
        data = json.loads(msg)
        core_msg = json.loads(base64.b64decode(data['value']))
        json_array.append(core_msg)

    # JSON 배열 형식으로 변환
    formatted_data = "\n".join([json.dumps(item) for item in json_array])

    result = client.put_object(namespace_name=namespace,
                        bucket_name=bucket_name, object_name=modified_file_name(object_name), 
                        put_object_body=formatted_data.encode('utf-8'))

    if result.status == 200:
        logging.getLogger().info("json file uploaded successfully.")
    else:
        logging.getLogger().error("Error uploading json file: {}".format(result.data.message))

    return response.Response(
        ctx, response_data=json.dumps({"message": "data"}),
        headers={"Content-Type": "application/json"}
    )

def modified_file_name(file_name):
    start_index = file_name.rfind('/') + 1
    end_index = file_name.rfind('.data.gz')
    modified_name = file_name[start_index:end_index]+'.json'
    return modified_name