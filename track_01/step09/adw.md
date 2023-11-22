BEGIN
  DBMS_CLOUD.COPY_DATA(
    credential_name => 'OBJ_STORE_CRED',
    table_name => 'A_20230614T104545Z_20230614T104620Z0',
    file_uri_list => 'https://objectstorage.ap-tokyo-1.oraclecloud.com/n/apackrsct01/b/dpws1_demo_converted_data/o/20230614T104545Z_20230614T104620Z.0.parquet',
    format =>  '{"type":"parquet"}'
    );
END;
/


begin 
    DBMS_CLOUD.create_credential(
        credential_name => 'OBJ_STORE_CRED',
        username => 'taewanme@gmail.com',
        password => 'r7oCKgz3wE[q2BB#R#W9');
end;
/


BEGIN
  DBMS_CLOUD.COPY_DATA(
    credential_name => 'OBJ_STORE_CRED_WS',
    table_name => 'DEMO',
    file_uri_list => 'https://objectstorage.ap-tokyo-1.oraclecloud.com/n/apackrsct01/b/dpws1_demo_converted_data/o/20230615T064317Z_20230615T064405Z.0.parquet',
    format =>  '{"type":"parquet"}'
    );
END;
/


CREATE OR REPLACE PROCEDURE Parquet_loader(TARGET_URI IN VARCHAR2) AS
BEGIN
  DBMS_CLOUD.COPY_DATA(
    credential_name => 'OBJ_STORE_CRED_WS',
    table_name => 'DEMO',
    file_uri_list => TARGET_URI,
    format => '{"type":"parquet"}'
  );
END;
/

BEGIN
  Parquet_loader('https://objectstorage.ap-tokyo-1.oraclecloud.com/n/apackrsct01/b/dpws1_demo_converted_data/o/20230615T064317Z_20230615T064405Z.0.parquet');
END;
/

select * from DEMO
delete from DEMO

```
CREATE TABLE "ADMIN"."LIVELABS" (
  "LIVELAB_ID" NUMBER(19, 0),
  "TITLE" VARCHAR2(4000 BYTE),
  "URL" VARCHAR2(256 BYTE),
  "TYPE" VARCHAR2(64 BYTE),
  "DESC" VARCHAR2(4000 BYTE),
  "DURATION" VARCHAR2(64 BYTE),
  "PUBLISHED_TIME" VARCHAR2(64 BYTE),
  "PRODUCED_TIME" VARCHAR2(64 BYTE),
  "TITLE_KO" VARCHAR2(4000 BYTE),
  "DESC_KO" VARCHAR2(4000 BYTE),
  "DURATION_KO" VARCHAR2(64 BYTE),
  "OCI_PRODUCTS" VARCHAR2(4000 BYTE),
  "KEY_PHRASE" VARCHAR2(4000 BYTE),
  CONSTRAINT "PK_LIVELABS" PRIMARY KEY ("LIVELAB_ID")
);
```