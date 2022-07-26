create temporary table entry_page1
select 
ws.website_session_id,
min(website_pageview_id) as entry_page

from website_pageviews wp
join
website_sessions ws on ws.website_session_id = wp.website_session_id
where wp.created_at < '2012-07-28'
and wp.website_pageview_id >= '23504'
and utm_source = 'gsearch'
and utm_campaign = 'nonbrand'
group by ws.website_session_id;



select
min(date(created_at)) as week_start_date,
website_session_id
from website_sessions
group by week(created_at);

create temporary table nonbrand_sessions_first_page_demo2
select 
ep.website_session_id,
wp.website_pageview_id as first_pageview_id

from website_pageviews wp
join 
entry_page1 ep on wp.website_pageview_id = ep.entry_page
where pageview_url IN ('/home', '/lander-1')
;

create temporary table nonbrand_sessions_first_page_viewcount_demo2
select 
s.website_session_id,
s.first_pageview_id,
count(distinct wp.website_pageview_id) as pagesviewed
from
nonbrand_sessions_first_page_demo2 s
join website_pageviews wp
on s.website_session_id = wp.website_session_id
group by s.website_session_id,
s.first_pageview_id;

create temporary table sessions_with_counts_firstpage_createdat
select
s.website_session_id,
s.first_pageview_id ,
wp.created_at as sessions_created_at,
wp.pageview_url as landing_page,
s.pagesviewed
FROM
nonbrand_sessions_first_page_viewcount_demo2 s
JOIN 
website_pageviews wp ON s.first_pageview_id = wp.website_pageview_id;




create temporary table final_report_home_lander1
select
yearweek(sessions_created_at) as year_week,
min(date(sessions_created_at)) as week_start_date,
count(distinct website_session_id) as total_sessions,
count(distinct case when pagesviewed = 1 Then website_session_id else null end) as bounced_sessions,
count(distinct case when pagesviewed = 1 Then website_session_id else null end)/count(distinct website_session_id) as bounce_rate,
count(distinct case when landing_page = "/home" then website_session_id else null end) as home_sessions,
count(distinct case when landing_page = "/lander-1" then website_session_id else null end) as lander1_sessions
from sessions_with_counts_firstpage_createdat
group by yearweek(sessions_created_at);

select
week_start_date,
bounce_rate,
home_sessions,
lander1_sessions
from
final_report_home_lander1;



