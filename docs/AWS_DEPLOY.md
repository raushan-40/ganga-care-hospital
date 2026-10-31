# Deploy on AWS (EC2 + Docker, simplest path)
1. **Billing alarm first:** Billing > Budgets > create a Rs 500 budget alert.
2. **Launch EC2:** Amazon Linux 2023, t3.micro (or free-tier type), default VPC. Security group: allow 80 from anywhere, 22 from *your IP only*.
3. **IAM role** for the instance: attach `CloudWatchAgentServerPolicy`.
4. **Install Docker:**
   ```
   sudo dnf install -y docker git bc && sudo systemctl enable --now docker
   sudo usermod -aG docker ec2-user && newgrp docker
   sudo curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose --create-dirs && sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
   ```
5. **Run:** `git clone <your-repo> && cd hospital-cloud && docker compose up -d --build`. Open `http://<EC2-public-IP>/`.
6. **CloudWatch:** alarms on `StatusCheckFailed` and `CPUUtilization`. Optional: CloudWatch agent for memory and Docker logs. Dashboard: CPU, NetworkIn, status checks. Optional: Route 53 health check on `/health`.
7. **Failure tests (TTR):**
   - Container crash: `./scripts/ttr_test.sh http://localhost/health 3`
   - Instance failure: put the instance in an **Auto Scaling Group (min=max=1)** with a launch template whose user data runs the steps above, behind an ALB with health check path `/health`, then terminate the instance and time the recovery.
8. **Evidence:** screenshot the console, the CloudWatch dip and recovery, the live URL; screen-record the crash.
9. **Cleanup after the demo:** terminate EC2, delete the ALB and volumes.
