#!/bin/bash
#
# MAXIMUS AI - Oracle Cloud Infrastructure Deployment Script
#
# Deploys all 8 MAXIMUS services + Max-Code CLI to OCI Free Tier
# Architecture: Single ARM VM (4 OCPUs, 24GB RAM) with Docker Compose
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  MAXIMUS AI - Oracle Cloud Infrastructure Deployment  ${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════${NC}\n"

# Configuration
export SUPPRESS_LABEL_WARNING=True
TENANCY_ID="ocid1.tenancy.oc1..aaaaaaaarli27auxmkctvgshmxpizaxurghqktjn6xfzlgpd3e2u4miilr3a"
REGION="sa-vinhedo-1"
DISPLAY_NAME="maximus-ai-vm"
SHAPE="VM.Standard.A1.Flex"  # ARM Free Tier
OCPUS=4
MEMORY_IN_GBS=24
BOOT_VOLUME_SIZE_IN_GBS=50  # Minimum for ARM
IMAGE_ID=""  # Will be fetched automatically

# Step 1: Get latest Ubuntu ARM image
echo -e "${YELLOW}[1/7]${NC} Fetching latest Ubuntu 22.04 ARM image..."

IMAGE_ID=$(oci compute image list \
    --compartment-id $TENANCY_ID \
    --operating-system "Canonical Ubuntu" \
    --operating-system-version "22.04" \
    --shape $SHAPE \
    --sort-by TIMECREATED \
    --sort-order DESC \
    --limit 1 \
    --query 'data[0].id' \
    --raw-output 2>/dev/null)

if [ -z "$IMAGE_ID" ]; then
    echo -e "${RED}✗ Failed to fetch Ubuntu image${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Image ID: $IMAGE_ID${NC}"

# Step 2: Get VCN (Virtual Cloud Network)
echo -e "\n${YELLOW}[2/7]${NC} Checking VCN (Virtual Cloud Network)..."

VCN_ID=$(oci network vcn list \
    --compartment-id $TENANCY_ID \
    --query 'data[0].id' \
    --raw-output 2>/dev/null)

if [ -z "$VCN_ID" ]; then
    echo -e "${CYAN}Creating new VCN...${NC}"
    VCN_ID=$(oci network vcn create \
        --compartment-id $TENANCY_ID \
        --cidr-block "10.0.0.0/16" \
        --display-name "maximus-vcn" \
        --dns-label "maximusvcn" \
        --query 'data.id' \
        --raw-output \
        --wait-for-state AVAILABLE)
fi

echo -e "${GREEN}✓ VCN ID: $VCN_ID${NC}"

# Step 3: Get Subnet
echo -e "\n${YELLOW}[3/7]${NC} Checking Subnet..."

SUBNET_ID=$(oci network subnet list \
    --compartment-id $TENANCY_ID \
    --vcn-id $VCN_ID \
    --query 'data[0].id' \
    --raw-output 2>/dev/null)

if [ -z "$SUBNET_ID" ]; then
    echo -e "${CYAN}Creating new Subnet...${NC}"

    # Get Availability Domain
    AD_NAME=$(oci iam availability-domain list \
        --compartment-id $TENANCY_ID \
        --query 'data[0].name' \
        --raw-output)

    SUBNET_ID=$(oci network subnet create \
        --compartment-id $TENANCY_ID \
        --vcn-id $VCN_ID \
        --cidr-block "10.0.0.0/24" \
        --display-name "maximus-subnet" \
        --availability-domain "$AD_NAME" \
        --dns-label "maximussub" \
        --query 'data.id' \
        --raw-output \
        --wait-for-state AVAILABLE)
fi

echo -e "${GREEN}✓ Subnet ID: $SUBNET_ID${NC}"

# Step 4: Create/Update Security List (Firewall Rules)
echo -e "\n${YELLOW}[4/7]${NC} Configuring Security List..."

# Get default security list
SECLIST_ID=$(oci network security-list list \
    --compartment-id $TENANCY_ID \
    --vcn-id $VCN_ID \
    --query 'data[0].id' \
    --raw-output 2>/dev/null)

# Update security list to allow MAXIMUS ports
oci network security-list update \
    --security-list-id $SECLIST_ID \
    --ingress-security-rules '[
        {
            "protocol": "6",
            "source": "0.0.0.0/0",
            "tcpOptions": {"destinationPortRange": {"min": 22, "max": 22}},
            "description": "SSH"
        },
        {
            "protocol": "6",
            "source": "0.0.0.0/0",
            "tcpOptions": {"destinationPortRange": {"min": 8150, "max": 8157}},
            "description": "MAXIMUS Services (8150-8157)"
        },
        {
            "protocol": "6",
            "source": "0.0.0.0/0",
            "tcpOptions": {"destinationPortRange": {"min": 80, "max": 80}},
            "description": "HTTP"
        },
        {
            "protocol": "6",
            "source": "0.0.0.0/0",
            "tcpOptions": {"destinationPortRange": {"min": 443, "max": 443}},
            "description": "HTTPS"
        }
    ]' \
    --force 2>/dev/null

