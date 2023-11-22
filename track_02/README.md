# 부하 발생 

## 테이블 생성

```
drop table "ADMIN"."LIVELABS" 

CREATE TABLE "ADMIN"."LIVELABS" 
(	"ID" NUMBER(19,0) PRIMARY KEY, 
	"TITLE" VARCHAR2(4000 BYTE), 
	"URL" VARCHAR2(256 BYTE), 
	"TYPE" VARCHAR2(64 BYTE), 
	"DESCRIPTION" VARCHAR2(4000 BYTE), 
	"DURATION" VARCHAR2(64 BYTE), 
	"PUBLISHED_TIME" VARCHAR2(64 BYTE), 
	"TITLE_KO" VARCHAR2(4000 BYTE), 
	"DESC_KO" VARCHAR2(4000 BYTE), 
	"DURATION_KO" VARCHAR2(64 BYTE), 
	"OCI_PRODUCTS" VARCHAR2(4000 BYTE), 
	"KEY_PHRASE" VARCHAR2(4000 BYTE)
);
```

## 파일 업로드

- <home>/data/all_enahnced_livelabs.json
- object storate 업로드
    - Bucket 명 패턴: dpws1_<IAM_USER_ID>_converted_data

## Stored Procedure 생성

```
begin 
    DBMS_CLOUD.create_credential(
        credential_name => 'OBJ_STORE_CRED_DPWS',
        username => 'taewanme@gmail.com',
        password => 'r7oCKgz3wE[q2BB#R#W9');
end;
/

```

'''
CREATE OR REPLACE PROCEDURE Parquet_loader(TARGET_URI IN VARCHAR2) AS
BEGIN
  DBMS_CLOUD.COPY_DATA(
    credential_name => 'OBJ_STORE_CRED_DPWS',
    table_name => 'LIVELABS',
    file_uri_list => TARGET_URI,
    format => JSON_OBJECT('type' value 'json', 'columnpath' value '[
    "$.id", "$.title", "$.url", "$.type", "$.description", "$.duration", 
    "$.published_time", "$.title_ko",
    "$.description_ko", "$.duration_ko", "$.oci_products", "$.key_phrase"]')
  );
END;
/
'''

```
BEGIN
  Parquet_loader('https://objectstorage.ap-tokyo-1.oraclecloud.com/n/apackrsct01/b/dpws1_demo_converted_data/o/all_enhanced_livelabs.json');
END;
/
```