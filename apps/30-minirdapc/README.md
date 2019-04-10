# Mini RDAP Client

**Date: 2019-03-15**

**Author: carlos@xt6.us**

## Description

Simple, minimal RDAP client.

## Features

Has the following features:

- Queries for ip, autnum and entity
- Allows json search strings as parameter
- Has a simple local cache in order to avoid as much as possible hitting the server with the same queries
- Can be used as a CLI tool or as a library

## Usage:

Use as follows:

```
./minirdapc --query xxxx --type yyyy [--host rdap.lacnic.net] [--jq 'json query'] [--clean-cache]
```

Where: 

  - type: ip, autnum, entity
  - query: string to query rdap for
