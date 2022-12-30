# github.com/ncwhale/docker-caddy-cloudflare-companion

[![GitHub release](https://img.shields.io/github/v/tag/ncwhale/docker-caddy-cloudflare-companion?style=flat-square)](https://github.com/ncwhale/docker-caddy-cloudflare-companion/releases/latest)
[![Build Status](https://img.shields.io/github/workflow/status/ncwhale/docker-caddy-cloudflare-companion/build?style=flat-square)](https://github.com/ncwhale/docker-caddy-cloudflare-companion/actions?query=workflow%3Abuild)
[![Docker Stars](https://img.shields.io/docker/stars/whalemo/caddy-cloudflare-companion.svg?style=flat-square&logo=docker)](https://hub.docker.com/r/whalemo/caddy-cloudflare-companion/)
[![Docker Pulls](https://img.shields.io/docker/pulls/whalemo/caddy-cloudflare-companion.svg?style=flat-square&logo=docker)](https://hub.docker.com/r/whalemo/caddy-cloudflare-companion/)
[![Become a sponsor](https://img.shields.io/badge/sponsor-ncwhale-181717.svg?logo=github&style=flat-square)](https://github.com/sponsors/ncwhale)

## About

This builds a Docker image to automatically update Cloudflare DNS records upon container start. A time saver if you are regularly moving containers around to different systems. This will allow you to set multiple zone's you wish to update.

    Fork from: [tiredofit/docker-traefik-cloudflare-companion](https://github.com/tiredofit/docker-traefik-cloudflare-companion)

## Maintainer

- [Whale Mo](http://github/ncwhale/)

## Table of Contents

- [github.com/ncwhale/docker-caddy-cloudflare-companion](#githubcomncwhaledocker-caddy-cloudflare-companion)
  - [About](#about)
  - [Maintainer](#maintainer)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites and Assumptions](#prerequisites-and-assumptions)
  - [Installation](#installation)
    - [Build from Source](#build-from-source)
    - [Prebuilt Images](#prebuilt-images)
      - [Multi Architecture](#multi-architecture)
  - [Configuration](#configuration)
    - [Quick Start](#quick-start)
    - [Persistent Storage](#persistent-storage)
    - [Environment Variables](#environment-variables)
      - [Base Images used](#base-images-used)
      - [Docker Secrets](#docker-secrets)
    - [Discovery](#discovery)
      - [Docker](#docker)
      - [Docker Swarm](#docker-swarm)
      - [Caddy Polling](#caddy-polling)
        - [Filtering](#filtering)
          - [Include Patterns](#include-patterns)
          - [Exclude Patterns](#exclude-patterns)
  - [Maintenance](#maintenance)
    - [Shell Access](#shell-access)
  - [Support](#support)
    - [Usage](#usage)
    - [Bugfixes](#bugfixes)
    - [Feature Requests](#feature-requests)
    - [Updates](#updates)
  - [License](#license)
  - [References](#references)

## Prerequisites and Assumptions
*  Assumes you have either a Global or a Scoped API key from Cloudflare.
*  Assumes you are using Caddy as a reverse proxy with `caddy-docker-proxy`:
   * [Caddy](https://caddyserver.com/)
   * [caddy-docker-proxy](https://github.com/lucaslorentz/caddy-docker-proxy)

## Installation
### Build from Source
Clone this repository and build the image with `docker build -t (imagename) .`

### Prebuilt Images
Builds of the image are available on [Docker Hub](https://hub.docker.com/r/whalemo/caddy-cloudflare-companion) and is the recommended method of installation.

```bash
docker pull whalemo/caddy-cloudflare-companion:(imagetag)
```
The following image tags are available along with their tagged release based on what's written in the [Changelog](CHANGELOG.md):

| Container OS | Tag       |
| ------------ | --------- |
| Alpine       | `:latest` |

#### Multi Architecture
Images are built primarily for `amd64` architecture, and may also include builds for `arm/v6`, `arm/v7`, `arm64` and others. These variants are all unsupported. Consider [sponsoring](https://github.com/sponsors/ncwhale) my work so that I can work with various hardware. To see if this image supports multiple architecures, type `docker manifest (image):(tag)`

## Configuration

### Quick Start

* The quickest way to get started is using [docker-compose](https://docs.docker.com/compose/). See the examples folder for a working [docker-compose.yml](examples/docker-compose.yml) that can be modified for development or production use.

* Set various [environment variables](#environment-variables) to understand the capabilities of this image.

Upon startup the image looks for a label containing `caddy[_\d+]` (version 2) from your running containers of either updates Cloudflare with a CNAME record of your `TARGET_DOMAIN`. Previous versions of this container used to only update one Zone, however with the additional of the `DOMAIN` environment variables it now parses the containers variables and updates the appropriate zone.

For those wishing to assign multiple CNAMEs to a container use the following format:

- Caddy 2.x
````
labels:
  caddy: example1.domain.tld, example2.domain.tld
  caddy_1: example3.domain.tld
````

### Persistent Storage
| File                   | Description                                                              |
| ---------------------- | ------------------------------------------------------------------------ |
| `/var/run/docker.sock` | You must have access to the docker socket in order to utilize this image |

* * *
### Environment Variables

#### Base Images used

This image relies on an [Alpine Linux](https://hub.docker.com/r/tiredofit/alpine) base image that relies on an [init system](https://github.com/just-containers/s6-overlay) for added capabilities. Outgoing SMTP capabilities are handlded via `msmtp`. Individual container performance monitoring is performed by [zabbix-agent](https://zabbix.org). Additional tools include: `bash`,`curl`,`less`,`logrotate`, `nano`,`vim`.

Be sure to view the following repositories to understand all the customizable options:

| Image                                                  | Description                            |
| ------------------------------------------------------ | -------------------------------------- |
| [OS Base](https://github.com/tiredofit/docker-alpine/) | Customized Image based on Alpine Linux |


| Parameter                      | Description                                                                                                                                          | Default                      |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| `CADDY_VERSION`                | What version of Caddy do you want to work with - `2` Only                                                                                            | `2`                          |
| `DOCKER_ENTRYPOINT`            | Docker Entrypoint default (local mode)                                                                                                               | `unix://var/run/docker.sock` |
| `DOCKER_HOST`                  | (optional) If using tcp connection e.g. `tcp://111.222.111.32:2376`                                                                                  |                              |
| `DOCKER_CERT_PATH`             | (optional) If using tcp connection with TLS - Certificate location e.g. `/docker-certs`                                                              |                              |
| `DOCKER_TLS_VERIFY`            | (optional) If using tcp conneciton to socket Verify TLS                                                                                              | `1`                          |
| `REFRESH_ENTRIES`              | If record exists, update entry with new values `TRUE` or `FALSE`                                                                                     | `FALSE`                      |
| `SWARM_MODE`                   | Enable Docker Swarm Mode `TRUE` or `FALSE`                                                                                                           | `FALSE`                      |
| `ENABLE_CADDY_POLL`            | Enable Caddy Polling Mode `TRUE` or `FALSE`                                                                                                          | `FALSE`                      |
| `CADDY_POLL_URL`               | (optional) If using Caddy Polling mode - URL to Caddy API endpoint                                                                                   |                              |
| `CADDY_POLL_SECONDS`           | (optional) If using Caddy Polling mode - Seconds to delay between poll attemps                                                                       | `60`                         |
| `CADDY_INCLUDED_HOST1`         | (optional) If using Caddy Polling mode - Regex patterns for hosts to include                                                                         | `.*`                         |
| `CADDY_INCLUDED_HOST...`       | (optional caddy host include pattern 2 - N)                                                                                                          |                              |
| `CADDY_EXCLUDED_HOST1`         | (optional) If using Caddy Polling mode - Regex patterns for hosts to exclude                                                                         |                              |
| `CADDY_EXCLUDED_HOST...`       | (optional caddy host exclude pattern 2 - N)                                                                                                          |                              |
| `DRY_RUN`                      | Enable Dry Run Mode `TRUE` or `FALSE`                                                                                                                | `FALSE`                      |
| `CF_EMAIL`                     | Email address tied to Cloudflare Account - Leave Blank  for Scoped API                                                                               |                              |
| `CF_TOKEN`                     | API Token for the Domain                                                                                                                             |                              |
| `DEFAULT_TTL`                  | TTL to apply to records                                                                                                                              | `1`                          |
| `TARGET_DOMAIN`                | Destination Host to forward records to e.g. `host.example.com`                                                                                       |                              |
| `DOMAIN1`                      | Domain 1 you wish to update records for.                                                                                                             |                              |
| `DOMAIN1_ZONE_ID`              | Domain 1 Zone ID from Cloudflare                                                                                                                     |                              |
| `DOMAIN1_PROXIED`              | Domain 1 True or False if proxied                                                                                                                    |                              |
| `DOMAIN1_TARGET_DOMAIN`        | (optional specify target_domain for Domain 1, overriding the default value from TARGET_DOMAIN)                                                       |                              |
| `DOMAIN1_EXCLUDED_SUB_DOMAINS` | (optional specify sub domain trees to be ignored in lables) ex: `DOMAIN1_EXCLUDED_SUB_DOMAINS=int` would not create a CNAME for `*.int.example.com`  |                              |
| `DOMAIN2`                      | (optional Domain 2 you wish to update records for.)                                                                                                  |                              |
| `DOMAIN2_ZONE_ID`              | Domain 2 Zone ID from Cloudflare                                                                                                                     |                              |
| `DOMAIN2_PROXIED`              | Domain 1 True or False if proxied                                                                                                                    |                              |
| `DOMAIN2_TARGET_DOMAIN`        | (optional specify target_domain for Domain 2, overriding the default value from TARGET_DOMAIN)                                                       |                              |
| `DOMAIN2_EXCLUDED_SUB_DOMAINS` | (optional specify sub domain trees to be ignored in lables) ex: `DOMAIN2_EXCLUDED_SUB_DOMAINS=int` would not create a CNAME for `*.int.example2.com` |                              |
| `DOMAIN3....`                  | And so on..                                                                                                                                          |                              |

#### Docker Secrets

`CF_EMAIL` and `CF_TOKEN` support Docker Secrets
Name your secrets either CF_EMAIL and CF_TOKEN or cf_email and cf_token.

### Discovery

cloudflare-companion supports three different discovery mode: Docker, Docker Swarm, and Caddy Polling.  The Docker discovery mode is the only mode enabled by default.  Once matching hosts are discovered, cloudflare-companion will add or update CNAMEs in CloudFlare that point to the configured `TARGET_DOMAIN`.

#### Docker

cloudflare-companion will discover running Docker containers by searching for supported labels.

The supported labels are:

| Caddy Version | Single Host                  | Multiple Host                                     |
| ------------- | ---------------------------- | ------------------------------------------------- |
| 2             | `caddy: example1.domain.tld` | `caddy: example1.domain.tld, example2.domain.tld`<br>`caddy_1: example3.domain.tld` |

#### Docker Swarm

Docker Swarm mode can be enabled by setting the environment variable `SWARM_MODE=TRUE`.  This will cause cloudflare-companion to discover running Docker Swarm services with supported labels.

The supported labels are:

| Caddy Version | Single Host                  | Multiple Host                                     |
| ------------- | ---------------------------- | ------------------------------------------------- |
| 2             | `caddy: example1.domain.tld` | `caddy: example1.domain.tld, example2.domain.tld`<br>`caddy_1: example3.domain.tld` |

#### Caddy Polling

Caddy Polling mode can be enabled by setting the environment variable `CADDY_VERSION=2`, `ENABLE_CADDY_POLL=TRUE`, and `CADDY_POLL_URL=http://<host>:<port>`.  This will cause cloudflare-companion to poll Caddy every 60s (default) and discover routers and include hosts which match the following rules:

1. Provider is not docker
2. Name is present and match the Domain Name Rule
3. Both http and tls hostnames are try to match
4. Host matches include patterns (default: .*)
5. Host does not match exclude patterns (default: none)

The polling interval can be configured by setting the environment variable `CADDY_POLL_SECONDS=120`.

##### Filtering

Discovered hosts are matched against include and exclude patterns to determine if they should be included in the sync to CloudFlare.  By default, all found hosts are included.  Exclude patterns are higher priority than include patterns.  The defaults can be changed by configuring include and exclude patterns.

###### Include Patterns

Include patterns can be specified by defining one or more `CADDY_INCLUDED_HOST<XXX>` variables such as `CADDY_INCLUDED_HOST1=.*-data\.foobar\.com` and `CADDY_INCLUDED_HOST2=.*-api\.foobar\.com`.  The pattern is a regular expression that is used to determine if the host should be included.

###### Exclude Patterns

Exclude patterns can be specified by defining one or more `CADDY_EXCLUDED_HOST<XXX>` variables such as `CADDY_EXCLUDED_HOST1=private-data\.foobar\.com` and `CADDY_EXCLUDED_HOST2=.*-internal-api\.foobar\.com`.  The pattern is a regular expression that is used to determine if the host should be excluded.  Exclude patterns filter out results after include patterns are executed.

## Maintenance
### Shell Access

For debugging and maintenance purposes you may want access the containers shell.

```bash
docker exec -it (whatever your container name is e.g. caddy-cloudflare-companion) bash
```

## Support

These images were built to serve a specific need in a production environment and gradually have had more functionality added based on requests from the community.
### Usage
- The [Discussions board](../../discussions) is a great place for working with the community on tips and tricks of using this image.
- Consider [sponsoring me](https://github.com/sponsors/ncwhale) personalized support.
### Bugfixes
- Please, submit a [Bug Report](issues/new) if something isn't working as expected. I'll do my best to issue a fix in short order.

### Feature Requests
- Feel free to submit a feature request, however there is no guarantee that it will be added, or at what timeline.
- Consider [sponsoring me](https://github.com/sponsors/ncwhale) regarding development of features.

### Updates
- Best effort to track upstream changes, More priority if I am actively using the image in a production environment.
- Consider [sponsoring me](https://github.com/sponsors/ncwhale) for up to date releases.

## License
MIT. See [LICENSE](LICENSE) for more details.

## References

* https://www.cloudflare.com
* https://github.com/tiredofit/docker-traefik-cloudflare-companion
* https://github.com/code5-lab/dns-flare
