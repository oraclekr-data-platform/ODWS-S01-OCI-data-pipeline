import io
import oci
import json
import requests
import logging
import base64
from base64 import b64encode  
from fdk import response
from confluent_kafka import Producer


def handler(ctx, data: io.BytesIO=None):
    try:
        cfg = ctx.Config()
        bootstrap_servers = cfg["bootstrap.servers"]
        sasl_username = cfg["sasl.username"]
        sasl_password = cfg["sasl.password"]
        topic = cfg["topic"]
        compartmentocid = cfg["compartmentocid"]
    except Exception:
        logging.getLogger().error('Missing function parameters: bootstrap.servers, sasl.username, sasl.password and topic')
        raise
 
    kafka_conf = {  
        'bootstrap.servers': bootstrap_servers,
        'security.protocol': 'SASL_SSL',    
        'sasl.mechanism': 'PLAIN',
        'sasl.username': sasl_username,  
        'sasl.password': sasl_password,  
    }  

    try:
        logs = json.loads(data.getvalue())
        logging.getLogger().info('Received {} entries.'.format(len(logs)))
    
        for item in logs:
            logging.getLogger().debug('Received Data: {}.'.format(item))
            if 'value' in item:
                value = base64_decode(item['value'])
            logging.getLogger().debug('Decoded value: {}.'.format(value))

            value = json.loads(value)
            value = add_ko_fields_with_crawled_data(value, compartmentocid)
            value = add_oci_services_field(value)
            value = add_key_phrase_field(value)
            
            logging.getLogger().debug('Enhanced value: {}.'.format(value))
            logging.getLogger().info('sent value to enhenced_stream: {}.'.format(value))
            produce_messages(kafka_conf, topic, json.dumps(value))

        return response.Response(ctx, status_code=200, response_data=json.dumps({"message": "Sussess {0}".format(logs)}), headers={"Content-Type": "application/json"})

    except (Exception, ValueError) as e:
        logging.getLogger().error(str(e))
        raise


def base64_decode(encoded):
    print(type(encoded))
    base64_bytes = encoded.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('utf-8')

def detect_language(src_text):
    signer = oci.auth.signers.get_resource_principals_signer()
    ai_client = oci.ai_language.AIServiceLanguageClient(config={}, signer=signer)    
    batch_language_detection_details =  oci.ai_language.models.DetectDominantLanguageDetails(text=src_text)
    output = ai_client.detect_dominant_language(batch_language_detection_details)
    
    return output.data.languages[0].code

def add_ko_fields_with_crawled_data(crawled_data, compartment_ocid):  
    signer = oci.auth.signers.get_resource_principals_signer()
    ai_client = oci.ai_language.AIServiceLanguageClient(config={}, signer=signer)   

    based_language_code = detect_language(crawled_data["title"])
    logging.getLogger().debug('Base Language Code: {}.'.format(based_language_code))

    docs = []
    doc = oci.ai_language.models.text_document.TextDocument(key='title', text=crawled_data['title'], language_code=based_language_code)
    docs.append(doc)
    
    if crawled_data['type']=='Hands-on':
        doc = oci.ai_language.models.text_document.TextDocument(key='description', text=crawled_data['description'], language_code=based_language_code)
        docs.append(doc)
        doc = oci.ai_language.models.text_document.TextDocument(key='duration', text=crawled_data['duration'], language_code=based_language_code)
        docs.append(doc)    
    
    batch_language_translate_details =  oci.ai_language.models.BatchLanguageTranslationDetails(documents=docs, 
                                    compartment_id=compartment_ocid, target_language_code="ko")
    output = ai_client.batch_language_translation(batch_language_translate_details)
    
    for document in output.data.documents:
        logging.getLogger().info('Translated Text: {}.'.format(document.translated_text))
        crawled_data[document.key+'_ko']=document.translated_text
    
    return crawled_data

def add_oci_services_field(crawled_data):

    signer = oci.auth.signers.get_resource_principals_signer()
    ai_client = oci.ai_language.AIServiceLanguageClient(config={}, signer=signer)   
    
    new_str = []
    new_str.append(crawled_data['title'])
    if crawled_data['type']=='Hands-on':
        new_str.append(crawled_data['description'])
        
    new_str = ''.join(new_str)
    
    details = oci.ai_language.models.DetectLanguageEntitiesDetails(text=new_str)
    output = ai_client.detect_language_entities(details)

    oci_services=set()
    for name_entity in output.data.entities:
        if name_entity.type=="PRODUCT" and name_entity.score > 0.8:
            oci_services.add(name_entity.text.lower())
    
    if len(oci_services)>0:
        crawled_data['oci_products']=','.join(oci_services)
            
    return crawled_data


def add_key_phrase_field(crawled_data):

    signer = oci.auth.signers.get_resource_principals_signer()
    ai_client = oci.ai_language.AIServiceLanguageClient(config={}, signer=signer)   
    
    new_str = []
    new_str.append(crawled_data['title'])
    
    if crawled_data['type']=='Hands-on':
        new_str.append(crawled_data['description'])
    
    new_str = ''.join(new_str)
    
    details = oci.ai_language.models.DetectLanguageKeyPhrasesDetails(text=new_str)
    output = ai_client.detect_language_key_phrases(details)

    key_phrase_list=[]
    for key_phrase in output.data.key_phrases:
        if key_phrase.score > 0.99:
            key_phrase_list.append(key_phrase.text)
    
    if len(key_phrase_list)>0:
        return_index = min(10, len(key_phrase_list))
        crawled_data['key_phrase']=','.join(key_phrase_list[:return_index])

    return crawled_data


def produce_messages(conf, topic, json_str):
    producer = Producer(**conf)  
    producer.produce(topic, value=json_str) 
    producer.flush()
