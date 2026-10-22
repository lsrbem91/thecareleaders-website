# Cloudflare DNS for thecareleaders.com before the switch (22 October 2026, 22:10)

Rollback: set the two website records back to these values (Proxied).

| Name | Type | Content | Proxy |
|---|---|---|---|
| thecareleaders.com | A | 185.53.56.90 | Proxied |
| www.thecareleaders.com | A | 185.53.56.90 | Proxied |
| k2._domainkey | CNAME | dkim2.mcsv.net | DNS only (Mailchimp) |
| k3._domainkey | CNAME | dkim3.mcsv.net | DNS only (Mailchimp) |
| lwmail | CNAME | eu.mailgun.org | DNS only |
| s1._domainkey | CNAME | s1._domainkey.thecareleaders.com.s011.ascendbywix.com | Proxied |
| s2._domainkey | CNAME | s2._domainkey.thecareleaders.com.s011.ascendbywix.com | Proxied |
| sel1._domainkey | CNAME | sel1._domainkey.thecareleaders.com.ascendbywix.com | Proxied |
| thecareleaders.com | MX 10 | thecareleaders-com.mail.protection.outlook.com | DNS only |
| _dmarc | TXT | v=DMARC1; p=none; fo=1; rua=mailto:hello@thecareleaders.com | DNS only |
| email._domainkey | TXT | k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC3N6eUBXdQd3+LepfTvOsT34Hum1QNtG1/EyxYoS7oa80pxd+N8XUvzLdSs5IDH77NRPIP+PLE/XAx3+LfMXeZ68XYBfKVpi8CqdGn2v4RYczFDilcOBc+3yN/124HQRfL0VSLnCYTf0CBiJdyuyCg3jktY/0JeYI84sRinTMQ9QIDAQAB | DNS only |
| thecareleaders.com | TXT | lw=657869b804b2d5c858ec1644 | DNS only |
| thecareleaders.com | TXT | v=spf1 include:spf.protection.outlook.com include:relay.mailchannels.net ip4:185.53.56.85 ip4:185.53.56.86 ip4:185.53.56.90 include:mailgun.org -all | DNS only |

Nameservers: colette.ns.cloudflare.com, marty.ns.cloudflare.com (registrar 20i).

## careleadersfellowship.com (Cloudflare zone), original Wix records, replaced 22 Oct 2026
- A @ 185.230.63.107 (proxied)
- A @ 185.230.63.171 (proxied)
- A @ 185.230.63.186 (proxied)
- CNAME www cdn3.wixdns.net (proxied)
Replaced with A @ 192.0.2.1 and A www 192.0.2.1 (proxied) so the redirect rule to /fellowship.html fires. Wix answered first while the records pointed at it.
