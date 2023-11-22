# Step 05 - Loading Data into ATP

## 테이블 생성

```
CREATE TABLE "ADMIN"."LIVELABS" 
(	"ID" NUMBER(19,0) PRIMARY KEY, 
	"TITLE" VARCHAR2(4000 BYTE), 
	"URL" VARCHAR2(256 BYTE), 
	"TYPE" VARCHAR2(64 BYTE), 
	"DESCRIPTION" VARCHAR2(4000 BYTE), 
	"DURATION" VARCHAR2(64 BYTE), 
	"PUBLISHED_TIME" VARCHAR2(64 BYTE), 
	"TITLE_KO" VARCHAR2(4000 BYTE), 
	"DESCRIPTION_KO" VARCHAR2(4000 BYTE), 
	"DURATION_KO" VARCHAR2(64 BYTE), 
	"OCI_PRODUCTS" VARCHAR2(4000 BYTE), 
	"KEY_PHRASE" VARCHAR2(4000 BYTE)
);

```

## Credential 생성

```
begin 
    DBMS_CLOUD.create_credential(
        credential_name => 'OBJ_STORE_CRED_DPWS',
        username => '<<Please Update with OCI IAM User ID in Excel>>',
        password => '<<Please Update with User Auth Token in Excel>>');
end;
/
```

## Stored Procedure 생성

```
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
```

## Stored Procedure 호출 예제

```
BEGIN
  Parquet_loader('https://objectstorage.ap-tokyo-1.oraclecloud.com/n/apackrsct01/b/dpws1_demo_converted_data/o/sample2.json');
END;
/
```

