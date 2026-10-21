# Security architecture (v0.23)

Research control plane with strengthened zero-trust, expanded redaction (incl. BIP39), simulated lineage encryption, and lineage. Not a certified product.

## Trust boundaries

Synthetic fixtures -> Source attestation + Merkle-style lineage simulation (encrypted) -> Strategy rules + regime/anomaly/correlation -> Risk gate (caps, kill switch, drawdown, concentration) -> Paper fill only -> Hash-chained audit with encrypted lineage digest.

Trade/withdrawal keys refused. No live mode.

## Roles

Researcher / Auditor / Operator: all denied order placement. Operator can engage kill switch.

## Data classes

Symbol/OHLCV: public. Funding: public research. Source label: integrity (SYNTHETIC required). Read-only keys: optional, redacted. Trade keys: refused. Wallet: redacted/banned. Personal data: PDPA tripwire. Seeds: redacted.

## Enhanced controls

- Expanded redaction: API keys, secrets, passwords, tokens, AWS access keys, GitHub PATs, private key hex (64 chars), seed phrase proxies, BIP39 word proxies, JWTs, emails, wallets.
- Feed integrity: non-positive, stale (>15 min), jump (>25%), volume-price divergence anomaly.
- Anomaly score: statistical (skew, kurtosis), volume consistency, isolation proxy, RSI divergence.
- Audit: SHA-256 chain + simulated Merkle lineage over events with XOR encryption simulation.
- Zero-trust: mutual attestation simulation, isolation checks, data residency note (research only), correlation gates.

## Threats and controls

Secret committed: gitleaks + expanded redaction. Strategy injection: SYNTHETIC + attestation. Stale/jumped feed: status flags. Oversized risk: class caps + adaptive + correlation. Runaway: drawdown + kill switch. Audit tamper: chain + encrypted lineage. Live-order: mode guard + RBAC. Personal data / seeds: tripwire.

## Incident handling

1. Kill switch. 2. Freeze audit + lineage digest. 3. Rotate any pasted secret outside repo. 4. Human review before clear.

Default: research only. Promoting signals to broker is separate human-approved system.
