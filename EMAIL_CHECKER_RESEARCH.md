# Email Checker Research

## What an email checker really does

An email checker is not just a regex.

In practice, a useful checker usually combines these layers:

1. Input normalization
2. Syntax validation
3. Domain validation
4. DNS mail-routing validation
5. Policy checks such as disposable-domain blocking
6. Optional SMTP probing
7. Real user-controlled verification by OTP or magic link

The last step is the only one that proves the user actually controls the inbox.

## How it works step by step

### 1. Normalize the input

Typical steps:

- trim whitespace
- split into `localPart@domain`
- lowercase the domain
- keep the local part unchanged unless you have provider-specific rules
- convert internationalized domains to IDNA / punycode if needed

Important note:

- `validator.js` documents that lowercasing the entire local part may violate RFC 5321 because local parts can be case-sensitive in theory

### 2. Validate syntax

Do not try to hand-write a huge RFC regex.

Practical approach:

- client side: use `<input type="email">`
- server side: validate again with a library such as `validator.js`

Important reality:

- browser validation only means the value looks like an email address
- it does not prove that the mailbox exists

### 3. Validate the domain

Check that:

- the domain is a valid FQDN
- the domain actually resolves
- if the domain is internationalized, DNS lookup uses IDNA-compatible form

Advanced note:

- RFC 6531 allows internationalized mailbox names through `SMTPUTF8`
- if you do not want that complexity in MVP, accept ASCII mailbox names first and add SMTPUTF8 later

### 4. Check DNS for mail delivery

This is the most important technical step after syntax validation.

Flow:

1. Query MX records for the domain
2. If MX records exist, use them
3. If no MX records exist, RFC 5321 says the domain may still accept mail via an implicit MX using its A or AAAA record
4. If the domain publishes a Null MX (`MX 0 .`), it explicitly does not accept email

This means:

- `no MX` does not always mean `invalid`
- `Null MX` is a strong `invalid for email delivery` signal

### 5. Apply policy checks

These are business rules, not protocol rules.

Common checks:

- disposable or temporary email domain
- role-based inbox such as `admin@`, `support@`, `info@`
- blocked provider list
- allowlist for company-only signup such as `@yourcompany.com`

Disposable-domain checks are usually done with a maintained list instead of custom guessing.

### 6. Optional SMTP probing

This is the classic "mailbox exists?" check, but it is tricky.

How it usually works:

1. Connect to the chosen MX host on SMTP
2. Send `EHLO`
3. Send `MAIL FROM:<>` or a controlled sender
4. Send `RCPT TO:<target@example.com>`
5. Interpret the reply

Possible outcomes:

- server rejects recipient immediately
- server accepts recipient
- server accepts everything because it is catch-all
- server delays decision until after `DATA`
- server rate-limits, tarpits, or blocks probes

Why this is unreliable:

- RFC 5321 says some servers do not perform recipient verification until after message data is received
- RFC 5321 also notes that sites may disable or limit `VRFY` and `EXPN` for security reasons
- SMTP command timeouts can be long enough that inline signup-time probing hurts UX

Recommendation:

- do not depend on SMTP probing for your MVP
- if you use it, run it asynchronously in a background job and treat the result as probabilistic

### 7. Real verification

If your product needs confidence that the user owns the mailbox, do this:

- send OTP code or magic link
- mark the email as verified only after the user clicks or submits the code

This is more trustworthy than SMTP probing.

## Best MVP to build first

If you want a useful production-ready first version, build this:

1. Frontend email field with basic instant feedback
2. Backend endpoint such as `POST /api/check-email`
3. Server-side syntax validation
4. DNS MX lookup plus implicit A/AAAA fallback handling
5. Null MX detection
6. Disposable-domain blocklist check
7. Verification email with OTP or magic link
8. Cache DNS results and rate-limit the endpoint

This gets you most of the value without risky SMTP behavior.

## Advanced version after MVP

After the MVP works, you can add:

- SMTP probe worker
- catch-all detection
- provider-specific normalization rules
- risk scoring instead of binary valid/invalid
- audit logging
- analytics dashboard for invalid or risky signups
- admin rules for allowlist and blocklist management

## Suggested statuses to return from the API

Instead of a single boolean, return structured status values:

- `invalid_syntax`
- `invalid_domain`
- `null_mx`
- `no_mail_route`
- `disposable_domain`
- `risky_role_based`
- `smtp_unconfirmed`
- `deliverable_likely`
- `verified`

This makes the UI and future reporting much easier.

## Suggested Node.js implementation

Because this repository is empty, a practical JS/Node stack would be:

- `validator.js` for syntax validation
- `node:dns/promises` for `resolveMx()` and A/AAAA lookups
- `nodemailer` for OTP or magic-link emails
- `bullmq` or another queue if you later add SMTP probes
- a maintained disposable-domain source such as `disposable-email-domains` or `mailchecker`

## Minimal architecture

One clean service split is:

- `emailNormalizer`
- `emailSyntaxValidator`
- `emailDnsChecker`
- `emailPolicyChecker`
- `emailVerificationSender`
- `emailCheckController`

That keeps the code easy to test and extend.

## Pseudocode for the core decision flow

```ts
async function checkEmail(rawEmail: string) {
  const email = normalizeEmailInput(rawEmail);

  if (!isValidSyntax(email)) {
    return { status: "invalid_syntax" };
  }

  const { localPart, domain } = splitEmail(email);

  if (isDisposableDomain(domain)) {
    return { status: "disposable_domain" };
  }

  const dnsResult = await lookupMailRouting(domain);

  if (dnsResult.nullMx) {
    return { status: "null_mx" };
  }

  if (!dnsResult.hasMailRoute) {
    return { status: "no_mail_route" };
  }

  return {
    status: "deliverable_likely",
    mailHosts: dnsResult.mailHosts,
  };
}
```

## Important product decision

If the goal is:

- "does this string look like an email?" then syntax is enough
- "can mail probably be routed?" then syntax plus DNS is enough
- "does the user own the mailbox?" then OTP or magic link is required

These are different products, and mixing them causes bad UX and wrong expectations.

## Recommended build order

1. Syntax validation
2. DNS mail-route check
3. Disposable-domain filter
4. Verification email flow
5. Background SMTP probing only if your business truly needs it

## Sources

- RFC 5322: Internet Message Format
  https://datatracker.ietf.org/doc/html/rfc5322
- RFC 5321: Simple Mail Transfer Protocol
  https://datatracker.ietf.org/doc/rfc5321/
- RFC 7505: Null MX
  https://datatracker.ietf.org/doc/html/rfc7505
- RFC 6531: SMTPUTF8 for internationalized email
  https://datatracker.ietf.org/doc/rfc6531/
- MDN `<input type="email">`
  https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/email
- Node.js DNS docs
  https://nodejs.org/api/dns.html
- validator.js
  https://github.com/validatorjs/validator.js
- disposable-email-domains
  https://github.com/disposable-email-domains/disposable-email-domains
