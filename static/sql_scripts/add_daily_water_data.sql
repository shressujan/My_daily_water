CREATE PROCEDURE `sp_add_daily_water_data` (
	IN p_username VARCHAR(20),
    IN p_shower DECIMAL(65),
    IN p_toilet DECIMAL(65),
    IN p_bathroom_sink DECIMAL(65),
    IN p_kitchen_sink DECIMAL(65),
    IN p_drinking_water DECIMAL(65),
    IN p_sprinkler DECIMAL(65),
    IN p_miscellaneous DECIMAL(65),
    IN p_date DATETIME
)
BEGIN
	INSERT INTO Daily_Water_Usage(username, shower, toilet, bathroom_sink, kitchen_sink, drinking_water, sprinkler, miscellaneous, date)
	VALUES (p_username, p_shower, p_toilet, p_bathroom_sink, p_kitchen_sink, p_drinking_water, p_sprinkler, p_miscellaneous, p_date);
END
