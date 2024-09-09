SELECT * FROM customers;
SELECT * FROM stores;
SELECT * FROM products;
SELECT * FROM orders;
SELECT * FROM shipments;
SELECT * FROM inventory;
SELECT * FROM order_items;

truncate table order_items;
/************************** 2. Split full name into first name and last name **************************/
--ex: FIRST_NAME: Tammy , LAST_NAME: Bryant

SELECT *
FROM customers
WHERE FIRST_NAME IS NOT NULL
OR LAST_NAME     IS NOT NULL;


SELECT FULL_NAME,
  SUBSTR(FULL_NAME, 1, INSTR(FULL_NAME, ' ')-1) AS FIRST_NAME,
  SUBSTR(FULL_NAME, INSTR(FULL_NAME, ' ')   +1) AS LAST_NAME
FROM CUSTOMERS;

UPDATE CUSTOMERS
SET FIRST_NAME = SUBSTR(FULL_NAME, 1, INSTR(FULL_NAME, ' ')-1) ,
  LAST_NAME    = SUBSTR(FULL_NAME, INSTR(FULL_NAME, ' ')   +1);
  
COMMIT;


/************************** 3. Correct phone numbers and email which are not in proper format **************************/

--Append .com in email id.

SELECT * 
FROM CUSTOMERS
WHERE upper(EMAIL_ADDRESS) LIKE upper('%.com%');

UPDATE CUSTOMERS
SET EMAIL_ADDRESS = EMAIL_ADDRESS || '.com'
WHERE upper(EMAIL_ADDRESS) NOT LIKE upper('%.com%');

COMMIT;

--How many records have . in contact number?
--Solution
--remove .* from contact number

SELECT COUNT(*) 
FROM CUSTOMERS
WHERE CONTACT_NUMBER LIKE '%.%';

SELECT CONTACT_NUMBER, SUBSTR(CONTACT_NUMBER, 1, INSTR(CONTACT_NUMBER, '.')-1)
FROM CUSTOMERS
WHERE CONTACT_NUMBER LIKE '%.%';

UPDATE CUSTOMERS
SET CONTACT_NUMBER = SUBSTR(CONTACT_NUMBER, 1, INSTR(CONTACT_NUMBER, '.')-1)
WHERE CONTACT_NUMBER LIKE '%.%';

COMMIT;


/************************** 4. Correct contact number and remove full name **************************/

--How many contact number are less than 10 digit?
--Solution
--Make contact number as 9999999999 if the length is less than 10.

SELECT CONTACT_NUMBER, LENGTH(CONTACT_NUMBER) 
FROM customers
WHERE LENGTH(CONTACT_NUMBER) < 10;

UPDATE CUSTOMERS
SET CONTACT_NUMBER = 9999999999
WHERE LENGTH(CONTACT_NUMBER) < 10;

COMMIT;

--Check for contact number where length is more than 10.

SELECT CONTACT_NUMBER, LENGTH(CONTACT_NUMBER) 
FROM customers
WHERE LENGTH(CONTACT_NUMBER) > 10;

SELECT distinct LENGTH(CONTACT_NUMBER) 
FROM customers;

--Remove Full Name column from customers table

ALTER TABLE customers DROP COLUMN FULL_NAME;

-- branch test2

