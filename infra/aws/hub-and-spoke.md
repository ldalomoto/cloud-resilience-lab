# Hub-and-Spoke Architecture on AWS

## Purpose
Connect multiple isolated VPCs through a central hub instead of building complex point-to-point peering meshes.

## Topology Overview
- **Hub:** AWS Transit Gateway handling centralized routing.
- **Spoke 1 (App VPC):** Hosts containerized application workloads (ECS / EC2).
- **Spoke 2 (Data / Internal VPC):** Hosts private internal resources or databases.

## Setup Steps in AWS
1. Create Spoke 1 VPC and Spoke 2 VPC with non-overlapping CIDR blocks.
2. Create subnets and route tables in each VPC.
3. Create an AWS Transit Gateway (Hub).
4. Attach both VPCs to the Transit Gateway.
5. Update route tables and Security Groups to allow only required traffic between spokes.
