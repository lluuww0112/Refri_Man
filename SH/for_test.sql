-- DELIMITER $$

-- -- AFTER UPDATE 트리거 수정
-- CREATE TRIGGER after_contain_update
-- AFTER UPDATE ON `refri_man`.`contain`
-- FOR EACH ROW
-- BEGIN
--     -- 만약 count가 0으로 변경되면, 삭제를 위해 플래그를 세팅
--     IF NEW.count = 0 THEN
--         -- 여기에서 DELETE를 하지 않고, 플래그를 세팅하는 방법을 사용할 수 있음
--         UPDATE `refri_man`.`contain` 
--         SET count = 0 
--         WHERE food_name = OLD.food_name
--         AND input_date = OLD.input_date
--         AND refri_id = OLD.refri_id;
--     END IF;
-- END $$

-- -- BEFOR DELETE 트리거 추가
-- CREATE TRIGGER before_contain_delete
-- BEFORE DELETE ON `refri_man`.`contain`
-- FOR EACH ROW
-- BEGIN
--     -- 삭제하기 전에 'count'가 0이라면 자동 삭제
--     IF OLD.count = 0 THEN
--         DELETE FROM `refri_man`.`contain`
--         WHERE food_name = OLD.food_name
--         AND input_date = OLD.input_date
--         AND refri_id = OLD.refri_id;
--     END IF;
-- END $$

-- DELIMITER ;

-- select * from contain; 