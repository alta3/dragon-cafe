sudo apt-get update
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.8 python3.8-venv python3.8-dev python3-pip build-essential -y
python3.8 -m venv venv
echo "venv/" >> .gitigrnore
source venv/bin/activate
python3 -m pip install -r requirements.txt
