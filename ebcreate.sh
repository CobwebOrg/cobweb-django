#!/usr/bin/env bash

eb create cobweb-dev \
    --database \
    --database.engine postgres \
    --database.instance db.t2.micro \
    --database.size 5 \
    --database.username cobweb \
    