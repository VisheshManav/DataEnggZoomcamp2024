Q3-6:  
3. Count Records
```sql
SELECT 
	COUNT(1) AS "Total Trips"
FROM 
	hw_green_taxi_data g
WHERE 
	DATE(g.lpep_pickup_datetime) = '2019-09-18' AND
	DATE(g.lpep_dropoff_datetime) = '2019-09-18'
```
Answer: 15612  
  
4. Longest Trip 
```sql
SELECT 
	DATE(g.lpep_pickup_datetime) AS date,
	MAX(g.trip_distance) AS max_dist
FROM 
	hw_green_taxi_data g
GROUP BY
	DATE(g.lpep_pickup_datetime)
ORDER BY
	max_dist DESC
LIMIT 1;
```
Answer: 2019-09-26  
  
5. Three Biggest Pickup Borough
```sql
SELECT 
	z."Borough",
	SUM(g."total_amount") AS sum_amt
FROM 
	hw_green_taxi_data g JOIN zones z
		ON g."PULocationID" = z."LocationID"
WHERE
	DATE(g."lpep_pickup_datetime") = '2019-09-18'
GROUP BY
	z."Borough"
ORDER BY
	sum_amt DESC
LIMIT 3;
	
```
Answer: "Brooklyn" "Manhattan" "Queens"  
  
6. Largest Tip
```sql
SELECT z."Zone"
FROM zones z
WHERE z."LocationID" = (
	SELECT g."DOLocationID"
	FROM hw_green_taxi_data g
	WHERE
		EXTRACT(year FROM g."lpep_pickup_datetime") = '2019' AND
		EXTRACT(month FROM g."lpep_pickup_datetime") = '09' AND
		g."PULocationID" = (
			SELECT z."LocationID" FROM zones z WHERE z."Zone" = 'Astoria'
		)
	GROUP BY g."DOLocationID"
	ORDER BY MAX(g."tip_amount") DESC
	LIMIT 1
	);
```
Answer: JFK Airport