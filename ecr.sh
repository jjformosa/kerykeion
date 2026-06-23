aws ecr get-login-password --region us-east-1 --profile jj1220dev | docker login --username AWS --password-stdin 540052993261.dkr.ecr.us-east-1.amazonaws.com

docker build -t inseen/kerykeion -f Dockerfile.lambda .

docker tag inseen/kerykeion:latest 540052993261.dkr.ecr.us-east-1.amazonaws.com/inseen/kerykeion:latest

docker push 540052993261.dkr.ecr.us-east-1.amazonaws.com/inseen/kerykeion:latest