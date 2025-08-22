# Security Policy

## Supported Versions

Mastodon.py makes an effort to always be as backwards-compatible as possible so that you can update to the newest 
version without causing compatibility issues. As such, we're not generally going to backport any possible 
security-related fixes to older versions - the supported version is the latest one.

## Reporting a Vulnerability

If you find a security vulnerability that you think is critical enough to warrant such caution, please 
feel free to report it privately to halcy+mastopysec@halcy.de . I will try to respond as quickly as possible and
work through it with you.

A possible example of such a vulnerability would be a way for a malicious server instance to overwrite local files, 
or execute code on a client. A *non-example* would be a vulnerability in Mastodon itself - please report these to
Mastodon, not here, Mastodon.py does not *depend* on server software and as such is not transitively vulnerable.
