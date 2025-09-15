-- 0001-users.sql

create table if not exists users (
    id integer not null primary key autoincrement,
    telegram_id integer not null,
		first_name text not null,
		last_name text,
		is_active boolean not null,
    is_admin boolean not null default false,
    creation_date datetime not null default current_timestamp
);

-- Insert a dummy user with no privileges to kickstart the autoincrement.
insert into users (
    id,
    telegram_id,
		first_name,
		last_name,
    is_active,
    is_admin
)
values (
    0,
    0,
		'Test User',
		null,
    false, -- inactive
    false  -- Not an admin
);
