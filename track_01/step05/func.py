import io
import json
import requests
import logging

from fdk import response

def invoke_stored_procedure(ordsbaseurl, dbschema, dbpwd, uri):
    logging.getLogger().info("ordsbaseurl:()".format(ordsbaseurl))
    logging.getLogger().info("source file:()".format(uri))
    headers = {"Content-Type": "application/json"}
    #auth=(dbschema, dbpwd)
    data={"target_uri":uri}
    #res = requests.post(ordsbaseurl, auth=auth, headers=headers, data=body)
    res = requests.post(ordsbaseurl, headers=headers, json=data)
    
    return {"status":res.status_code}

def handler(ctx, data: io.BytesIO=None):
    try:
        cfg = ctx.Config()
        ordsbaseurl = cfg["ords-base-url"]
        dbuser = cfg["dbuser"]
        password = cfg["password"]
        object_storage_baase_url = cfg["base-objectstorage-url"]
    except Exception:
        logging.getLogger().error('Missing function parameters: ords-base-url', flush=True)
        raise

    try:
        body = json.loads(data.getvalue())
        data = body['data']
        object_name = data['resourceName']
        src_bucket_name = data['additionalDetails']['bucketName']
        namespace = data['additionalDetails']['namespace']

    except (Exception, ValueError) as ex:
        logging.getLogger().error('error parsing Parquet payload: ' + str(ex))

    uri="{}/n/{}/b/{}/o/{}".format(object_storage_baase_url,namespace,src_bucket_name,object_name)
    logging.getLogger().info('src file in object storage: {}'.format(uri))

    result = invoke_stored_procedure(ordsbaseurl, dbuser, password, uri)
    logging.getLogger().info('Completed - invoking stored procedure: {}'.format(uri))

    return response.Response(
        ctx, 
        response_data=json.dumps(result),
        headers={"Content-Type": "application/json"}
    )