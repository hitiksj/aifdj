SELECT RANK() OVER (PARTITION BY ABCD ORDER BY EFGH DESC) AS A_RANK
FROM
    A_TABLE;
