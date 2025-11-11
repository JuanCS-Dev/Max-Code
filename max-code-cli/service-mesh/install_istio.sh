#!/bin/bash
# Install Istio (lightweight profile)
set -e

echo "📦 Installing Istio..."

# Download istioctl
curl -L https://istio.io/downloadIstio | sh -
cd istio-*/bin
export PATH=$PWD:$PATH

# Install Istio (demo profile for development)
istioctl install --set profile=demo -y

# Enable sidecar injection for default namespace
kubectl label namespace default istio-injection=enabled

# Verify installation
kubectl get pods -n istio-system

echo "✅ Istio installed!"
