# SLA targets (fill "Measured" after your tests)
| Metric | Target | Measured |
|---|---|---|
| Availability | 99.5% monthly | |
| Response time (p95) | < 500 ms | (scripts/loadtest.sh) |
| RTO / TTR | < 120 s | (scripts/ttr_test.sh) |
| Error rate under load | < 1% | |

99.5% availability allows about 3.6 hours of downtime per month.

# Cost estimate (approx. ap-south-1 Mumbai; verify in AWS Pricing Calculator; 1 USD = Rs 85 assumed)
| Item | Monthly (USD) | Monthly (Rs) |
|---|---|---|
| EC2 t3.micro (or free-tier type if eligible) | ~9 | ~765 |
| 20 GB gp3 EBS | ~2 | ~170 |
| Application Load Balancer | ~20 | ~1,700 |
| Data transfer + CloudWatch (basic) | ~2 | ~170 |
| **Total (with ALB)** | **~33** | **~2,800** |
| **Total (single EC2, no ALB)** | **~13** | **~1,100** |

Savings: free tier or credits, stop instances after the demo, skip the ALB for a small demo, Reserved or Spot for long-term use.
