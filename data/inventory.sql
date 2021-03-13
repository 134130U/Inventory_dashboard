select product_type,etat, cost_price::double precision,country,tenant_id,stock_type, count(distinct serial) as quantite
from (select stock_id,a.created_at,serial,a.etat,ph.cost_price,split_part(b.name,'-',1) as stock_manager,
b.tenant_id,b.stock_type,c.locality,d.name as product_type,b.name as stock_name,
case when b.tenant_id = 1 then 'Senegal'
	when b.tenant_id = 2 then 'Mali'
    when b.tenant_id = 3 then 'Nigeria'
    When b.tenant_id = 4 then 'Burkina'
    when b.tenant_id = 5 then 'Niger'
	when b.tenant_id = 6 then 'Cameroun'
    else  'others' end as country 
from public.stocks_products
inner join (select * from public.products)a on product_id = a.id
inner join (select * from public.stocks)b on stock_id = b.id 
inner join(select id as id_loc,name as locality,type_locality from public.localities)c on locality_id = c.id_loc
inner join(select * from public.product_types)d on product_type_id = d.id
inner join (select * from product_hashes)ph on ph.serial_number = a.serial)tab
where etat in ('Neuf','Endommagé') --and tenant_id=1
group by 1,2,3,4,5,6