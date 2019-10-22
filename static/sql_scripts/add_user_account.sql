DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_add_user`(
	IN p_username VARCHAR(20),
    IN p_password VARCHAR(20),
    IN p_first_name VARCHAR(20),
    IN p_last_name VARCHAR(20),
    IN p_street_address VARCHAR(20),
    IN p_state VARCHAR(20),
    IN p_city VARCHAR(20),
    IN p_zip_code INT(11)
)
BEGIN
	IF(SELECT EXISTS(SELECT 1 FROM User_Account WHERE username = p_username)) THEN
			SELECT 'Username Exists !!';
		ELSE
			INSERT INTO User_Account(username, password)
			VALUES(p_username, p_password);
			
			INSERT INTO Address(street_address, state, city, zip_code)
			VALUES(p_street_address, p_state, p_city, p_zip_code);
			
			SET @p_address_id = LAST_INSERT_ID();
			
			INSERT INTO User(username, first_name, last_name, address_id)
			VALUES (p_username, p_first_name, p_last_name, @p_address_id);
			
		END IF;
END

DELIMITER ;
