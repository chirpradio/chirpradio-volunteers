-- update the site (was example.com)
begin;
update django_site set 
        domain = "chirp-volunteers.farmdev.com", 
        name = "Temporary Django deployment to Kumar's server"
        where id = 1;
commit;