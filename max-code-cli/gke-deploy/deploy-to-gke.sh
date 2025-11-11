#!/bin/bash
# Deploy MAXIMUS to GKE - Production Ready
# Execute: ./gke-deploy/deploy-to-gke.sh

set -e

PROJECT_ID="${GCP_PROJECT_ID:-maximus-ai-prod}"
CLUSTER_NAME="${GKE_CLUSTER:-maximus-cluster}"
REGION="${GKE_REGION:-us-central1}"
NAMESPACE="maximus"

echo "🚀 MAXIMUS GKE Deployment"
echo "   Project: $PROJECT_ID"
echo "   Cluster: $CLUSTER_NAME"
echo "   Region: $REGION"
echo ""

# 1. Authenticate
echo "1️⃣ Authenticating to GCP..."
gcloud auth login
gcloud config set project $PROJECT_ID

# 2. Get credentials
echo "2️⃣ Getting GKE credentials..."
gcloud container clusters get-credentials $CLUSTER_NAME --region $REGION

# 3. Create namespace
echo "3️⃣ Creating namespace..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# 4. Deploy PostgreSQL (Cloud SQL or StatefulSet)
echo "4️⃣ Deploying PostgreSQL..."
kubectl apply -f gke-deploy/manifests/postgres.yaml -n $NAMESPACE

# 5. Deploy Redis
echo "5️⃣ Deploying Redis..."
kubectl apply -f gke-deploy/manifests/redis.yaml -n $NAMESPACE

# 6. Deploy Prometheus + Grafana
echo "6️⃣ Deploying Observability..."
kubectl apply -f gke-deploy/manifests/prometheus.yaml -n $NAMESPACE
kubectl apply -f gke-deploy/manifests/grafana.yaml -n $NAMESPACE

# 7. Deploy MAXIMUS Services
echo "7️⃣ Deploying MAXIMUS Services..."
kubectl apply -f gke-deploy/manifests/maximus-core.yaml -n $NAMESPACE
kubectl apply -f gke-deploy/manifests/penelope.yaml -n $NAMESPACE
kubectl apply -f gke-deploy/manifests/maba.yaml -n $NAMESPACE
kubectl apply -f gke-deploy/manifests/nis.yaml -n $NAMESPACE

# 8. Wait for deployments
echo "8️⃣ Waiting for deployments..."
kubectl rollout status deployment/maximus-core -n $NAMESPACE
kubectl rollout status deployment/penelope -n $NAMESPACE
kubectl rollout status deployment/maba -n $NAMESPACE
kubectl rollout status deployment/nis -n $NAMESPACE

# 9. Get external IP
echo "9️⃣ Getting external IPs..."
kubectl get services -n $NAMESPACE

echo ""
echo "✅ MAXIMUS deployed to GKE!"
echo ""
echo "📋 Next Steps:"
echo "   1. kubectl get pods -n maximus"
echo "   2. kubectl logs -f deployment/maximus-core -n maximus"
echo "   3. kubectl get ingress -n maximus"
