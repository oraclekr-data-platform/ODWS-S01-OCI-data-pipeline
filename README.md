# ODWS-S01-OCI-Data-Pipeline

Oracle Data Platform 워크샵에서 OCI Data Pipeline 부분은 OCI cloud native 서비스를 사용해서 near-real time으로 데이터가 이동하는 데이터 파이프라인을 생성해 볼 것입니다. 원천의 Json 파일에서 데이터를 메시지로 생성하면, near-real time으로 OCI Streaming, object storage, Autonomous Transaction Processing DB (ATP)로 load, 저장할 수 있도록 데이터 파이프라인을 생성합니다.

이 프로젝트는 Oracle Live labs의 웹 페이지에서 hands-on 실습을 검색할때 불편함을 해소하고자 웹페이지의 데이터를 Crawling 해서 Json 파일을 만들고 Json 파일에서 실습 lab의 각각의 정보를 message로 생성해서 near-real time으로 OCI Streaming에 load한 후 활용할 수 있도록 하는 것이 목적입니다.

사용하는 OCI Native Cloud Services

- OCI Streaming
  
- Functions
  
- Connector Hub
  
- Object Storage
  
- Autonomous Transaction Processing (ATP)
  
<Oracle Live Labs>
<img width="475" alt="0-00" src="https://github.com/oraclekr-data-platform/ODWS-S01-OCI-data-pipeline/assets/150219167/c90616af-746e-4662-baaf-df596293be55">
<img src="https://github.com/oraclekr-data-platform/ODWS-S01-OCI-data-pipeline/assets/150219167/a7a17eee-ff22-42b9-b03d-fd9a02c9d422" height="250px"></p>


![7-10](https://github.com/oraclekr-data-platform/ODWS-S01-OCI-data-pipeline/assets/150219167/7abb3229-a111-481c-879d-f216f60b94d1)

![0-0000](https://github.com/oraclekr-data-platform/ODWS-S01-OCI-data-pipeline/assets/150219167/c0f0bfc4-90b3-4837-8f71-4ca6a066491c)





 
  ![0-0](https://github.com/oraclekr-data-platform/ODWS-S01-OCI-data-pipeline/assets/150219167/9cd6342e-39d3-402d-a8fa-c635c94b988f)
 - 1. Jason파일을 Generate_msg.py로 OCI crawled_stream에 로딩함OCI Streaming
    
- 2. enhancement FN (AI 한글 번역)을 생성해서 번역 후 enhanced _stream에 로딩함
    
- 3. enhanced_stream 과 object storage를 연결하면 encoded 데이터로 저장됨
    
- 4. Converting FN(디코딩)을 생성 및 실행하면 decoded 데이터로 저장됨
    
- 5. Jasonloader(SP) 생성 후 FN으로 object storage  ATP로 데이터 복제하는 REST API 실행함
