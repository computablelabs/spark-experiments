#!/bin/bash

kubectl apply -f api-role.yaml

kubectl create clusterrolebinding add-on-pod-role \
      --clusterrole=pod-role \
      --serviceaccount=default:default
