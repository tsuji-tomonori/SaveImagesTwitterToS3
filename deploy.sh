# If there is already a directory for deploy, delete it.
if [ -d deploy ]; then
    rm deploy -rf
fi

# Copy the Lambda source to the deploy directory
mkdir deploy
cp -r lambda/* deploy

# pip install
cd deploy
for dir in `ls -d -1 *`
do
    if [ -e ${dir}/requirements.txt ]; then
        pip install -r ${dir}/requirements.txt -t ${dir}/
    fi
done