echo -e "${GREEN}✓ Security List configured (ports: 22, 80, 443, 8150-8157)${NC}"

# Step 5: Get Availability Domain
echo -e "\n${YELLOW}[5/7]${NC} Getting Availability Domain..."

AD_NAME=$(oci iam availability-domain list \
    --compartment-id $TENANCY_ID \
    --query 'data[0].name' \
    --raw-output)

echo -e "${GREEN}✓ Availability Domain: $AD_NAME${NC}"

# Step 6: Generate Cloud-Init Script
echo -e "\n${YELLOW}[6/7]${NC} Preparing Cloud-Init script..."

cat > /tmp/cloud-init-maximus.yaml <<'CLOUDINIT'
#cloud-config

# MAXIMUS AI - Cloud-Init Configuration
# Installs Docker, Docker Compose, and sets up MAXIMUS services

package_update: true
package_upgrade: true

packages:
  - docker.io
  - docker-compose
  - git
  - curl
  - jq
  - htop
  - vim

runcmd:
  # Configure Docker
  - systemctl start docker
  - systemctl enable docker
  - usermod -aG docker ubuntu

  # Pull MAXIMUS Docker images (placeholder - você precisará criar essas images)
  - echo "MAXIMUS deployment preparation complete"

  # Create data directories
  - mkdir -p /opt/maximus/{data,logs,config}
  - chown -R ubuntu:ubuntu /opt/maximus

  # Clone Max-Code CLI repository
  - cd /opt/maximus
  - git clone https://github.com/your-org/max-code-cli.git || echo "Repository will be added later"

  # Install Python and Max-Code CLI dependencies
  - apt-get install -y python3-pip python3-venv

  # Setup completion message
  - echo "MAXIMUS AI VM setup complete!" > /opt/maximus/SETUP_COMPLETE
  - echo "Next steps:" >> /opt/maximus/SETUP_COMPLETE
  - echo "1. SSH into the VM: ssh ubuntu@<public-ip>" >> /opt/maximus/SETUP_COMPLETE
  - echo "2. Deploy MAXIMUS services: cd /opt/maximus/max-code-cli && docker-compose up -d" >> /opt/maximus/SETUP_COMPLETE
  - echo "3. Configure Claude API key in ~/.max-code/config.json" >> /opt/maximus/SETUP_COMPLETE

write_files:
  - path: /opt/maximus/README.md
    content: |
      # MAXIMUS AI - Oracle Cloud Deployment

      ## Services
      - Port 8150: MAXIMUS Core (Consciousness & Safety)
      - Port 8151: Penelope (7 Fruits & Healing)
      - Port 8152: MABA (Browser Agent)
      - Port 8153: NIS (Narrative Intelligence)
      - Port 8154: Orchestrator (Workflow Coordination)
      - Port 8155: Eureka (Insights & Discovery)
      - Port 8156: Oraculo (Predictions)
      - Port 8157: DLQ Monitor (Dead Letter Queue)

      ## Quick Start
      ```bash
      cd /opt/maximus/max-code-cli
      docker-compose up -d
      ```

      ## Health Check
      ```bash
      curl http://localhost:8150/health
      ```
CLOUDINIT

echo -e "${GREEN}✓ Cloud-Init script prepared${NC}"

# Step 7: Launch Instance
echo -e "\n${YELLOW}[7/7]${NC} Launching MAXIMUS VM..."
echo -e "${CYAN}Configuration:${NC}"
echo -e "  Shape: ${GREEN}$SHAPE${NC} (ARM)"
echo -e "  OCPUs: ${GREEN}$OCPUS${NC}"
echo -e "  Memory: ${GREEN}${MEMORY_IN_GBS}GB${NC}"
echo -e "  Storage: ${GREEN}${BOOT_VOLUME_SIZE_IN_GBS}GB${NC}"
echo -e ""
echo -e "${YELLOW}Creating instance... (this may take 2-3 minutes)${NC}\n"

