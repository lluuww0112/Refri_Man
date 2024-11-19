WITH exp_table AS (
    SELECT exp_day, refri_id  -- refri_id가 있다면, 그것으로 구분
    FROM contain
		NATURAL JOIN category
)
UPDATE contain 
JOIN exp_table  ON contain.refri_id = exp_table.refri_id  -- refri_id 또는 다른 컬럼으로 연결
SET contain.status = CASE
    WHEN DATEDIFF(contain.exp_date, CURDATE()) > exp_table.exp_day THEN 0
    WHEN DATEDIFF(contain.exp_date, CURDATE()) = exp_table.exp_day THEN 1
    WHEN DATEDIFF(contain.exp_date, CURDATE()) < 0 THEN 2
END;
