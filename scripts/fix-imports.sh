#!/bin/bash
# Script to fix imports from 'shared.' to 'libs.'
# Part of MAXIMUS AI standalone migration

set -e

PROJECT_ROOT="/media/juan/DATA1/projects/MAXIMUS AI"
cd "$PROJECT_ROOT"

echo "🔧 Fixing imports from 'shared.' to 'libs.'"
echo "================================================"

# Backup count
backup_dir=".migration_backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"

# Find all Python files with 'from shared.' imports
files_to_fix=$(find services -name "*.py" -type f -exec grep -l "from shared\." {} \;)

count=0
for file in $files_to_fix; do
    # Backup original file
    cp "$file" "$backup_dir/$(basename $file).bak"

    # Replace imports
    sed -i 's/from shared\.vertice_registry_client/from libs.registry.client/g' "$file"
    sed -i 's/from shared\.constitutional_tracing/from libs.constitutional.tracing/g' "$file"
    sed -i 's/from shared\.constitutional_metrics/from libs.constitutional.metrics/g' "$file"
    sed -i 's/from shared\.constitutional_logging/from libs.constitutional.logging/g' "$file"
    sed -i 's/from shared\.metrics_exporter/from libs.constitutional.metrics/g' "$file"
    sed -i 's/from shared\.health_checks/from libs.common.health/g' "$file"
    sed -i 's/from shared\./from libs.common./g' "$file"

    count=$((count + 1))
    echo "✓ Fixed: $file"
done

echo ""
echo "================================================"
echo "✅ Fixed $count files"
echo "📦 Backups saved to: $backup_dir"
echo ""
echo "Next steps:"
echo "  1. Review changes: git diff services/"
echo "  2. Test imports: ./scripts/test-imports.sh"
echo "  3. Run tests: ./scripts/test-all.sh"
