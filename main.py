# Importing Required Modules
import boto3
import json
import boto3
import json
import botocore
import paramiko
import secrets
import string
import os
from dotenv import load_dotenv
load_dotenv()

#Connecting To Ec2 Service
client_ec2 = boto3.client('ec2', region_name=os.getenv('region_name'), aws_access_key_id= os.getenv('aws_access_key_id'),
                          aws_secret_access_key= os.getenv('aws_secret_access_key') )
volumes_dict = {
                  'INSTANCE-NAME' : 'vol-0fdb066aeb3d2ab44' ,
                  'INstance-2'    : 'vol-009a0cd8dd351ebc1'
          }
successful_snapshots = dict()

#Taking Snapshots Of Above Instances
for snapshot in volumes_dict:
    try:
        response = client_ec2.create_snapshot(
            Description= snapshot,
            VolumeId= volumes_dict[snapshot],
            DryRun= False
        )
        
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        snapshot_id = response['SnapshotId']
        if status_code == 200:
            successful_snapshots[snapshot] = snapshot_id
    except Exception as e:
        exception_message = "There was error in creating snapshot " + snapshot + " with volume id "+volumes_dict[snapshot]+" and error is: \n"\
                            + str(e)

#Printing  Snapshots Of Volumes
print(successful_snapshots) 


#Generating Random String
N = 32
res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
												for i in range(N))
passpharse=str(res)
print(passpharse)

#Creting 

#Generating ssh keypairs with passphares Using Shell Command

#Below Defination/Function To Execute Shell Command In Python
import os
def sh(cmd):
 os.system("bash -c '%s'" % cmd)

#Shell Cmd to Ganarate  Key With Passpharse and With Comment as mykey You Can Change the Comment If Required 
sh("echo $0")
sh("ls -l")
sh("echo done")
sh("ssh-keygen -f ./key-file -N {passpharse} -m pem -C mykey -y")



#Reading Content of  A File Into Python Variable. i,e public and private key
with open('key-file','w+') as file :
    private_key=file.read()

with open('key-file.pub','w+') as file :
    public_key=file.read()
    
passpharse_key=passpharse

#Connecting To Aws Secret manager Service
client_secert_manager = boto3.client('secretsmanager', region_name=os.getenv('region_name'), aws_access_key_id= os.getenv('aws_access_key_id'),
                          aws_secret_access_key= os.getenv('aws_secret_access_key') )


#Creating/Adding Our Keys Which are stored in Variables to  Aws Secret manager as Key-value Pairs
response_sm_create = client_secert_manager.create_secret(
    Name='Insatnce-key',
    SecretString=json.dumps({"public_key": public_key,"private_key":private_key,"passpharse": passpharse})
)    

try:
        status_code = response_sm_create['ResponseMetadata']['HTTPStatusCode']
        if status_code == 200:
            print("response:",response_sm_create)
            print("Key With :",response_sm_create['Name'] ,"Created")
except  Exception as e:
    exception_message="Unable to Create A Key Secret_Manager :",response_sm_create['Name'] ,"and terminited with exception",str(e)
            

# TO List The Secrets In SecrestsManger(
response_sm_list = client_secert_manager.list_secrets()

#To Print Keys
for secret in response_sm_list['SecretList']:
  print(secret['Name'])



# Getting Public Of A Instances Using Its Name Tag
response_ec2= client_ec2.describe_instances(
     Filters = [{'Name':'tag:Name', 'Values':['rrr']}])
pub_ip=response_ec2['Reservations'][0]['Instances'][0]['PublicIpAddress']
print("ec2 response:",response_ec2['Reservations'][0]['Instances'][0]['PublicIpAddress'])

#Connecting To EC2 Instance With Above Public Ip and  .Pem File
key=paramiko.RSAKey.from_private_key_file(filename="./upendars.pem",password=None)
ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    #Execting Cmds In Remote Ec2/Connected Ec2
    ssh_client.connect(hostname=str(pub_ip),username="ubuntu", pkey=key)
    # ssh_client.exec_command("mkdir example_folder")
    # ssh_client.exec_command("touch .ssh/old_authorized_keys")
    # ssh_client.exec_command("cat .ssh/authorized_keys > .ssh/old_authorized_keys")
    # ssh_client.exec_command("echo pub>> .ssh/authorized_keys")
  
except Exception as e:
    print ("execetion:",e) 