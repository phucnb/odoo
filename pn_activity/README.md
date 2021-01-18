1. Chạy SQL sau để update data activity overview lần đầu.

1.1 Chạy lệnh sau đầu tiên:

insert into mail_activity_overview (mail_activity_id, res_name, activity_type_id, summary, date_deadline, model_name)
select r.id, r.res_name, r.activity_type_id, r.summary, r.date_deadline, im.name
from mail_activity r
inner join ir_model im
on r.res_model_id = im.id;

1.2 Chạy lệnh dưới khi xong lệnh (1.1)

insert into mail_activity_overview_rel (overview_id, mail_activity_id)
select id, mail_activity_id from mail_activity_overview;