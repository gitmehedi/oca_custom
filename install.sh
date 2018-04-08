#!/bin/bash

maindir="/opt/odoo/"
version="10.0"
dirs=(
"3rd-addons"
"custom"
)
main="https://github.com/genweb2/gbs.git"

# change director and create a custom folder named "addons"
mkdir main && cd addons
git clone -b 10.0 --single-branch $main
echo "Repository: "$main " ready"
cd ../ && mkdir custom && cd custom

custom=(
    "https://github.com/OCA/operating-unit.git"
    "https://github.com/OCA/hr.git"
    "https://github.com/OCA/web.git"
    "https://github.com/OCA/server-tools.git"
    "https://bitbucket.org/matiarrahman/odoo-community-addons.git"
    "https://github.com/OCA/sale-workflow.git"
    "https://github.com/OCA/purchase-workflow.git"
    "https://github.com/OCA/partner-contact.git"
)

for element in ${custom[@]}
do
    git clone -b 10.0 --single-branch $element
    echo
done

echo "--------------------------------------"
echo "No of reporo downloads:" ${#custom[@]}

echo ""
echo ${custom[@]}