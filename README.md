# AWS Serverless Student Data App

A small web application for saving and viewing student records. The browser-based frontend sends requests to Amazon API Gateway, which invokes AWS Lambda functions. The functions read and write records in Amazon DynamoDB.

## How it fits together

```text
Browser ──loads site──> Amazon CloudFront ──serves files──> Amazon S3
  └──calls API──> Amazon API Gateway
                   ├── POST → insertStudentData.py → DynamoDB
                   └── GET  → getStudents.py       → DynamoDB
```

CloudFront is optional, but provides HTTPS and content delivery for the static site. API Gateway and Lambda serve the data operations.

## Repository files

- `index.html` — Form for entering a student and a table for displaying student records.
- `scripts.js` — Sends `POST` and `GET` requests to the API Gateway endpoint.
- `insertStudentData.py` — Lambda handler that writes a student record to DynamoDB.
- `getStudents.py` — Lambda handler that retrieves one student or scans the table for all students.

## Before you begin

You will need an AWS account and permission to create DynamoDB tables, Lambda functions and roles, API Gateway APIs, S3 buckets, and CloudFront distributions.

Choose an AWS Region for the DynamoDB table, Lambda functions, and API. Use that same Region when configuring these resources.

## 1. Create the DynamoDB table

1. In the DynamoDB console, create a table named **`studentData`**.
2. Set **`studentid`** as the partition key, using the string type.
3. Choose on-demand capacity or configure provisioned capacity to suit your needs.

The table name and key must match the values used in `insertStudentData.py` and `getStudents.py`.

## 2. Create the Lambda functions

Create two Python Lambda functions and add the corresponding file contents:

- **Insert function:** use `insertStudentData.py`. It reads the request body and writes an item to `studentData`.
- **Get function:** use `getStudents.py`. It returns a student when a `studentid` query parameter is provided; otherwise, it returns all table items.

Give each function an execution role with CloudWatch Logs permissions and only the DynamoDB access it needs on `studentData`: `PutItem` for the insert function, and `GetItem` and `Scan` for the get function.

## 3. Configure API Gateway

Create an API with Lambda proxy integrations:

- Configure **POST** to invoke the insert function.
- Configure **GET** to invoke the get function.
- Deploy the API to a stage and copy its invoke URL.

The handlers return CORS response headers. Configure API Gateway CORS as needed for your deployment, and make sure the allowed origin includes the site that will host the frontend.

## 4. Connect and test the frontend

In `scripts.js`, replace `API_ENDPOINT` with the invoke URL for your deployed API. Then open `index.html` in a browser or upload the frontend files to S3.

Before testing, make the field names consistent across the form, JavaScript, and Lambda handler. **The current files do not match:** the frontend sends `studentid`, `name`, `class`, and `age`, while `insertStudentData.py` stores `studentid`, `name`, `course`, and `email`. `getStudents.py` returns the stored item, and the page displays `class` and `age`. Update the code to use one shared schema so saved values display as expected.

Once the schema is aligned:

1. Enter a student and select **Save Student Data**.
2. Select **View all Students** to load the records.
3. Check the Lambda logs in CloudWatch if a request fails.

## 5. Host the site on S3 and CloudFront (optional)

1. Upload `index.html` and `scripts.js` to an S3 bucket.
2. Create a CloudFront distribution with that bucket as its origin. Prefer a private bucket with CloudFront Origin Access Control (OAC), rather than making the bucket publicly readable.
3. Configure the distribution to use HTTPS, then wait for it to deploy.
4. Open the CloudFront domain and test saving and viewing student records.

If you change the frontend after deployment, invalidate the relevant CloudFront cache paths or wait for the cached files to expire.

## Notes

- `getStudents.py` scans the whole table when no `studentid` query parameter is supplied. Scans can become slow and costly as the table grows.
- Do not put AWS credentials in frontend code. The browser should call API Gateway; Lambda should access DynamoDB using its execution role.
