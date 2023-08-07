---
title: Homelab Single-Sign On?
slug: homelab-single-sign-on
date: 2023-02-01T11:00:00.000Z
draft: false
featured: false
image: "images/cover.jpg"
tags:
    - Homelab
    - Docker
    - Security
    - Tutorials
authors:
    - samuel
---

Installing an SSO solution in my homelab with Authelia to facilitate the user management and reduce the number of logins required.

<!--more-->

First, what is single-sign-on:
> **Single sign-on** (**SSO**) is an authentication scheme that allows a user to login with a single ID to any of several related, yet independent, software systems.
> 
> True single sign-on allows the user to log in once and access services without re-entering authentication factors. It should not be confused with same-sign on (Directory Server Authentication), it refers to systems requiring authentication for each application but using the same credentials from a directory server

In my homelab, I don't really care if I need to reenter my login/password to sign in to an app. So, what I'm actually using is Same-Sign On, however, in this article I'll only show examples of Single-Sign On in this post.

## Which one?

There are multiple options, which all have advantages/disadvantages. Here is a list of the one I investigated and my up/downs of each:
- CAS (Central Authentication Service)
	- Overall really amazing 🔥, it's used by numerous universities in France mainly because the CAS protocol is available on many educational tools like Moodle. However, it's Java-based which already tells a lot, it's extremely resource intensive, especially on the ram. It's also a bit annoying to configure since you need to recompile the thing each time. It supports just about every authentication source and authentication protocol possible
	- Keycloak, pretty suitable option, it's a bit more lightweight than CAS (but it's still Java 😒). It supports an LDAP backend. Overall pretty fantastic, used by numerous pros.
	- ADFS, I want the damn thing to work, lol
	- Kerberos, well, it might work but not many tools/app support it, so it's a no-go
	- Authelia, it's perfect, Go-based, supports most of the authentication scheme I want to use, as well as Webauthn, TOTP and mobile push notifications, easy to configure, pretty good community, multiple integrations with proxies and apps

I tested a lot of them, so I probably forgot to mention one, don't hesitate to comment!

## Installation
I choose to use the full `docker-compose` method with some modifications to suit my setup. The original example uses traefik because it assumes the same network this is fine, but I'm using multiple hosts for apps, so it had to go. Here is what my docker-compose.yml looks like:

```yaml
version: '3.1'
services:
  server:
    image: caddy
    ports:
      - '80:80'
      - '443:443'
    volumes:
      - './Caddyfile:/etc/caddy/Caddyfile'
      - './root_ca.pem:/etc/caddy/root_ca.pem'
      - './certs:/certs'
    restart: unless-stopped

  authelia:
     image: authelia/authelia
     container_name: authelia
     ports:
        - 9091:9091/tcp
     volumes:
        - ./authelia:/config
     restart: unless-stopped
     
  redis:
    image: redis:alpine
    container_name: redis
    volumes:
     - ./redis:/data
    expose:
      - 6379
    restart: unless-stopped
```

The `Caddyfile` is pretty simple, just a simple reverse proxy that registers the domain to my acme server: 
```caddy
auth.internal.tugler.fr {
        tls {
                ca https://cert.internal.tugler.fr/acme/acme/directory
                ca_root /etc/caddy/root_ca.pem
        }
        reverse_proxy authelia:9091
}
```
## Configuration
The Authelia config is pretty long but easy to do compared to some other tools I tried.

The first thing to configure is some internal settings to Authelia, like default variables
```yaml
theme: light

jwt_secret: -----censored-----
default_redirection_url: https://internal.tugler.fr/
default_2fa_method: ""
```

