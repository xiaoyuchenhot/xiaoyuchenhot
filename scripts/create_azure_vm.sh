#!/usr/bin/env bash
set -euo pipefail

# --- Configuration ---
RESOURCE_GROUP="rg-test-australiaeast"
LOCATION="australiaeast"
VNET_NAME="vnet-test"
SUBNET_NAME="subnet-test"
NSG_NAME="nsg-test-vm"
PUBLIC_IP_NAME="pip-test-vm"
NIC_NAME="nic-test-vm"
VM_NAME="vm-test-australiaeast"
VM_SIZE="Standard_B1ls"
VM_IMAGE="Ubuntu2204"
ADMIN_USER="azureuser"
SSH_KEY_PATH="$HOME/.ssh/azure_test_vm"

# Generate SSH key pair if not present
if [ ! -f "$SSH_KEY_PATH" ]; then
  echo "Generating SSH key at $SSH_KEY_PATH..."
  ssh-keygen -t rsa -b 4096 -f "$SSH_KEY_PATH" -N "" -C "azure-test-vm"
fi

# Verify Azure CLI is logged in
if ! az account show > /dev/null 2>&1; then
  echo "Not logged in to Azure. Run: az login"
  exit 1
fi

echo "Creating resource group: $RESOURCE_GROUP"
az group create \
  --name "$RESOURCE_GROUP" \
  --location "$LOCATION" \
  --output none

echo "Creating virtual network and subnet..."
az network vnet create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$VNET_NAME" \
  --address-prefix "10.0.0.0/16" \
  --subnet-name "$SUBNET_NAME" \
  --subnet-prefix "10.0.1.0/24" \
  --output none

echo "Creating network security group..."
az network nsg create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$NSG_NAME" \
  --output none

# Restrict SSH to caller's current public IP
MY_IP=$(curl -s https://api.ipify.org)
echo "Adding SSH rule restricted to $MY_IP..."
az network nsg rule create \
  --resource-group "$RESOURCE_GROUP" \
  --nsg-name "$NSG_NAME" \
  --name "allow-ssh" \
  --priority 100 \
  --protocol Tcp \
  --direction Inbound \
  --source-address-prefixes "$MY_IP" \
  --destination-port-ranges 22 \
  --access Allow \
  --output none

echo "Creating public IP..."
az network public-ip create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$PUBLIC_IP_NAME" \
  --sku Basic \
  --allocation-method Static \
  --output none

echo "Creating network interface..."
az network nic create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$NIC_NAME" \
  --vnet-name "$VNET_NAME" \
  --subnet "$SUBNET_NAME" \
  --public-ip-address "$PUBLIC_IP_NAME" \
  --network-security-group "$NSG_NAME" \
  --output none

echo "Creating VM: $VM_NAME ($VM_SIZE, $VM_IMAGE)..."
az vm create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$VM_NAME" \
  --nics "$NIC_NAME" \
  --image "$VM_IMAGE" \
  --size "$VM_SIZE" \
  --admin-username "$ADMIN_USER" \
  --ssh-key-values "${SSH_KEY_PATH}.pub" \
  --os-disk-sku "Standard_LRS" \
  --storage-sku "Standard_LRS" \
  --output none

PUBLIC_IP=$(az network public-ip show \
  --resource-group "$RESOURCE_GROUP" \
  --name "$PUBLIC_IP_NAME" \
  --query "ipAddress" \
  --output tsv)

echo ""
echo "VM created successfully."
echo "Connect: ssh -i $SSH_KEY_PATH $ADMIN_USER@$PUBLIC_IP"
echo ""
echo "To stop billing for compute (without deleting):"
echo "  az vm deallocate --resource-group $RESOURCE_GROUP --name $VM_NAME"
echo ""
echo "To delete all resources:"
echo "  az group delete --name $RESOURCE_GROUP --yes --no-wait"
