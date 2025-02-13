# 📦 Affinity Answers - Take-Home Assignment

This repository contains my solutions for the Affinity Answers recruitment assignment. The tasks cover address validation using a PIN code API, SQL queries for a public dataset, and a shell script for extracting financial data.

---

## 📂 Repository Structure

| File Name         | Description |
|------------------|-------------|
| `pincode.py`      | Python script for address verification using the [postalpincode.in](https://postalpincode.in/Api-Details) API. Includes test cases. |
| `testcases.txt`   | List of test cases used to validate the address verification program. |
| `affinity.sql`    | SQL queries to answer questions related to the Rfam public database. |
| `data.sh`         | Shell script to extract "Scheme Name" and "Asset Value" from NAVAll.txt and save it in a TSV format. |

---

## 🚀 Problem Statements & Solutions

### 1️⃣ Address Validation - `pincode.py`
#### 📌 Problem:
BestDelivery Courier Company faces incorrect PIN codes in parcel addresses, leading to misrouted packages. The task is to validate if the provided PIN code matches the locality.

#### 🛠️ Solution:
- Uses the **postalpincode.in API** to fetch valid locations for a given PIN code.
- Parses the input address and validates locality-PIN code matching.
- Handles edge cases such as **missing PIN codes, incorrect formats, and locality mismatches**.

📄 **Test Cases**: Refer to `testcases.txt` for validation scenarios.

---

### 2️⃣ SQL Queries - `affinity.sql`
#### 🗄️ Questions Answered:
- **Types of tigers in the taxonomy table** and **ncbi_id of Sumatran Tiger**.
- **Finding table relationships** in the Rfam database.
- **Longest DNA sequence for rice species**.
- **Pagination query** for family names based on DNA sequence lengths.

📊 Queries are written using **PostgreSQL syntax** and optimized for performance.

---

### 3️⃣ Shell Scripting - `data.sh`
#### 📑 Task:
- Extract **Scheme Name** and **Asset Value** from `NAVAll.txt`.
- Save the output as a **TSV (tab-separated values)** file.
- Ensures **data integrity** and handles **irregular input formats**.

🔄 **Why not JSON?**  
- JSON is structured but **not ideal for tabular financial data**.
- TSV is **lightweight, easy to process, and can be imported into databases directly**.

---
