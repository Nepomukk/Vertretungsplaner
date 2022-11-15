create table users
(
    userid    serial
        constraint users_pk
            primary key,
    username  varchar not null,
    pwd       varchar not null,
    firstname varchar not null,
    lastname  varchar not null,
    email     varchar not null
);

alter table users
    owner to postgres;

create table roles
(
    roleid serial
        constraint roles_pk
            primary key,
    name   varchar not null,
    admin  boolean not null,
    level  integer not null
);

alter table roles
    owner to postgres;

create table absensereasons
(
    id    integer default nextval('absencereasons_id_seq'::regclass) not null
        constraint absencereasons_pk
            primary key,
    descr varchar                                                    not null
);

alter table absensereasons
    owner to postgres;

create table statustypes
(
    id    serial
        constraint statustypes_pk
            primary key,
    descr varchar not null
);

alter table statustypes
    owner to postgres;

create table substitutiontypes
(
    id    serial
        constraint substitutiontypes_pk
            primary key,
    descr varchar not null
);

alter table substitutiontypes
    owner to postgres;

create table forms
(
    formatid      serial
        constraint forms_pk
            primary key
        constraint forms_absensereasons_id_fk
            references absensereasons,
    absensereason integer,
    other         varchar,
    appendfile    varchar,
    pdffile       varchar,
    createdate    date,
    activ         boolean,
    fcomment      varchar,
    status        integer not null
        constraint forms_statustypes_id_fk
            references statustypes,
    userid        integer not null
        constraint forms_users_userid_fk
            references users
);

alter table forms
    owner to postgres;

create table confirmation
(
    id       serial
        constraint confirmation_pk
            primary key,
    userid   integer   not null
        constraint confirmation_users_userid_fk
            references users,
    formatid integer   not null
        constraint confirmation_forms_formatid_fk
            references forms,
    comdate  timestamp not null,
    ok       boolean   not null
);

alter table confirmation
    owner to postgres;

create table sublessons
(
    id              serial
        constraint sublessons_pk
            primary key,
    formatid        integer not null
        constraint sublessons_forms_formatid_fk
            references forms,
    lessonsnumber   integer not null,
    lessonstype     varchar not null,
    classname       varchar not null,
    subteachingtype integer not null
        constraint sublessons_substitutiontypes_id_fk
            references substitutiontypes,
    subteacher      integer not null
        constraint sublessons_users_userid_fk_2
            references users,
    userid          integer not null
        constraint sublessons_users_userid_fk
            references users,
    createdate      date    not null
);

alter table sublessons
    owner to postgres;

create table departments
(
    id       serial
        constraint departments_pk
            primary key,
    descr    varchar not null,
    shortcut varchar not null
);

alter table departments
    owner to postgres;

create table usertorole
(
    userid       integer not null
        constraint usertorole_users_userid_fk
            references users,
    roleid       integer not null
        constraint usertorole_roles_roleid_fk
            references roles,
    departmentid integer not null
        constraint usertorole_departments_id_fk
            references departments,
    constraint usertorole_pk
        primary key (userid, roleid, departmentid)
);

alter table usertorole
    owner to postgres;

create table fromattodepartment
(
    formatid     integer not null
        constraint table_name_forms_formatid_fk
            references forms,
    departmentid integer not null
        constraint fromattodepartment_pk
            primary key
        constraint fromattodepartment_departments_id_fk
            references departments
);

alter table fromattodepartment
    owner to postgres;



-- Metadaten ------------------------------------------

INSERT INTO public.statustypes (id, descr) VALUES (1, 'erstellt');
INSERT INTO public.statustypes (id, descr) VALUES (2, 'bearbeiten fertig gestellt');
INSERT INTO public.statustypes (id, descr) VALUES (3, 'abgelehnt von Bereichsleiter');
INSERT INTO public.statustypes (id, descr) VALUES (4, 'angenommen von Bereichsleiter');
INSERT INTO public.statustypes (id, descr) VALUES (5, 'abgelehnt von Vertretungsplaner');
INSERT INTO public.statustypes (id, descr) VALUES (6, 'angenommen von Vertretungsplaner');


INSERT INTO public.substitutiontypes (id, descr) VALUES (1, 'Fachvertretung');
INSERT INTO public.substitutiontypes (id, descr) VALUES (2, 'passive Vertretung');


INSERT INTO public.absensereasons (id, descr) VALUES (1, 'Dienstveranstaltung');
INSERT INTO public.absensereasons (id, descr) VALUES (2, 'Prüfungsausschuss');
INSERT INTO public.absensereasons (id, descr) VALUES (3, 'Fortbildung');
INSERT INTO public.absensereasons (id, descr) VALUES (4, 'Unterrichtsgang');
INSERT INTO public.absensereasons (id, descr) VALUES (5, 'Sonstiges');

INSERT INTO public.departments (id, descr, shortcut) VALUES (1, 'AV Abteilung', 'AV');
INSERT INTO public.departments (id, descr, shortcut) VALUES (2, 'Elektrotechnik', 'ET');
INSERT INTO public.departments (id, descr, shortcut) VALUES (3, 'IT Abteilung', 'IT');
INSERT INTO public.departments (id, descr, shortcut) VALUES (4, 'BFS Abteilung', 'BFS');
INSERT INTO public.departments (id, descr, shortcut) VALUES (5, 'ITA Abteilung', 'ITA');
INSERT INTO public.departments (id, descr, shortcut) VALUES (6, 'FOS Abteilung', 'FOS');
INSERT INTO public.departments (id, descr, shortcut) VALUES (7, 'FS Abteilung', 'FS');
