create temporary table pageview_level
select
ws.website_session_id,
wp.pageview_url,
case when pageview_url = '/products' then 1 else 0 end as products_page,
case when pageview_url = '/the-original-mr-fuzzy' then 1 else 0 end as original_mr_fuzzy_page,
case when pageview_url = '/cart'then 1 else 0 end as cart_page,
case when pageview_url = '/shipping' then 1 else 0 end as shipping_page,
case when pageview_url = '/billing' then 1 else 0 end as billing_page,
case when pageview_url = '/thank-you-for-your-order' then 1 else 0 end as thank_you_order_page
from
website_sessions ws
left JOIN website_pageviews wp
on ws.website_session_id = wp.website_session_id 
where ws.website_session_id between '18240' and '25000'
order by 
ws.website_session_id,
wp.created_at;

create temporary table session_pages_reached
select
website_session_id,
max(products_page) as products_reached,
max(original_mr_fuzzy_page) as mr_fuzzy_reached,
max(cart_page) as cart_reached,
max(shipping_page) as shipping_reached,
max(billing_page) as billing_reached,
max(thank_you_order_page) as thank_you_reached
from  pageview_level
group by
website_session_id;

create temporary table final_click_rate
select 
count(distinct website_session_id) as sessions,
count(distinct case when products_reached = 1 then website_session_id else null end) as to_products,
count(distinct case when mr_fuzzy_reached = 1 then website_session_id else null end) as to_mrfuzzy,
count(distinct case when cart_reached = 1 then website_session_id else null end) as to_cart,
count(distinct case when shipping_reached = 1 then website_session_id else null end) as to_shipping,
count(distinct case when billing_reached = 1 then website_session_id else null end) as to_billing,
count(distinct case when thank_you_reached = 1 then website_session_id else null end) as to_thankyou
from session_pages_reached
;

select
count(distinct case when products_reached = 1 then website_session_id else null end)/count(distinct website_session_id) as lander_click_rate,
count(distinct case when mr_fuzzy_reached = 1 then website_session_id else null end)/count(distinct case when products_reached = 1 then website_session_id else null end) as products_click_rate,
count(distinct case when cart_reached = 1 then website_session_id else null end)/count(distinct case when mr_fuzzy_reached = 1 then website_session_id else null end) as mr_fuzzy_click_rate,
count(distinct case when shipping_reached = 1 then website_session_id else null end)/count(distinct case when cart_reached = 1 then website_session_id else null end) as cart_click_rate,
count(distinct case when billing_reached = 1 then website_session_id else null end)/count(distinct case when shipping_reached = 1 then website_session_id else null end) as shipping_click_rate,
count(distinct case when thank_you_reached = 1 then website_session_id else null end)/ count(distinct case when billing_reached = 1 then website_session_id else null end) as billing_click_rate
from session_pages_reached;