INSTANCE_ID=$(oci compute instance launch \
    --compartment-id $TENANCY_ID \
    --availability-domain "$AD_NAME" \
    --shape $SHAPE \
    --shape-config "{\"ocpus\": $OCPUS, \"memoryInGBs\": $MEMORY_IN_GBS}" \
    --image-id $IMAGE_ID \
    --subnet-id $SUBNET_ID \
    --display-name "$DISPLAY_NAME" \
    --assign-public-ip true \
    --boot-volume-size-in-gbs $BOOT_VOLUME_SIZE_IN_GBS \
    --user-data-file /tmp/cloud-init-maximus.yaml \
    --query 'data.id' \
    --raw-output \
    --wait-for-state RUNNING)

if [ -z "$INSTANCE_ID" ]; then
    echo -e "${RED}✗ Failed to launch instance${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Instance launched successfully!${NC}"
echo -e "  Instance ID: ${CYAN}$INSTANCE_ID${NC}\n"

# Get Public IP
echo -e "${YELLOW}Fetching public IP...${NC}"
sleep 10  # Wait for IP assignment

PUBLIC_IP=$(oci compute instance list-vnics \
    --instance-id $INSTANCE_ID \
    --query 'data[0]."public-ip"' \
    --raw-output 2>/dev/null)

# Display Summary
echo -e "\n${GREEN}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}          MAXIMUS AI DEPLOYMENT SUCCESSFUL!             ${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}\n"

echo -e "${CYAN}Instance Details:${NC}"
echo -e "  Name: ${GREEN}$DISPLAY_NAME${NC}"
echo -e "  Public IP: ${GREEN}$PUBLIC_IP${NC}"
echo -e "  SSH Command: ${YELLOW}ssh ubuntu@$PUBLIC_IP${NC}\n"

echo -e "${CYAN}MAXIMUS Services (will be available after Docker Compose start):${NC}"
echo -e "  Core:         http://$PUBLIC_IP:8150/health"
echo -e "  Penelope:     http://$PUBLIC_IP:8151/health"
echo -e "  MABA:         http://$PUBLIC_IP:8152/health"
echo -e "  NIS:          http://$PUBLIC_IP:8153/health"
echo -e "  Orchestrator: http://$PUBLIC_IP:8154/health"
echo -e "  Eureka:       http://$PUBLIC_IP:8155/health"
echo -e "  Oraculo:      http://$PUBLIC_IP:8156/health"
echo -e "  DLQ Monitor:  http://$PUBLIC_IP:8157/health\n"

echo -e "${YELLOW}Next Steps:${NC}"
echo -e "  1. Wait ~2 minutes for cloud-init to complete"
echo -e "  2. SSH into VM: ${CYAN}ssh ubuntu@$PUBLIC_IP${NC}"
echo -e "  3. Check setup: ${CYAN}cat /opt/maximus/SETUP_COMPLETE${NC}"
echo -e "  4. Deploy services: ${CYAN}cd /opt/maximus/max-code-cli && docker-compose up -d${NC}\n"

echo -e "${GREEN}Deployment script complete!${NC}\n"

# Save instance details
cat > maximus-oci-info.txt <<EOF
MAXIMUS AI - OCI Deployment Info
Generated: $(date)

Instance ID: $INSTANCE_ID
Public IP: $PUBLIC_IP
Region: $REGION
Shape: $SHAPE ($OCPUS OCPUs, ${MEMORY_IN_GBS}GB RAM)

SSH: ssh ubuntu@$PUBLIC_IP

Services:
- Core:         http://$PUBLIC_IP:8150
- Penelope:     http://$PUBLIC_IP:8151
- MABA:         http://$PUBLIC_IP:8152
- NIS:          http://$PUBLIC_IP:8153
- Orchestrator: http://$PUBLIC_IP:8154
- Eureka:       http://$PUBLIC_IP:8155
- Oraculo:      http://$PUBLIC_IP:8156
- DLQ Monitor:  http://$PUBLIC_IP:8157
EOF

echo -e "${CYAN}Instance details saved to: ${GREEN}maximus-oci-info.txt${NC}\n"
