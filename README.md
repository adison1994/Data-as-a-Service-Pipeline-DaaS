# Data-as-a-Service-Pipeline (DaaS)


CLAAT Link - https://codelabs-preview.appspot.com/?file_id=1RU0VFAtEOq2Wmisp00X2sNH4aQsW1qim4Zh-A3m7jYc#0

## Data Pipeline Design 

***"Data as a service (DaaS) is a data management strategy that uses the cloud to deliver data storage, integration, processing, and/or analytics services via a network connection."***

DaaS is similar to software as a service, or SaaS, a cloud computing strategy that involves delivering applications to end-users over the network, rather than having them run applications locally on their devices. Just as SaaS removes the need to install and manage software locally, DaaS outsources most data storage, integration, and processing operations to the cloud.

![Design](https://github.com/Nikhilkohli1/Data-as-a-Service-Pipeline/blob/main/Design/daas_design_assignment.png)


The overall architecture flow originates from the trigger event on file upload in two different S3 buckets. Both the buckets have data uploaded, which further invocates two different Lambda functions executing concurrently. The functions are mainly responsible for importing data from both the buckets into two different DynamoDB tables. Since one of the DynamoDB tables requires pre-processing for cleaning the underlying data another invocation of a different Lambda function happens to perform necessary transformations and data cleaning. This data is further stored in a new dynamodb table.
