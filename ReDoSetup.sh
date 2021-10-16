#!/bin/bash
USERNAME=ghazi
mkdir temp
cd temp
git clone $USERNAME@192.168.1.100:/home/git/repository/health.git
git clone https://www.github.com/odoo/odoo --depth 1 --branch 14.0 --single-branch
cd odoo
rm -rf .git*
cd ..
mv ../odoo ./odoo.old
mv ../custom ./custom.old
mv health/custom/ ../
mv odoo ../
cd ..

