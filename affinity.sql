-- How many types of tigers can be found in the taxonomy table of the dataset?
SELECT COUNT(*) AS tiger_count
FROM taxonomy
WHERE tax_string LIKE '%Panthera tigris%';

-- What is the "ncbi_id" of the Sumatran Tiger?
SELECT ncbi_id
FROM taxonomy
WHERE tax_string LIKE '%Panthera tigris sondaica%';

-- Which type of rice has the longest DNA sequence? 
SELECT rfamseq_acc, length
FROM rfamseq
WHERE ncbi_id IN (
    SELECT ncbi_id
    FROM taxonomy
    WHERE tax_string LIKE '%Oryza%'
)
ORDER BY length DESC
LIMIT 1;

-- Give a query that will return the 9th page when there are 15 results per page.
SELECT f.rfam_acc, f.rfam_id, MAX(r.length) AS max_length
FROM family f
JOIN full_region fr ON f.rfam_acc = fr.rfam_acc
JOIN rfamseq r ON fr.rfamseq_acc = r.rfamseq_acc
GROUP BY f.rfam_acc, f.rfam_id
HAVING MAX(r.length) > 1000000
ORDER BY max_length DESC
LIMIT 15 OFFSET 120;
