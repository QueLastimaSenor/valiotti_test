select id, coalesce(max(A), '') as A, coalesce(max(B), '') as B, coalesce(max(C), '') as C
from (
	select id, 
		case when name = 'A' then val end A,
		case when name = 'B' then val end B,
		case when name = 'C' then val end C
	from nums
) as source_tab
group by id
order by id asc