Next is the server, the `docker-compose.yml` exposes port 9091, so it's the one to be used, I'm using the subdomain `auth.internal.tugler.fr` so I don't need to change the root path. I also didn't set up ssl directly in there because I have it in the reverse proxy with the acme. The rest is default.
```yaml
server:
  host: 0.0.0.0
  port: 9091

  path: ""
  # asset_path: /config/assets/

  read_buffer_size: 4096
  write_buffer_size: 4096

  enable_pprof: false
  enable_expvars: false
  
  disable_healthcheck: false

  tls:
    key: ""
    certificate: ""
    client_certificates: []

  headers:
    csp_template: ""
```
I don't need to save the logs (docker takes care of it anyway usually) so, debug level and that's it.
```yaml
log:
  level: debug
  # format: json
  # file_path: /config/authelia.log
  # keep_stdout: false
```
Next is double authentication, I've enabled TOTP and WebAuthn just in case, but I don't actually intend to use it on most apps, maybe on core services like proxmox, but it's not determined yet
```yaml
totp:
  disable: false
  issuer: tugler.fr
  algorithm: sha1
  digits: 6
  period: 30
  skew: 1
  secret_size: 32
  
webauthn:
  disable: false
  timeout: 60s
  display_name: Tugler
  attestation_conveyance_preference: indirect
  user_verification: preferred

duo_api:
  disable: true
  hostname: api-123456789.example.com
  integration_key: ABCDEF
  secret_key: 1234567890abcdefghifjkl
  enable_self_enrollment: false
```

Needs the time to be accurate, apparently 🤷‍♂️
```yaml
ntp:
  address: "time.cloudflare.com:123"
  version: 4
  max_desync: 3s
  disable_startup_check: false
  disable_failure: false

```

