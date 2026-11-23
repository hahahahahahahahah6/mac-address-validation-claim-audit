# Documentation Claim Audit

This MIT-licensed offline tool compares documented claims about judging hardware address strings with recognizable Python call sites. It uses static patterns, not execution or semantic reasoning. Install either distribution with pip, then run:

```sh
python3 -m pip install mac_address_validation_claim_audit-0.1.0-py3-none-any.whl
mac-address-validation-claim-audit audit .
python3 -m mac_address_validation_claim_audit audit . --json --fail-on medium
```

The optional repository defaults to the current directory. Use `--verbose` for details and repeat `--ignore PREFIX` to exclude path prefixes. The default failure threshold is `high`; `medium` includes test-only findings. Exit status is 0 for a pass, 2 for findings at the threshold, and 1 for usage or I/O errors. The tool reads root README and Markdown under docs, excluding fenced blocks. Inline code counts. Production source, test source, fixtures, examples, and symlinks are treated separately.

Finding identifiers:

```text
documented-mac-address-validation-claim-false
documented-no-mac-address-validation-claim-false
```

## Differentiation


This audit concerns hardware address strings. Other families cover generic input checks; ISBN book-number and ISSN serial-number check digits; IBAN bank-account check digits; UUID identifiers; semantic versions; card payments; extracting card details; one-time codes and confirmation links for account authentication; password verification, hashing, generation, and strength; PDF encryption; sending email and SMS; document extraction; barcode decoding and generation; email address, phone number, JSON Schema, calendar date, card number, domain, URL, IP address, and numeric address checks. A possible BIC family concerns business identifiers.

Other operations include JSON decoding, regex matching, splitting or fetching a web address, DNS resolution, reading an account number from a document, hardware address retrieval, vendor prefix lookup, generation, formatting by changing separators or case, comparison, database lookup, and encoding an account number into a barcode strip. Those are distinct from judging an input string.

Other claim-audit families cover spreadsheet and word-document reading and generation, presentation reading and generation, PDF extraction, generation, merging, splitting, rotation, form-filling, watermarking, redaction, compression and annotation, table extraction, OCR, document extraction, e-signature, screen recording, video generation, QR and barcode generation, barcode scanning, audio mixing, generation and editing, source separation, speech recognition, text-to-speech, noise suppression, music generation and transcription. Their claims are outside this tool's phrase lists.

## Limitations

Matching is exact, so paraphrases are missed and unrelated uses can be flagged.

```text
validate mac address
```

A database or remote registry lookup may be intended. This can produce a false positive.

```text
check mac address
```

A manual runbook step may be intended. This can produce a false positive.

```text
mac address validation
```

A roadmap feature may be intended. This can produce a false positive.

```text
mac address validator
```

A hosted web page may be intended. This can produce a false positive.

```text
valid mac address
```

A reader advice may be intended. This can produce a false positive.

```text
mac address is valid
```

A successful lookup may be intended. This can produce a false positive.

```text
mac address string validation
```

A specification section may be intended. This can produce a false positive.

```text
validate mac address string
```

A allow-list check may be intended. This can produce a false positive.

```text
verify mac address
```

A registry existence lookup may be intended. This can produce a false positive.

```text
detect invalid mac address
```

A length-only check may be intended. This can produce a false positive.

```text
mac address well formed
```

A theoretical discussion may be intended. This can produce a false positive.

```text
is valid mac address
```

A generated value may be intended. This can produce a false positive.

```text
mac address format validation
```

A spacing-only check may be intended. This can produce a false positive.

```text
validate mac address version
```

This phrase is deliberately excluded; hardware addresses have no version to judge.

```text
validate mac
```

A Mac computer, app, or file check may be intended. This can produce a false positive.

```text
mac validation
```

A Mac computer or app check may be intended. This can produce a false positive.

```text
valid mac
```

A Mac computer test may be intended. This can produce a false positive.

```text
mac check
```

A Mac computer check may be intended. This can produce a false positive.

```text
mac address check
```

A manual runbook step may be intended. This can produce a false positive.

```text
mac address string check
```

A specification section may be intended. This can produce a false positive.

```text
validate hardware address
```

A database lookup may be intended. This can produce a false positive.

Integer-only EUI construction is not evidence.

Reading an EUI component is not evidence.

OUI construction is not evidence.

IAB construction is not evidence.

Retrieving the local address with getmac is not evidence.

Retrieving the local address with uuid is not evidence.

Reading interfaces with psutil is not evidence.

Reading interfaces with socket is not evidence.

Reading interfaces with ioctl is not evidence.

Matching a regular expression alone is not evidence.

The netaddr boolean route covers six-group addresses only.

Untraceable variable chains are missed.

A bare import is not evidence.

A roadmap claim still counts.

A changelog claim still counts.

A TODO claim still counts.

Denials outside the phrase list may be missed.

Claims outside root README and docs are missed.

Evidence split across modules does not combine.

Local definitions shadow route names.

Dead code counts as evidence.

Subprocess calls are not evidence.

A generic input check alone is not evidence.

An email check alone is not evidence.

A phone number check alone is not evidence.

A URL check alone is not evidence.

An IP address check alone is not evidence.

A domain check alone is not evidence.

An ISBN check alone is not evidence.

An ISSN check alone is not evidence.

An IBAN check alone is not evidence.

A UUID check alone is not evidence.

A semantic version check alone is not evidence.

Extraction alone is not evidence.

A locally defined generic route name is shadowed.

Untraceable alias chains are missed.

Only source files in the supported language are inspected.

Dynamic imports and runtime plugins are invisible.

The tool never executes inspected code or accesses the network.

