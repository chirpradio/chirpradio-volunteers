begin;
-- there were duplicated tasks due to old structure:
update volunteers_taskassignment set task_id = (
        select id from volunteers_task where description = 'Ears&Eyes Fest at Hideout' order by id limit 1)
    where task_id in (
        select id from volunteers_task where description = 'Ears&Eyes Fest at Hideout');
delete from volunteers_task where description = 'Ears&Eyes Fest at Hideout' and id not in (
    select id from volunteers_task where description = 'Ears&Eyes Fest at Hideout' order by id limit 1);
commit;