Next, I need to set up the actual backend, to check users I have a Windows server running just for that (it's about the only thing that works well). The config was pretty simple, there is a pretty good example in the docs to get started. Even if my `ldap_bind` user has the permissions to modify password, I didn't actually enable it for now. 
The password policy also doesn't need to be enabled.
```yaml
authentication_backend:
  disable_reset_password: true

  password_reset:
    custom_url: ""

  refresh_interval: 5m

  ldap:
    implementation: activedirectory
    url: ldap://ad1.internal.tugler.fr
    timeout: 5s
    start_tls: false
    tls:
      skip_verify: false
      minimum_version: TLS1.2

    base_dn: dc=tugler,dc=fr
    username_attribute: sAMAccountName
    additional_users_dn: ou=People
    users_filter: (&({username_attribute}={input})(objectCategory=person)(objectClass=user))
    
    additional_groups_dn: ou=Groups
    groups_filter: (&(member={dn})(objectClass=group))
    group_name_attribute: cn

    mail_attribute: mail
    # display_name_attribute: displayName
    permit_referrals: false

    user: cn=ldap_bind,cn=Users,dc=tugler,dc=fr
    password: -----censored-----

password_policy:
  standard:
    enabled: false
    min_length: 8
    max_length: 0
    require_uppercase: true
    require_lowercase: true
    require_number: true
    require_special: true
  zxcvbn:
    enabled: false
    min_score: 3
```

Next is the access control part, the default is to deny everything, I allow my internal network at `10.10.0.0/16` and the network of my internal VPN at `10.5.0.0/16`.
I also added set my app dashboard (`internal.tugler.fr`) to bypass any auth and only allow users with the group `Apps_Paperless_Admin` to access `paperless.internal.tugler.fr` (explained later).
I then proceeded by configuring the Redis cache for the session store and the anti-brute force settings.
```yaml
access_control:
  default_policy: deny

  networks:
    - name: internal
      networks:
        - 10.10.0.0/16
    - name: VPN
      networks: 10.5.0.0/16

  rules:
    - domain: 'internal.tugler.fr'
      policy: bypass

    - domain: 'paperless.internal.tugler.fr'
      policy: one_factor
      subject:
        - ['group:Apps_Paperless_Admin']
        
session:
  name: authelia_session
  domain: internal.tugler.fr
  same_site: lax
  secret: -----censored-----

  expiration: 4h
  inactivity: 45m
  remember_me_duration: 1M
  
  redis:
    host: redis
    port: 6379

regulation:
  max_retries: 3
  find_time: 2m
  ban_time: 5m
```

Then, I added the credentials for my PostgreSQL database 
```yaml
storage:
  encryption_key: -----censored-----
  postgres:
    host: db.internal.tugler.fr
    port: 5432
    database: authelia
    username: authelia
    password: -----censored-----
    timeout: 5s
```
Notifications are something I didn't configure, I'll probably add email notifications in the future, but I don't have a mail server setup right now, so file system notification it is, just to make the thing happy.
```yaml
notifier:
  disable_startup_check: false
  filesystem:
    filename: /config/notification.txt
```

The final thing to configure is the OpenID connect provider, for which I basically used the default config. The `clients` array will be configured on the next part.
```yaml
identity_providers:
  oidc:
    hmac_secret: -----censored-----
    issuer_private_key: |
        -----BEGIN RSA PRIVATE KEY-----
              -----censored-----
        -----END RSA PRIVATE KEY-----

    access_token_lifespan: 4h
    authorize_code_lifespan: 5m
    id_token_lifespan: 4h
    refresh_token_lifespan: 2h

    cors:
      endpoints:
         - authorization
         - token
         - revocation
         - introspection
         - userinfo

      allowed_origins_from_client_redirect_uris: true
      
    clients: []
```

And that's it.

## Configuration
### Proxmox Backup Server
The PBS is pretty easy to configure because it supports OpenID Connect, the only thing to set is the ID, the secret, the redirect URI and the scopes.
```yaml
      - id: pbs
        description: ProxmoxBackup
        secret: -----censored-----
        public: false
        authorization_policy: one_factor
        scopes:
          - openid
          - groups
          - email
          - profile

        redirect_uris:
          - https://10.10.15.23:8007
        userinfo_signing_algorithm: RS256
```
Server side it's the url of Authelia, the ID, secret and scope
![enter image description here](images/dl_firefox_2022_12_06_12-31-40_Z3VHXrCux4.png)

Here is a demo:
https://youtu.be/EpZrtVe7h_M

### Paperless-NGX
Paperless is a bit different since it doesn't support traditional auth methods like OIDC, LDAP, SAML, …. Instead, it supports header auth (See: https://github.com/paperless-ngx/paperless-ngx/pull/100#issuecomment-1045277482). 

Basically, you need a reverse proxy that will do the authentication and send user information as a header to the source. Here is my config for caddy:
```caddy
paperless.internal.tugler.fr {
        tls {
                ca https://cert.internal.tugler.fr/acme/acme/directory
                ca_root /etc/caddy/root_ca.pem
        }
        forward_auth http://auth.internal.tugler.fr:9091 {
                uri /api/verify?rd=https://auth.internal.tugler.fr
                copy_headers Remote-User Remote-Groups Remote-Name Remote-Email
        }
        redir /404     /dashboard
        reverse_proxy paperless:8000
}
direct.paperless.internal.tugler.fr {
        tls {
                ca https://cert.internal.tugler.fr/acme/acme/directory
                ca_root /etc/caddy/root_ca.pem
        }
        reverse_proxy paperless:8000
}
```
My case is a bit special because I use the api of paperless for automatically ingesting PDFs from my emails and can't automate the login flow. 
Hence, why I have two hosts, one is `direct.paperless.internal.tugler.fr` which proxies paperless directly (And use the standard paperless auth which have one user specifically for this), and the other is `paperless.internal.tugler.fr` which goes through Authelia first.

Caddy is configured to send these headers to paperless:
- Remote-User → Username
- Remote-Groups → Groups of said user
- Remote-Name → Full name of the user
- Remote-Email → Email of the user

I also needed to configure environment variables for the docker container. Here is a **very** reduced example:
```yaml
  paperless:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    restart: unless-stopped
    environment:
      PAPERLESS_ENABLE_HTTP_REMOTE_USER: 1
      PAPERLESS_LOGOUT_REDIRECT_URL: https://auth.internal.tugler.fr/logout?rq=https://paperless.internal.tugler.fr
```
Demo video:
https://youtu.be/9sVzXl-Ttlk

#### Update
Seems that there are some discussions in the Paperless-NGX repo about multi-user, permission and SSO support:
- https://github.com/paperless-ngx/paperless-ngx/discussions/295
- https://github.com/paperless-ngx/paperless-ngx/discussions/625
- https://github.com/paperless-ngx/paperless-ngx/pull/1746
It would be wonderful to be able to use OIDC directly instead of the in my opinion, hacky remote header way.

## Conclusion
Overall, I'm very pleased with this setup. It will simplify the login process for all the apps and eliminate the need for multiple user database (for those which don't support LDAP) 😀. 

Moreover, it's f-ing cool to have a proper setup in a homelab 😎.
**Self-Host all the things!**
