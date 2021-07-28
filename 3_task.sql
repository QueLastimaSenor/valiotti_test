-- with users as (
-- 	select user_id, min(time) as installed_at
-- 	from MOCK_DATA
-- 	group by user_id
-- ),
-- client_session as (
-- 	select user_id, time as created_at
-- 	from MOCK_DATA
-- ),
with day_diff as (
	select a.user_id, to_char(a.installed_at, 'MM') as installed_at, 
	to_char(b.created_at, 'MM-dd') as created_at,
	b.created_at - a.installed_at as diff
	from users a
	join client_session b
	on a.user_id = b.user_id
)

select to_char(b.installed_at, 'MM') as orign_day,
round((sum(case when a.diff = 0 then 1 else 0 end)::float /
	(select count(user_id) from users))::numeric, 3) * 100.0
day_0,
round((sum(case when a.diff = 1 then 1 else 0 end)::float /
	(select count(user_id) from users))::numeric, 3) * 100.0 
day_1,
round((sum(case when a.diff = 3 then 1 else 0 end)::float /
	(select count(user_id) from users))::numeric, 3)  * 100.0 
day_3,
(sum(case when a.diff = 7 then 1 else 0 end)::float /
	(select count(user_id) from users)) * 100.0 
day_7

from day_diff a
left outer join users b
on a.user_id = b.user_id
and a.installed_at = to_char(b.installed_at, 'MM')
group by to_char(b.installed_at, 'MM') 
order by to_char(b.installed_at, 'MM') 

