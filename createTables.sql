CREATE TABLE binaryhashes (
    name text,
    set text,
    ahash bit(64),
    phash bit(64),
    psimplehash bit(64),
    dhash bit(64),
    vertdhash bit(64),
    whash bit(64)
);

CREATE TABLE hashes (
    name text,
    set text,
    ahash bytea,
    phash bytea,
    psimplehash bytea,
    dhash bytea,
    vertdhash bytea,
    whash bytea
);

