#!/usr/bin/env bash
set -ex

PKGNAME="scanner-lambda"
BUCKET="splaysh-private-artifacts"
AWSACCOUNT="796019718156"
SRCROOT=~/git/wbornor/$PKGNAME/

#build package
rm /tmp/$PKGNAME.zip

cd $SRCROOT
zip -r /tmp/$PKGNAME.zip . --exclude .git/\* .idea\*

pip3 install boto3 -t /tmp/$PKGNAME/

cd /tmp/$PKGNAME/
zip -r  -u /tmp/$PKGNAME.zip .

#deploy s3

aws s3 cp \
--profile personal \
/tmp/$PKGNAME.zip \
s3://$BUCKET/$PKGNAME/;


#cycle lambda

aws lambda create-function \
--profile personal \
--region us-east-1 \
--function-name $PKGNAME \
--code S3Bucket=$BUCKET,S3Key="$PKGNAME/$PKGNAME.zip" \
--role "arn:aws:iam::$AWSACCOUNT:role/$PKGNAME"  \
--handler scanner.handler \
--runtime python3.6 \
--timeout 59 \
--memory-size 256 \
|| \
aws lambda update-function-code \
--profile personal \
--region us-east-1 \
--function-name "$PKGNAME" \
--s3-bucket=$BUCKET \
--s3-key="$PKGNAME/$PKGNAME.zip"



echo "done!"
