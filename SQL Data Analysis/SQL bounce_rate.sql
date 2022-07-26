create temporary table entry_page
select 
ws.website_session_id,
min(website_pageview_id) as entry_page

from website_pageviews wp
join
website_sessions ws on ws.website_session_id = wp.website_session_id
where wp.created_at < '2012-07-28'
and wp.website_pageview_id >= '23504'
group by ws.website_session_id;

create temporary table nonbrand_sessions_first_page_demo1
select 
wp.website_session_id,
wp.pageview_url as landing_page
from website_pageviews wp
join 
entry_page ep on wp.website_pageview_id = ep.entry_page
where pageview_url IN ('/home', '/lander-1')
;

create temporary table nonbrand_bounced_sessions_only
select
wp.website_session_id,
s.landing_page,
count(distinct wp.website_pageview_id) as pagesviewed
FROM
nonbrand_sessions_first_page_demo1 s
JOIN 
website_pageviews wp ON s.website_session_id = wp.website_session_id
group by 
landing_page,
wp.website_session_id 
HAVING 
pagesviewed = '1'
order by wp.website_session_id
;

select  
s.landing_page,
count(distinct s.website_session_id) as sessions,
count(distinct b.website_session_id) as bounced_sessions,
count(distinct b.website_session_id)/count(distinct s.website_session_id) as bounce_rate
FROM
 nonbrand_sessions_first_page_demo1 s
LEFT JOIN nonbrand_bounced_sessions_only b
on b.website_session_id = s.website_session_id
join
website_sessions ws
on s.website_session_id = ws.website_session_id


group by s.landing_page;