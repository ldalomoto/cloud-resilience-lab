# Bastion Host & Lift-and-Shift Strategy on AWS

## 1. Bastion Host (Controlled Private Access)
- **Public Subnet:** Hosts a small EC2 Bastion instance used strictly for administrative access.
- **Private Subnet:** Hosts private workloads/instances with no direct public exposure.
- **Security Groups:** Restrict SSH/management traffic from the Bastion to private instances only (or prefer AWS Systems Manager Session Manager when available).

### AWS Setup Steps
1. Create a VPC with one public subnet and one private subnet.
2. Launch a Bastion EC2 instance in the public subnet.
3. Launch a target EC2 instance in the private subnet.
4. Configure Security Groups so private access comes only from the Bastion.
5. Connect to the Bastion first and jump into the private instance.

## 2. Lift-and-Shift Migration Strategy
- Move the existing application and container image (`app/backend/Dockerfile`) to an AWS EC2 instance or container host with minimal or no code rewrites.
- **Stages:** Assessment -> Preparation -> Migration -> Validation -> Cutover.
- **Trade-off:** Faster migration time, while keeping original architecture constraints until future modernization.
