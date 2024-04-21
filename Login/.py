CREATE TABLE users (
    username text not null default ''::text,
    password text not null,
    constraint users_pkey primary key (username),
    constraint users_username_key unique (username),
    constraint users_password_check check (
      (
        length(
          trim(
            both
            from
              password
          )
        ) > 1
      )
    ),
    constraint users_username_check check (
      (
        length(
          trim(
            both
            from
              username
          )
        ) > 1
      )
    )
  ) tablespace pg_default;
