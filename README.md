# spark-experiments

- Steps to setup Spark and create EKS cluster:

1. Install awscli and setup aws credentials

sudo pip install awscli
aws configure

2. Install eksctl:

curl --silent --location "https://github.com/weaveworks/eksctl/releases/download/latest_release/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

3. Install Spark locally (Pyspark currently requires not yet released Spark, so need to build from source):

git clone https://github.com/apache/spark
cd spark && ./build/mvn -DskipTests=true -Pkubernetes package && cd python && python setup.py sdist && sudo pip install dist/*.tar.gz

4. Create eks cluster:

eksctl create cluster --name=computable-spark-test --nodes=4 --kubeconfig=./kubeconfig.spark-test.yaml --node-ami=auto
export KUBECONFIG=`pwd`/kubeconfig.spark-test.yaml

5. Verify kubernetes clusters is up and connectable:

kubectl get nodes

6. Update core-site.xml to have AWS Access key ID and secret

7. Run grant-api-role.sh to allow default service account to launch more pods for Spark

- Steps to run Spark job

1. Update Spark job script to run desire query in sql.py

2. Push sql script to s3

aws s3 cp sql.py --acl public-read s3://computable-spark/sql.py

3. Get K8s Master URL from kubeconfig.spark-test.yaml (clusters -> server) and update that to KUBE_MASTER env variable

export KUBE_MASTER=k8s://https://xxxxxxxx.amazonaws.com

3. Submit Spark job to run query aganist S3

HADOOP_CONF_DIR=`pwd` spark-submit --deploy-mode cluster --master $KUBE_MASTER --conf spark.kubernetes.container.image=tnachen/spark-py:latest2 s3a://computable-spark/sql.py

4. After Spark job completed, check kubernetes driver log for results

# Find the latest completed driver pod name
kubectl get pods

kubectl logs <pod_name>